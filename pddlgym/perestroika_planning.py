import pddlgym
from pddlgym.utils import run_demo
from agents.app_agent import APPAgent



def demo_random_perestroika():
    # Create the Sokoban environment
    env = pddlgym.make("PDDLEnvPerestroika-v0")

    # Fix the problem index (optional for reproducibility)
    env.fix_problem_index(0)
    policy = APPAgent(env)

    # Specify video output path
    video_path = "perestroika_app_agent.mp4"

    # Run the demo for exactly 5 steps with rendering
    run_demo(env, policy, nature_type="IndependentEvents", max_num_steps=50, render=True, video_path=video_path, fps=3, verbose=True)

    print(f"Video saved to {video_path}")


if __name__ == "__main__":
    demo_random_perestroika()