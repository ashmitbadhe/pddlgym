import math
import random
from collections import defaultdict

from pddlgym.structs import Anti, Literal, LiteralConjunction
from pddlgym.prolog_interface import PrologInterface

class MCTSAgent:
    def __init__(self, env, num_simulations=100, exploration_const=1.41, max_depth=10):
        self.env = env
        self.num_simulations = num_simulations
        self.exploration_const = exploration_const
        self.max_depth = max_depth
        self.Q = defaultdict(float)     # Q-values: (state, action) -> value
        self.N = defaultdict(int)       # Visit counts: (state, action) -> count
        self.Ns = defaultdict(int)      # State visit counts: state -> count
        self.actions = set()

    def __call__(self, obs):
        self.actions = set(self.env.action_space.all_ground_literals(obs))
        for _ in range(self.num_simulations):
            self._simulate(obs, depth=0)

        for action in self.actions:
            print(action, self.Q[obs, action])

        # Choose best action
        if self.actions:
            best_action = max(
                self.actions,
                key=lambda a: self.Q[(obs, a)] / self.N[(obs, a)] if self.N[(obs, a)] > 0 else float('-inf')
            )
        else:
            return None
        return best_action

    def _simulate(self, obs, depth):
        if depth >= self.max_depth:
            return 0

        if self.Ns[obs] == 0:
            # First visit: expand and return rollout value
            return self._rollout(obs, depth)

        # Select action using UCB1
        best_score = float('-inf')
        best_action = None
        actions = set(self.env.action_space.all_ground_literals(obs))
        for action in actions:
            q = self.Q[(obs, action)]
            n = self.N[(obs, action)]
            ns = self.Ns[obs]
            ucb = q / (n + 1e-4) + self.exploration_const * math.sqrt(math.log(ns + 1) / (n + 1e-4))
            if ucb > best_score:
                best_score = ucb
                best_action = action

        # Simulate the environment
        action_applied_state = self.env.simulate_events(best_action, obs)
        event_applied_state = self.env.simulate_events(self.select_event(self.env.action_space.event_literals, action_applied_state), action_applied_state)
        reward, done = self.calculate_reward(action_applied_state, event_applied_state)
        # Recursively simulate
        total_reward = reward
        if not done:
            total_reward += self._simulate(event_applied_state, depth + 1)

        # Backpropagate
        self.N[(obs, best_action)] += 1
        self.Ns[obs] += 1
        self.Q[(obs, best_action)] += total_reward

        return total_reward

    def _rollout(self, obs, depth):
        # Random rollout
        current_obs = obs
        total_reward = 0
        for _ in range(self.max_depth - depth):
            applicable_actions = set(self.env.action_space.all_ground_literals(obs))
            if len(applicable_actions) != 0:
                action = list(applicable_actions).pop(0)
            else:
                action = None
            if action != None:
                self.N[obs, action] += 1
            action_applied_state = self.env.simulate_events(action, current_obs)
            event_applied_state = self.env.simulate_events(self.select_event(self.env.action_space.event_literals, action_applied_state), action_applied_state)
            reward, done = self.calculate_reward(action_applied_state, event_applied_state)
            total_reward += reward
            if done:
                break
        self.Ns[obs] +=1
        return total_reward

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

    def calculate_reward(self, pre_event_state, post_event_state):
        if all(self.check_goal(pre_event_state, lit) for lit in pre_event_state.goal.literals):
            print("found goal")
            return 1.0, True
        elif any(lit in pre_event_state.literals and lit not in post_event_state.literals for lit in post_event_state.goal.literals):
            return 0.0, True
        elif any(lit in pre_event_state.literals for lit in post_event_state.goal.literals):
            encouraging_literals = post_event_state.literals & set(post_event_state.goal.literals)
            reward = len(encouraging_literals) / len(post_event_state.goal.literals)
            return reward, False
        else:
            return 0.5, False, None
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