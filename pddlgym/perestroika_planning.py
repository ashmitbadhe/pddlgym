import pddlgym
from pddlgym.utils import run_demo
from agents.app_agent import APPAgent
from agents.limit_agent import LIMITAgent



def demo_random_perestroika():
    # Create the Sokoban environment
    env = pddlgym.make("PDDLEnvAuv-v0")

    # Fix the problem index (optional for reproducibility)
    env.fix_problem_index(0)
    domain_filepath ="pddlgym/pddl/auv.pddl"
    problem_filepath = "pddlgym/pddl/auv/problem1.pddl"
    safe_states_filepath = "pddlgym/pddl/auv/safe1.txt"
    policy = LIMITAgent(env, domain_filepath, problem_filepath, safe_states_filepath)

    # Specify video output path
    video_path = "perestroika_limit_agent.mp4"

    # Run the demo for exactly 5 steps with rendering
    run_demo(env, policy, nature_type="IndependentEvents", max_num_steps=50, render=True, video_path=video_path, fps=10, verbose=True)

    print(f"Video saved to {video_path}")


if __name__ == "__main__":
    demo_random_perestroika()