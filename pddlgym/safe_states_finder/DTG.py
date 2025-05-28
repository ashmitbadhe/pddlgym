from pddlgym.structs import Anti

class DTGMatrixElement:
    def __init__(self):
        self.edge = False
        self.path = False
        self.leaf = False

class DTG:
    def __init__(self, problem, obs_lits, operator_type='both'):
        self._problem = problem
        self.obs_lits = obs_lits
        self._type_operators = operator_type
        self._DTGs = {}

    def process_STRIPS_Operator(self, op):
        for eff in op.add_effects:
            predicate = eff.predicate
            if predicate not in self._DTGs:
                continue

            for lit in self._DTGs[predicate]:
                if lit == eff:
                    if eff in op.preconditions:
                        self._DTGs[predicate][lit][1][1].edge = True  # stays true
                    else:
                        self._DTGs[predicate][lit][0][1].edge = True  # becomes true

        for eff in op.del_effects:
            predicate = eff.predicate
            if predicate not in self._DTGs:
                continue

            anti_eff = Anti(eff)
            for lit in self._DTGs[predicate]:
                if lit == anti_eff:
                    self._DTGs[predicate][lit][1][0].edge = True  # becomes false

    def detect_Paths(self, matrix):
        for from_val in [0, 1]:
            for to_val in [0, 1]:
                if matrix[from_val][to_val].edge:
                    matrix[from_val][to_val].path = True

        for val in [0, 1]:
            if not matrix[val][1 - val].path:
                matrix[val][val].leaf = True

    def BuildDTGs(self):
        predicates = self._problem.get_predicates()

        for pred in predicates:
            self._DTGs[pred] = {}
            for lit in self.obs_lits:
                if lit.predicate == pred:
                    self._DTGs[pred][lit] = [[DTGMatrixElement() for _ in range(2)] for _ in range(2)]

        for act in self._problem.get_actions():
            self.process_STRIPS_Operator(act)

        for pred in self._DTGs:
            for lit in self._DTGs[pred]:
                self.detect_Paths(self._DTGs[pred][lit])

    def isLeaf(self, predicate, lit, value):
        try:
            return self._DTGs[predicate][lit][value][value].leaf
        except KeyError:
            return False

    def isPath(self, predicate, lit, from_value, to_value):
        try:
            return self._DTGs[predicate][lit][from_value][to_value].path
        except KeyError:
            return False

    def outputDTGInfo(self):
        for pred in self._DTGs:
            print(f"Predicate: {pred}")
            for lit in self._DTGs[pred]:
                for j in [0, 1]:
                    if self.isLeaf(pred, lit, j):
                        print(f"  {lit} = {bool(j)} is a leaf")
                    for k in [0, 1]:
                        if j != k and self.isPath(pred, lit, j, k):
                            print(f"  {lit} = {bool(j)} --> {bool(k)}")
