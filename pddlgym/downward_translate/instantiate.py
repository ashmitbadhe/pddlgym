#! /usr/bin/env python3


from collections import defaultdict

from . import build_model
from . import pddl_to_prolog
from . import pddl
from . import timers

def get_fluent_facts(task, model):
    fluent_predicates = set()
    for operator in task.actions+ task.events:
        for effect in operator.effects:
            fluent_predicates.add(effect.literal.predicate)
    for axiom in task.axioms:
        fluent_predicates.add(axiom.name)
    return {fact for fact in model
            if fact.predicate in fluent_predicates}

def get_objects_by_type(typed_objects, types):
    result = defaultdict(list)
    supertypes = {}
    for type in types:
        supertypes[type.name] = type.supertype_names
    for obj in typed_objects:
        result[obj.type_name].append(obj.name)
        for type in supertypes[obj.type_name]:
            result[type].append(obj.name)
    return result

def instantiate(task, model):
    relaxed_reachable = False
    fluent_facts = get_fluent_facts(task, model)
    init_facts = set()
    init_assignments = {}
    for element in task.init:
        if isinstance(element, pddl.Assign):
            init_assignments[element.fluent] = element.expression
        else:
            init_facts.add(element)

    type_to_objects = get_objects_by_type(task.objects, task.types)

    instantiated_actions = []
    instantiated_axioms = []
    reachable_action_parameters = defaultdict(list)
    for atom in model:
        if isinstance(atom.predicate, pddl.Action) or isinstance(atom.predicate, pddl.Event):
            action = atom.predicate
            parameters = action.parameters
            inst_parameters = atom.args[:len(parameters)]
            # Note: It's important that we use the action object
            # itself as the key in reachable_action_parameters (rather
            # than action.name) since we can have multiple different
            # actions with the same name after normalization, and we
            # want to distinguish their instantiations.
            reachable_action_parameters[action].append(inst_parameters)
            variable_mapping = {par.name: arg
                                for par, arg in zip(parameters, atom.args)}
            inst_action = action.instantiate(
                variable_mapping, init_facts, init_assignments,
                fluent_facts, type_to_objects,
                task.use_min_cost_metric)
            if inst_action:
                instantiated_actions.append(inst_action)
        elif isinstance(atom.predicate, pddl.Axiom):
            axiom = atom.predicate
            variable_mapping = {par.name: arg
                                for par, arg in zip(axiom.parameters, atom.args)}
            inst_axiom = axiom.instantiate(variable_mapping, init_facts, fluent_facts)
            if inst_axiom:
                instantiated_axioms.append(inst_axiom)
        elif atom.predicate == "@goal-reachable":
            relaxed_reachable = True
    return (relaxed_reachable, fluent_facts, instantiated_actions,
            sorted(instantiated_axioms), reachable_action_parameters)

def explore(task):
    prog = pddl_to_prolog.translate(task)
    model = build_model.compute_model(prog)
    with timers.timing("Completing instantiation"):
        return instantiate(task, model)

if __name__ == "__main__":
    import pddl_parser
    task = pddl_parser.open()
    relaxed_reachable, atoms, actions, events, axioms, _, _ = explore(task)
    print("goal relaxed reachable: %s" % relaxed_reachable)
    print("%d atoms:" % len(atoms))
    for atom in atoms:
        print(" ", atom)
    print()
    print("%d actions:" % len(actions))
    print("%d events:" % len(events))
    for action in actions:
        action.dump()
        print()
    print()
    for event in events:
        event.dump()
        print()
    print()
    print("%d axioms:" % len(axioms))
    for axiom in axioms:
        axiom.dump()
        print()
