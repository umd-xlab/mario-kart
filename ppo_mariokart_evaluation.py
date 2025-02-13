"""
Evaluate an agent using Proximal Policy Optimization from Stable Baselines 3
"""

import argparse
import csv
import gymnasium as gym
import numpy as np
from gymnasium.wrappers.time_limit import TimeLimit
from stable_baselines3 import PPO
from stable_baselines3.common.atari_wrappers import ClipRewardEnv, WarpFrame
from stable_baselines3.common.vec_env import (
    SubprocVecEnv,
    VecFrameStack,
    VecTransposeImage,
)

import retro


class StochasticFrameSkip(gym.Wrapper):
    def __init__(self, env, n, stickprob):
        gym.Wrapper.__init__(self, env)
        self.n = n
        self.stickprob = stickprob
        self.curac = None
        self.rng = np.random.RandomState()
        self.supports_want_render = hasattr(env, "supports_want_render")

    def reset(self, **kwargs):
        self.curac = None
        return self.env.reset(**kwargs)

    def step(self, ac):
        terminated = False
        truncated = False
        totrew = 0
        for i in range(self.n):
            # First step after reset, use action
            if self.curac is None:
                self.curac = ac
            # First substep, delay with probability=stickprob
            elif i == 0:
                if self.rng.rand() > self.stickprob:
                    self.curac = ac
            # Second substep, new action definitely kicks in
            elif i == 1:
                self.curac = ac
            if self.supports_want_render and i < self.n - 1:
                ob, rew, terminated, truncated, info = self.env.step(
                    self.curac,
                    want_render=False,
                )
            else:
                ob, rew, terminated, truncated, info = self.env.step(self.curac)
            totrew += rew
            if terminated or truncated:
                break
        return ob, totrew, terminated, truncated, info


def make_retro(*, game, state=None, max_episode_steps=4500, **kwargs):
    if state is None:
        state = retro.State.DEFAULT
    env = retro.make(game, state, **kwargs)
    env = StochasticFrameSkip(env, n=4, stickprob=0.25)
    if max_episode_steps is not None:
        env = TimeLimit(env, max_episode_steps=max_episode_steps)
    return env


def wrap_deepmind_retro(env):
    """
    Configure environment for retro games, using config similar to DeepMind-style Atari in openai/baseline's wrap_deepmind
    """
    env = WarpFrame(env)
    env = ClipRewardEnv(env)
    return env
   
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--game", default="SuperMarioKart-UMD")
    parser.add_argument("--state", default=retro.State.DEFAULT)
    parser.add_argument("--scenario", default=None)
    args = parser.parse_args()

    def make_env():
        env = make_retro(game=args.game, state=args.state, scenario=args.scenario)
        env = wrap_deepmind_retro(env)
        return env

    venv = VecTransposeImage(VecFrameStack(SubprocVecEnv([make_env] * 8), n_stack=4))
    model = PPO.load("/home/kvsakano/OUTPUT/SuperMarioKart-UMD-2025-02-06_17-38-30/SuperMarioKart-UMD-ppo2-CnnPolicy-40000")

    obs = venv.reset()
    done = False
    step = 0
    total_reward = 0
    data = []   

    headers = ["step", "x_position", "y_position", "direction", "speed", "drivingMode", "gameMode",
        "frame", "current_checkpoint", "surface", "reward", "total_reward"]
    
    with open("mario_kart_data.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)


        while step < 1000:
            action, _ = model.predict(obs, deterministic=True)
            obs, rewards, done, infos = venv.step(action)
        
            data = [step,
                [info["kart1_X"] for info in infos],
                [info["kart1_Y"] for info in infos],
                [info["kart1_direction"] for info in infos],
                [info["kart1_speed"] for info in infos],
                [info["DrivingMode"] for info in infos],
                [info["GameMode"] for info in infos],
                [info["getFrame"] for info in infos],
                [info["current_checkpoint"] for info in infos],
                [info["surface"] for info in infos],
                rewards,
                total_reward]
        
            writer.writerow(data)

            step += 1
        print('done')

if __name__ == "__main__":
    main()

