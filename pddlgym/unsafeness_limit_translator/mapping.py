import sys

from pddlgym.downward_translate.sas_tasks import SASTask
from pddlgym.downward_translate.pddl.tasks import Task

announced_ignored = list()


class PDDLPredicate:

    def __init__(self, list: list):
        self.list = list

    def to_SAS_string(self) -> str:
        if self.list:
            if self.is_negative():
                return "NegatedAtom " + self.list[1][0] + "(" + ", ".join(self.list[1][1:]) + ")"
            else:
                return "Atom " + self.list[0] + "(" + ", ".join(self.list[1:]) + ")"
        else:
            return ""

    def get_name(self) -> str:
        if self.is_negative():
            return self.list[1][0]
        else:
            return self.list[0]

    def is_negative(self) -> bool:
        if self.list and self.list[0] == "not":
            return True
        else:
            return False

    def is_positive(self) -> bool:
        return not self.is_negative()

    def negate(self):
        if self.is_negative():
            return PDDLPredicate(self.list[1])
        else:
            return PDDLPredicate(["not", self.list])

    """
    Do not store result of this function. SAS object may differ its arrays so index may be changed.
    """

    def find_sas_variable(self, sas_object: SASTask, pddl_task: Task):
        if self.get_name() in [x.name for x in pddl_task.predicates]:
            for i in range(0, len(sas_object.variables.value_names)):
                for j in range(0, len(sas_object.variables.value_names[i])):
                    # This will work only when 'Atom' and 'NegatedAtom' are always under the same variable.
                    if self.to_SAS_string() == sas_object.variables.value_names[i][j] \
                            or self.negate().to_SAS_string() == sas_object.variables.value_names[i][j]:
                        return (i, j)
            if self.get_name() not in announced_ignored:
                announced_ignored.append(self.get_name())
                print(
                    "Predicate %s was optimized out by translator. Therefore it will be ignored in safe states declarations." % self.get_name())
        else:
            print(
                "No matching variable found for %s. Check for typing errors in safe-states file." % self.to_SAS_string(),
                file=sys.stderr)
            exit(1)
