import pddlgym
from pddlgym.utils import run_demo
import sys
from agents.app_agent import APPAgent
from agents.limit_agent import LIMITAgent
from agents.fond_agent import FONDAgent
from agents.mcts_agent import MCTSAgent

def demo_random_perestroika():


    # Create the Perestroika environment
    env = pddlgym.make("PDDLEnvAuv-v0")


    # Fix the problem index (optional for reproducibility)
    env.fix_problem_index(0)

    state, _ = env.reset()
    env._state = state
    domain_filepath = sys.argv[1]
    problem_filepath = sys.argv[2]
    #safe_states_filepath = sys.argv[4]

    policy = APPAgent(env, domain_filepath, problem_filepath, verbose=False)
    #policy = LIMITAgent(env, domain_filepath, problem_filepath, safe_states_filepath, verbose=False)
    #policy = MCTSAgent(env)
    #policy = FONDAgent(env, domain_filepath, problem_filepath)


    # Specify video output path
    video_path = "auv_app_agent.mp4"

    # Run the demo for exactly 15 steps with rendering
    run_demo(env, policy, nature_type="IndependentEvents", max_num_steps=150, render=False, video_path=video_path, fps=3, verbose=True)


if __name__ == "__main__":
    demo_random_perestroika()