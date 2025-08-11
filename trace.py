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
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack, VecTransposeImage, SubprocVecEnv
from stable_baselines3.common.atari_wrappers import ClipRewardEnv, WarpFrame, StickyActionEnv
from env_utils import make_retro

import numpy as np
import random
import torch

import tkinter as tk          # Package for UI selection of folders
from tkinter import filedialog

import imageio                # Package for 


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

def pick_model_folder(base_dir="../../OUTPUT"):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_selected = filedialog.askdirectory(initialdir=base_dir, title="Select Model Folder")
    root.destroy()
    if not folder_selected:
        raise ValueError("No folder selected.")
    
    if (folder_selected == '/home/kvsakano/mario-kart/OUTPUT'):
        print('You need to select the correct folder. Make sure you click into the folder, then OK.')
        folder_selected = filedialog.askdirectory(initialdir=base_dir, title="Select Model Folder")
        root.destroy()
    return folder_selected

def main():
    parser = argparse.ArgumentParser(description="Play model with trace logging")
    parser.add_argument("--model", default='pick', help="Path to trained model")
    parser.add_argument("--game", default="SuperMarioKart-Snes")
    parser.add_argument("--state", default=retro.State.DEFAULT)
    parser.add_argument("--scenario", default=None)
    parser.add_argument("--num_traces", default=9, type=int, help="How many traces do you want to make?")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for numpy, torch, and random.")
    args = parser.parse_args()


    def make_env(rank, base_seed=0):
        def _init():
            env = make_retro(game=args.game, state=args.state, scenario=args.scenario, num_players=1)
            env.action_space.seed(base_seed + rank)
            env = WarpFrame(env)
            env = ClipRewardEnv(env)
            return env
        return _init

    
    #env = DummyVecEnv([make_env])
    #env.seed(args.seed)
    #env = SubprocVecEnv([make_env(i, base_seed=args.seed) for i in range(4)])
    #env = VecTransposeImage(VecFrameStack(env, n_stack=4))

    env = SubprocVecEnv([make_env(i, base_seed=args.seed) for i in range(args.num_traces)])
    env = VecTransposeImage(VecFrameStack(env, n_stack=4))


    if args.model == "pick":
        folder = pick_model_folder()
        print(f"[INFO] Selected folder: {folder}")
        args.model = find_zip_in_folder(folder)
    elif args.model == "latest":
        args.model = find_latest_model()
        print(f"[INFO] Using latest model: {args.model}")
    output_dir = os.path.dirname(args.model)
    
    # Load model
    model = PPO.load(args.model, env=env)

    # iterate for the number of traces you need
    for trace_idx in range(args.num_traces):
        trace_seed = args.seed + trace_idx
        random.seed(trace_seed)
        np.random.seed(trace_seed)
        torch.manual_seed(trace_seed)

    # Reset environment for each trace
    obs = env.reset()
    total_reward = 0
    done = [False]
    state=env.reset()
    step = 0

    while True:
        # Prepare unique output folders/files for each trace for only 1 iteration
        #if (trace_idx == 0):
        # Prepare video folder
        frames_dir = os.path.join(output_dir, "frames")
        os.makedirs(frames_dir, exist_ok=True)
    
        # Prepare CSV
        csv_filename = f"playback_trace{trace_idx:02d}.csv"
        csv_path = os.path.join(output_dir, csv_filename)
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            headers = ["step", "kart1_X", "kart1_Y", "kart1_direction", "kart1_speed",
                       "DrivingMode", "GameMode", "getFrame", "current_checkpoint",
                       "surface", "reward", "total_reward"]
            writer.writerow(headers)
        
            # Run simulation
            obs = env.reset()
            total_reward = 0
            step = 0
            #done = [False]
        
            while not done[0]:# and step < 1000:
                #if (trace_idx == 0):
                frame = env.render(mode='rgb_array') # This grabs the frame in RGB (x,y,3)
                imageio.imwrite(os.path.join(frames_dir, f"frame_{step:05d}.png"), frame)

                #if (trace_idx == args.num_traces -1):
                env.render(mode='human') # Viewable screen for us to watch a playback
                action, _ = model.predict(obs, deterministic=False)
                #if (args.num_traces == 1): # If we only want 1 trace, we likely want it to be deterministic=True
                #    action, _ = model.predict(obs, deterministic=True)
                #else:
                #    action, _ = model.predict(obs, deterministic=False) # Otherwise, make it false
                obs, rewards, done, infos = env.step(action)
                total_reward += rewards[0]
            
                # Write trace data
                info = infos[0]
                data = [step,
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


