import math
import random
from collections import defaultdict
from dataclasses import replace

from pddlgym.structs import Anti, Literal, LiteralConjunction
from pddlgym.prolog_interface import PrologInterface
from pddlgym.pddlgym_planners.fd import FD  # FastDownward

class MCTSAgent:
    def __init__(self, env, num_simulations=100, exploration_const=1.41, max_depth=5):
        self.env = env
        self.num_simulations = num_simulations
        self.exploration_const = exploration_const
        self.max_depth = max_depth
        self.Q = defaultdict(float)     # Q-values: (state, action) -> value
        self.N = defaultdict(int)       # Visit counts: (state, action) -> count
        self.Ns = defaultdict(int)      # State visit counts: state -> count
        self.RAVE = defaultdict(float)  # RAVE action-value estimates (state, action) -> aggregated value
        self.RAVE_N = defaultdict(int)  # Number of visits for each action across all parent nodes
        self.actions = set()
        self.parent_map = {}  # Maps child_state -> (parent_state, action)
        self.planner = FD(alias_flag="--alias seq-opt-lmcut")
        self.reference_plan = None
        self.reference_plan_indices = {}
        self.action_uses = defaultdict(int)

    def __call__(self, obs):
        self.actions = self.env.action_space.all_ground_literals(obs) | {None}

        # Compute reference plan only once
        if self.reference_plan is None:
            try:
                print("Generating reference plan using Fast Downward...")
                plan = self.planner(self.env.domain, obs)
                self.reference_plan = plan
                self.reference_plan_indices = {
                    action: i for i, action in enumerate(self.reference_plan)
                }
                print(f"Reference plan length {len(plan)}")
            except:
                print("generating reference plan failed or took too long, proceeding with Random Play simulation ")


        for _ in range(self.num_simulations):
            self._simulate(obs, depth=0)

        # Choose best action
        if self.actions:
            best_action = max(
                self.actions,
                key=lambda a: self.Q[(obs, a)] if self.N[(obs, a)] > 0 else float('-inf')
            )
            print(self.Q[(obs,best_action)])
            if self.Q[(obs,best_action)] < 0.1:
                return None
        else:
            return None
        return best_action

    def _simulate(self, obs, depth, simulation_path=None):
        if simulation_path is None:
            simulation_path = []

        if depth >= self.max_depth:
            return 0

        if self.Ns[obs] == 0:
            # First visit: expand and return rollout value
            return self._rollout(obs, depth)

        # Select action using UCB1
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

        # Simulate environment
        action_applied_state = self.apply_action(best_action, obs)
        event_applied_state = self.apply_action(
            self.select_event(self.env.action_space.event_literals, action_applied_state), action_applied_state)

        # Record parent-child transition
        self.parent_map[event_applied_state] = (obs, best_action)

        reward, done = self.calculate_reward(event_applied_state, best_action)

        # Add current step to simulation path
        simulation_path.append((obs, best_action))

        # Recursive simulation
        total_reward = reward
        if not done:
            total_reward += self._simulate(event_applied_state, depth + 1, simulation_path)

        # Backpropagate Q and visit counts
        self.N[(obs, best_action)] += 1
        self.Ns[obs] += 1
        self.Q[(obs, best_action)] = (
                (self.Q[(obs, best_action)] * (self.N[(obs, best_action)] - 1) + total_reward)
                / self.N[(obs, best_action)]
        )

        # RAVE update for the full path
        for past_state, past_action in simulation_path:
            self.RAVE_N[(past_state, past_action)] += 1
            self.RAVE[(past_state, past_action)] = (
                    (self.RAVE[(past_state, past_action)] * (self.RAVE_N[(past_state, past_action)] - 1) + total_reward)
                    / self.RAVE_N[(past_state, past_action)]
            )


        return total_reward

    def get_parent_states(self, state):
        parents = []
        if state in self.parent_map:
            parent, action = self.parent_map[state]
            parents.append(parent)
        return parents

    def get_best_heuristic(self, actions, previous_heuristic):
        best_action = None
        best_distance = float("inf")
        best_value = float("-inf")  # Track best known plan index

        for action in actions:
            value = self.reference_plan_indices.get(action, float("-inf"))

            # Case 1: First time choosing heuristic-guided action
            if previous_heuristic is None:
                # Prefer any action in the reference plan
                if value > best_value:
                    best_value = value
                    best_action = action
            else:
                # Compute distance safely
                if value == float("-inf"):
                    distance = float("inf")  # Not in plan
                else:
                    if value != previous_heuristic:
                        distance = value - previous_heuristic
                    else:
                        distance = float("inf")

                # Choose the one with the smallest forward distance
                if distance < best_distance:
                    best_distance = distance
                    best_value = value
                    best_action = action

        # If all actions were -inf and best_action is still None, fallback to random
        if best_action is None and actions:
            best_action = random.choice(list(actions))
            best_value = float("-inf")  # Indicates no reference match

        return best_action, best_value

    def _rollout(self, obs, depth):
        # Random rollout
        current_obs = obs
        total_reward = 0
        heuristic = None

        for _ in range(self.max_depth - depth):
            applicable_actions = self.env.action_space.all_ground_literals(current_obs)
            if len(applicable_actions) == 0:
                break

            # Stronger bias toward goal-oriented actions later in rollouts

            if random.random() < 0.5:
                action, heuristic = self.get_best_heuristic(applicable_actions, heuristic)
            else:
                action = random.choice(list(applicable_actions))

            self.N[obs, action] += 1

            action_applied_state = self.apply_action(action, current_obs)

            # Record the transition
            self.parent_map[action_applied_state] = (obs, action)

            reward, done = self.calculate_reward(action_applied_state, action)
            total_reward += reward
            if done:
                break
            current_obs = action_applied_state
        self.Ns[obs] +=1
        return total_reward

    def apply_action(self, action, state):
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
        new_state = state.with_literals(frozenset(state_literals))
        return new_state



    def select_event(self, event_literals, state):
        self.env.action_space._update_objects_from_state(state)
        applicable_events = set()
        for event in event_literals:
            pos_preconds = self.env.action_space._ground_action_to_pos_preconds[event]
            if not pos_preconds.issubset(state.literals):
                continue
            neg_preconds = self.env.action_space._ground_action_to_neg_preconds[event]
            if len(neg_preconds & state.literals) > 0:
                continue
            effects = self.env.action_space._ground_action_to_effects[event]
            for effect in effects:
                if Anti(effect) in state.goal.literals:
                    return event
            applicable_events.add(event)
        if len(applicable_events) != 0:
            return random.choice(list(applicable_events))
        else:
            return None

    def calculate_reward(self, state, action):
        self.action_uses[action] += 1
        usage_penalty = 1 / math.sqrt(self.action_uses[action])  # smoother than 1 / x

        if all(self.check_goal(state, lit) for lit in state.goal.literals):
            #print("found_goal")
            return 1.0, True

        elif any(lit not in state.literals for lit in state.goal.literals):
            missing_literals = set(state.goal.literals) - state.literals
            total_literals = len(state.goal.literals)
            num_missing = len(missing_literals)

            progress = (total_literals - num_missing) / total_literals
            reward = progress * 0.9 * usage_penalty
            return reward, False

        else:
            return 0.0, False
    def check_goal(self, state, goal):
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