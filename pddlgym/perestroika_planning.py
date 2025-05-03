import pddlgym
from pddlgym.utils import run_demo
import sys
from agents.app_agent import APPAgent
from agents.limit_agent import LIMITAgent
from agents.fond_agent import FONDAgent



def demo_random_perestroika():
    # Create the Sokoban environment
    env = pddlgym.make("PDDLEnvPerestroika-v0")

    # Fix the problem index (optional for reproducibility)
    env.fix_problem_index(0)
    domain_filepath = sys.argv[1]
    problem_filepath = sys.argv[2]
    safe_states_filepath = sys.argv[3]
    unsafeness_limit = sys.argv[4]
    policy = APPAgent(env, domain_filepath, problem_filepath, safe_states_filepath, unsafeness_limit)

    # Specify video output path
    video_path = "perestroika_limit_agent.mp4"

    # Run the demo for exactly 5 steps with rendering
    run_demo(env, policy, nature_type="IndependentEvents", max_num_steps=200, render=True, video_path=video_path, fps=3, verbose=True)

    print(f"Video saved to {video_path}")


if __name__ == "__main__":
    demo_random_perestroika()