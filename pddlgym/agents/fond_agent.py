import os
import tempfile
import shutil
import time
import subprocess
from pathlib import Path
import re
from pddlgym.structs import Anti, Literal, Predicate, TypedEntity, Type
from pddlgym.downward_translate.pddl.conditions import Atom, NegatedAtom

class FONDAgent:
    def __init__(self, env, domain_file, problem_file, safe_states_file=None, unsafety_limit=10):
        self.timestamp_id = int(time.time())
        self.data_dir = Path("pddlgym/FONDfiles/")

        self.domain_file = domain_file
        self.problem_file = problem_file
        self.safe_states_file = None
        self.unsafety_limit = unsafety_limit
        self.domain = env.domain
        self.objects = self.get_objects_from_problem()
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
        if not self.init_done:
            self.init(self.domain_file, self.problem_file)
        selected_action = self.find_action(state)
        return selected_action

    def init(self, domain_file, problem_file):
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
        # Construct the command
        command = f"python pddlgym/toFOND/toFOND2.py {domain_file} {problem_file} {self.safe_states_file} {self.unsafety_limit} {self.fond_domain} {self.fond_problem}"

        # Run the subprocess and capture the output and error
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # # Print stdout and stderr for debugging
        print("STDOUT:")
        print(result.stdout)
        #
        print("STDERR:")
        print(result.stderr)

    def find_policy(self):
        self.fond_problem = Path(self.fond_problem).as_posix()
        self.fond_domain = Path(self.fond_domain).as_posix()
        command = f"bash pddlgym/planner-for-relevant-policies/src/prp {self.fond_domain} {self.fond_problem} --dump-policy {2}"

        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # # Print stdout and stderr for debugging
        # print("STDOUT:")
        # print(result.stdout)
        #
        # print("STDERR:")
        # print(result.stderr)
        # with open(self.policy_file, 'r') as file:
        #     contents = file.read()
        #
        # print(contents)
        shutil.copy("policy.out","pddlgym/FONDfiles/policy.out")

    def translate_strategy(self):
        with open('pddlgym/FONDfiles/ground_data.txt', 'r') as file:
            # Read the content of the file and store it in a variable
            self.ground_actions = list(filter(None, re.split(r'[()]', file.read())))

        with open("output.sas", 'r') as f:
            file_content = f.read()
        variable_mapping = self.parse_variables(file_content)

        with open(self.policy_file, 'r') as f:
            lines = f.readlines()

        # Process the file in reverse order
        for i in range(len(lines) - 1, 0, -1):  # Start from the last line and move backwards
            line = lines[i].strip()

            # Check if the line contains "Execute:"
            if "Execute:" in line:
                action = line.split("Execute:")[1].strip().split(" ")[0]  # Extract action
                # Skip lines with "selector" or "goal"
                if action in self.ground_actions:
                    self.plan[action] = []

                    # Look for the line before that contains "If holds:"
                    holds_line = lines[i - 1].strip()
                    if "If holds:" in holds_line:
                        # Extract variables and values
                        variables = re.findall(r'(\w+):(\d+)', holds_line)
                        # Write each variable and its value
                        for var, value in variables:
                            if var in variable_mapping:
                                if variable_mapping[var][int(value)] != "act-turn":
                                    self.plan[action].append(variable_mapping[var][int(value)])
        print(self.plan)
        return True

    def find_action(self, current_state):
        best_action = None
        for action, conditions in self.plan.items():  # iterate through the actions and their conditions
            # Iterate over each condition in the action
            for condition in conditions:
                negated = False
                if condition[:4] == "not ":
                    negated = True
                condition = self.to_Literal(condition)
                if negated:
                    if condition in current_state.literals:
                        break
                else:
                    if condition not in current_state.literals:
                        break

            else:
                # If all conditions passed (i.e., no `break` happened), set the action as best action yet
                best_action = action

        # If no action is found (all conditions failed), increment noop counter
        self.number_of_noops += 1

        if best_action is not None:
            return self.to_Literal(best_action)
        else:
            return None  # No-op if no action is found

    def to_Literal(self, string):
        if "not " in string:
            nn_string = string[4:]
        else:
            nn_string = string

        nn_string =  f"({nn_string.replace('_', ' ')})"
        str_stripped = nn_string[1:-1]
        vars = list(str_stripped.split(" ")[1:])
        for i in range(len(vars)):
            if vars[i] in self.objects:
                vars[i] = self.objects[vars[i]]
        pred = Predicate(str_stripped.split(" ")[0], len(vars))
        action_literal = Literal(pred, vars)
        return action_literal

    def get_objects_from_problem(self):
        """
        Extract all objects from the problem file.
        Assumes that the objects are listed under the `:objects` section of the PDDL problem.
        """
        with open(self.problem_file, 'r') as problem_file:
            problem_content = problem_file.read()

        # Search for the :objects section using regex
        objects_match = re.search(r"\(:objects(.*?)\)", problem_content, re.DOTALL)

        if objects_match:
            # Extract the objects part and strip it of extra whitespace
            objects_str = objects_match.group(1).strip()

            # The objects are typically listed after the parentheses
            # Now we split by spaces and consider each object as a separate item
            objects = objects_str.split()
            types = [None]
            typed_objects = {}
            for i in range(len(objects)):
                index = len(objects)-1-i
                if objects[index] in self.domain.types:
                    types.append(objects[index])
                elif objects[index] == '-':
                    pass
                else:
                    typed_objects[objects[index]] = (TypedEntity(objects[index], Type(types[-1])))




            # Return the objects as a list of strings
            return typed_objects

        return []

    def parse_variables(self, text):
        var_mapping = {}
        lines = text.strip().splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line == "begin_variable":
                var_name = lines[i + 1].strip()  # e.g., var2
                domain_size = int(lines[i + 3].strip())  # number of atoms
                atoms = []
                for j in range(domain_size):
                    atom_line = lines[i + 4 + j].strip()
                    match = re.match(r"(Atom|NegatedAtom) (.+)\(\)", atom_line)
                    if match:
                        atom_type, atom_name = match.groups()
                        if atom_name.split("_")[0] in self.domain.predicates:
                            if atom_type == "Atom":
                                atoms.append(atom_name)
                            else:  # NegatedAtom
                                atoms.append("not "+ atom_name)
                if atoms != []:
                    var_mapping[var_name] = atoms
                i += 4 + domain_size  # move past this variable
            else:
                i += 1
        return var_mapping


    def show_statistics(self, actions_taken, total_time):
        print("Statistics:")
        print(f"Actions: {actions_taken}, Total Time: {total_time:.2f}s, Noops: {self.number_of_noops}, Preprocessing Time: {self.preprocess_time:.2f}s")
