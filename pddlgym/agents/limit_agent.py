from pddlgym.agents.helper.helper_functions import Helper
import subprocess
import os
import re

class LIMITAgent:
    """
    A planning agent that attempts to generate and execute a plan under increasing levels of unsafeness,
    as described in planning against nature settings. It uses a helper for simulation and Fast Downward
    as the underlying planner.

    Attributes:
        env: The PDDLGym environment.
        domain_filepath: Path to the domain PDDL file.
        problem_filepath: Path to the problem PDDL file.
        safe_states_filepath: Optional path to file containing known safe states.
        unsafeness_start: Starting unsafeness level to attempt planning from.
        unsafeness_limit: Maximum unsafeness level to allow.
        verbose: If True, prints debug information.
    """

    def __init__(self, env, domain_filepath, problem_filepath, safe_states_filepath=None,
                 unsafeness_start=0, unsafeness_limit=10, verbose=False):
        """
        Initializes the LIMITAgent with environment, filepaths, and configuration.

        Args:
            env: PDDLGym environment object.
            domain_filepath: Path to domain PDDL file.
            problem_filepath: Path to problem PDDL file.
            safe_states_filepath: Optional; path to safe states file.
            unsafeness_start: Starting unsafeness level.
            unsafeness_limit: Maximum unsafeness level.
            verbose: If True, enables verbose debug printing.
        """
        self.env = env
        self.domain = self.env.domain
        self.domain_filepath = domain_filepath
        self.problem_filepath = problem_filepath
        self.helper = Helper(env, self.domain_filepath, self.problem_filepath)
        self.objects = self.helper.get_objects_from_problem()
        self.safe_states_filepath = safe_states_filepath
        self.plan_file = "sas_plan"
        self.space = self.env.action_space
        self.plan = None
        self.safe_sequence = []

        self.unsafeness_start = unsafeness_start
        self.unsafeness_limit = unsafeness_limit
        self.plan_found = False
        self.useful_event = None
        self.verbose = verbose

    def __call__(self, state):
        """
        Returns the next safe and applicable action to take from the current state.

        Args:
            state: The current environment state.

        Returns:
            A safe and applicable action or None (no-op).

        Raises:
            Exception: If no plan is available.
        """
        if self.plan is None:
            state, _ = self.env.reset()
            limit = self.unsafeness_start - 1

            while not self.plan_found and limit <= self.unsafeness_limit - 1:
                limit += 1
                print(f"Trying to generate a plan with unsafeness limit {limit}...")

                sas_filepath = self.generate_limited_domain(limit)
                self.plan = self.run_fastdownward(sas_filepath)

                if self.plan:
                    self.plan_found = True
                    print(f"Generated plan with limit {limit}: {self.plan}")
                    self.plan = self.retranslate_plan()
                else:
                    print(f"Planning failed at limit {limit}")

        if self.plan:
            if self.safe_sequence and self.helper.is_action_applicable(self.safe_sequence[0], state):
                selected_action = self.safe_sequence.pop(0)
                self.plan.pop(0)
                if self.verbose:
                    print(f"Selected action from safe sequence: {selected_action}")
            else:
                self.find_safe_sequence(state)
                selected_action = self.safe_sequence.pop(0) if self.safe_sequence else None
                if selected_action and self.plan:
                    self.plan.pop(0)
                if self.verbose:
                    print(f"Selected action from safe sequence: {selected_action}")
            return selected_action
        else:
            raise Exception("Plan is empty. No more actions to take.")

    def generate_limited_domain(self, limit):
        """
        Translates the original domain and problem into a modified SAS file
        with the given unsafeness limit.

        Args:
            limit: Unsafeness threshold.

        Returns:
            Path to the generated SAS file.

        Raises:
            Exception: If translation fails.
        """
        command = [
            "python",
            "pddlgym/unsafeness_limit_translator/translator.py",
            "--add-events-as-operators",
            self.domain_filepath,
            self.problem_filepath,
            self.safe_states_filepath,
            str(limit)
        ]

        log_filepath = os.path.join("pddlgym/unsafeness_limit_translator/", "translation.log")
        with open(log_filepath, "w") as log_file:
            result = subprocess.run(command, stdout=log_file, stderr=log_file)

        if result.returncode != 0:
            raise Exception("Error generating SAS file. Check logs.")

        return "pddlgym/unsafeness_limit_translator/output.sas"

    def find_safe_sequence(self, current_state):
        """
        Finds a robust safe sequence of actions starting from current state by simulating
        actions and filtering out those violating robustness criteria.

        Args:
            current_state: The state to start the sequence from.
        """
        state = current_state
        self.safe_sequence.clear()
        p_plus = set()
        p_minus = set()
        safe_index = None

        for i in range(len(self.plan)):
            action = self.helper.to_Literal(self.plan[i])
            if self.verbose:
                print(f"\n[STEP {i}] Considering action: {action}")

            if not self.helper.is_action_applicable(action, state):
                self.safe_sequence = self.safe_sequence[:safe_index + 1] if safe_index is not None else []
                if self.verbose:
                    print(f"  ❌ Action not applicable at this step.")
                break

            pos_preconds = self.space._ground_action_to_pos_preconds[action]
            neg_preconds = self.space._ground_action_to_neg_preconds[action]
            next_state = self.helper.simulate_action(state, action)
            applicable_events = self.helper.applicable_events(self.space.event_literals, next_state, p_plus, p_minus)

            for event in applicable_events:
                add_effects, del_effects = self.helper.get_add_del_effects(event, next_state)
                p_plus.update(add_effects)
                p_minus.update(del_effects)

            if pos_preconds & p_minus or neg_preconds & p_plus:
                self.safe_sequence = self.safe_sequence[:safe_index + 1] if safe_index is not None else []
                if self.verbose:
                    print(f"  ⚠️ UNSAFE ACTION at step {i}")
                break

            self.safe_sequence.append(action)
            if self.plan[i] == self.untranslated_plan[i]:
                safe_index = i
            if self.verbose:
                print(f"  ✅ Action added to safe sequence.")

            state = next_state

    def run_fastdownward(self, sas_filepath):
        """
        Executes the FastDownward planner on the given SAS file.

        Args:
            sas_filepath: Path to the SAS file.

        Returns:
            A list of actions representing the plan, or None if planning failed.
        """
        command = [
            "python", "pddlgym/pddlgym_planners/FD/fast-downward.py",
            "--search", "--alias", "lama-first",
            "--sas-file", sas_filepath,
            sas_filepath
        ]

        log_filepath = os.path.join("pddlgym/unsafeness_limit_translator/", "fd_log.txt")
        with open(log_filepath, "w") as log_file, open(sas_filepath, "rb") as sas_file:
            result = subprocess.run(command, stdin=sas_file, stdout=log_file, stderr=log_file)

        return self.parse_plan(self.plan_file) if result.returncode == 0 else None

    def parse_plan(self, plan_filepath):
        """
        Parses the generated plan file into a list of actions.

        Args:
            plan_filepath: Path to the plan file.

        Returns:
            A list of plan actions as strings.
        """
        with open(plan_filepath, "r") as plan_file:
            plan = plan_file.readlines()
        return [action.strip() for action in plan]

    def retranslate_plan(self):
        """
        Cleans and retranslates the raw FastDownward plan by removing suffixes
        and event artifacts, preparing it for robust planning.

        Returns:
            A cleaned list of plan actions.
        """
        try:
            with open(self.plan_file, 'r') as plan_file:
                plan_content = plan_file.read()

            plan_content = re.sub(r';.*$', '', plan_content, flags=re.MULTILINE)
            plan_content = re.sub(r'^.*event-action-[^\s]+.*\n?', '', plan_content, flags=re.MULTILINE)

            partially_translated = plan_content.strip()

            plan_content = re.sub(
                r'\((\S+?)(?:-inc-copy-\d+-\d+|-constrained-zeroing-copy|-constrained-inc-copy|-unsafe-copy-\d)',
                r'(\1',
                plan_content
            ).strip()

            with open(self.plan_file, 'w') as f:
                f.write(partially_translated)

            self.untranslated_plan = self.parse_plan(self.plan_file)

            with open(self.plan_file, 'w') as f:
                f.write(plan_content)

            return self.parse_plan(self.plan_file)
        except Exception as e:
            print(f"Error during retranslating the plan: {e}")
            return None
