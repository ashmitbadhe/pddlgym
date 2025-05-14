import pddlgym
from pddlgym.utils import run_demo
import sys
from agents.app_agent import APPAgent
from agents.limit_agent import LIMITAgent
from agents.fond_agent import FONDAgent
from agents.mcts_agent import MCTSAgent
from agents.LinearExecutionAgent import LinearExecutionAgent
from agents.NEXTGEN import NextGenAgent
from pddlgym.safe_states_finder.DTG import DTG
from pddlgym.safe_states_finder.strips_problem_wrapper import SimpleSTRIPSProblem




def demo_random_perestroika():


    # Create the Perestroika environment
    env = pddlgym.make("PDDLEnvAuv-v0")


    # Fix the problem index (optional for reproducibility)
    env.fix_problem_index(0)
    sim_count = 100

    noop_count = 0
    success_count = 0
    step_count = 0

    step_list = []



    for i in range(sim_count):
        print(f"[SIM NUMBER] {i}")

        state, _ = env.reset()
        env._state = state
        domain_filepath = sys.argv[1]
        problem_filepath = sys.argv[2]
        safe_states_filepath = sys.argv[3]
        unsafeness_limit = sys.argv[4]


        # try:
        #policy = APPAgent(env, domain_filepath, problem_filepath, safe_states_filepath, unsafeness_limit, verbose=False)

        policy = LinearExecutionAgent(env, domain_filepath, problem_filepath)
        # except:
        #     continue
        # Wrap the environment into a simple STRIPS problem
        #policy = MCTSAgent(env)
        #policy = LinearExecutionAgent(env, domain_filepath, problem_filepath)


        # Specify video output path
        video_path = "perestroika_limit_agent.mp4"

    #     # Run the demo for exactly 5 steps with rendering
        noops, successes, steps = run_demo(env, policy, nature_type="IndependentEvents", max_num_steps=1000, render=False, video_path=video_path, fps=3, verbose=True)
        #run_demo(env, policy, nature_type="IndependentEvents", max_num_steps=50, render=False, video_path=video_path, fps=3, verbose=True)
        #
        if successes == 0:
            step_list.append(steps)
        else:
            noop_count+=noops
            success_count+=successes
            step_count+= steps
        print(noop_count, success_count, step_count, step_list)

        avg_noops = noop_count/sim_count
        success_rate = success_count/sim_count
        avg_steps = step_count/sim_count

    with open("pddlgym/agents/statistics.txt", "a") as f:
        f.write(f"\n[APP] -------------- \n Average number of noops: {avg_noops}\n Success rate: {success_rate} \n Average Execution Steps: {avg_steps}")
    print(avg_noops, success_rate, avg_steps, step_list)


if __name__ == "__main__":
    demo_random_perestroika()