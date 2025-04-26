import os
import shutil
import time
import subprocess
from pathlib import Path

class FONDAgent:
    def __init__(self, env, domain_file, problem_file, safe_states_file=None, unsafety_limit=10):
        self.timestamp_id = int(time.time())
        self.data_dir = Path("pddlgym/FONDfiles/")

        self.domain_file = domain_file
        self.problem_file = problem_file
        self.safe_states_file = ""
        self.unsafety_limit = unsafety_limit
        self.fond_domain = self.data_dir / "fond_domain.pddl"
        self.fond_problem = self.data_dir / "fond_problem.pddl"
        self.policy_file = self.data_dir / "policy.sas"
        self.translated_policy_file = self.data_dir / "translated_policy.sas"
        self.log_file = self.data_dir / "log.txt"

        self.init_done = False
        self.remove_temp_files = True
        self.preprocess_time = 0
        self.number_of_noops = 0

        self.data_dir.mkdir(parents=True, exist_ok=True)

    def __call__(self, state):
        if not self.init_done:
            self.init(self.domain_file, self.problem_file)
        selected_action = self.find_action(state)
        print(selected_action)
        return selected_action

    def init(self, domain_file, problem_file):
        print("Preprocessing started.")
        start = time.time()

        self.translate_to_fond(domain_file, problem_file)
        self.find_policy()
        self.load_fond_problem()
        self.translate_strategy()

        end = time.time()
        self.preprocess_time = end - start
        self.init_done = True
        print("Preprocessing done.")

    def translate_to_fond(self, domain_file, problem_file):
        # Construct the command
        command = f"python pddlgym/toFOND/toFOND2.py {domain_file} {problem_file} {self.safe_states_file} {self.unsafety_limit} {self.fond_domain}  {self.fond_problem}"

        # Run the subprocess and capture the output and error
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print stdout and stderr for debugging
        print("STDOUT:")
        print(result.stdout)

        print("STDERR:")
        print(result.stderr)

    def find_policy(self):
        command = f"python pddlgym/pddlgym_planners/FD/fast-downward.py {self.fond_domain} {self.fond_problem} --dump-policy >> {self.log_file} 2>&1"
        subprocess.run(command, shell=True)
        with open(self.policy_file, 'r') as file:
            contents = file.read()

        print(contents)
        shutil.copy("pddlgym/toFOND/policy.out", self.policy_file)

    def load_fond_problem(self):
        # Dummy: in reality, you'd load the problem's variables and actions from SAS
        self.fond_problem_vars = {}
        return True

    def translate_strategy(self):
        # Dummy: in reality, you'd replace variable IDs in the policy file with human-readable actions
        shutil.copy(self.policy_file, self.translated_policy_file)
        return True

    def find_action(self, current_state):
        with open(self.translated_policy_file, 'r') as f:
            lines = f.readlines()

        # Dummy matching: In reality, you'd check current state against conditions
        for line in lines:
            if "Execute:" in line:
                continue
            if self.is_action_applicable(current_state, line):
                action = self.extract_action_from_line(line)
                print(f"Action chosen: {action}")
                return action

        self.number_of_noops += 1
        return "(<noop-action>)"

    def is_action_applicable(self, current_state, line):
        # Dummy check: Match state features with policy line
        return True

    def extract_action_from_line(self, line):
        # Extract action name
        action_name = line.strip().split()[1]
        return f"({action_name.replace('_', ' ')})"

    def show_statistics(self, actions_taken, total_time):
        print("Statistics:")
        print(f"Actions: {actions_taken}, Total Time: {total_time:.2f}s, Noops: {self.number_of_noops}, Preprocessing Time: {self.preprocess_time:.2f}s")
