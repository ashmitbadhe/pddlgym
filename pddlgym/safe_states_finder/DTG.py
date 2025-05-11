class DTGMatrixElement:
    def __init__(self):
        self.edge = False
        self.path = False
        self.leaf = False

class DTG:
    def __init__(self, problem, operator_type):
        self._problem = problem  # Assuming 'problem' has methods like get_variables(), get_events(), etc.
        self._type_operators = operator_type
        self._DTGs = []  # This will store the DTG matrices

    def process_STRIPS_Operator(self, op):
        # For each add effect, create an edge from preconditions to the fact becoming true
        for eff in op.add_effects:
            if eff in op.preconditions:
                self._DTGs[eff][True][True].edge = True  # self-loop
            else:
                self._DTGs[eff][False][True].edge = True

        # For each delete effect, create an edge from preconditions to the fact becoming false
        for eff in op.del_effects:
            if eff in op.preconditions:
                self._DTGs[eff][True][False].edge = True  # transition from True to False
            else:
                self._DTGs[eff][True][False].edge = True

    def detect_Paths(self, graph):
        n = 2  # Only two states: False (0), True (1)

        for i in range(n):
            if not graph[i][i].leaf:
                to_process = [i]
                expanded = [[] for _ in range(n)]
                visited = [False] * n

                while to_process:
                    curr = to_process.pop()
                    visited[curr] = True
                    expanded[curr].append(curr)
                    possible_leaf = True

                    for j in range(n):
                        if j != curr and graph[curr][j].edge:
                            possible_leaf = False
                            if not visited[j]:
                                to_process.append(j)
                            expanded[j] = expanded[curr]
                            for k in expanded[j]:
                                graph[k][j].path = True

                    if possible_leaf:
                        graph[curr][curr].leaf = True

    def BuildDTGs(self):
        predicates = self._problem.get_predicates()
        for pred in predicates:
            # Create a 2x2 matrix: [False, True] x [False, True]
            empty = DTGMatrixElement()
            mat = [[DTGMatrixElement() for _ in range(2)] for _ in range(2)]
            self._DTGs[pred] = mat

        for act in self._problem.get_actions():
            self.process_STRIPS_Operator(act)

        for pred in self._DTGs:
            self.detect_Paths(self._DTGs[pred])

    def unreachable(self, to, from_):
        for fact in to:
            if from_.contains(fact[0]) and fact[1] != from_.get(fact[0]) and not self.isPath(fact[0],
                                                                                             from_.get(fact[0]),
                                                                                             fact[1]):
                return True
        return False

    def leavesOF(self, variable, value):
        leaves = []
        if self.isLeaf(variable, value):
            leaves.append(value)
        else:
            for i in range(self._problem.get_variables()[variable].get_range()):
                if self.isPath(variable, value, i) and self.isLeaf(variable, i):
                    leaves.append(i)
        return leaves

    def outputDTGInfo(self):
        for i in range(self.getNumberOfDTGs()):
            print(f"Variable: {self._problem.get_variables()[i].get_name()}")
            for j in range(self._problem.get_variables()[i].get_range()):
                if self.isLeaf(i, j):
                    print(f"{self._problem.get_variables()[i].get_value(j)} is a leaf node")
                else:
                    for k in range(self._problem.get_variables()[i].get_range()):
                        if j != k and self.isPath(i, j, k):
                            print(
                                f"{self._problem.get_variables()[i].get_value(j)} --> {self._problem.get_variables()[i].get_value(k)}")

    # You need to implement or adapt these methods
    def getNumberOfDTGs(self):
        # This method should return the number of DTGs
        pass

    def isLeaf(self, variable, value):
        # Check if the specified variable and value are leaf nodes
        pass

    def isPath(self, variable, from_value, to_value):
        # Check if there is a path from from_value to to_value for the given variable
        pass
