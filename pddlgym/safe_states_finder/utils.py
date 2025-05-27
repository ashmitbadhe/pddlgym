import os
import sys
import copy

from typing import List, Set, Dict, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "fast_downward", "translate"))) # necessary for correct importing inside translator

from pddlgym.downward_translate.sas_tasks import SASVariables

def argmax(list: List[int]) -> List[int]:
    max_index = [0]
    max_value = list[0]
    for i in range(1, len(list)):
        if list[i] > max_value:
            max_index = [i]
            max_value = list[i]
        elif list[i] == max_value:
            max_index.append(i)
    return max_index

def range_permutations(variables: SASVariables, variable_indeces: List[int]) -> List[Dict[int, int]]:
    permutations = [dict()]
    for v in variable_indeces:
        new_permutations = []
        for permutation in permutations:
            for value in range(variables.ranges[v]):
                new_permutation = permutation.copy()
                new_permutation[v] = value
                new_permutations.append(new_permutation)
        permutations = new_permutations
    return permutations

