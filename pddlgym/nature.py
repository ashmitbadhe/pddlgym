import random
from abc import ABC, abstractmethod
from pddlgym.structs import Anti
import random
class BaseNature(ABC):
    def __init__(self, state, environment):
        self.state = state
        self.env = environment.env
        self.space = self.env.action_space
        if self.space.__class__.__name__ != "LiteralActionSpace":
            raise ValueError("Input provided not compatible with natural events")
        self.event_literals = self.space.event_literals
        self.environment = environment

    @abstractmethod
    def apply_nature(self, state):
        """Abstract method that must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method")


class IndependentEvents(BaseNature):
    def apply_nature(self, state):
        obs = None
        selected_events = []
        selectable = self.is_applicable(self.event_literals, state)

        # select number from 0 to len(selectable_events)
        # this number is the position of nth action from selectable applicable events
        # 0 stands for noop event, and it is used for termination

        while (event_order := random.randint(0, len(selectable))) != 0:
            effect_index = 0
            current_order = 0
            while (current_order != event_order):
                while (selectable[effect_index] is False):
                    effect_index += 1
                current_order += 1
                effect_index += 1
            effect_index -= 1

            event = selectable[effect_index]

            #check if concurrently applicable
            if self.is_pairwise_independent(event, selected_events):
                selected_events.append(event)
            else:
                selectable.pop(effect_index)

        #apply selected events to state
        if len(selected_events) != 0:
            obs = self.environment.simulate_events(selected_events, apply_bool=True)
        else:
            obs = state

        return obs, selected_events, self.event_literals



    def is_pairwise_independent(self, event, selected_events):
        """ Check if an event can be applied along with already selected ones. """
        preconditions_ei = self.space._ground_action_to_pos_preconds[event]
        all_effects_ei = self.space._ground_action_to_effects[event]
        add_effects_ei = set()
        del_effects_ei = set()
        for effect in all_effects_ei:
            if "Anti" in str(effect):
                del_effects_ei.add(Anti(effect))
            else:
                add_effects_ei.add(effect)

        # Check conditions against already selected events
        for selected_event in selected_events:
            preconditions_ej = self.space._ground_action_to_pos_preconds[selected_event]
            all_effects_ej = self.space._ground_action_to_effects[event]
            add_effects_ej = set()
            del_effects_ej = set()
            for effect in all_effects_ej:
                if "Anti" in str(effect):
                    del_effects_ei.add(Anti(effect))
                else:
                    add_effects_ei.add(effect)

            # Condition 1: addEffect(ei) ∩ (precondition(ej) ∪ delEffect(ej)) = ∅
            if add_effects_ei & (preconditions_ej | del_effects_ej):
                return False

            # Condition 2: delEffect(ei) ∩ (precondition(ej) ∪ addEffect(ej)) = ∅
            if del_effects_ei & (preconditions_ej | add_effects_ej):
                return False

            # Condition 3: addEffect(ej) ∩ (precondition(ei) ∪ delEffect(ei)) = ∅
            if add_effects_ej & (preconditions_ei | del_effects_ei):
                return False

            # Condition 4: delEffect(ej) ∩ (precondition(ei) ∪ addEffect(ei)) = ∅
            if del_effects_ej & (preconditions_ei | add_effects_ei):
                return False

        return True

    def is_applicable(self, all_event_literals, state):
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


class NoNature(BaseNature):
    def apply_nature(self, state):
        selected_events = None
        self.event_literals = None
        return state, selected_events, self.event_literals


def create_nature(nature_type, state, environment):
    nature_classes = {
        "IndependentEvents": IndependentEvents,
        "NoNature": NoNature
    }

    if nature_type not in nature_classes:
        raise ValueError(f"Unknown nature type: {nature_type}")

    return nature_classes[nature_type](state, environment)