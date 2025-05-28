Implementations of planning agents can be accessed in the [agents folder](pddlgym/agents). 
For usage example of a planning agent to solve non-deterministic tasks in domains such as AUV and Perestroika, see [demo](pddlgym/demo_agent_planning.py). 

Making the environment for AUV:
  env = pddlgym.make("PDDLEnvAuv-v0")

Making the environment for Perestroika:
  env = pddlgym.make("PDDLEnvPerestroika-v0")

Please make sure to run the demo file with the following arguments: domain_filepath, problem_filepath, safe_states_filepath, unsafeness_limit



Implementation of "nature" to simulate non-deterministic events can be found [here](pddlgym/nature.py).
