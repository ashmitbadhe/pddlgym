from pddlgym.pddlgym_planners.fd import FD
from pddlgym.structs import Anti, LiteralConjunction
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
            self.current_plan_index = 0
            print("Generated plan:", self.plan)

        # If there is a plan, check for the safe sequence
        if self.plan:
            # Attempt to find safe sequence if it is not empty
            if self.safe_sequence and \
                    self.is_action_applicable(self.safe_sequence[0], state) and \
                    self.is_state_safe(self.simulate_action(state, self.safe_sequence[0])):

                selected_action = self.safe_sequence.pop(0)
                self.current_plan_index += 1
                print(f"Selected action from safe sequence: {selected_action}")
            else:
                # Find a new safe sequence from the current state
                self.find_safe_sequence(state)
                if not self.safe_sequence:
                    selected_action = None # no-op
                    self.noops_performed += 1
                else:
                    selected_action = self.safe_sequence.pop(0)
                    self.current_plan_index +=1
                    print(f"New safe sequence of length {len(self.safe_sequence)}", self.safe_sequence)
        #
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

        for i in range(self.current_plan_index, len(self.plan)):
            action = self.plan[i]
            add_effects, del_effects = self.get_add_del_effects(action, state)
            applicable = self.is_action_applicable(action, state)
            if not applicable:
                print(f"Action {action} not applicable at step {i}")
                break

            # Simulate deterministic action transition
            next_deterministic_state = self.simulate_action(state, action)

            # Check if this action is safe w.r.t p_plus/p_minus
            safe, unsafe_literal = self.is_state_safe(next_deterministic_state)
            if not safe:
                print(f"Action {action} considered unsafe because anti goal state {unsafe_literal} found")
                break

            self.safe_sequence.append(action)

            print(f"[STEP {i}] Considering action: {action}")
            print(f"  Applicable: {applicable}")
            print(f" Safe: {safe}")

            state = next_deterministic_state
    def get_add_del_effects(self, action, state):
        self.space._update_objects_from_state(state)
        all_effects = self.space._ground_action_to_effects[action]
        add_effects = set()
        del_effects = set()
        for effect in all_effects:
            if "Anti" in str(effect):
                del_effects.add(Anti(effect))
            else:
                add_effects.add(effect)
        return add_effects, del_effects

    def is_action_applicable(self, action, state):
        self.space._update_objects_from_state(state)
        pos_preconds = self.space._ground_action_to_pos_preconds[action]
        if not pos_preconds.issubset(state.literals):
            return False
        neg_preconds = self.space._ground_action_to_neg_preconds[action]
        if len(neg_preconds & state.literals) > 0:
            return False
        return True

    def is_state_safe(self, state):
        all_event_literals = self.space.event_literals
        applicable_events = self.applicable_events(all_event_literals, state)
        for event in applicable_events:
            effects = self.space._ground_action_to_effects[event]
            # if str(event) == "shrink-small-agent(l-2-1:location,l1:lvl)":
            #     print(effects)
            for effect in effects:
                if Anti(effect) in state.goal.literals:
                    return False, effect
        return True,None




    def simulate_action(self, state, action):
        # Make a deep copy of the environment to avoid changing the real one
        sim_env = copy.deepcopy(self.env)
        sim_env.set_state(state)
        next_deterministic_state, _, _, _, _ = sim_env.step(action)
        return next_deterministic_state

    def applicable_events(self, all_event_literals, state):
        self.space._update_objects_from_state(state)
        valid_literals = set()
        for event_literal in all_event_literals:
            pos_preconds = self.space._ground_action_to_pos_preconds[event_literal]
            if not pos_preconds.issubset(state.literals):
                continue
            neg_preconds = self.space._ground_action_to_neg_preconds[event_literal]
            if len(neg_preconds & state.literals) > 0:
                continue
            valid_literals.add(event_literal)
        return list(valid_literals)

    def get_noops_count(self):
        return self.noops_performed
