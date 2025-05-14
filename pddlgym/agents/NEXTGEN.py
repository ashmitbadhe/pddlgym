import subprocess
import time
from collections import defaultdict, deque
import tempfile
import os
import shutil
from pddlgym.pddlgym_planners.fd import FD  # FastDownward

class SGPAgent:
    def __init__(self, env, domain_path, problem_path):
        self.env = env
        self.domain_path = domain_path
        self.domain = env.domain
        self.problem_path = problem_path
        self.safe_states = self.compute_safe_state_envelope()
        self.event_model = EventModel()
        self.goal_predicates = set(lit.predicate for lit in env._state.goal.literals)

        self.planner = FD(alias_flag="--alias seq-opt-lmcut")

    def compute_safe_state_envelope(self):
        safe = set()
        visited = set()
        self.env.reset()
        queue = deque([self.env._state])
        while queue:
            state = queue.popleft()
            if state in visited:
                continue
            visited.add(state)
            if self.is_safe(state):
                safe.add(state)
                for action in self.env.action_space.all_ground_literals():
                    if self.env.check_applicable(state, action):
                        try:
                            next_state, _, _, _ = self.env.step(action)
                            queue.append(next_state)
                            self.env.set_state(state)  # reset for next try
                        except:
                            pass
        print(safe)
        return safe

    def is_safe(self, state):
        literals = state.literals
        return all("dead" not in str(l) for l in literals) and all("none" not in str(l) for l in literals)

    def is_high_risk(self, state):
        risk_score = 0
        for event in self.event_model.event_log:
            t = self.event_model.predict_time_to_event(event)
            risk_score += 1 / (t + 1)
        return risk_score > 0.5 or state not in self.safe_states

    def observe(self, state):
        self.event_model.observe(state)

    def find_safe_fallback(self, state):
        for safe in self.safe_states:
            if safe != state:
                return safe  # naive fallback
        return state

    def __call__(self, state):
        goal_predicates = self.goal_predicates
        self.observe(state)
        goal_state = self.find_safe_fallback(state) if self.is_high_risk(state) else goal_predicates
        return self.plan_with_constraints(state).pop(0)

    def plan_with_constraints(self, state):
        plan = self.planner(self.domain, state)
        return plan

    def extract_plan(self, output):
        lines = output.splitlines()
        plan = []
        for line in lines:
            if line.startswith("step"):
                act = line.split(":")[1].strip().lower()
                plan.append(act)
        return plan

class EventModel:
    def __init__(self):
        self.event_log = defaultdict(list)

    def observe(self, state):
        # You can improve this with actual change detection
        for lit in state.literals:
            if "level" in str(lit):
                self.event_log["shrink"].append(time.time())

    def predict_time_to_event(self, event):
        timestamps = self.event_log[event]
        if len(timestamps) < 2:
            return float('inf')
        interval = (timestamps[-1] - timestamps[0]) / (len(timestamps) - 1)
        return max(0, interval - (time.time() - timestamps[-1]))
