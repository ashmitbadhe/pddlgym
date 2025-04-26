from pddlgym.pddlgym_planners.fd import FD
import copy
from copy import deepcopy
from pddlgym.structs import Anti, Literal, Predicate, TypedEntity, Type
import subprocess
import os
import re

class LIMITAgent:
    def __init__(self, env, domain_filepath, problem_filepath, safe_states_filepath=None, unsafeness_start=0, unsafeness_limit=15):
        self.env = env
        self.domain = self.env.domain
        self.domain_filepath = domain_filepath
        self.problem_filepath = problem_filepath
        self.objects = self.get_objects_from_problem()
        self.safe_states_filepath = safe_states_filepath
        self.plan_file = "pddlgym/unsafeness_limit_finder/plan.txt"
        self.space = self.env.action_space
        self.planner = FD()
        self.plan = None
        self.safe_sequence = []  # Safe sequence for actions
        self.noops_performed = 0  # Counter for no-ops

        self.unsafeness_start = unsafeness_start
        self.unsafeness_limit = unsafeness_limit
        self.plan_found = False

    def __call__(self, state):
        if self.plan is None:
            state, _ = self.env.reset()
            limit = self.unsafeness_start - 1

            while not self.plan_found and limit <= self.unsafeness_limit-1:
                limit += 1
                print(f"Trying to generate a plan with unsafeness limit {limit}...")

                sas_filepath = self.generate_limited_domain(self.domain, limit)
                # Run FastDownward to generate the plan
                self.plan = self.run_fastdownward(sas_filepath)

                if self.plan:
                    self.plan_found = True
                    self.current_plan_index = 0
                    print(f"Generated plan with limit {limit}: {self.plan}")
                    self.plan = self.retranslate_plan()
                else:
                    print(f"Planning failed at limit {limit}")

        # If there is a plan, check for the safe sequence
        if self.plan:
            # Attempt to find safe sequence if it is not empty
            if self.safe_sequence and \
                    self.is_action_applicable(self.safe_sequence[0], state) and \
                    self.is_state_safe(self.simulate_action(state, self.safe_sequence[0]))[0]:

                selected_action = self.safe_sequence.pop(0)
                self.current_plan_index += 1
                print(f"Selected action from safe sequence: {selected_action}")
            else:
                # Find a new safe sequence from the current state
                self.find_safe_sequence(state)
                if not self.safe_sequence:
                    selected_action = None # no-op
                    self.noops_performed += 1
                else:
                    selected_action = self.safe_sequence.pop(0)
                    self.current_plan_index +=1
                    print(f"New safe sequence of length {len(self.safe_sequence)}", self.safe_sequence)
        #
            return selected_action
        else:
            raise Exception("Plan is empty. No more actions to take.")

    def generate_limited_domain(self, domain_obj, limit):
        command = [
            "python",
            "pddlgym/unsafeness_limit_finder/translator.py",
            "--add-events-as-operators",
            self.domain_filepath,
            self.problem_filepath,
            self.safe_states_filepath,
            str(limit)
        ]

        log_filepath = os.path.join("pddlgym/unsafeness_limit_finder/", "translation.log")
        # Run the translation and log output
        with open(log_filepath, "a") as log_file:
            result = subprocess.run(command, stdout=log_file, stderr=log_file)

        if result.returncode != 0:
            raise Exception("Error generating SAS file. Check logs.")

        return "pddlgym/unsafeness_limit_finder/output.sas"

    def find_safe_sequence(self, current_state):
        """
        Updated to follow Proposition 3. Tracks p_plus, p_minus, Ei for each step.
        Builds a robust safe sequence starting from the current state.
        """
        state = current_state
        self.safe_sequence.clear()

        p_plus = set()  # Initially empty per Proposition 3
        p_minus = set()

        for i in range(self.current_plan_index, len(self.plan)):
            action = self.to_Literal(self.plan[i])
            print(f"\n[STEP {i}] Considering action: {action}")

            if not self.is_action_applicable(action, state):
                print(f"  ❌ Action not applicable at this step.")
                break

            # Get positive preconditions
            pos_preconds = self.space._ground_action_to_pos_preconds[action]

            # Check robustness: preconditions must not intersect with p_minus
            if pos_preconds & p_minus:
                print(f"  ❌ Action preconditions {pos_preconds} intersect with p_minus {p_minus}")
                break  # not robust

            # Simulate the action
            next_state = self.simulate_action(state, action)

            # Check if next state is goal-violating
            safe, unsafe_literal = self.is_state_safe(next_state)
            if not safe:
                print(f"  ⚠️ Unsafe due to anti-goal literal {unsafe_literal}")
                break

            # Append the action to safe sequence
            self.safe_sequence.append(action)
            print(f"  ✅ Action added to safe sequence.")

            # Compute next Ei, p_plus, p_minus
            applicable_events = self.applicable_events(self.space.event_literals, next_state)

            # Update p_plus and p_minus per Proposition 3
            action_effects = self.space._ground_action_to_effects[action]
            for eff in action_effects:
                if eff.is_negative:
                    p_plus.discard(eff.atom)
                else:
                    p_minus.discard(eff)

            for e in applicable_events:
                for eff in self.space._ground_action_to_effects[e]:
                    if eff.is_negative:
                        p_minus.add(eff.atom)
                    else:
                        p_plus.add(eff)

            # Move to the next state
            state = next_state

    def to_Literal(self, action_str):
        action_str_stripped = action_str[1:-1]
        vars = list(action_str_stripped.split(" ")[1:])
        for i in range(len(vars)):
            if vars[i] in self.objects:
                vars[i] = self.objects[vars[i]]
        pred = Predicate(action_str_stripped.split(" ")[0], len(vars))
        action_literal = Literal(pred, vars)
        return action_literal

    def is_action_applicable(self, action, state):
        self.space._update_objects_from_state(state)
        pos_preconds = self.space._ground_action_to_pos_preconds[action]
        if not pos_preconds.issubset(state.literals):
            return False
        neg_preconds = self.space._ground_action_to_neg_preconds[action]
        if len(neg_preconds & state.literals) > 0:
            return False
        return True

    def is_state_safe(self, state):
        all_event_literals = self.space.event_literals
        applicable_events = self.applicable_events(all_event_literals, state)
        for event in applicable_events:
            effects = self.space._ground_action_to_effects[event]
            for effect in effects:
                if Anti(effect) in state.goal.literals:
                    return False, effect
        return True,None

    def simulate_action(self, state, action):
        next_deterministic_state = self.env.simulate_events(action, state, False)
        return next_deterministic_state

    def applicable_events(self, all_event_literals, state):
        self.space._update_objects_from_state(state)
        valid_literals = set()
        for event_literal in all_event_literals:
            pos_preconds = self.space._ground_action_to_pos_preconds[event_literal]
            if not pos_preconds.issubset(state.literals):
                continue
            neg_preconds = self.space._ground_action_to_neg_preconds[event_literal]
            if len(neg_preconds & state.literals) > 0:
                continue
            valid_literals.add(event_literal)
        return list(valid_literals)

    def get_noops_count(self):
        return self.noops_performed

    def run_fastdownward(self, sas_filepath):
        # Run FastDownward on the generated SAS file
        command = [
            "pddlgym/pddlgym_planners/FD/builds/release/bin/downward.exe",
            "--search", "astar(lmcut())",
            "--internal-plan-file", self.plan_file
        ]

        log_filepath = os.path.join("pddlgym/unsafeness_limit_finder/", "fd_log.txt")
        with open(log_filepath, "a") as log_file, open(sas_filepath, "rb") as sas_file:
            result = subprocess.run(
                command,
                stdin=sas_file,  # Feed SAS input via stdin
                stdout=log_file,
                stderr=log_file
            )

        if result.returncode != 0:
            return None

        # Parse the plan from the output file
        return self.parse_plan(self.plan_file)

    def parse_plan(self, plan_filepath):
        # Read the generated plan from FastDownward
        with open(plan_filepath, "r") as plan_file:
            plan = plan_file.readlines()

        # Parse the plan if needed (you may need to adjust this based on your format)
        parsed_plan = [action.strip() for action in plan[:-1]]

        return parsed_plan

    def retranslate_plan(self):
        try:
            # Read the content of the plan file
            with open(self.plan_file, 'r') as plan_file:
                plan_content = plan_file.read()

            # Remove events and comments using regex
            plan_content = re.sub(r';.*$', '', plan_content, flags=re.MULTILINE)  # Remove comments
            plan_content = re.sub(r'\(events[^\)]*\)', '', plan_content)  # Remove events section
            plan_content = re.sub(r'event-action-[^\s]+', '', plan_content)  # Remove event actions
            plan_content = re.sub(r'-unsafe-copy-[0-9]+\s', ' ', plan_content)  # Remove unsafe-copy digits

            # Write the modified content to the original plan file
            with open(self.plan_file, 'w') as original_plan_file:
                original_plan_file.write(plan_content)

            # Parse the plan from the output file
            return self.parse_plan(self.plan_file)
        except Exception as e:
            print(f"Error during retranslating the plan: {e}")
            return None

    def get_objects_from_problem(self):
        """
        Extract all objects from the problem file.
        Assumes that the objects are listed under the `:objects` section of the PDDL problem.
        """
        with open(self.problem_filepath, 'r') as problem_file:
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


