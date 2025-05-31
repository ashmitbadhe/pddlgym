## PDDLGYM Setup
To setup PDDLGYM please refer to the original README.md provided by Tom Silver and Rohan Chitnis. To use classical planners such as Fast-Downward (which is required for the agents to function) please see this repository to install FD files: https://github.com/ronuchit/pddlgym_planners/blob/d552c8a75a50a47f5ad46b1b55194254995331b2/README.md.

## Locations of Relevant Code
- Implementations of planning agents can be accessed in the [agents folder](pddlgym/agents). 
- For usage example of a planning agent to solve non-deterministic tasks in domains such as AUV and Perestroika, see [demo](pddlgym/demo_agent_planning.py). 
- Implementation of "nature" to simulate non-deterministic events can be found [here](pddlgym/nature.py).
## Making the environment for AUV:
  env = pddlgym.make("PDDLEnvAuv-v0")

## Making the environment for Perestroika:
  env = pddlgym.make("PDDLEnvPerestroika-v0")

## Running the demo file
Please make sure to run the demo file with the following arguments: "domain_filepath", "problem_filepath", "safe_states_filepath"

Example arguments for AUV domain Problem 1:
"pddlgym/pddl/auv.pddl" "pddlgym/pddl/auv/problem1.pddl" "--safe_states_file" "pddlgym/pddl/auv/safe1.txt"


domain_filepath and problem_filepath is required for all agents (APP, LIMIT, MCTS, and FOND), while the safe_states_filepath is only required for LIMIT agent.
