"""
MLP model, for RL.
"""

# import
import logging
import torch
import torch.nn as nn


class ActorCritic(nn.Module):
    """
    Actor Critic
    """
    def __init__(self, num_inputs, num_actions, hidden_size):
        """
        Initialize
        """
        super(ActorCritic, self).__init__()
        self.seed = torch.manual_seed(1)
        # critic
        self.num_actions = num_actions
        self.critic_linear1 = nn.Linear(num_inputs, 500)
        self.critic_actvtn1 = nn.Tanh()
        self.critic_linear2 = nn.Linear(500, 200)
        self.critic_actvtn2 = nn.Tanh()
        self.critic_linear3 = nn.Linear(200, 1)
        # actor
        self.actor_linear1 = nn.Linear(num_inputs, hidden_size)
        self.actor_actvtn1 = nn.Tanh()
        self.actor_linear2 = nn.Linear(hidden_size, num_actions)
        self.actor_actvtn2 = nn.Softmax(dim=0)

    def forward(self, input_seq):
        """
        input_seq: states, torch.tensor.
        """
        # critic
        value = self.critic_linear1(input_seq)
        value = self.critic_actvtn1(value)
        value = self.critic_linear2(value)
        value = self.critic_actvtn2(value)
        value = self.critic_linear3(value)
        # actor
        policy_dist = self.actor_linear1(input_seq)
        policy_dist = self.actor_actvtn1(policy_dist)
        policy_dist = self.actor_linear2(policy_dist)
        policy_dist = self.actor_actvtn2(policy_dist)
        # return
        return value, policy_dist


def printgradnorm_1(self, grad_input, grad_output, **kwargs):
    logging.info('Inside ' + self.__class__.__name__ + ' backward\n')
    logging.info('Inside class:' + self.__class__.__name__ + '\n')
    logging.info('grad_input: {}\n'.format(grad_input[0]))
    logging.info('grad_input size: {}\n'.format(grad_input[0].size()))
    logging.info('grad_output: {}\n'.format(grad_output))
    logging.info('grad_output size: {}\n'.format(grad_output[0].size()))


def printgradnorm_2(self, grad_input, grad_output, **kwargs):
    logging.info('Inside ' + self.__class__.__name__ + ' backward\n')
    logging.info('Inside class:' + self.__class__.__name__ + '\n')
    logging.info('grad_input: {}\n'.format(grad_input[0]))
    logging.info('grad_input size: {}\n'.format(grad_input[0].size()))
    logging.info('grad_output: {}\n'.format(grad_output))
    logging.info('grad_output size: {}\n'.format(grad_output[0].size()))


class Actor(nn.Module):
    """
    Actor network for A2C.
    """
    def __init__(self, hidden_layers, input_size, output_size, seed=1):
        """
        `hidden_layers`: list, the number of neurons for every layer;
        `input_size`: number of states;
        `output_size`: number of actions;
        `seed`: random seed.
        """
        super().__init__()
        # parameters
        self.seed = torch.manual_seed(seed)
        # NN, adding layers dynamically.
        self.layers = nn.Sequential()
        # ---------------------- input -----------------------
        self.layers.add_module(
            'Linear_inp', nn.Linear(input_size, hidden_layers[0])
        )
        self.layers.add_module('Act_inp', nn.Tanh())
        # ---------------------- hidden ----------------------
        for i in range(1, len(hidden_layers)):
            self.layers.add_module(
                'Linear_{}'.format(i),
                nn.Linear(hidden_layers[i - 1], hidden_layers[i])
            )
            self.layers.add_module('Act_{}'.format(i), nn.Tanh())
        # ----------------------- output ---------------------
        self.layers.add_module(
            'Linear_out', nn.Linear(hidden_layers[-1], output_size)
        )
        self.layers.add_module('Act_out', nn.LogSoftmax(dim=0))
        # actor
        # self.actor_linear1 = nn.Linear(input_size, hidden_layers[0])
        # self.actor_actvtn1 = nn.Tanh()
        # self.actor_linear2 = nn.Linear(hidden_layers[0], output_size)
        # self.actor_actvtn2 = nn.Sigmoid()
        # self.actor_actvtn2 = nn.LogSoftmax(dim=0)
        # self.actor_linear1.register_backward_hook(printgradnorm_1)
        # self.actor_linear2.register_backward_hook(printgradnorm_2)

    def forward(self, input_seq):
        """
        `input_seq`: states, torch.FloatTensor.
        """
        # actor
        # policy_dist = self.actor_linear1(input_seq)
        # policy_dist = self.actor_actvtn1(policy_dist)
        # policy_dist = self.actor_linear2(policy_dist)
        # policy_dist = self.actor_actvtn2(policy_dist)
        # policy_dist = self.actor_actvtn3(policy_dist)
        # return
        # return policy_dist
        return self.layers(input_seq)


class Critic(nn.Module):
    """
    Critic network for A2C.
    """
    def __init__(self, hidden_layers, input_size, seed=1):
        """
        `hidden_layers`: list, the number of neurons for every layer;
        `input_size`: number of states;
        `output_size`: number of actions;
        `seed`: random seed.
        """
        super().__init__()
        # parameters
        self.seed = torch.manual_seed(seed)
        # NN, adding layers dynamically.
        self.layers = nn.Sequential()
        # ---------------------- input -----------------------
        self.layers.add_module(
            'Linear_inp', nn.Linear(input_size, hidden_layers[0])
        )
        self.layers.add_module('Act_inp', nn.ReLU())
        # ---------------------- hidden ----------------------
        for i in range(1, len(hidden_layers)):
            self.layers.add_module(
                'Linear_{}'.format(i),
                nn.Linear(hidden_layers[i - 1], hidden_layers[i])
            )
            self.layers.add_module('Act_{}'.format(i), nn.ReLU())
        # ----------------------- output ---------------------
        self.layers.add_module(
            'Linear_out', nn.Linear(hidden_layers[-1], 1)
        )

    def forward(self, input_seq):
        """
        `input_seq`: states, torch.FloatTensor.
        """
        return self.layers(input_seq)
