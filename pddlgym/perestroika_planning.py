import pddlgym
from pddlgym_planners.ff import FF  # FastForward
from pddlgym_planners.fd import FD  # FastDownward

# Planning with FastDownward (--alias seq-opt-lmcut)
fd_planner = FD()
env = pddlgym.make("PDDLEnvAuv-v0")
state, _ = env.reset()
print("Plan:", fd_planner(env.domain, state))
print("Statistics:", fd_planner.get_statistics())

# Planning with FastDownward (--alias lama-first)
lama_first_planner = FD(alias_flag="--alias lama-first")
env = pddlgym.make("PDDLEnvBlocks-v0")
state, _ = env.reset()
print("Plan:", lama_first_planner(env.domain, state))
print("Statistics:", lama_first_planner.get_statistics())