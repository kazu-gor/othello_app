import copy
import importlib
import math
import os
import pickle
import sys
import time
from glob import glob

import numpy
import torch

from . import diagnose_model, models, replay_buffer, self_play, shared_storage, trainer
from .games import othello

class MuZero:
    """
    Main class to manage MuZero.

    Args:
        game_name (str): Name of the game module, it should match the name of a .py file
        in the "./games" directory.

        config (dict, MuZeroConfig, optional): Override the default config of the game.

        split_resources_in (int, optional): Split the GPU usage when using concurent muzero instances.

    Example:
        >>> muzero = MuZero("cartpole")
        >>> muzero.train()
        >>> muzero.test(render=True)
    """

    def __init__(self, game_name, config=None, split_resources_in=1):
        # Load the game and the config from the module with the game name
        try:
            self.Game = othello.Game
            self.config = othello.MuZeroConfig()
            
        except ModuleNotFoundError as err:
            print(
                f'{game_name} is not a supported game name, try "cartpole" or refer to the documentation for adding a new game.'
            )
            raise err

        # Overwrite the config
        if config:
            if type(config) is dict:
                for param, value in config.items():
                    setattr(self.config, param, value)
            else:
                self.config = config

        # Fix random generator seed
        numpy.random.seed(self.config.seed)
        torch.manual_seed(self.config.seed)

        # Manage GPUs
        if self.config.max_num_gpus == 0 and (
            self.config.selfplay_on_gpu
            or self.config.train_on_gpu
            or self.config.reanalyse_on_gpu
        ):
            raise ValueError(
                "Inconsistent MuZeroConfig: max_num_gpus = 0 but GPU requested by selfplay_on_gpu or train_on_gpu or reanalyse_on_gpu."
            )
        if (
            self.config.selfplay_on_gpu
            or self.config.train_on_gpu
            or self.config.reanalyse_on_gpu
        ):
            total_gpus = (
                self.config.max_num_gpus
                if self.config.max_num_gpus is not None
                else torch.cuda.device_count()
            )
        else:
            total_gpus = 0
        self.num_gpus = total_gpus / split_resources_in
        if 1 < self.num_gpus:
            self.num_gpus = math.floor(self.num_gpus)


        # Checkpoint and replay buffer used to initialize workers
        self.checkpoint = {
            "weights": None,
            "optimizer_state": None,
            "total_reward": 0,
            "muzero_reward": 0,
            "opponent_reward": 0,
            "episode_length": 0,
            "mean_value": 0,
            "training_step": 0,
            "lr": 0,
            "total_loss": 0,
            "value_loss": 0,
            "reward_loss": 0,
            "policy_loss": 0,
            "num_played_games": 0,
            "num_played_steps": 0,
            "num_reanalysed_games": 0,
            "terminate": False,
        }
        self.replay_buffer = {}

        cpu_actor = CPUActor()
        cpu_weights = cpu_actor.get_initial_weights(self.config)
        self.checkpoint["weights"], self.summary = copy.deepcopy(cpu_weights)

        # Workers
        self.self_play_workers = None
        self.test_worker = None
        self.training_worker = None
        self.reanalyse_worker = None
        self.replay_buffer_worker = None
        self.shared_storage_worker = None

    def application_match(self, render = True, board=None, observation=None):
        self.config.board = board
        
        self_play_worker = self_play.SelfPlay(self.checkpoint, self.Game, self.config, numpy.random.randint(10000))
        
        game_history, next_action = self_play_worker.play_game_beta(
            0, 0, render, observation
        )
        
        action_row = math.floor(next_action / self.config.board_size)
        action_col = next_action % self.config.board_size
        return action_row, action_col


    def load_model(self, checkpoint_path=None, replay_buffer_path=None):
        """
        Load a model and/or a saved replay buffer.

        Args:
            checkpoint_path (str): Path to model.checkpoint or model.weights.

            replay_buffer_path (str): Path to replay_buffer.pkl
        """
        # Load checkpoint
        if checkpoint_path:
            if os.path.exists(checkpoint_path):
                self.checkpoint = torch.load(checkpoint_path)
                print(f"\nUsing checkpoint from {checkpoint_path}")
            else:
                print(f"\nThere is no model saved in {checkpoint_path}.")

        # Load replay buffer
        if replay_buffer_path:
            if os.path.exists(replay_buffer_path):
                with open(replay_buffer_path, "rb") as f:
                    replay_buffer_infos = pickle.load(f)
                self.replay_buffer = replay_buffer_infos["buffer"]
                self.checkpoint["num_played_steps"] = replay_buffer_infos[
                    "num_played_steps"
                ]
                self.checkpoint["num_played_games"] = replay_buffer_infos[
                    "num_played_games"
                ]
                self.checkpoint["num_reanalysed_games"] = replay_buffer_infos[
                    "num_reanalysed_games"
                ]

                print(f"\nInitializing replay buffer with {replay_buffer_path}")
            else:
                print(
                    f"Warning: Replay buffer path '{replay_buffer_path}' doesn't exist.  Using empty buffer."
                )
                self.checkpoint["training_step"] = 0
                self.checkpoint["num_played_steps"] = 0
                self.checkpoint["num_played_games"] = 0
                self.checkpoint["num_reanalysed_games"] = 0

    def diagnose_model(self, horizon):
        """
        Play a game only with the learned model then play the same trajectory in the real
        environment and display information.

        Args:
            horizon (int): Number of timesteps for which we collect information.
        """
        game = self.Game(self.config.seed)
        obs = game.reset()
        dm = diagnose_model.DiagnoseModel(self.checkpoint, self.config)
        dm.compare_virtual_with_real_trajectories(obs, game, horizon)
        input("Press enter to close all plots")
        dm.close_all()



class CPUActor:
    # Trick to force DataParallel to stay on CPU to get weights on CPU even if there is a GPU
    def __init__(self):
        pass

    def get_initial_weights(self, config):
        model = models.MuZeroNetwork(config)
        weigths = model.get_weights()
        summary = str(model).replace("\n", " \n\n")
        return weigths, summary


if __name__ == "__main__":

    board = numpy.zeros((8, 8), dtype="int32")
    board[3][3], board[4][4], board[3][4], board[4][3] = 1, 1, -1, -1
    board[4][5], board[4][4] = -1, -1
    muzero = MuZero("othello")
    
    board_player1 = numpy.where(board == 1, 1.0, 0.0)
    board_player2 = numpy.where(board == -1, 1.0, 0.0)
    board_to_play = numpy.full((8, 8), 1, dtype="int32")
    observation = numpy.array([board_player1, board_player2, board_to_play])
    row, col = muzero.application_match(render=True, board=board, observation=observation)
    print(f"Next Action: [{row}, {col}]")
    print("\nDone")
