from pddlgym.pddlgym_planners.fd import FD
from pddlgym.structs import Anti
import copy
class APPAgent:
    def __init__(self, env):
        self.env = env
        self.domain = self.env.domain
        self.space = self.env.action_space
        self.planner = FD()
        self.plan = None
        self.safe_sequence = []  # Safe sequence for actions
        self.noops_performed = 0  # Counter for no-ops

    def __call__(self, state):
        # Only plan once
        if self.plan is None:
            state, _ = self.env.reset()
            self.plan = self.planner(self.env.domain, state)
            print("Generated plan:", self.plan)

        # If there is a plan, check for the safe sequence
        if self.plan:
            # Attempt to find safe sequence if it is not empty
            if self.safe_sequence:
                selected_action = self.safe_sequence.pop(0)
                print(f"Selected action from safe sequence: {selected_action}")
            else:
                # Find a new safe sequence from the current state
                self.find_safe_sequence(state)
                if not self.safe_sequence:
                    selected_action = None # no-op
                    self.noops_performed += 1
                else:
                    selected_action = self.safe_sequence.pop(0)
                    print(f"New safe sequence of length {len(self.safe_sequence)}", self.safe_sequence)

            return selected_action
        else:
            raise Exception("Plan is empty. No more actions to take.")

    def find_safe_sequence(self, current_state):
        """
        Logic to find the safe sequence of actions based on the current state.
        Mimicking the logic of the C++ `find_safe_sequence` method in your original code.
        """
        state = current_state
        self.safe_sequence.clear()  # Clear any existing safe sequence
        plan_size = len(self.plan)

        p_plus = set()  # must stay true
        p_minus = set() # must not be deleted

        for i, action in enumerate(self.plan):
            if not self.is_action_applicable(action, state):
                print(f"Action {action} not applicable at step {i}")
                break

            # Check if this action is safe w.r.t p_plus/p_minus
            if not self.is_action_safe(action, p_plus, p_minus):
                print(f"Action {action} considered unsafe due to p+ or p- at step {i}")
                break

            self.safe_sequence.append(action)

            print(f"[STEP {i}] Considering action: {action}")
            print(f"  Applicable: {self.is_action_applicable(action, state)}")
            print(f"  Safe: {self.is_action_safe(action, p_plus, p_minus)}")
            print(f"  Current p+: {p_plus}")
            print(f"  Current state: {state}")

            # Simulate deterministic action transition
            next_state = self.simulate_action(self.env, state, action)

            # add preconditions of *future* actions (i+1 and onward) to p_plus
            for future_action in self.plan[i + 1:]:
                future_preconds = self.space._ground_action_to_pos_preconds[future_action]
                p_plus.update(future_preconds)

            state = next_state
    def is_action_applicable(self, action, state):
        self.space._update_objects_from_state(state)
        pos_preconds = self.space._ground_action_to_pos_preconds[action]
        if not pos_preconds.issubset(state.literals):
            return False
        neg_preconds = self.space._ground_action_to_neg_preconds[action]
        if len(neg_preconds & state.literals) > 0:
            return False
        return True
    def is_action_safe(self, action, p_plus, p_minus):
        """
        For now: check that this action does not break anything in p_minus,
        and that everything in p_plus will stay true after applying it.
        You can expand this logic using actual effect information.
        """
        all_effects = self.space._ground_action_to_effects[action]
        add_effects = set()
        del_effects = set()
        for effect in all_effects:
            if "Anti" in str(effect):
                del_effects.add(Anti(effect))
            else:
                add_effects.add(effect)

        for fact in del_effects:
            if fact in p_plus or fact in p_minus:
                print(f"Fact: {fact}")
                print(f"p_plus: {p_plus}")
                print(f"p_minus: {p_minus}")
                return False
        return True

    def simulate_action(self, env, state, action):
        # Make a deep copy of the environment to avoid changing the real one
        sim_env = copy.deepcopy(env)
        sim_env.set_state(state)
        next_state, _, _, _, _ = sim_env.step(action)
        return next_state

    def get_noops_count(self):
        return self.noops_performed
