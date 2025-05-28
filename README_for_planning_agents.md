Implementations of planning agents can be accessed in the [agents folder](pddlgym/agents). 
For usage example of a planning agent to solve non-deterministic tasks in domains such as AUV and Perestroika, see [demo](pddlgym/demo_agent_planning.py). 

Making the environment for AUV:
  env = pddlgym.make("PDDLEnvAuv-v0")

Making the environment for Perestroika:
  env = pddlgym.make("PDDLEnvPerestroika-v0")

Please make sure to run the demo file with the following arguments: "domain_filepath", "problem_filepath", "safe_states_filepath"

Example arguments for AUV domain Problem 1:
"pddlgym/pddl/auv.pddl" "pddlgym/pddl/auv/problem1.pddl" "--safe_states_file" "pddlgym/pddl/auv/safe1.txt"


domain_filepath and problem_filepath is required for all agents (APP, LIMIT, MCTS, and FOND), while the safe_states_filepath is only required for LIMIT agent.



Implementation of "nature" to simulate non-deterministic events can be found [here](pddlgym/nature.py).
