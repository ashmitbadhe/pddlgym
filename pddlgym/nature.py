from abc import ABC, abstractmethod
class BaseNature(ABC):
    def __init__(self, state, environment, event_literals):
        self.state = state
        self.env = environment.env
        self.space = self.env.action_space
        if self.space.__class__.__name__ != "LiteralActionSpace":
            raise ValueError("Input provided not compatible with natural events")
        self.event_literals = event_literals if event_literals is not None else self.space.event_literals
        self.environment = environment

    @abstractmethod
    def apply_nature(self):
        """Abstract method that must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method")


class IndependentEvents(BaseNature):
    def apply_nature(self):
        obs = None
        selected_events = []
        required = set() #Tracks preconditions that must hold
        changed = set() # tracks variables that have changed
        selectable = self.event_literals.copy()

        while selectable:
            # Randomly select an event from the selectable list
            event_order = self.space.np_random.choice(len(selectable))
            event = selectable[event_order-1]

            if self.is_pairwise_independent(event, self.state, selected_events, required, changed):
                preconditions = self.space._ground_action_to_pos_preconds[event]
                effects = self.space._ground_action_to_effects[event]
                print(effects)

                for precondition in preconditions:
                    required.add(precondition) # Add precondition as needed
                for effect in effects:
                    changed.add(effect) # Add effect as changed

                selected_events.append(event)
            selectable.pop(event_order)
        if len(selected_events) != 0:
            for event in selected_events:
                obs, reward, done, _, _ = self.environment.step(event)
        else:
            obs = self.state

        return obs, selected_events, self.event_literals



    def is_pairwise_independent(self, event, state, selected_events, required, changed):
        """ Check if an event can be applied along with already selected ones. """
        preconditions = self.space._ground_action_to_pos_preconds[event]
        effects = self.space._ground_action_to_effects[event]

        # Condition 1: Precondition should not be marked as changed by a previous event
        for precondition in preconditions:
            if precondition in changed:
                return False

        # Condition 2: Effects should not override required preconditions
        for effect in effects:
            if effect in required:
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


class NoNature(BaseNature):
    def apply_nature(self):
        selected_events = None
        self.event_literals = None
        return self.state, selected_events, self.event_literals


def create_nature(nature_type, state, environment, event_literals):
    nature_classes = {
        "IndependentEvents": IndependentEvents,
        "NoNature": NoNature
    }

    if nature_type not in nature_classes:
        raise ValueError(f"Unknown nature type: {nature_type}")

    return nature_classes[nature_type](state, environment, event_literals)