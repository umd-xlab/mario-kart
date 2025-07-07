"""
Play a model with SuperMarioKart-Snes
"""

import warnings
warnings.filterwarnings("ignore")

import os
import sys
import time
import argparse
from common import get_model_file_name, com_print, init_logger, create_output_dir
from models_utils import init_model
from env_utils import init_env
import glob

import csv
import retro
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack, VecTransposeImage
from stable_baselines3.common.atari_wrappers import ClipRewardEnv, WarpFrame
from env_utils import make_retro

import numpy as np
import random
SEED = 0
random.seed(SEED)
np.random.seed(SEED)

def find_zip_in_folder(folder_path):
    # Find all .zip files in the folder (non-recursive)
    zip_files = glob.glob(os.path.join(folder_path, "*.zip"))
    if not zip_files:
        raise FileNotFoundError(f"No .zip files found in {folder_path}")
    # If multiple, pick the first (or sort for most recent if you prefer)
    return zip_files[0]

def find_latest_model(base_dir="../../OUTPUT"):
    # Get all folders in OUTPUT
    folders = [os.path.join(base_dir, d) for d in os.listdir(base_dir)
               if os.path.isdir(os.path.join(base_dir, d))]
    if not folders:
        raise FileNotFoundError("No folders found in OUTPUT directory.")

    # Sort folders by modification time, newest last
    folders.sort(key=os.path.getmtime)
    latest_folder = folders[-1]

    # Model file has the same name as the folder, with .zip extension
    folder_name = os.path.basename(latest_folder)
    model_zip = find_zip_in_folder(latest_folder)
    model_path = os.path.join(latest_folder, model_zip)
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Model file {model_path} not found in latest folder.")
    return model_path

def main():
    parser = argparse.ArgumentParser(description="Play model with trace logging")
    parser.add_argument("--model", required=True, help="Path to trained model")
    parser.add_argument("--output", default="playback_trace.csv", help="Output CSV file")
    parser.add_argument("--game", default="SuperMarioKart-Snes")
    parser.add_argument("--state", default=retro.State.DEFAULT)
    parser.add_argument("--scenario", default=None)
    args = parser.parse_args()

    # Create environment
    def make_env():
        env = make_retro(game=args.game, state=args.state, scenario=args.scenario, num_players=1)
        env = WarpFrame(env)
        env = ClipRewardEnv(env)
        return env
    
    env = DummyVecEnv([make_env])
    env = VecTransposeImage(VecFrameStack(env, n_stack=4))

    if args.model == "latest":
        args.model = find_latest_model()
        print(f"[INFO] Using latest model: {args.model}")

    
    # Load model
    model = PPO.load(args.model, env=env)
    
    # Prepare CSV
    with open(args.output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        headers = ["step", "kart1_X", "kart1_Y", "kart1_direction", "kart1_speed",
                   "DrivingMode", "GameMode", "getFrame", "current_checkpoint",
                   "surface", "reward", "total_reward"]
        writer.writerow(headers)
        
        # Run simulation
        obs = env.reset()
        total_reward = 0
        step = 0
        done = [False]
        
        while not done[0] and step < 1000:
            action, _ = model.predict(obs, deterministic=True)
            obs, rewards, done, infos = env.step(action)
            total_reward += rewards[0]
            
            # Write trace data
            info = infos[0]
            data = [
                step,
                info.get("kart1_X", 0),
                info.get("kart1_Y", 0),
                info.get("kart1_direction", 0),
                info.get("kart1_speed", 0),
                info.get("DrivingMode", 0),
                info.get("GameMode", 0),
                info.get("getFrame", 0),
                info.get("current_checkpoint", 0),
                info.get("surface", 0),
                rewards[0],
                total_reward
            ]
            writer.writerow(data)
            step += 1

if __name__ == "__main__":
    main()
