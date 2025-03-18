import pddlgym
from pddlgym.utils import run_demo

def demo_random_perestroika():
    # Create the Sokoban environment
    env = pddlgym.make("PDDLEnvAuv-v0")

    # Fix the problem index (optional for reproducibility)
    env.fix_problem_index(0)

    # Define a random policy (agent)
    policy = lambda s: env.action_space.sample(s)

    # Specify video output path
    video_path = "auv_random_agent_10_steps.mp4"

    # Run the demo for exactly 5 steps with rendering
    run_demo(env, policy, nature_type="IndependentEvents", max_num_steps=10, render=True, video_path=video_path, fps=3, verbose=True)

    print(f"Video saved to {video_path}")


if __name__ == "__main__":
    demo_random_perestroika()