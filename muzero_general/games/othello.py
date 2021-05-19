import datetime
import math
import os

import numpy
import torch

from .abstract_game import AbstractGame


class MuZeroConfig:
    def __init__(self):
        # More information is available here: https://github.com/werner-duvaud/muzero-general/wiki/Hyperparameter-Optimization

        self.seed = 0  # Seed for numpy, torch and the game
        self.max_num_gpus = None  # Fix the maximum number of GPUs to use. It's usually faster to use a single GPU (set it to 1) if it has enough memory. None will use every GPUs available



        ### Game
        self.observation_shape = (3, 8, 8)  # (channels, height, width)
        self.action_space = list(range(8 * 8))  # Fixed list of all possible actions. You should only edit the length
        self.players = list(range(2))  # List of players. You should only edit the length
        self.stacked_observations = 0  # Number of previous observations and previous actions to add to the current observation

        # Evaluate
        self.muzero_player = 0  # Turn Muzero begins to play (0: MuZero plays first, 1: MuZero plays second)
        self.opponent = "random"  # Hard coded agent that MuZero faces to assess his progress in multiplayer games. It doesn't influence training. None, "random" or "expert" if implemented in the Game class



        ### Self-Play
        self.num_workers = 2  # Number of simultaneous threads/workers self-playing to feed the replay buffer
        self.selfplay_on_gpu = True
        self.max_moves = 60  # Maximum number of moves if game is not finished before
        self.num_simulations = 400  # Number of future moves self-simulated
        self.discount = 1  # Chronological discount of the reward
        self.temperature_threshold = None  # Number of moves before dropping the temperature given by visit_softmax_temperature_fn to 0 (ie selecting the best action). If None, visit_softmax_temperature_fn is used every time

        # Root prior exploration noise
        self.root_dirichlet_alpha = 0.3
        self.root_exploration_fraction = 0.25

        # UCB formula
        self.pb_c_base = 19652
        self.pb_c_init = 1.25



        ### Network
        self.network = "resnet"  # "resnet" / "fullyconnected"
        self.support_size = 10  # Value and reward are scaled (with almost sqrt) and encoded on a vector with a range of -support_size to support_size. Choose it so that support_size <= sqrt(max(abs(discounted reward)))

        # Residual Network
        self.downsample = "CNN"  # Downsample observations before representation network, False / "CNN" (lighter) / "resnet" (See paper appendix Network Architecture)
        self.blocks = 6  # Number of blocks in the ResNet
        self.channels = 128  # Number of channels in the ResNet
        self.reduced_channels_reward = 2  # Number of channels in reward head
        self.reduced_channels_value = 2  # Number of channels in value head
        self.reduced_channels_policy = 4  # Number of channels in policy head
        self.resnet_fc_reward_layers = [64]  # Define the hidden layers in the reward head of the dynamic network
        self.resnet_fc_value_layers = [64]  # Define the hidden layers in the value head of the prediction network
        self.resnet_fc_policy_layers = [64]  # Define the hidden layers in the policy head of the prediction network

        # Fully Connected Network
        self.encoding_size = 32
        self.fc_representation_layers = []  # Define the hidden layers in the representation network
        self.fc_dynamics_layers = [64]  # Define the hidden layers in the dynamics network
        self.fc_reward_layers = [64]  # Define the hidden layers in the reward network
        self.fc_value_layers = []  # Define the hidden layers in the value network
        self.fc_policy_layers = []  # Define the hidden layers in the policy network



        ### Training
        self.results_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../results", os.path.basename(__file__)[:-3], datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S"))  # Path to store the model weights and TensorBoard logs
        self.save_model = True  # Save the checkpoint in results_path as model.checkpoint
        self.training_steps = 10000  # Total number of training steps (ie weights update according to a batch)
        self.batch_size = 512  # Number of parts of games to train on at each training step
        self.checkpoint_interval = 50  # Number of training steps before using the model for self-playing
        self.value_loss_weight = 1  # Scale the value loss to avoid overfitting of the value function, paper recommends 0.25 (See paper appendix Reanalyze)
        self.train_on_gpu = torch.cuda.is_available()  # Train on GPU if available

        self.optimizer = "Adam"  # "Adam" or "SGD". Paper uses SGD
        self.weight_decay = 1e-4  # L2 weights regularization
        self.momentum = 0.9  # Used only if optimizer is SGD

        # Exponential learning rate schedule
        self.lr_init = 0.002  # Initial learning rate
        self.lr_decay_rate = 0.9  # Set it to 1 to use a constant learning rate
        self.lr_decay_steps = 10000



        ### Replay Buffer
        self.replay_buffer_size = 10000  # Number of self-play games to keep in the replay buffer
        self.num_unroll_steps = 60  # Number of game moves to keep for every batch element
        self.td_steps = 60  # Number of steps in the future to take into account for calculating the target value
        self.PER = True  # Prioritized Replay (See paper appendix Training), select in priority the elements in the replay buffer which are unexpected for the network
        self.PER_alpha = 0.5  # How much prioritization is used, 0 corresponding to the uniform case, paper suggests 1

        # Reanalyze (See paper appendix Reanalyse)
        self.use_last_model_value = True  # Use the last model to provide a fresher, stable n-step value (See paper appendix Reanalyze)
        self.reanalyse_on_gpu = False



        ### Adjust the self play / training ratio to avoid over/underfitting
        self.self_play_delay = 0  # Number of seconds to wait after each played game
        self.training_delay = 0  # Number of seconds to wait after each training step
        self.ratio = 1  # Desired training steps per self played step ratio. Equivalent to a synchronous version, training can take much longer. Set it to None to disable it


    def visit_softmax_temperature_fn(self, trained_steps):
        """
        Parameter to alter the visit count distribution to ensure that the action selection becomes greedier as training progresses.
        The smaller it is, the more likely the best action (ie with the highest visit count) is chosen.

        Returns:
            Positive float.
        """
        if trained_steps < 0.5 * self.training_steps:
            return 1.0
        elif trained_steps < 0.75 * self.training_steps:
            return 0.5
        else:
            return 0.25


class Game(AbstractGame):
    """
    Game wrapper.
    """

    def __init__(self, seed=None):
        self.env = Othello()

    def pass_step(self):
        observation, reward, done = self.env.pass_step()
        return observation, reward, done

    def step(self, action):
        """
        Apply action to the game.

        Args:
            action : action of the action_space to take.

        Returns:
            The new observation, the reward and a boolean if the game has ended.
        """
        observation, reward, done = self.env.step(action)
        return observation, reward, done

    def to_play(self):
        """
        Return the current player.

        Returns:
            The current player, it should be an element of the players list in the config.
        """
        return self.env.to_play()

    def legal_actions(self):
        """
        Should return the legal actions at each turn, if it is not available, it can return
        the whole action space. At each turn, the game have to be able to handle one of returned actions.

        For complex game where calculating legal moves is too long, the idea is to define the legal actions
        equal to the action space but to return a negative reward if the action is illegal.

        Returns:
            An array of integers, subset of the action space.
        """
        return self.env.legal_actions()

    def reset(self):
        """
        Reset the game for a new game.

        Returns:
            Initial observation of the game.
        """
        return self.env.reset()

    def close(self):
        """
        Properly close the game.
        """
        pass

    def render(self):
        """
        Display the game observation.
        """
        self.env.render()
        input("Press enter to take a step ")

    def human_to_action(self):
        """
        For multiplayer games, ask the user for a legal action
        and return the corresponding action number.

        Returns:
            An integer from the action space.
        """
        valid = False
        while not valid:
            valid, action = self.env.human_input_to_action()
        return action

    def action_to_string(self, action):
        """
        Convert an action number to a string representing the action.
        Args:
            action_number: an integer from the action space.
        Returns:
            String representing the action.
        """
        return self.env.action_to_human_input(action)


class Othello:
    def __init__(self):
        self.board_size = 8
        self.board = numpy.zeros((self.board_size, self.board_size), dtype="int32")
        self.board[3][3], self.board[4][4], self.board[3][4], self.board[4][3] = 1, 1, -1, -1
        self.player = 1
        self.board_markers = [
            str(x) for x in range(self.board_size)
        ]

    def to_play(self):
        return 0 if self.player == 1 else 1

    def reset(self):
        self.board = numpy.zeros((self.board_size, self.board_size), dtype="int32")
        self.board[3][3], self.board[4][4], self.board[3][4], self.board[4][3] = 1, 1, -1, -1
        self.player = 1
        return self.get_observation()

    def pass_step(self):
        done = self.is_finished()

        reward = 1 if done else 0

        self.player *= -1

        return self.get_observation(), reward, done

    def step(self, action):
        row = math.floor(action / self.board_size)
        col = action % self.board_size
        self.board[row][col] = self.player

        self.board = self.update(action)

        done = self.is_finished()

        reward = 1 if done else 0

        self.player *= -1

        return self.get_observation(), reward, done

    def get_observation(self):
        board_player1 = numpy.where(self.board == 1, 1.0, 0.0)
        board_player2 = numpy.where(self.board == -1, 1.0, 0.0)
        board_to_play = numpy.full((8, 8), self.player, dtype="int32")
        return numpy.array([board_player1, board_player2, board_to_play])

    def legal_actions(self):
        legal = []
        relations = {}
        direction = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                     (0, 1), (1, -1), (1, 0), (1, 1))
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] != self.player:
                    continue
                for d in direction:
                    row, col = i, j
                    count = 0
                    while True:
                        row += d[0]
                        col += d[1]
                        count += 1
                        if (row not in range(self.board_size) or
                            col not in range(self.board_size)):
                            break
                        if (self.board[row][col] != -1*self.player and count == 1):
                            break
                        elif (self.board[row][col] == self.player):
                            break
                        elif (self.board[row][col] == 0):
                            relations.setdefault(int(f"{row}{col}"), []).append(int(f"{i}{j}"))
                            legal.append(row * self.board_size + col)
                            break
        self.relations = relations
        return legal

    def update(self, action):
        """
        Update the Othello board from the action.
        """
        # print(f"relations: \n{self.relations}")
        action_row = math.floor(action / self.board_size)
        action_col = action % self.board_size
        if int(f"{action_row}{action_col}") not in self.relations.keys():
            return self.board
        for init in self.relations[int(f"{action_row}{action_col}")]:
            if init < 10:
                init_row, init_col = 0, int(str(init)[0])
            else:
                init_row, init_col = int(str(init)[0]), int(str(init)[1])
            distance_row, distance_col = action_row - init_row, action_col - init_col
            if (abs(distance_row) == 0):
                """ horizontal direction """
                if action_col > init_col:
                    self.board[action_row, init_col+1: action_col] = self.player
                else:
                    self.board[action_row, action_col+1: init_col] = self.player
            elif (abs(distance_col) == 0):
                """ vertical direction """
                if action_row > init_row:
                    self.board[init_row+1: action_row, action_col] = self.player
                else:
                    self.board[action_row+1: init_row, action_col] = self.player
            elif (distance_row == distance_col):
                """ downword to the right """
                if action_row > init_row:
                    for i in range(1, abs(distance_row)):
                        self.board[init_row+i, init_col+i] = self.player
                else:
                    for i in range(1, abs(distance_row)):
                        self.board[action_row+i, action_col+i] = self.player
            elif (distance_row + distance_col == 0):
                """ downword to the left """
                if action_row > init_row:
                    for i in range(1, abs(distance_row)):
                        self.board[init_row+i, init_col-i] = self.player
                else:
                    for i in range(1, abs(distance_row)):
                        self.board[action_row+i, action_col-i] = self.player
        return self.board

    def is_finished(self):
        print(f"""\
numpy.sum(self.board == 1) == 0: {numpy.sum(self.board == 1) == 0}
numpy.sum(self.board == -1) == 0: {numpy.sum(self.board == -1) == 0}
numpy.sum(self.board == 0) == 0: {numpy.sum(self.board == 0) == 0}
""")
        if (numpy.sum(self.board == 1) == 0 or
            numpy.sum(self.board == -1) == 0 or
            numpy.sum(self.board == 0) == 0):
            return True
        return False

    def render(self):
        marker = "  "
        for i in range(self.board_size):
            marker = marker + self.board_markers[i] + " "
        print(marker)
        for row in range(self.board_size):
            print(row, end=" ")
            for col in range(self.board_size):
                ch = self.board[row][col]
                if ch == 0:
                    print(".", end=" ")
                elif ch == 1:
                    print("X", end=" ")
                elif ch == -1:
                    print("O", end=" ")
            print()

    def human_input_to_action(self):
        human_input = input("Enter an action: ")
        if (
            # 入力値は行列の数字二組が望ましい，example: "12"(row: 1, col: 2)
            len(human_input) == 2
            and human_input[0] in self.board_markers
            and human_input[1] in self.board_markers
        ):
            row, col = int(human_input[0]), int(human_input[1])
            if (
                self.board[row][col] == 0
                and (row * self.board_size + col) in self.legal_actions()):
                return True, row * self.board_size + col
        return False, -1

    def action_to_human_input(self, action):
        row = math.floor(action / self.board_size)
        col = action % self.board_size
        return row + col