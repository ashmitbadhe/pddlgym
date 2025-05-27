import shutil
import time
import subprocess
from pathlib import Path
import re
from pddlgym.agents.helper.helper_functions import Helper
from pddlgym.structs import Literal, Predicate

class FONDAgent:
    """
    An agent that uses Fully Observable Non-Deterministic (FOND) planning
    to solve PDDL tasks using external tools for plan translation and policy generation.

    Attributes:
        env: The pddlgym environment.
        domain_file (str): Path to the PDDL domain file.
        problem_file (str): Path to the PDDL problem file.
    """

    def __init__(self, env, domain_file, problem_file):
        """
        Initializes the FONDAgent and sets up directories, files, and internal state.

        Args:
            env: The pddlgym environment instance.
            domain_file (str): Path to the domain PDDL file.
            problem_file (str): Path to the problem PDDL file.
        """
        self.timestamp_id = int(time.time())
        self.data_dir = Path("pddlgym/toFOND/")

        self.domain_file = domain_file
        self.problem_file = problem_file
        self.helper = Helper(env, self.domain_file, self.problem_file)
        self.domain = env.domain
        self.objects = self.helper.get_objects_from_problem()
        self.fond_domain = self.data_dir / "fond_domain.pddl"
        self.fond_problem = self.data_dir / "fond_problem.pddl"
        self.policy_file = self.data_dir / "policy.out"
        self.translated_policy_file = self.data_dir / "translated_policy.sas"
        self.log_file = self.data_dir / "log.txt"

        self.init_done = False
        self.remove_temp_files = True
        self.preprocess_time = 0
        self.number_of_noops = 0
        self.plan = {}
        self.ground_actions = None

        self.data_dir.mkdir(parents=True, exist_ok=True)

    def __call__(self, state):
        """
        Selects an action for the given state using the learned policy.

        Args:
            state: The current pddlgym state.

        Returns:
            Literal: The chosen action as a Literal object, or None for a no-op.
        """
        if not self.init_done:
            self.init(self.domain_file, self.problem_file)
        selected_action = self.find_action(state)
        if selected_action is not None and self.helper.is_action_applicable(selected_action, state):
            return selected_action
        else:
            return None

    def init(self, domain_file, problem_file):
        """
        Initializes the agent by preprocessing the domain/problem and computing the policy.

        Args:
            domain_file (str): Path to the domain PDDL file.
            problem_file (str): Path to the problem PDDL file.
        """
        print("Preprocessing started.")
        start = time.time()

        self.translate_to_fond(domain_file, problem_file)
        self.find_policy()
        self.translate_strategy()

        end = time.time()
        self.preprocess_time = end - start
        self.init_done = True
        print("Preprocessing done.")

    def translate_to_fond(self, domain_file, problem_file):
        """
        Translates the domain and problem to a FOND-compatible representation.
        Runs toFOND2.py to do the translation.

        Args:
            domain_file (str): Path to the original domain file.
            problem_file (str): Path to the original problem file.
        """
        command = f"python pddlgym/toFOND/toFOND2.py {domain_file} {problem_file} {self.domain_file} {20} {self.fond_domain} {self.fond_problem}"
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def find_policy(self):
        """
        Calls the external PRP planner to compute a FOND policy and saves the output to file.
        """
        self.fond_problem = Path(self.fond_problem).as_posix()
        self.fond_domain = Path(self.fond_domain).as_posix()
        command = f"bash pddlgym/planner-for-relevant-policies/src/prp {self.fond_domain} {self.fond_problem} --dump-policy {2} --detect-deadends {1}"
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        shutil.copy("policy.out", self.policy_file)

    def translate_strategy(self):
        """
        Reads and processes the generated FOND policy to build a condition-based action plan.

        Returns:
            bool: True when processing succeeds.
        """
        with open('pddlgym/toFOND/ground_data.txt', 'r') as file:
            self.ground_actions = list(filter(None, re.split(r'[()]', file.read())))

        with open("output.sas", 'r') as f:
            file_content = f.read()
        variable_mapping = self.parse_variables(file_content)

        with open(self.policy_file, 'r') as f:
            lines = f.readlines()

        for i in range(len(lines) - 1, 0, -1):
            line = lines[i].strip()
            if "Execute:" in line:
                action = line.split("Execute:")[1].strip().split(" ")[0]
                if action in self.ground_actions:
                    self.plan[action] = []
                    holds_line = lines[i - 1].strip()
                    if "If holds:" in holds_line:
                        variables = re.findall(r'(\w+):(\d+)', holds_line)
                        for var, value in variables:
                            if var in variable_mapping:
                                condition = variable_mapping[var][int(value)]
                                if condition != "act-turn":
                                    self.plan[action].append(condition)
        return True

    def find_action(self, current_state):
        """
        Finds the next action from the policy that is applicable in the current state.

        Args:
            current_state: The current state in pddlgym.

        Returns:
            Literal: The applicable action or None if no action is applicable (no-op).
        """
        best_action = None
        for action, conditions in self.plan.items():
            for condition in conditions:
                negated = condition.startswith("not ")
                lit = self.to_Literal(condition)
                if (not negated and lit not in current_state.literals) or \
                   (negated and lit in current_state.literals):
                    break
            else:
                best_action = action

        self.number_of_noops += 1
        return self.to_Literal(best_action) if best_action else None

    def to_Literal(self, string):
        """
        Converts a string into a pddlgym Literal object.

        Args:
            string (str): The string representation of a grounded action or predicate.

        Returns:
            Literal: The converted Literal object.
        """
        if "not " in string:
            nn_string = string[4:]
        else:
            nn_string = string

        nn_string = f"({nn_string.replace('_', ' ')})"
        str_stripped = nn_string[1:-1]
        vars = list(str_stripped.split(" ")[1:])
        for i in range(len(vars)):
            if vars[i] in self.objects:
                vars[i] = self.objects[vars[i]]
        pred = Predicate(str_stripped.split(" ")[0], len(vars))
        return Literal(pred, vars)

    def parse_variables(self, text):
        """
        Parses the SAS output to build a mapping from variable names to their atom values.

        Args:
            text (str): The contents of the SAS output file.

        Returns:
            dict: Mapping of SAS variable names to list of atoms or negated atoms.
        """
        var_mapping = {}
        lines = text.strip().splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line == "begin_variable":
                var_name = lines[i + 1].strip()
                domain_size = int(lines[i + 3].strip())
                atoms = []
                for j in range(domain_size):
                    atom_line = lines[i + 4 + j].strip()
                    match = re.match(r"(Atom|NegatedAtom) (.+)\(\)", atom_line)
                    if match:
                        atom_type, atom_name = match.groups()
                        if atom_name.split("_")[0] in self.domain.predicates:
                            atoms.append(atom_name if atom_type == "Atom" else "not " + atom_name)
                if atoms:
                    var_mapping[var_name] = atoms
                i += 4 + domain_size
            else:
                i += 1
        return var_mapping
