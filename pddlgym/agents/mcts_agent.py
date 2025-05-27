import math
import random
from collections import defaultdict

from pddlgym.structs import Anti, Literal, LiteralConjunction
from pddlgym.prolog_interface import PrologInterface
from pddlgym.pddlgym_planners.fd import FD  # FastDownward


class MCTSAgent:
    """
    Monte Carlo Tree Search (MCTS) agent for use in PDDL environments via pddlgym.

    Supports:
    - Simulation-based planning using UCB1 + RAVE.
    - Action selection with heuristic guidance via reference plans.
    - Rollouts with a blend of heuristic and random strategies.
    - Safe event simulation and reward shaping based on goal proximity.
    """

    def __init__(self, env, num_simulations=100, exploration_const=1.41, max_depth=20):
        """
        Initialize the MCTSAgent.

        Args:
            env: The pddlgym environment.
            num_simulations (int): Number of simulations to run per decision.
            exploration_const (float): Exploration constant for UCB1.
            max_depth (int): Maximum depth for simulations and rollouts.
        """
        self.env = env
        self.num_simulations = num_simulations
        self.exploration_const = exploration_const
        self.max_depth = max_depth
        self.Q = defaultdict(float)
        self.N = defaultdict(int)
        self.Ns = defaultdict(int)
        self.RAVE = defaultdict(float)
        self.RAVE_N = defaultdict(int)
        self.actions = set()
        self.parent_map = {}
        self.planner = FD(alias_flag="--alias seq-opt-lmcut")
        self.reference_plan = None
        self.reference_plan_indices = {}
        self.action_uses = defaultdict(int)

    def __call__(self, obs):
        """
        Select the next action based on MCTS simulations.

        Args:
            obs: The current observation (state).

        Returns:
            The selected action.
        """
        self.actions = self.env.action_space.all_ground_literals(obs) | {None}

        if self.reference_plan is None:
            try:
                print("Generating reference plan using Fast Downward...")
                plan = self.planner(self.env.domain, obs)
                self.reference_plan = plan
                self.reference_plan_indices = {action: i for i, action in enumerate(plan)}
                print(f"Reference plan length {len(plan)}")
            except:
                print("Generating reference plan failed or timed out.")

        for _ in range(self.num_simulations):
            self._simulate(obs, depth=0)

        if self.actions:
            best_action = max(
                self.actions,
                key=lambda a: self.Q[(obs, a)] if self.N[(obs, a)] > 0 else float('-inf')
            )
        else:
            return None
        return best_action

    def _simulate(self, obs, depth, simulation_path=None):
        """
        Run a simulation from a given state.

        Args:
            obs: Current state.
            depth: Current depth of simulation.
            simulation_path: History of visited (state, action) pairs.

        Returns:
            The cumulative reward from the simulation.
        """
        if simulation_path is None:
            simulation_path = []

        if depth >= self.max_depth:
            return 0

        if self.Ns[obs] == 0:
            return self._rollout(obs, depth)

        best_score = float('-inf')
        best_action = None
        actions = self.env.action_space.all_ground_literals(obs)

        for action in actions:
            q = self.Q[(obs, action)]
            n = self.N[(obs, action)]
            ns = self.Ns[obs]

            ucb_classical = q / (n + 1e-4) + self.exploration_const * math.sqrt(math.log(ns + 1) / (n + 1e-4))
            rave_q = self.RAVE[(obs, action)]
            rave_n = self.RAVE_N[(obs, action)]
            ucb_rave = rave_q / (rave_n + 1e-4) + self.exploration_const * math.sqrt(math.log(ns + 1) / (rave_n + 1e-4))

            ucb_combined = ucb_classical + ucb_rave

            if ucb_combined > best_score:
                best_score = ucb_combined
                best_action = action

        action_applied_state = self.apply_action(best_action, obs)
        event_applied_state = self.apply_action(
            self.select_event(self.env.action_space.event_literals, action_applied_state),
            action_applied_state)

        self.parent_map[event_applied_state] = (obs, best_action)

        reward, done = self.calculate_reward(event_applied_state, best_action)
        simulation_path.append((obs, best_action))

        total_reward = reward
        if not done:
            total_reward += self._simulate(event_applied_state, depth + 1, simulation_path)

        self.N[(obs, best_action)] += 1
        self.Ns[obs] += 1
        self.Q[(obs, best_action)] = (
            (self.Q[(obs, best_action)] * (self.N[(obs, best_action)] - 1) + total_reward)
            / self.N[(obs, best_action)]
        )

        for past_state, past_action in simulation_path:
            self.RAVE_N[(past_state, past_action)] += 1
            self.RAVE[(past_state, past_action)] = (
                (self.RAVE[(past_state, past_action)] * (self.RAVE_N[(past_state, past_action)] - 1) + total_reward)
                / self.RAVE_N[(past_state, past_action)]
            )

        return total_reward

    def _rollout(self, obs, depth):
        """
        Perform a random rollout from the current state.

        Args:
            obs: Starting state.
            depth: Starting depth.

        Returns:
            Accumulated reward from rollout.
        """
        current_obs = obs
        total_reward = 0
        heuristic = None

        for _ in range(self.max_depth - depth):
            applicable_actions = self.env.action_space.all_ground_literals(current_obs)
            if not applicable_actions:
                break

            if random.random() < 0.5:
                action, heuristic = self.get_best_heuristic(applicable_actions, heuristic)
            else:
                action = random.choice(list(applicable_actions))

            self.N[obs, action] += 1
            action_applied_state = self.apply_action(action, current_obs)
            self.parent_map[action_applied_state] = (obs, action)

            reward, done = self.calculate_reward(action_applied_state, action)
            total_reward += reward
            if done:
                break
            current_obs = action_applied_state

        self.Ns[obs] += 1
        return total_reward

    def get_best_heuristic(self, actions, previous_heuristic):
        """
        Choose the best action based on a reference plan.

        Args:
            actions: Set of applicable actions.
            previous_heuristic: Index of the previous heuristic action in the reference plan.

        Returns:
            A tuple (best_action, plan_index).
        """
        best_action = None
        best_distance = float("inf")
        best_value = float("-inf")

        for action in actions:
            value = self.reference_plan_indices.get(action, float("-inf"))

            if previous_heuristic is None:
                if value > best_value:
                    best_value = value
                    best_action = action
            else:
                distance = value - previous_heuristic if value != float("-inf") else float("inf")
                if distance < best_distance:
                    best_distance = distance
                    best_value = value
                    best_action = action

        if best_action is None and actions:
            best_action = random.choice(list(actions))
            best_value = float("-inf")

        return best_action, best_value

    def apply_action(self, action, state):
        """
        Apply an action to a state and return the new state.

        Args:
            action: The action to apply.
            state: The current state.

        Returns:
            The resulting state.
        """
        if action is None:
            return state

        self.env.action_space._update_objects_from_state(state)
        state_literals = set(state.literals)
        all_effects = self.env.action_space._ground_action_to_effects[action]
        for effect in all_effects:
            if "Anti" in str(effect):
                if Anti(effect) in state.literals:
                    state_literals.remove(Anti(effect))
                else:
                    state_literals.add(effect)
            else:
                state_literals.add(effect)
        return state.with_literals(frozenset(state_literals))

    def select_event(self, event_literals, state):
        """
        Select a non-deterministic event to apply to a state.

        Args:
            event_literals: Available event actions.
            state: Current state.

        Returns:
            An applicable event.
        """
        self.env.action_space._update_objects_from_state(state)
        applicable_events = set()
        for event in event_literals:
            pos_preconds = self.env.action_space._ground_action_to_pos_preconds[event]
            neg_preconds = self.env.action_space._ground_action_to_neg_preconds[event]
            if not pos_preconds.issubset(state.literals) or neg_preconds & state.literals:
                continue
            effects = self.env.action_space._ground_action_to_effects[event]
            for effect in effects:
                if Anti(effect) in state.goal.literals:
                    return event
            applicable_events.add(event)
        return random.choice(list(applicable_events)) if applicable_events else None

    def calculate_reward(self, state, action):
        """
        Compute the reward for a state and action.

        Args:
            state: Resulting state.
            action: Action taken.

        Returns:
            Tuple (reward, done).
        """
        self.action_uses[action] += 1
        usage_penalty = 1 / math.sqrt(self.action_uses[action])

        if all(self.check_goal(state, lit) for lit in state.goal.literals):
            return 1.0, True
        elif any(lit not in state.literals for lit in state.goal.literals):
            missing_literals = set(state.goal.literals) - state.literals
            total_literals = len(state.goal.literals)
            progress = (total_literals - len(missing_literals)) / total_literals
            return progress * 0.9 * usage_penalty, False
        return 0.0, False

    def check_goal(self, state, goal):
        """
        Check if a goal is satisfied in the state.

        Args:
            state: State to check.
            goal: Goal condition.

        Returns:
            True if goal is satisfied, False otherwise.
        """
        if isinstance(goal, Literal):
            if goal.is_negative and goal.positive in state.literals:
                return False
            if not goal.is_negative and goal not in state.literals:
                return False
            return True
        if isinstance(goal, LiteralConjunction):
            return all(self.check_goal(state, lit) for lit in goal.literals)
        prolog_interface = PrologInterface(state.literals, goal,
                                           max_assignment_count=2,
                                           allow_redundant_variables=True)
        assignments = prolog_interface.run()
        return len(assignments) > 0

    def get_parent_states(self, state):
        """
        Retrieve parent states that led to a given state.

        Args:
            state: The child state.

        Returns:
            List of parent states.
        """
        parents = []
        if state in self.parent_map:
            parent, _ = self.parent_map[state]
            parents.append(parent)
        return parents
