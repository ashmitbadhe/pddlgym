"""Utilities
"""
from collections import defaultdict
import contextlib
import sys
import itertools
import numpy as np
import os
import gym
import imageio
from pddlgym.nature import create_nature


def get_object_combinations(objects, arity, var_types=None,
                            type_to_parent_types=None, allow_duplicates=False):
    type_to_objs = defaultdict(list)

    for obj in sorted(objects):
        if type_to_parent_types is None:
            type_to_objs[obj.var_type].append(obj)
        else:
            for t in type_to_parent_types[obj.var_type]:
                type_to_objs[t].append(obj)

    if var_types is None:
        choices = [sorted(objects) for _ in range(arity)]
    else:
        assert len(var_types) == arity
        choices = [type_to_objs[vt] for vt in var_types]

    for choice in itertools.product(*choices):
        if not allow_duplicates and len(set(choice)) != len(choice):
            continue
        yield choice
        yield choice

def run_demo(env, policy, nature_type = "NoNature", max_num_steps=10, render=False,
             video_path=None, fps=3, verbose=False, seed=None,
             check_reward=False):
    images = []

    if seed is not None:
        env.seed(seed)

    obs, _ = env.reset()

    if seed is not None:
        env.action_space.seed(seed)

    #Create an instance of nature if applicable to domain
    if nature_type != "NoNature":
        nature_instance = create_nature(nature_type, obs, env)


    for t in range(max_num_steps):
        # if verbose:
        #     print("Obs:", obs)

        if render:
            images.append(env.render())

        action = policy(obs)

        if verbose:
            print(f"Act {t}:", action)

        obs, reward, done, _, _ = env.step(action)
        completion = (sum(lit in obs.literals for lit in obs.goal.literals) / len(obs.goal.literals)) * 100
        print(f"{completion:.2f}% Completed")

        if render:
            images.append(env.render())
        if verbose:
            print("Rew:", reward)

        if done:
            break

        #apply nature to environment if applicable
        if nature_type != "NoNature":
            obs, applied_events, event_literals = nature_instance.apply_nature(obs)
            # if verbose:
            #     print("Events:", applied_events)


    if verbose:
        print("Final obs:", obs)
        print()

    if render:
        images.append(env.render())
        imageio.mimwrite(video_path, images, fps=fps)
        print("Wrote out video to", video_path)

    env.close()
    if check_reward:
        assert tot_reward > 0
    if verbose:
        input("press enter to continue to next problem")


class DummyFile:
    def write(self, x):
        pass

    def flush(self):
        pass


@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = DummyFile()
    yield
    sys.stdout = save_stdout