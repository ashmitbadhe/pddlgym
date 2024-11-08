import matplotlib.pyplot as plt
import time
from pddlgym.utils import run_demo
import pddlgym


def demo_random(env_name, render=True, problem_index=0, verbose=True):
    # Create the environment
    env = pddlgym.make("PDDLEnv{}-v0".format(env_name.capitalize()))
    env.fix_problem_index(problem_index)

    # Define random policy for the agent
    policy = lambda s: env.action_space.sample(s)

    # Set up the video path (this will save the video but isn't necessary for visualization)
    video_path = "/tmp/{}_random_demo.mp4".format(env_name)

    # Initialize the plot
    fig, ax = plt.subplots()
    plt.ion()  # Enable interactive mode
    ax.set_xticks([])
    ax.set_yticks([])

    # Run the simulation with real-time rendering
    obs, debug_info = env.reset()  # Correct the unpacking to match the return value

    while True:
        # Get the action using the policy
        action = policy(obs)

        # Perform the action in the environment
        obs, reward, done, debug_info = env.step(action)[:4]

        # Print what's happening (state, action, reward)
        print(f"Step: Action taken: {action}")

        # Check if event has been triggered
        if "event_triggered" in [lit.predicate.name for lit in obs.literals]:
            print("Event has been triggered!")

        # Render the current state
        img = env.render()

        # Clear the previous plot and display the new image
        ax.clear()
        ax.imshow(img)
        plt.draw()

        # Pause to allow visualization of the frame
        plt.pause(0.01)  # Adjust time for frame update speed



        time.sleep(0.1)  # Add a small delay between steps for visualization clarity

        if done:
            print("Episode done!")
            break

    # Disable interactive mode and show the final frame
    plt.ioff()
    plt.show()


# Run the demo for Sokoban
demo_random("sokoban", render=True, verbose=True)
