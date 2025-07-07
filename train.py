"""
Train a Model on NHL 94
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

import csv
import os

import random
import numpy as np
import torch

SEED = 0
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
# If using CUDA:
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #suppress warnings



class TraceLogger:
    def __init__(self, path, num_envs):
        self.path = os.path.join(path, "training_trace.csv")
        self.num_envs = num_envs
        self.header_written = False

    def write_step(self, step, infos, rewards):
        with open(self.path, 'a', newline='') as f:
            writer = csv.writer(f)
            if not self.header_written:
                headers = ['env_id', 'step', 'x', 'y', 'checkpoint', 'surface', 'reward']
                writer.writerow(headers)
                self.header_written = True
            for env_id in range(self.num_envs):
                info = infos[env_id]
                row = [
                    env_id,
                    step,
                    info.get("kart1_X", 0),
                    info.get("kart1_Y", 0),
                    info.get("current_checkpoint", -1),
                    info.get("surface", -1),
                    rewards[env_id],
                ]
                writer.writerow(row)


def parse_cmdline(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--alg', type=str, default='ppo2')
    parser.add_argument('--nn', type=str, default='CnnPolicy')
    parser.add_argument('--nnsize', type=int, default='256')
    parser.add_argument('--env', type=str, default='SuperMarioKart-Snes')
    parser.add_argument('--state', type=str, default=None)
    parser.add_argument('--num_players', type=int, default='1')
    parser.add_argument('--num_env', type=int, default=6)
    parser.add_argument('--num_timesteps', type=int, default=10000)
    parser.add_argument('--output_basedir', type=str, default='../../OUTPUT')
    parser.add_argument('--load_p1_model', type=str, default='')
    parser.add_argument('--display_width', type=int, default='1440')
    parser.add_argument('--display_height', type=int, default='810')
    parser.add_argument('--alg_verbose', default=True, action='store_true')
    parser.add_argument('--info_verbose', default=True, action='store_true')
    parser.add_argument('--play', default=False, action='store_true')
    parser.add_argument('--rf', type=str, default='')
    parser.add_argument('--deterministic', default=True, action='store_true')
    parser.add_argument('--hyperparams', type=str, default='../hyperparams/default.json')

    args = parser.parse_args(argv)

    #if args.info_verbose is False:
    #    logger.set_level(logger.DISABLED)

    return args

class ModelTrainer:
    def __init__(self, args, logger):
        self.args = args

        #if self.args.alg_verbose:
        #    logger.log('========= Init =============')

        self.output_fullpath = create_output_dir(args)
        model_savefile_name = get_model_file_name(args)
        self.model_savepath = os.path.join(self.output_fullpath, model_savefile_name)

        self.env = init_env(self.output_fullpath, args.num_env, args.state, args.num_players, args)
        obs = self.env.reset()

        self.p1_model = init_model(self.output_fullpath, args.load_p1_model, args.alg, args, self.env, logger)

        #if self.args.alg_verbose:
        com_print('OUTPUT PATH:   %s' % self.output_fullpath)
        com_print('ENV:           %s' % args.env)
        com_print('STATE:         %s' % args.state)
        com_print('NN:            %s' % args.nn)
        com_print('ALGO:          %s' % args.alg)
        com_print('NUM TIMESTEPS: %s' % args.num_timesteps)
        com_print('NUM ENV:       %s' % args.num_env)
        com_print('NUM PLAYERS:   %s' % args.num_players)

    def train(self):
        com_print('========= Start Training ==========')

        if self.args.alg == 'es':
            self.p1_model.train(num_generations=500)
        else:
            self.p1_model.learn(total_timesteps=self.args.num_timesteps)

        com_print('========= End Training ==========')

        self.p1_model.save(self.model_savepath)
        com_print('Model saved to:%s' % self.model_savepath)

        return self.model_savepath

    def play(self, args, continuous=True):
        com_print('========= Start Play Loop ==========')

        trace_rows = []
        headers = ['step', 'x', 'y', 'checkpoint', 'surface', 'reward']

        episode_num = 0
        while True:
            state = self.env.reset()
            done = [False]
            step = 0
            trace_rows.clear()  # clear previous episode's trace

            while not done[0]:
                self.env.render(mode='human')
                p1_actions = self.p1_model.predict(state, deterministic=args.deterministic)
                state, reward, done, info = self.env.step(p1_actions[0])
                # Collect trace data for this step
                row = [
                    step,
                    info[0].get("kart1_X", 0),
                    info[0].get("kart1_Y", 0),
                    info[0].get("current_checkpoint", -1),
                    info[0].get("surface", -1),
                    reward[0],
                ]
                trace_rows.append(row)
                step += 1

                if done[0] and episode_num==0:
                    # Save trace to CSV for this episode
                    out_dir = self.output_fullpath
                    os.makedirs(out_dir, exist_ok=True)
                    trace_file = os.path.join(out_dir, f"play_trace_ep{episode_num}.csv")
                    with open(trace_file, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(headers)
                        writer.writerows(trace_rows)
                    print(f"[INFO] Saved trace for episode {episode_num} to {trace_file}")

                    episode_num += 1
                    break  # End this episode

            if not continuous:
                break  # Only play one episode if not continuous


def main(argv):

    args = parse_cmdline(argv[1:])

    logger = init_logger(args)
    com_print("=========== Params ===========")
    com_print(args)

    trainer = ModelTrainer(args, logger)

    trainer.train()

    if args.play:
        trainer.play(args)


if __name__ == '__main__':
    main(sys.argv)
