import time
import os
from pddlgym import make
from pddlgym.pddlgym_planners.fd import FD  # FastDownward
from pddlgym.structs import Anti, Literal, LiteralConjunction


class LinearExecutionAgent:
    def __init__(self, env, domain_file, problem_file):
        # Load the environment using pddlgym
        self.env = env
        self.domain_file = domain_file
        self.domain = env.domain
        self.problem_file = problem_file
        self.plan = []  # Will hold the plan (sequence of actions)
        self.planner = FD(alias_flag="--alias seq-opt-lmcut")
        self.current_state = None

    def generate_initial_plan(self, obs):
        # Use Fast Downward to generate the initial plan
        self.plan = self.planner(self.domain, obs)

    def is_action_applicable(self, action, state):
        # Check if an action is applicable given the current state
        return self.env.is_action_applicable(action, state)

    def execute_action(self, action):
        # Execute the action in the environment
        self.current_state, reward, done, _, _ = self.env.step(action)
        return reward, done

    def verify_plan(self, state):
        print("Verifying the plan...")
        current_state = state

        for action in self.plan:
            print(f"Considering action {action}")

            # Try direct applicability
            if self.is_applicable(current_state, action):
                print("Action directly applicable.")
                current_state = self.apply(current_state, action)
                continue

            # Try to make it applicable via events
            print("Action not applicable, trying to apply events...")
            event_helped = False

            for _ in range(5):  # max 5 event steps
                applicable_events = self.get_applicable(current_state, self.env.action_space.event_literals)
                if not applicable_events:
                    break  # no possible events

                for event in applicable_events:
                    simulated_state = self.apply(current_state, event)

                    if self.is_applicable(simulated_state, action):
                        print(f"Event {event} made action applicable.")
                        current_state = self.apply(simulated_state, action)
                        event_helped = True
                        break  # exit inner loop

                    current_state = simulated_state  # keep progressing

                if event_helped:
                    break  # go to next action

            if not event_helped:
                print("FAILURE: Action is not applicable and no events helped.")
                return False

        print("Plan verified successfully.")
        return True
    def is_applicable(self, state, action):
        self.env.action_space._update_objects_from_state(state)
        pos_preconds = self.env.action_space._ground_action_to_pos_preconds[action]
        if not pos_preconds.issubset(state.literals):
            return False
        neg_preconds = self.env.action_space._ground_action_to_neg_preconds[action]
        if len(neg_preconds & state.literals) > 0:
            return False
        return True

    def get_applicable(self, state, actions):
        applicable = set()
        for action in actions:
            self.env.action_space._update_objects_from_state(state)
            pos_preconds = self.env.action_space._ground_action_to_pos_preconds[action]
            if not pos_preconds.issubset(state.literals):
                continue
            neg_preconds = self.env.action_space._ground_action_to_neg_preconds[action]
            if len(neg_preconds & state.literals) > 0:
                continue
            applicable.add(action)
        return applicable

    def apply(self, state, action):
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


    def replanning(self):
        # Replan using Fast Downward (for simplicity, regenerating the entire plan)
        print("Replanning...")
        self.generate_initial_plan(self.current_state)
        self.verify_plan(self.current_state)

    def __call__(self, state):
        self.current_state = state
        # Main loop for linear execution
        start_time = time.time()
        verification_result = True
        if len(self.plan) == 0:
            self.generate_initial_plan(state)
            verification_result = self.verify_plan(state)

        if len(self.plan) != 0:
            if verification_result:
                if self.is_applicable(self.current_state, self.plan[0]):
                    print("Plan verified successfully")
                    return self.plan.pop(0)
                else:
                    return None
        else:
            print("Plan verification failed. Replanning...")
            self.replanning()

        # Measure time elapsed
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"Total execution time: {elapsed_time} ms")

