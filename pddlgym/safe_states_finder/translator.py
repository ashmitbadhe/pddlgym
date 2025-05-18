#!/usr/bin/env python3

import os
import sys
import math
import copy
import random

from typing import List, Tuple, Set, Mapping, Dict
from pddlgym.downward_translate.pddl.actions import Action

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "fast_downward",
                                             "translate")))  # necessary for correct importing inside translator

from pddlgym.downward_translate import timers
from pddlgym.downward_translate import normalize
from pddlgym.downward_translate import pddl_parser
from pddlgym.downward_translate.translate import pddl_to_sas, dump_statistics
from pddlgym.downward_translate import options
from pddlgym.downward_translate.sas_tasks import SASVariables, SASOperator, SASTask, SASInit
from pddlgym.downward_translate.pddl.tasks import Task

from utils import argmax, range_permutations
from eoDTG import eoDTG, eoDTG_edge, eoDTG_path
from finder import bfs_any_path_existance_search, bfs_shortest_path_search, dfs_all_paths_search
from relations import holds_in, is_achiever, is_cloberrer, is_cloberrer_for, is_fake_cloberrer

event_prefix = "event-action-"


def translate() -> None:
    sas_task: SASTask = get_sas_task()

    actions = [operator for operator in sas_task.operators if event_prefix not in operator.name]
    irreversible_events, reversible_events, reversible_events_with_states = find_reversible_events(sas_task)

    if (irreversible_events, reversible_events, reversible_events_with_states) == (None, None, None):
        sys.exit(1)

    new_actions = []

    # contruct a new graphs
    eoDTGs: Dict[eoDTG] = {v: eoDTG(v, sas_task.variables, reversible_events) for v in
                           set(var for _, var, _ in reversible_events_with_states)}

    # count maximal and minimal distances
    maximal_distances: Dict[Tuple[int, int], int] = dict()
    minimal_distances: Dict[Tuple[int, int, int], int] = dict()
    for e, v, s in reversible_events_with_states:
        for x in range(sas_task.variables.ranges[v]):
            maximal_distance = -1
            for y in range(sas_task.variables.ranges[v]):
                paths = dfs_all_paths_search(eoDTGs[v], y, x)
                maximal_distance = max(maximal_distance, max(p.length() for p in paths))
                minimal_distances[(v, y, x)] = min(maximal_distance, min(p.length() for p in paths))
            maximal_distances[(v, x)] = maximal_distance

    # add unsafe_count to variables and init
    max_unsafe_count = max(sas_task.variables.ranges[v] for _, v, _ in reversible_events_with_states)
    unsafe_count_variable = len(sas_task.variables.ranges)
    add_unsafe_count_to_init(sas_task.init)
    add_unsafe_count_to_variables(sas_task.variables, max_unsafe_count)

    # add d_v_x's to variables and their values to the initial state
    distance_variables: Dict[Tuple[int, int], int] = dict()
    for v, x in maximal_distances.keys():
        distance_variables[(v, x)] = len(sas_task.variables.ranges)
        add_distance_to_variables(sas_task.variables, v, x, maximal_distances[(v, x)])
        add_distance_to_init(sas_task.init, minimal_distances[(v, sas_task.init.values[v], x)])

    # translate actions
    for action in actions:

        increment: bool = any(is_achiever(action, irreversible_event) for irreversible_event in irreversible_events)
        affected_events: List[irreversible_events] = [irreversible_event for irreversible_event in irreversible_events
                                                      if is_fake_cloberrer(action, irreversible_event)]
        limit: bool = len(affected_events) > 0

        if limit:

            preconditions = set()

            for affected_event in affected_events:
                preconditions |= set((v, pre) for v, pre in affected_event.prevail) | set(
                    (v, pre) for (v, pre, _, _) in affected_event.pre_post)

            vx_pairs = set(
                (v, val) for v, val in preconditions if v in set(var for _, var, _ in reversible_events_with_states))
            permutations = range_permutations(sas_task.variables, [distance_variables[x] for x in vx_pairs])
            unsafe_count_permutations = create_unsafe_count_permutations(permutations, unsafe_count_variable,
                                                                         max_unsafe_count)

            if increment:
                new_actions += constrained_incrementing_copies(action, unsafe_count_variable, unsafe_count_permutations)
            else:
                new_actions += constrained_zeroing_copies(action, unsafe_count_variable, unsafe_count_permutations)

        elif increment:
            new_actions += incrementing_copies(action, max_unsafe_count, unsafe_count_variable)

        else:
            for unsafe_count in range(1, max_unsafe_count):
                copy = copy_with_name_suffix(action, f"-inc-copy-{unsafe_count}-{unsafe_count + 1}")
                copy.pre_post.append((unsafe_count_variable, unsafe_count, unsafe_count + 1, []))
                new_actions.append(copy)
            action.prevail.append((unsafe_count_variable, 0))
            new_actions.append(action)

    # add reversible events to new actions
    for reversible_event in reversible_events:
        copy = copy_with_name_suffix(reversible_event, "-req-0")
        copy.prevail.append((unsafe_count_variable, 0))
        vx_pairs = set((v, post) for v, pre, post, [] in reversible_event.pre_post if
                       v in set(var for _, var, s in reversible_events_with_states))
        for v, x in vx_pairs:
            for y in range(sas_task.variables.ranges[v]):
                copy.pre_post.append((distance_variables[(v, y)], -1, minimal_distances[(v, x, y)], []))
        new_actions.append(copy)

    # replace actions
    sas_task.operators = new_actions

    # write to file
    with timers.timing("Writing output"):
        with open(os.path.join(os.path.dirname(__file__), "output.sas"), "w") as output_file:
            sas_task.output(output_file)
    print("Done!")


def add_distance_to_variables(variables: SASVariables, v: int, x: int, max_value: int):
    variables.axiom_layers.append(-1)
    variables.ranges.append(max_value + 1)
    variables.value_names.append([f'Atom distance_{v}_{x}_{i}()' for i in range(max_value + 1)])


def add_distance_to_init(init: SASInit, value: int):
    init.values.append(value)


def create_unsafe_count_permutations(permutations: List[Dict[int, int]], unsafe_count_variable: int,
                                     max_unsafe_count: int):
    new_permutations = []
    for permutation in permutations:
        for unsafe_count in range(min(max_unsafe_count, min(value for key, value in permutation.items())) + 1):
            new_permutation = permutation.copy()
            new_permutation[unsafe_count_variable] = unsafe_count
            new_permutations.append(new_permutation)
    return new_permutations


def constrained_zeroing_copies(operator: SASOperator, unsafe_count_variable: int,
                               precondition_permutations: List[Dict[int, int]]) -> List[SASOperator]:
    copies = []
    for permutation in precondition_permutations:
        copy = copy_with_name_suffix(operator, f'-constrained-zeroing-copy')
        for variable, value in permutation.items():
            if variable == unsafe_count_variable:
                copy.pre_post.append((variable, value, 0, []))
            else:
                copy.prevail.append((variable, value))
        copies.append(copy)
    return copies


def constrained_incrementing_copies(operator: SASOperator, unsafe_count_variable: int,
                                    precondition_permutations: List[Dict[int, int]]) -> List[SASOperator]:
    copies = []
    for permutation in precondition_permutations:
        copy = copy_with_name_suffix(operator, f'-constrained-inc-copy')
        for variable, value in permutation.items():
            if variable == unsafe_count_variable:
                copy.pre_post.append((variable, value, value + 1, []))
            else:
                copy.prevail.append((variable, value))
        copies.append(copy)
    return copies


def incrementing_copies(operator: SASOperator, up_to: int, v: int) -> List[SASOperator]:
    copies = []
    for pre_value in range(up_to):
        copy = copy_with_name_suffix(operator, f"-inc-copy-{pre_value}-{pre_value + 1}")
        copy.pre_post.append((v, pre_value, pre_value + 1, []))
        copies.append(copy)
    return copies


def add_unsafe_count_to_variables(variables: SASVariables, max: int):
    variables.axiom_layers.append(-1)
    variables.ranges.append(max + 1)
    variables.value_names.append([f'Atom unsafe-count{i}()' for i in range(max + 1)])


def add_unsafe_count_to_init(init: SASInit):
    init.values.append(0)


def copy_with_name_suffix(operator: SASOperator, suffix: str) -> SASOperator:
    new_name = operator.name.replace(" ", suffix + " ", 1)
    return SASOperator(new_name, operator.prevail.copy(), operator.pre_post.copy(), operator.cost)


"""
    Implementation of algorithm 2.
"""


def find_reversible_events(sas_task: SASTask) -> Tuple[
    Set[SASOperator], Set[SASOperator], Tuple[SASOperator, int, List]]:
    events = [o for o in sas_task.operators if event_prefix in o.name]
    eoDTGs: List[eoDTG] = [eoDTG(i, sas_task.variables, events) for i in range(len(sas_task.variables.ranges))]

    undecided_events: Set[SASOperator] = set(events)
    irreversible_events: Set[SASOperator] = set()
    reversible_events_with_states: Tuple[SASOperator, int, List] = set()

    # remove effect with -1 in precondition
    # -1 should not appear in e.prevail, it simply does not make sense
    irreversible_events |= set(e for e in undecided_events if any(pre == -1 for var, pre, post, cond in e.pre_post))
    undecided_events -= irreversible_events

    print(f'{len(irreversible_events)} events were filtered out and marked as irreversible due to -1 in precondition.')

    # remove effect which can not be S reversible
    irreversible_events |= set(e for e in undecided_events if not can_be_S_reversible(e, eoDTGs))
    undecided_events -= irreversible_events

    for event in undecided_events:
        v, state = revert(sas_task.variables, undecided_events, event)
        if v is None and state is None:
            irreversible_events.add(event)
        else:
            reversible_events_with_states.add((event, v, state))

    print(f'{len(irreversible_events)} irreversible events found.')
    print(f'{len(reversible_events_with_states)} are likely reversible.')

    event_reachable_predicates = set((i, value) for i, value in enumerate(sas_task.init.values))
    event_reachable_predicates |= set(
        (var, post) for var, pre, post, cond in event.pre_post for event, _, _ in reversible_events_with_states)
    for irreversible_event in irreversible_events:
        preconditions = set(
            irreversible_event.prevail + [(var, pre) for (var, pre, post, cond) in irreversible_event.pre_post])
        if preconditions.issubset(event_reachable_predicates):
            return None, None, None

    for e, v, s in reversible_events_with_states:
        for e_prime, v_prime, s_prime in reversible_events_with_states:
            if e is not e_prime:
                if v not in set(var for var, pre, post, cond in e_prime.pre_post):
                    if is_cloberrer(e_prime, e):
                        return None, None, None

    reversible_events: Set[SASOperator] = set(e for e, v, s in reversible_events_with_states)

    # for e, v, s in reversible_events_with_states:
    #     graph = eoDTG(v, sas_task.variables, list(reversible_events))
    #     for node in graph.nodes:
    #         x = node.value
    #         y = sas_task.init.values[v]
    #         for path in dfs_all_paths_search(graph, y, x):
    #             for e_prime, v_prime, s_prime in reversible_events_with_states:
    #                 if v == v_prime:
    #                     for edge in graph.nodes[x].edges:
    #                         if edge.operator is e_prime:
    #                             gamma_state = sas_task.init.values.copy()
    #                             for path_edge in path.path:
    #                                 for var, pre, post, cond in path_edge.operator.pre_post:
    #                                     gamma_state[var] = post
    #                             gamma_state = set((v, val) for v, val in enumerate(gamma_state))
    #                             if not holds_in(s_prime, gamma_state):
    #                                 return None, None, None

    print('Validation done.')

    return irreversible_events, reversible_events, reversible_events_with_states


def revert(variables: SASVariables, events: Set[SASOperator], event: SASOperator) -> Tuple[int, List[Tuple[int, int]]]:
    assert len(variables.ranges) > 0

    affected_varibles = [var for (var, pre, post, cond) in event.pre_post]
    affected_ranges = [variables.ranges[affected_varible] for affected_varible in affected_varibles]
    var = affected_varibles[random.choice(argmax(affected_ranges))]

    graph = eoDTG(var, variables, list(events))

    # since we filter out operators with -1 in pre, there will always be only one
    x, y = graph.get_connected_nodes(event)[0]
    path = bfs_shortest_path_search(graph, y, x)

    if path is None:
        return None, None

    s = [-1 for i in range(len(variables.ranges))]
    for operator in [event] + [edge.operator for edge in path.path]:

        preconditions = operator.prevail + [(var, pre) for (var, pre, post, cond) in operator.pre_post]
        effects = [(var, post) for (var, pre, post, cond) in operator.pre_post]

        for (v, pre) in preconditions:
            if s[v] == -1:
                s[v] = pre
        if not holds_in(s, preconditions):
            return None, None
        for (v, post) in effects:
            s[v] = post

    preconditions = event.prevail + [(var, pre) for (var, pre, post, cond) in event.pre_post]

    if not holds_in(s, preconditions):
        return None, None
    else:
        return var, frozenset((i, val) for i, val in enumerate(s) if val is not None)


"""
    Implementation of Lemma 14.
"""


def can_be_S_reversible(e: SASOperator, eoDTGs: List[eoDTG]) -> bool:
    for graph in eoDTGs:
        pairs = graph.get_connected_nodes(e)
        for x, y in pairs:
            if not bfs_any_path_existance_search(graph, y, x):
                return False
    return True


def get_sas_task() -> SASTask:
    timer = timers.Timer()
    with timers.timing("Parsing", True):
        task = pddl_parser.open()

    # replace actions with events
    for event in task.events:
        event.name = event_prefix + event.name
    task.actions += task.events

    with timers.timing("Normalizing task"):
        normalize.normalize(task)

    if options.generate_relaxed_task:
        # Remove delete effects.
        for action in task.actions:
            for index, effect in reversed(list(enumerate(action.effects))):
                if effect.literal.negated:
                    del action.effects[index]

    sas_task = pddl_to_sas(task)
    dump_statistics(sas_task)

    return sas_task


if __name__ == "__main__":
    translate()
