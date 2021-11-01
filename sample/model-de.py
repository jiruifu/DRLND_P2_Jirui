#Neural Network Model
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F

# Initilize the weight of target and main network
def finit(layer):
    fan_in = layer.weight.data.size()[0]
    lim = 1. / np.sqrt(fan_in)
    return (-lim, lim)

# Construct the Actor network
class Actor(nn.Module):
    """Actor (Policy) Network
    Parameters
    ==========
    state_size(int): Dimension of the state space
    action_size(int): Dimension of the action space
    seed(int): Random seed
    hidden_dims (tuple): Size of hidden layers
    """
    def __init__(self, state_size, action_size, seed, hidden_dims = (256,)):
        super(Actor, self).__init__()

        self.seed = torch.manual_seed(seed)
        self.input_layer = nn.Linear(
            state_size, hidden_dims[0]
        )
        self.hidden_layers = nn.ModuleList()
        for i in range(len(hidden_dims) - 1):
            hidden_layer = nn.Linear(hidden_dims[i], hidden_dims[i + 1])
            self.hidden_layers.append(hidden_layer)
        self.output_layer = nn.Linear(hidden_dims[-1], action_size)
        self.network_reset()

    def network_reset(self):
        self.input_layer.weight.data.uniform_(*finit(self.input_layer))
        self.output_layer.weight.data.uniform_(-3e-3, 3e-3)
        for i in range(len(self.hidden_layers)):
            self.hidden_layers[i].weight.data.uniform_(*finit(self.hidden_layers[i]))

    def forward(self, state):
        x = F.relu(self.input_layer(state))
        for i in range(len(self.hidden_layers)):
            x = F.relu(self.hidden_layers[i](x))
        x = self.output_layer(x)
        return torch.tanh(x)

class Critic(nn.Module):

    def __init__(self, state_size, action_size, seed, fcs_size = 400, hidden_dims = (256,)):
        super(Critic, self).__init__()
        self.seed = torch.manual_seed(seed)
        self.pre_layer = nn.Linear(state_size, fcs_size)
        self.input_layer = nn.Linear(fcs_size + action_size, hidden_dims[0])
        self.hidden_layers = nn.ModuleList()
        for i in range(len(hidden_dims) - 1):
            hidden_layer = nn.Linear(hidden_dims[i], hidden_dims[i + 1])
            self.hidden_layers.append(hidden_layer)
        self.output_layer = nn.Linear(hidden_dims[-1], 1)
        self.network_reset()

    def network_reset(self):
        self.pre_layer.weight.data.uniform_(*finit(self.pre_layer))
        self.input_layer.weight.data.uniform_(*finit(self.input_layer))
        self.output_layer.weight.data.uniform_(*finit(self.output_layer))
        for i in range(len(self.hidden_layers)):
            self.hidden_layers[i].weight.data.uniform_(*finit(self.hidden_layers[i]))

    def forward(self, state, action):
        x_pre = F.relu(self.pre_layer(state))
        x = torch.cat((x_pre, action), dim = 1)
        x = F.relu(self.input_layer(x))
        for i in range(len(self.hidden_layers)):
            x = F.relu(self.hidden_layers[i](x))

        x = self.output_layer(x)
        return x
