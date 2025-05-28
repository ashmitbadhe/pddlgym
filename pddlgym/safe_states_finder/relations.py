import os
import sys

from typing import Set, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "fast_downward", "translate"))) # necessary for correct importing inside translator

from pddlgym.downward_translate.sas_tasks import SASVariables, SASOperator, SASTask, SASInit


def is_cloberrer(x: SASOperator, y: SASOperator) -> bool:

    preconditions_y = {var: pre for var, pre in y.prevail}
    preconditions_y.update({var: pre for (var, pre, post, cond) in y.pre_post})
    effects_x = {var: post for (var, pre, post, cond) in x.pre_post}

    for v, val_prime in effects_x.items():
        if v in preconditions_y and val_prime != preconditions_y[v]:
            return True
    return False

def is_fake_cloberrer(x: SASOperator, y: SASOperator) -> bool:

    preconditions_y = {var: pre for var, pre in y.prevail}
    preconditions_y.update({var: pre for (var, pre, post, cond) in y.pre_post})
    preconditions_x = {var: pre for var, pre in x.prevail}
    preconditions_x.update({var: pre for (var, pre, post, cond) in x.pre_post})
    effects_x = {var: post for (var, pre, post, cond) in x.pre_post}

    for v, val_prime in effects_x.items():
        if v in preconditions_x and v in preconditions_y and val_prime != preconditions_y[v] and preconditions_x[v] == preconditions_y[v]:
            return True
    return False

def is_cloberrer_for(x: SASOperator, y: SASOperator) -> int:

    preconditions_y = {var: pre for var, pre in y.prevail}
    preconditions_y.update({var: pre for (var, pre, post, cond) in y.pre_post})
    effects_x = {var: post for (var, pre, post, cond) in x.pre_post}

    for v, val_prime in effects_x.items():
        if v in preconditions_y and val_prime != preconditions_y[v]:
            return v
    return None

def is_achiever(x: SASOperator, y: SASOperator) -> bool:

    preconditions_y = {var: pre for var, pre in y.prevail}
    preconditions_y.update({var: pre for (var, pre, post, cond) in y.pre_post})
    effects_x = {var: post for (var, pre, post, cond) in x.pre_post}

    for v, val_prime in effects_x.items():
        if v in preconditions_y and val_prime == preconditions_y[v]:
            return True
    return False

def holds_in(p: Set[Tuple[int, int]], q: Set[Tuple[int, int]]):
    if isinstance(p, list) and len(p) > 0 and isinstance(p[0], int):
        p = set((i, val) for i, val in enumerate(p))
    elif isinstance(p, list) and len(p) > 0 and isinstance(p[0], tuple):
        p = set(p)
    if isinstance(q, list) and len(q) > 0 and isinstance(q[0], int):
        q = set((i, val) for i, val in enumerate(q))
    elif isinstance(q, list) and len(q) > 0 and isinstance(q[0], tuple):
        q = set(q)
    return all((v, -1) in p or (v, val) in p for (v, val) in q if val != -1)
