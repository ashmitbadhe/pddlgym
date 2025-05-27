from pddlgym.agents.helper.helper_functions import Helper
import subprocess
import os
import re

class APPAgent:
    """
    Eventually Applicable Reference Plan (APP) Agent.

    This agent constructs a reference plan using Fast Downward and executes a safe sequence
    of actions from the plan that is guaranteed to be robust with respect to certain
    environmental dynamics (events). Based on the safe state tracking and planning logic,
    it simulates actions and filters them according to robustness criteria defined in Proposition 3.

    Attributes
    ----------
    env : pddlgym.environment.PDDLEnv
        The PDDLGym environment.
    domain_filepath : str
        Path to the PDDL domain file.
    problem_filepath : str
        Path to the PDDL problem file.
    helper : Helper
        Helper class instance used for simulation, parsing, and checks.
    objects : list
        Objects extracted from the problem.
    plan_file : str
        Path to the output plan file from Fast Downward.
    space : gym.Space
        Action space of the environment.
    plan : list
        The main plan (sequence of grounded actions).
    untranslated_plan : list
        The raw plan before retranslating action names.
    safe_sequence : list
        List of safe actions determined to be robust from the current state.
    verbose : bool
        If True, print debug information.
    plan_found : bool
        Whether a plan was successfully generated.
    """

    def __init__(self, env, domain_filepath, problem_filepath, verbose=False):
        """
        Initialize the APPAgent.

        Parameters
        ----------
        env : PDDLEnv
            PDDL environment.
        domain_filepath : str
            Path to the domain PDDL file.
        problem_filepath : str
            Path to the problem PDDL file.
        verbose : bool, optional
            Whether to print debug information, by default False.
        """
        self.env = env
        self.domain = self.env.domain
        self.domain_filepath = domain_filepath
        self.problem_filepath = problem_filepath
        self.helper = Helper(env, self.domain_filepath, self.problem_filepath)
        self.objects = self.helper.get_objects_from_problem()
        self.plan_file = "sas_plan"
        self.space = self.env.action_space
        self.plan = None
        self.safe_sequence = []  # Safe sequence for actions
        self.verbose = verbose
        self.untranslated_plan = None
        self.plan_found = False

    def __call__(self, state):
        """
        Decide on an action to take from the current state.

        Parameters
        ----------
        state : object
            The current environment state.

        Returns
        -------
        action : object
            The next action to execute from the safe sequence.
        """
        if self.plan is None:
            state, _ = self.env.reset()
            sas_filepath = self.generate_reversible_domain()
            self.plan = self.run_fastdownward(sas_filepath)

            if self.plan:
                self.plan_found = True
                self.plan = self.retranslate_plan()
            else:
                print(f"Planning failed")

        if self.plan:
            if self.safe_sequence and self.helper.is_action_applicable(self.safe_sequence[0], state):
                selected_action = self.safe_sequence.pop(0)
                self.untranslated_plan.pop(0)
                self.plan.pop(0)
                if self.verbose:
                    print(f"Selected action from safe sequence: {selected_action}")
            else:
                self.find_safe_sequence(state)
                if not self.safe_sequence:
                    selected_action = None  # no-op
                else:
                    selected_action = self.safe_sequence.pop(0)
                    self.plan.pop(0)
                    self.untranslated_plan.pop(0)
                    if self.verbose:
                        print(f"Selected action from safe sequence: {selected_action}")
            return selected_action
        else:
            raise Exception("Plan is empty. No more actions to take.")

    def generate_reversible_domain(self):
        """
        Runs the domain translator to generate a reversible PDDL SAS file.

        Returns
        -------
        str
            Path to the generated SAS file.
        """
        command = [
            "python",
            "pddlgym/safe_states_finder/translator.py",
            self.domain_filepath,
            self.problem_filepath,
            self.domain_filepath,
            "1"
        ]

        log_filepath = os.path.join("pddlgym/safe_states_finder/", "translation.log")
        with open(log_filepath, "w") as log_file:
            result = subprocess.run(command, stdout=log_file, stderr=log_file)

        if result.returncode != 0:
            raise Exception("Error generating SAS file. Check logs.")

        return "pddlgym/safe_states_finder/output.sas"

    def find_safe_sequence(self, current_state):
        """
        Build a robust safe action sequence starting from the current state.

        This method checks each planned action for applicability and robustness
        against interfering events using preconditions and p_plus/p_minus tracking.

        Parameters
        ----------
        current_state : object
            The current environment state.
        """
        state = current_state
        self.safe_sequence.clear()
        p_plus = set()
        p_minus = set()
        safe_index = None

        for i in range(0, len(self.plan)):
            action = self.helper.to_Literal(self.plan[i])
            if self.verbose:
                print(f"\n[STEP {i}] Considering action: {action}")

            if not self.helper.is_action_applicable(action, state):
                self.safe_sequence = self.safe_sequence[:safe_index+1] if safe_index is not None else []
                if self.verbose:
                    print(f"  ❌ Action not applicable at this step.")
                break

            pos_preconds = self.space._ground_action_to_pos_preconds[action]
            neg_preconds = self.space._ground_action_to_neg_preconds[action]

            next_state = self.helper.simulate_action(state, action)

            applicable_events = self.helper.applicable_events(
                self.space.event_literals, next_state, p_plus, p_minus)

            for event in applicable_events:
                add_effects, del_effects = self.helper.get_add_del_effects(event, next_state)
                p_plus.update(add_effects)
                p_minus.update(del_effects)

            if pos_preconds & p_minus or neg_preconds & p_plus:
                self.safe_sequence = self.safe_sequence[:safe_index+1] if safe_index is not None else []
                if self.verbose:
                    reason = "positive preconditions intersect with p_minus" if pos_preconds & p_minus else "negative preconditions intersect with p_plus"
                    print(f"  ⚠️ UNSAFE ACTION: {reason}")
                break

            self.safe_sequence.append(action)
            if self.plan[i] == self.untranslated_plan[i] or "zeroing" in str(self.untranslated_plan[i]):
                safe_index = i
            if self.verbose:
                print(f"  ✅ Action added to safe sequence.")

            state = next_state

    def run_fastdownward(self, sas_filepath):
        """
        Run Fast Downward planner on the given SAS file.

        Parameters
        ----------
        sas_filepath : str
            Path to the SAS file.

        Returns
        -------
        list or None
            The parsed plan, or None if planning failed.
        """
        command = [
            "python", "pddlgym/pddlgym_planners/FD/fast-downward.py",
            "--search", "--alias", "lama-first",
            "--sas-file", sas_filepath,
            sas_filepath
        ]

        log_filepath = os.path.join("pddlgym/safe_states_finder/", "fd_log.txt")
        with open(log_filepath, "w") as log_file, open(sas_filepath, "rb") as sas_file:
            result = subprocess.run(
                command,
                stdin=sas_file,
                stdout=log_file,
                stderr=log_file
            )

        if result.returncode != 0:
            return None

        return self.parse_plan(self.plan_file)

    def parse_plan(self, plan_filepath):
        """
        Parse the Fast Downward plan file.

        Parameters
        ----------
        plan_filepath : str
            Path to the plan file.

        Returns
        -------
        list
            Parsed plan as a list of action strings.
        """
        with open(plan_filepath, "r") as plan_file:
            plan = plan_file.readlines()

        return [action.strip() for action in plan]

    def retranslate_plan(self):
        """
        Retranslates and cleans up the Fast Downward plan file to match the expected format.

        Returns
        -------
        list or None
            The cleaned plan, or None if an error occurred.
        """
        try:
            with open(self.plan_file, 'r') as plan_file:
                plan_content = plan_file.read()

            plan_content = re.sub(r';.*$', '', plan_content, flags=re.MULTILINE)
            plan_content = re.sub(r'^.*event-action-[^\s]+.*\n?', '', plan_content, flags=re.MULTILINE)
            partially_translated = plan_content.strip()

            plan_content = re.sub(
                r'\((\S+?)(?:-inc-copy-\d+-\d+|-constrained-zeroing-copy|-constrained-inc-copy)',
                r'(\1',
                plan_content
            )
            plan_content = plan_content.strip()

            with open(self.plan_file, 'w') as original_plan_file:
                original_plan_file.write(partially_translated)

            self.untranslated_plan = self.parse_plan(self.plan_file)

            with open(self.plan_file, 'w') as original_plan_file:
                original_plan_file.write(plan_content)

            return self.parse_plan(self.plan_file)

        except Exception as e:
            print(f"Error during retranslating the plan: {e}")
            return None
