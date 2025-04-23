#!/usr/bin/env python3

import os
import sys
import math
import mypy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "fast_downward", "translate"))) # necessary for correct importing inside translator

from fast_downward.translate import timers
from fast_downward.translate import normalize
from fast_downward.translate import pddl_parser
from fast_downward.translate.translate import pddl_to_sas, dump_statistics
from fast_downward.translate import options
from fast_downward.translate.pddl_parser import lisp_parser
from fast_downward.translate.sas_tasks import SASVariables
from fast_downward.translate.sas_tasks import SASOperator
from fast_downward.translate.sas_tasks import SASTask
from fast_downward.translate.sas_tasks import SASInit
from fast_downward.translate.pddl.tasks import Task

import mapping
import safe_state_parser

# options
limit_predicate_name = "unsafe-token"
event_prefix = "event-action-"

def translate(safe_states_file) -> None:

    global limit_predicate_name

    # load safe states
    safe_states: list = safe_state_parser.parse_safe_states(safe_states_file)

    # translate to SAS
    timer = timers.Timer()
    with timers.timing("Parsing", True):
        task = pddl_parser.open()

    # add events to planner
    if options.add_events:
        for event in task.events:
            event.name = event_prefix + event.name
        task.actions += task.events

    with timers.timing("Normalizing task"):
        normalize.normalize(task)

    if options.generate_relaxed_task:
        for action in task.actions:
            for index, effect in reversed(list(enumerate(action.effects))):
                if effect.literal.negated:
                    del action.effects[index]

    sas_task = pddl_to_sas(task)
    dump_statistics(sas_task)

    # modify sas
    limit_predicate_name = check_limit_variable_name_availability(limit_predicate_name, task)
    add_limit_variable(sas_task.variables, limit_predicate_name)
    add_start_state_value(sas_task.init, options.unsafety_limit)
    translate_operators(sas_task.operators, safe_states, sas_task, task)

    # write to file
    with timers.timing("Writing output"):
        with open(os.path.join(os.path.dirname(__file__), "output.sas"), "w") as output_file:
            sas_task.output(output_file)
    print("Done! %s" % timer)

def add_start_state_value(init: SASInit, value: int) -> None:
    init.values.append(value)

def add_limit_variable(sas_variables: SASVariables, name: str) -> None:
    sas_variables.axiom_layers.append(-1)
    sas_variables.ranges.append(options.unsafety_limit + 1)
    sas_variables.value_names.append(["Atom " + name + str(x) + "()" for x in range(0, options.unsafety_limit + 1)])

def check_limit_variable_name_availability(name: str, task: Task) -> str:
    while not all(check_predicate_availability(name + str(x), task) for x in range(0, options.unsafety_limit + 1)):
        name = "alt-" + name
    return name

def check_predicate_availability(name: str, task: Task) -> bool:
    for predicate in task.predicates:
        if predicate.name == name:
            return False
    return True

def is_operator_safe(operator: SASOperator, safe_states: list, sas_task: SASTask, pddl_task: Task) -> bool:

    # TODO: conditional variables are not processed
    eff = set((var, post) for (var, pre, post, cond) in operator.pre_post) # Type: Set[Tuple[int, int]]
    pre = set(x for x in operator.prevail) | set((var, pre) for (var, pre, post, cond) in operator.pre_post) # Type: Set[Tuple[int, int]]

    for safe_state in safe_states:
        l_plus = set(predicate.find_sas_variable(sas_task, pddl_task) for predicate in safe_state if predicate.is_positive())
        l_minus = set(predicate.find_sas_variable(sas_task, pddl_task) for predicate in safe_state if predicate.is_negative())
        l_plus = set(x for x in l_plus if x is not None)
        l_minus = set(x for x in l_minus if x is not None)
        """ 
            1. for all v=val from l+:       (v=val \in eff(a)) or (v=val \in pre(a) and v does not change).
            2. for all v!=val from l-:      ((v=val' \in eff(a) or (v=val' \in pre(a) and v does not change))
                                                and val!=val'.
        """
        l_plus_rule_fulfilled = all(
                                    x in eff or (x in pre and x[0] not in set(y[0] for y in eff)) for x in l_plus
                                )
        l_minus_rule_fulfilled = all(
                                    # exists at least one val'
                                    any(
                                        minus_var == var and minus_val != val \
                                        for (var, val) in eff
                                    )
                                    # exists at least one val'
                                    or
                                    any(
                                        var not in set(y[0] for y in eff) \
                                        and minus_var == var and minus_val != val \
                                        for (var, val) in pre
                                    )
                                    for (minus_var, minus_val) in l_minus
                                )

        if l_plus_rule_fulfilled and l_minus_rule_fulfilled:
            return True
    return False    # no operator ends in no safe-state

def translate_operators(operators: list, safe_states: list, sas_task: SASTask, pddl_task: Task) -> None:
    global event_prefix
    operators_count = len(operators) # Type: int
    safe = 0
    unsafe = 0
    ignored = 0
    for i, operator in enumerate(operators.copy()):
        if (i + 1) % min(40, (math.ceil(operators_count / 6))) == 0 or i + 1 == operators_count: # limit logging
            print("Translating operator number %d of %d." % (i + 1, operators_count), file=sys.stderr)
        if options.skip_events and operator.name == "(events )":
            ignored += 1
            continue
        if options.add_events and operator.name.find("(" + event_prefix) == 0:
            ignored += 1
            continue
        if is_operator_safe(operator, safe_states, sas_task, pddl_task):
            translate_safe_operator(operator, sas_task)
            safe += 1
        else:
            translate_unsafe_operator(operator, sas_task)
            unsafe += 1
    print("Operator translating done. %d unsafe operators replaced with %d copies, %d safe operators persisted, %d operators ignored" % (unsafe, unsafe * options.unsafety_limit, safe, ignored))

def translate_safe_operator(operator: SASOperator, task: SASTask) -> None:
    limit_variable_index = len(task.variables.value_names) - 1      # TODO: this may cause bug - order of variables may change
    limit_max_value_index = len(task.variables.value_names[limit_variable_index]) - 1       # TODO: this may cause bug - order of values may change
    operator.pre_post.append((limit_variable_index, -1, limit_max_value_index, [])) # -1 for not caring about currect token level

def translate_unsafe_operator(operator: SASOperator, task: SASTask) -> None:
    limit_variable_index = len(task.variables.value_names) - 1      # TODO: this may cause bug - order of variables may change
    limit_max_value_index = len(task.variables.value_names[limit_variable_index]) - 1       # TODO: this may cause bug - order of values may change
    for step in range(1, limit_max_value_index + 1):
        new_operator = copy_with_name_suffix(operator, "-unsafe-copy-" + str(step))
        new_operator.pre_post.append((limit_variable_index, step, step - 1, []))
        task.operators.append(new_operator)
    task.operators.remove(operator)

def copy_with_name_suffix(operator: SASOperator, suffix: str) -> SASOperator:
    new_name = operator.name.replace(" ", suffix + " ", 1)
    return SASOperator(new_name, operator.prevail.copy(), operator.pre_post.copy(), operator.cost)

if __name__ == "__main__":
    translate(options.safe_state_filepath)