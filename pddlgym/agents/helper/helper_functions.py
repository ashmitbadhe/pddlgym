from pddlgym.structs import Anti, Literal, Predicate, TypedEntity, Type
import subprocess
import os
import re
class Helper:
    def __init__(self, env, domain_filepath, problem_filepath):
        self.env = env
        self.domain = env.domain
        self.space = env.action_space
        self.domain_filepath = domain_filepath
        self.problem_filepath = problem_filepath
        self.objects = self.get_objects_from_problem()
    def get_add_del_effects(self, action, state):
        self.space._update_objects_from_state(state)
        add_effects = set()
        del_effects = set()
        all_effects = self.space._ground_action_to_effects[action]
        for effect in all_effects:
            if "Anti" in str(effect):
                del_effects.add(Anti(effect))
            else:
                add_effects.add(effect)

        return add_effects, del_effects

    def to_Literal(self, action_str):
        action_str_stripped = action_str[1:-1]
        vars = list(action_str_stripped.split(" ")[1:])
        for i in range(len(vars)):
            if vars[i] in self.objects:
                vars[i] = self.objects[vars[i]]
        pred = Predicate(action_str_stripped.split(" ")[0], len(vars))
        action_literal = Literal(pred, vars)
        return action_literal

    def is_action_applicable(self, action, state):
        self.space._update_objects_from_state(state)
        pos_preconds = self.space._ground_action_to_pos_preconds[action]
        if not pos_preconds.issubset(state.literals):
            return False
        neg_preconds = self.space._ground_action_to_neg_preconds[action]
        if len(neg_preconds & state.literals) > 0:
            return False
        return True

    def simulate_action(self, state, action):
        next_deterministic_state = self.env.simulate_events(action, state, False)
        return next_deterministic_state

    def applicable_events(self, all_event_literals, state, p_plus=None, p_minus=None):
        self.space._update_objects_from_state(state)

        if p_plus is None:
            p_plus = set()
        if p_minus is None:
            p_minus = set()

        optimistic_state = state.literals | p_plus
        pessimistic_state = state.literals - p_minus

        valid_literals = set()

        for event_literal in all_event_literals:
            pos_preconds = self.space._ground_action_to_pos_preconds[event_literal]
            neg_preconds = self.space._ground_action_to_neg_preconds[event_literal]

            if pos_preconds.issubset(optimistic_state) and neg_preconds.isdisjoint(pessimistic_state):
                valid_literals.add(event_literal)

        return list(valid_literals)

    def get_objects_from_problem(self):
        """
        Extract all objects from the problem file.
        Assumes that the objects are listed under the `:objects` section of the PDDL problem.
        """
        with open(self.problem_filepath, 'r') as problem_file:
            problem_content = problem_file.read()

        # Search for the :objects section using regex
        objects_match = re.search(r"\(:objects(.*?)\)", problem_content, re.DOTALL)

        if objects_match:
            # Extract the objects part and strip it of extra whitespace
            objects_str = objects_match.group(1).strip()

            # The objects are typically listed after the parentheses
            # Now we split by spaces and consider each object as a separate item
            objects = objects_str.split()
            types = [None]
            typed_objects = {}
            for i in range(len(objects)):
                index = len(objects)-1-i
                if objects[index] in self.domain.types:
                    types.append(objects[index])
                elif objects[index] == '-':
                    pass
                else:
                    typed_objects[objects[index]] = (TypedEntity(objects[index], Type(types[-1])))




            # Return the objects as a list of strings
            return typed_objects

        return []

