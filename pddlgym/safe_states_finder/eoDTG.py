from __future__ import annotations

import sys
import os

from typing import List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "fast_downward",
                                             "translate")))  # necessary for correct importing inside translator

from pddlgym.downward_translate.sas_tasks import SASTask, SASOperator, SASVariables


class eoDTG:

    def __init__(self, variable: int, variables: SASVariables, operators: List[SASOperator]):

        assert 0 <= variable < len(variables.ranges)

        # conditional effects are ignored!
        def get_corresponding_pre_eff(variable: int, operator: SASOperator):
            for v, pre, post, cond in operator.pre_post:
                if v == variable:
                    return pre, post
            return None

        self.variable = variable
        self.nodes: List[eoDTG_node] = [eoDTG_node(i) for i in range(variables.ranges[variable])]

        for operator in operators:
            pre_post = get_corresponding_pre_eff(variable, operator)
            if pre_post is not None:
                edge = eoDTG_edge(operator, self.nodes[pre_post[1]])
                if pre_post[0] == -1:
                    for node in self.nodes:
                        if pre_post[1] != node.value:
                            node.edges.append(edge)
                else:
                    self.nodes[pre_post[0]].edges.append(edge)

    def get_connected_nodes(self, event: SASOperator):
        pairs = set()
        for node in self.nodes:
            pairs |= node.get_connected_nodes(event)
        return list(pairs)

    def dump(self):
        print("eoDTG(var={})".format(self.variable))
        if any(len(node.edges) > 0 for node in self.nodes):
            for node in self.nodes:
                node.dump()
        else:
            print("  - no edges")


class eoDTG_node:

    def __init__(self, value: int):
        assert value >= 0
        self.value: int = value
        self.edges: List[eoDTG_edge] = []

    def get_connected_nodes(self, event: SASOperator):
        return set((self.value, edge.node.value) for edge in self.edges if edge.operator is event)

    def dump(self):
        for edge in self.edges:
            print("{} == {} ==> {}".format(self.value, edge.operator.name, edge.node.value))


class eoDTG_edge:

    def __init__(self, operator: SASOperator, node: eoDTG_node):
        self.operator: SASOperator = operator
        self.node: eoDTG_node = node

    def dump(self):
        print(self.operator.name)


class eoDTG_path:

    def __init__(self, previous: eoDTG_path = None, new_edge: eoDTG_edge = None):
        self.path: List[eoDTG_edge] = []
        if previous is not None:
            self.path: List[eoDTG_edge] = previous.path.copy()
        if previous is not None:
            self.path.append(new_edge)

    def length(self) -> int:
        return len(self.path)

    def dump(self):
        print("eoDTG path", f"  - lenght {len(self.path)}", sep='\n')
        for edge in self.path:
            edge.dump()
