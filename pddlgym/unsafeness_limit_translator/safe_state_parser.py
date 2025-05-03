import sys

from typing import Tuple
from pddlgym.downward_translate.pddl_parser import lisp_parser

import mapping

def parse_safe_states(safe_states_file: str) -> list:
    with open(safe_states_file) as file:
        return [parse_safe_state(x) for x in file if x.strip() != ""]

def parse_safe_state(line: str) -> list:
    line = line.strip()
    if ';' in line:
        line = line.split(";")[0]
    elements = []
    element, rest = cut_element(line)
    elements.append(element)
    while rest.strip() != "":
        element, rest = cut_element(rest)
        elements.append(element)
    return [mapping.PDDLPredicate(lisp_parser.parse_nested_list([x])) for x in elements]

def cut_element(string: str) -> Tuple[str, str]:
    string = string.strip()
    remaining_count = 1
    if string[0] != '(':
        print("Missing ( at the beginning of the given string.", file=sys.stderr)
        exit(1)
    for i in range(1, len(string)):
        character = string[i]
        if character == '(':
            remaining_count += 1
        elif character == ')':
            remaining_count -= 1
            if remaining_count == 0:
                return string[: i + 1], string[i + 1:]
    print("Invalid element was tried to cut.", file=sys.stderr)
    exit(1)
