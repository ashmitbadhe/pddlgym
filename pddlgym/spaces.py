"""Gym spaces involving Literals.

Unlike typical spaces, Literal spaces may change with
each episode, since objects, and therefore possible
groundings, may change with each new PDDL problem.
"""
from pddlgym.structs import LiteralConjunction, Literal, ground_literal, State
from pddlgym.parser import PDDLProblemParser
from pddlgym.downward_translate.instantiate import explore as downward_explore
from pddlgym.downward_translate.pddl_parser import open as downward_open
from pddlgym.utils import nostdout
from gym.spaces import Space
from collections import defaultdict

import os
import tempfile
import itertools

TMP_PDDL_DIR = "/dev/shm" if os.path.exists("/dev/shm") else None


class LiteralSpace(Space):

    def __init__(self, predicates,
                 lit_valid_test=lambda state,lit: True,
                 type_hierarchy=None,
                 type_to_parent_types=None):
        self.predicates = sorted(predicates)
        self.num_predicates = len(predicates)
        self._objects = None
        self._lit_valid_test = lit_valid_test
        self.type_hierarchy = type_hierarchy
        self._type_to_parent_types = type_to_parent_types
        super().__init__()

    def reset_initial_state(self, initial_state):
        self._objects = None

    def _update_objects_from_state(self, state):
        """Given a state, extract the objects and if they have changed,
        recompute all ground literals
        """
        # Check whether the objects have changed
        # If so, we need to recompute the ground literals
        if state.objects == self._objects:
            return

        # Organize objects by type
        self._type_to_objs = defaultdict(list)

        for obj in sorted(state.objects):
            if self._type_to_parent_types is None:
                self._type_to_objs[obj.var_type].append(obj)
            else:
                for t in self._type_to_parent_types[obj.var_type]:
                    self._type_to_objs[t].append(obj)

        self._objects = state.objects
        self._all_ground_literals = sorted(self._compute_all_ground_literals(state))

    def sample_literal(self, state):
        while True:
            num_lits = len(self._all_ground_literals)
            if num_lits:
                idx = self.np_random.choice(num_lits)
            else:
                return None
            lit = self._all_ground_literals[idx]
            if self._lit_valid_test(state, lit):
                break
        return lit

    def sample(self, state):
        self._update_objects_from_state(state)
        return self.sample_literal(state)

    def all_ground_literals(self, state, valid_only=True):
        self._update_objects_from_state(state)
        if not valid_only:
            return set(self._all_ground_literals)
        return set(l for l in self._all_ground_literals \
                   if self._lit_valid_test(state, l))

    def _compute_all_ground_literals(self, state):
        all_ground_literals = set()
        for predicate in self.predicates:
            choices = [self._type_to_objs[vt] for vt in predicate.var_types]
            for choice in itertools.product(*choices):
                if len(set(choice)) != len(choice):
                    continue
                lit = predicate(*choice)
                all_ground_literals.add(lit)
        return all_ground_literals

    def contains(self, x):
        """Return boolean if x is a valid member of this space."""
        if not isinstance(x, State):
            return False

        # Check all predicates can be grounded from the objects in the state.
        try:
            # If the state contains object types not defined in the environment, a KeyError is raised.
            self._update_objects_from_state(x)
        except KeyError:
            return False

        # Check all state and goal literals are valid.
        for lit in (x.literals | set(x.goal.literals)):
            if lit not in self._all_ground_literals:
                return False

        return True



class LiteralActionSpace(LiteralSpace):
    """Literal space with more efficient valid action generation.

    For now, assumes operators_as_actions.
    """
    def __init__(self, domain, action_predicates, event_predicates,
                 type_hierarchy=None, type_to_parent_types=None):
        self.action_predicates = action_predicates
        self.event_predicates = event_predicates
        self.event_literals = []
        self.domain = domain
        self._initial_state = None
        if not domain.operators_as_actions:
            raise NotImplementedError()
        # Validate and organize operators
        action_predicate_to_operators = {}
        event_predicate_to_operators = {}
        for operator_name, operator in domain.operators.items():
            assert (len([p for p in action_predicates if p.name == operator_name]) == 1 or
            len([p for p in event_predicates if p.name == operator_name]) == 1)

            try:
                action_predicate = [p for p in action_predicates if p.name == operator_name][0]
                action_predicate_to_operators[action_predicate] = operator
            except:
                event_predicate = [p for p in event_predicates if p.name == operator_name][0]
                event_predicate_to_operators[event_predicate] = operator
            if isinstance(operator.preconds, LiteralConjunction):
                assert all([isinstance(l, Literal) for l in operator.preconds.literals])
            else:
                assert isinstance(operator.preconds, Literal)
        self._action_predicate_to_operators = action_predicate_to_operators
        self._event_predicate_to_operators = event_predicate_to_operators
        super().__init__(action_predicates+event_predicates,
            type_hierarchy=type_hierarchy,
            type_to_parent_types=type_to_parent_types)

    def reset_initial_state(self, initial_state):
        super().reset_initial_state(initial_state)
        self._initial_state = initial_state

    def _update_objects_from_state(self, state):
        # Check whether the objects have changed
        # If so, we need to recompute things
        if state.objects == self._objects:
            return

        # Parent class update
        super()._update_objects_from_state(state)

        # Recompute all ground operators
        # Associate each ground action literal with ground preconditions
        self._ground_action_to_pos_preconds = {}
        self._ground_action_to_neg_preconds = {}
        self._ground_action_to_effects = {}
        for ground_action in self._all_ground_literals+self.event_literals:
            if ground_action.predicate in self.action_predicates:
                operator = self._action_predicate_to_operators[ground_action.predicate]
            else:
                operator = self._event_predicate_to_operators[ground_action.predicate]

            lifted_effects = operator.effects.literals
            if isinstance(operator.preconds, LiteralConjunction):
                lifted_preconds = operator.preconds.literals
            else:
                assert isinstance(operator.preconds, Literal)
                lifted_preconds = [operator.preconds]
            subs = dict(zip(operator.params, ground_action.variables))
            subs.update(zip(self.domain.constants, self.domain.constants))
            preconds = [ground_literal(lit, subs) for lit in lifted_preconds]
            effects = [ground_literal(lit, subs) for lit in lifted_effects]
            pos_preconds, neg_preconds = set(), set()
            for p in preconds:
                if p.is_negative:
                    neg_preconds.add(p.positive)
                else:
                    pos_preconds.add(p)
            self._ground_action_to_pos_preconds[ground_action] = pos_preconds
            self._ground_action_to_neg_preconds[ground_action] = neg_preconds
            self._ground_action_to_effects[ground_action] = effects

    def sample_literal(self, state):
        valid_literals = self.all_ground_literals(state)
        valid_literals = list(sorted(valid_literals))
        if len(valid_literals) != 0:
            return valid_literals[self.np_random.choice(len(valid_literals))]

    def sample(self, state):
        return self.sample_literal(state)

    def all_ground_literals(self, state, valid_only=True):
        self._update_objects_from_state(state)
        assert valid_only, "The point of this class is to avoid the cross product!"
        valid_literals = set()
        for ground_action in self._all_ground_literals:
            pos_preconds = self._ground_action_to_pos_preconds[ground_action]
            if not pos_preconds.issubset(state.literals):
                continue
            neg_preconds = self._ground_action_to_neg_preconds[ground_action]
            if len(neg_preconds & state.literals) > 0:
                continue
            valid_literals.add(ground_action)
        return valid_literals

    def _compute_all_ground_literals(self, state):
        """Call FastDownward's instantiator.
        """
        # Generate temporary files to hand over to instantiator.
        assert state.objects == self._initial_state.objects
        d_desc, domain_fname = tempfile.mkstemp(dir=TMP_PDDL_DIR, text=True)
        self.domain.write(domain_fname)
        p_desc, problem_fname = tempfile.mkstemp(dir=TMP_PDDL_DIR, text=True)
        with os.fdopen(p_desc, "w") as f:
            PDDLProblemParser.create_pddl_file(
                file_or_filepath=f,
                objects=state.objects-set(self.domain.constants),
                initial_state=self._initial_state.literals,
                problem_name="myproblem",
                domain_name=self.domain.domain_name,
                goal=state.goal,
                fast_downward_order=True)
        # Call instantiator.
        task = downward_open(domain_fname, problem_fname)
        with nostdout():
            _, _, actions, _, _ = downward_explore(task)
        # Post-process to our representation.
        obj_name_to_obj = {obj.name: obj for obj in state.objects}
        action_ground_literals = set()
        for action in actions:
            is_event = False
            name = action.name.strip().strip("()").split()
            pred_name, obj_names = name[0], name[1:]
            if len(set(obj_names)) != len(obj_names):
                continue
            pred = None
            for p in self.action_predicates:
                if p.name == pred_name:
                    assert pred is None
                    pred = p
                    break
            for p in self.event_predicates:
                if p.name == pred_name:
                    assert pred is None
                    pred = p
                    is_event = True
                    break
            assert pred is not None
            objs = [obj_name_to_obj[obj_name] for obj_name in obj_names]
            if is_event:
                self.event_literals.append(pred(*objs))
            else:
                action_ground_literals.add(pred(*objs))
        os.close(d_desc)
        return action_ground_literals


class LiteralSetSpace(LiteralSpace):

    def sample(self):
        raise NotImplementedError()