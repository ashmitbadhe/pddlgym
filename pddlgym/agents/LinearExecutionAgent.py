import time
from pddlgym import make
import re
from pddlgym.pddlgym_planners.fd import FD
from pddlgym.structs import Anti
from pddlgym.safe_states_finder.strips_problem_wrapper import SimpleSTRIPSProblem
from pddlgym.safe_states_finder.DTG import DTG

class LinearExecutionAgent:
    def __init__(self, env, domain_file, problem_file):
        self.env = env
        self.domain_file = domain_file
        self.domain = env.domain
        self.problem_file = problem_file
        self.planner = FD(alias_flag="--alias seq-opt-lmcut")
        self.plan = []
        self.plan_with_waitfor = []
        self.current_state = None
        #self.dtg = dtg  # Pass in DTG instance

        self.problem = SimpleSTRIPSProblem(env)

        # Create the DTG
        # self.dtg = DTG(self.problem, env.observation_space._all_ground_literals)
        # self.dtg.BuildDTGs()
        #self.dtg.outputDTGInfo()

    def generate_initial_plan(self, obs):
        # Generate initial plan using the planner
        self.plan = self.planner(self.domain, obs)
        print(len(self.plan))
        self.compute_waitfor_conditions(obs)

    def compute_waitfor_conditions(self, initial_state):
        self.env.action_space._update_objects_from_state(initial_state)
        self.plan_with_waitfor = []

        # Initialize goal literals G_{n+1}
        goal_literals = set(initial_state.goal.literals)
        G_next = goal_literals

        for index in reversed(range(len(self.plan))):
            action = self.plan[index]
            pos_preconds = self.env.action_space._ground_action_to_pos_preconds[action]
            add_effects = set(
                e for e in self.env.action_space._ground_action_to_effects[action] if "Anti" not in str(e))
            #del_effects = set(Anti(e) for e in self.env.action_space._ground_action_to_effects[action] if "Anti" in str(e))

            # Step 2: Regress G_{i+1} through a_i to get G_i
            G_i = (G_next - add_effects) | pos_preconds

            # Step 1: Compute W_i
            waitfor = set()

            for g in G_i:
                for event in self.env.action_space.event_literals:
                    e_pos_preconds = self.env.action_space._ground_action_to_pos_preconds[event]
                    # e_add_effects = set(
                    #     e for e in self.env.action_space._ground_action_to_effects[event] if "Anti" not in str(e))
                    e_del_effects = set(
                        Anti(e) for e in self.env.action_space._ground_action_to_effects[event] if "Anti" in str(e))

                    # Event can delete a goal literal
                    if g in e_del_effects:
                        if e_pos_preconds & add_effects:
                            # Add its preconditions to waitfor
                            waitfor.update({Anti(p) for p in e_pos_preconds if p not in pos_preconds and p.predicate not in self.problem.static_predicates})
            self.plan_with_waitfor.insert(0, (frozenset(waitfor), action))
            G_next = G_i  # prepare for next step in regression
            #print(self.plan_with_waitfor[0])


    def is_applicable(self, state, action):
        self.env.action_space._update_objects_from_state(state)
        pos_preconds = self.env.action_space._ground_action_to_pos_preconds[action]
        if not pos_preconds.issubset(state.literals):
            return False
        neg_preconds = self.env.action_space._ground_action_to_neg_preconds[action]
        if len(neg_preconds & state.literals) > 0:
            return False
        return True

    def get_applicable(self, state, actions):
        applicable = set()
        for action in actions:
            self.env.action_space._update_objects_from_state(state)
            pos_preconds = self.env.action_space._ground_action_to_pos_preconds[action]
            if not pos_preconds.issubset(state.literals):
                continue
            neg_preconds = self.env.action_space._ground_action_to_neg_preconds[action]
            if len(neg_preconds & state.literals) > 0:
                continue
            applicable.add(action)
        return applicable

    def apply(self, state, action):
        if action is None:
            return state
        self.env.action_space._update_objects_from_state(state)
        state_literals = set(state.literals)
        all_effects = self.env.action_space._ground_action_to_effects[action]
        for effect in all_effects:
            if "Anti" in str(effect):
                state_literals.discard(effect.literal)  # Apply delete effect
            else:
                state_literals.add(effect)  # Apply add effect
        return state.with_literals(frozenset(state_literals))

    def is_waitfor_alive(self, waitfor, current_state):
        # Check if the wait-for conditions are alive in the DTG
        for lit in waitfor:
            if "Anti" in str(lit):
                if Anti(lit) in current_state.literals:
                    return False
            else:
                if lit not in current_state.literals:
                    return False
        return True

    def __call__(self, state):
        self.current_state = state

        if len(self.plan) == 0:
            self.generate_initial_plan(state)

        # Process the plan with wait-for conditions
        while self.plan_with_waitfor:
            waitfor, action = self.plan_with_waitfor[0]
            print(action)

            # First, check if action is applicable
            if not self.is_applicable(self.current_state, action):
                print("Action no longer applicable — replanning.")
                return None

            # Then, check if wait-for conditions are ALIVE (safe to proceed)
            if self.is_waitfor_alive(waitfor, self.current_state):
                print(f"Executing: {action}")
                self.plan_with_waitfor.pop(0)
                return action
            else:
                print(f"Waiting: Wait-for conditions for {action} are not alive.")
                return None

        # If no actions left
        print("Plan exhausted.")
        return None

