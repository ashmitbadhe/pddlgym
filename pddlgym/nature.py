import random
import pddlgym.core as core
class Nature:
    def __init__(self, state, environment):
        self.state = state
        self.env = environment.env
        self.space = self.env.action_space
        self.space._update_objects_from_state(state)
        self.event_literals = self.space.event_literals
        self.environment = environment


    def nature_KR2021(self):
        selected_events = []
        required = {} #Tracks preconditions that must hold
        changed = {} # tracks variables that have changed
        selectable = self.event_literals
        while selectable:
            # Randomly select an event from the selectable list
            event_order = self.space.np_random.choice(len(selectable))
            event = selectable[event_order-1]
            if self.is_pairwise_independent(event, self.state, selected_events, required, changed):
                preconditions = self.space._ground_action_to_pos_preconds[event]
                effects = self.space._ground_action_to_effects[event]

                for precondition in preconditions:
                    required[precondition] = True # Mark precondition as needed
                for effect in effects:
                    changed[effect] = True # Mark effect as changed

                selected_events.append(event)
            selectable.pop(event_order)

        for event in selected_events:
            obs, reward, done, _, _ = self.environment.step(event)
        return obs, reward, done, _, _

    def no_nature(state):
        return state

    def is_pairwise_independent(self, event, state, selected_events, required, changed):
        """ Check if an event can be applied along with already selected ones. """
        preconditions = self.space._ground_action_to_pos_preconds[event]
        effects = self.space._ground_action_to_effects[event]
        # Condition 1: Precondition should not be marked as changed by a previous event
        for precondition in preconditions:
            if precondition in changed and changed[precondition] != state.literals.get(precondition, None):
                return False

        # Condition 2: Effects should not override required preconditions
        for effect in effects:
            if effect in required and required[effect] != state.literals.get(effect, None):
                return False

        # Condition 3: Shared preconditions must have the same value
        for selected_event in selected_events:
            selected_preconditions = self.space._ground_action_to_pos_preconds[selected_event]
            for pre in preconditions & selected_preconditions:  # Intersection
                if pre in state.literals and pre in required and state.literals != required:
                    return False

        # Condition 4: Shared effects must have the same value
        for selected_event in selected_events:
            selected_effects = self.space._ground_action_to_effects[selected_event]
            for eff in set(effects) & set(selected_effects):  # Intersection
                if eff in state.literals and eff in changed and state.literals != changed:
                    return False

        return True