"""
Deep Reinforcement learning.
"""

# import
# import pickle
import logging
import numpy as np
import torch
import torch.nn.functional as F
import torch.optim as optim
from Q_MLP import Q_MLP
# import math
import matplotlib.pyplot as plt


def action_filter(state):
    """
    output valid actions for the state
    """
    actions = []
    for i in range(1, len(state)):
        if state[i] == 0:
            actions.append(i)
    if len(actions) == 0:
        actions.append(0)
    return actions

def ess_action_filter(state):
    """_summary_

    Args:
        state (_type_): represents current MG state:
                        [time, sky_condition, SOC]
        F (_type_): Max consecutive hours of discharge possible

    Returns:
        _type_: list of potential actions represented as values
                0=discharge
                1=charge
                2=idle
    """
    #                        D   C   I
    #                        0   1   2  Max hours
    # ESS directives values [1, -.c, 0, F]
    # look at the current SOC for the ESS and decide potential states
    state = list(state)
    SOC = state[2]
    
    Fx = state[-1]
    
    state = tuple(state)
    # print("SOC: ", SOC)
    # if not fully discharged or fully charged anything goes
    # if 0 < SOC < F: 
    if SOC < Fx and SOC > 0:
        # print("all 3")
        return [0, 1, 2]
    # if fully discharged we can only charge(1) or remain idle (2)
    elif SOC >= Fx:
        # print("charge only")
        # return [1, 2]
        return [1]
    # if fully charged we can only discharge(0) or remain idle (0)
    elif SOC == 0:
        # print("discharge only")
        # return [0, 2]
        return [0]
    
def abs_nrm_ess_evaluator(val, mn, mx, **kwargs):
    R = mn
    # normalize the score
    valnrm = R*((val-mn)/(mx-mn))
    return R - abs(valnrm)

def base_ess_reward(val, **kwargs):
    return val

def base_rpf_scale_ess_reward(val, rpf_scl = .2, goal=200, **kwargs):
    if val < 0:
        return val
    elif val > 0:
        return val * rpf_scl
    elif val == 0:
        return goal


def ess_state_action_reward(state, action, ess_values, PV, D, evaluator=max, 
                            verbose=False, **kwargs):
    ess_out = ess_values[action]*ess_values[-1]
    t = state[0]
    k = state[1]
    pv_out, demand = PV[t, k], D[t]
    return evaluator(PV+ess_out - demand, **kwargs)

class Agent:
    """
    Agent used in the DRL class.
    - name: str, name of the agent;
    - actions: a list of all actions;
    - input_size: int, size of the input, len(state);
    - hidden_layers: list, the number of neurons for the hidden layer,
    - output_size: int, size of the output, len(all actions);
    Keyword Arguments:
    - action_filter: function that filters actions for a given state;
    - Q_path: path to learned parameters of pytorch network.
    """

    def __init__(
        self, name, actions, input_size, hidden_layers, output_size,
        learning_rate=1e-3, learn_epoch=1, epsilon=.5, **kwargs
    ):
        super().__init__()
        # name & actions
        self.name, self.actions = name, actions
        # epsilon
        self.epsilon = epsilon
        # ------------- whether to use action_filter ----------------
        if 'action_filter' in kwargs:
            # print("Filtering actions!!")
            self.filter_action = True
            self.action_filter = kwargs['action_filter']
        else:        
            self.filter_action = False
        # ------------------- GPU ----------------
        if torch.cuda.is_available():
            self.dev = "cuda:0"
        else:
            self.dev = "cpu"
        # ----------------- construct network --------------------
        self.hidden_layers = hidden_layers
        self.input_size, self.output_size = input_size, output_size
        # prediction network
        self.Q = Q_MLP(
            hidden_layer_shape=self.hidden_layers,
            input_size=input_size,
            output_size=output_size,
            seed=1
        )
        self.Q.to(self.dev)
        # target network
        self.Q_target = Q_MLP(
            hidden_layer_shape=self.hidden_layers,
            input_size=input_size,
            output_size=output_size,
            seed=1
        )
        self.Q_target.to(self.dev)
        for p in self.Q.parameters():
            p.data.fill_(0)
        for p in self.Q_target.parameters():
            p.data.fill_(0)
        # load previous parameters
        if 'Q_path' in kwargs:
            self.Q.load_state_dict(torch.load(kwargs['Q_path']))
            self.Q.eval()
        # optimizer
        self.optimizer = optim.Adam(self.Q.parameters(), lr=learning_rate)
        # training step
        self.train_step = 1
        self.loss_memory = []
        self.G_memory = []
        self.learn_epoch = learn_epoch

    def load_parameter(self, actor_path, critic_path):
        """
        Load network parameter from path
        """
        self.actor.load_state_dict(torch.load(actor_path))
        self.critic.load_state_dict(torch.load(critic_path))
        return

    def generate_policy(self, states,):
        policy = {}
        for state in states:
            ky = "-".join(  [str(s)  for s in list(state)[:-1] ]   )
            policy[ ky ] = self.take_action(state)
        return policy


    def take_action(self, state, **kwargs):
        """
        take action (make prediction), based on the input state.
        """
        # make state to tensor
        input_seq = torch.tensor(
            state, dtype=torch.float, device=self.dev
        )
        # make a prediction
        self.Q.eval()
        with torch.no_grad():
            output_seq = list(self.Q(input_seq))
        self.Q.train()
        # valid_actions
        if self.filter_action:
            valid_actions = self.action_filter(state)
            # print("State: {}, Actions: {}".format(state, valid_actions))
        else:
            valid_actions = self.actions
        # get a random number between 0, 1
        if np.random.random() > self.epsilon:
            return valid_actions[np.argmax([
                output_seq[self.actions.index(i)]
                for i in valid_actions
            ])]
        else:
            return valid_actions[np.random.choice(
                range(len(valid_actions)), size=1, replace=False,
                p=[1 / len(valid_actions)] * len(valid_actions)
            )[0]]

    def simulate_action(self, state):
        """
        take action (for simulation), based on the input state.
        """
        # make state to tensor
        input_seq = torch.tensor(
            state, dtype=torch.float, device=self.dev
        )
        # make a prediction
        self.Q.eval()
        with torch.no_grad():
            output_seq = list(self.Q(input_seq))
        self.Q.train()
        # valid_actions
        if self.filter_action:
            valid_actions = self.action_filter(state)
        else:
            valid_actions = self.actions
        return valid_actions[np.argmax([
            output_seq[self.actions.index(i)]
            for i in valid_actions
        ])]

    def learn(self, memory, discount_factor):
        """
        train the network
        """
        # memories
        state_memory = memory[0]
        new_state_memory = memory[1]
        delta_memory = memory[2]
        action_memory = memory[3]
        reward_memory = memory[4]
        # action index
        action_ind = torch.tensor([
            [self.actions.index(a)] for a in action_memory
        ], device=self.dev)  # .flatten()
        # while True:
        for train_iter in range(self.learn_epoch):
            # set zero grad
            self.optimizer.zero_grad()
            # make a prediction
            Q_pred = self.Q(
                torch.FloatTensor(state_memory).to(self.dev)
            ).gather(1, action_ind).flatten()
            # calculate the target
            Q_targ_future = self.Q_target(
                torch.FloatTensor(new_state_memory).to(self.dev)
            ).detach().max(1)[0]
            # target
            Q_targ = torch.FloatTensor([
                reward_memory[i] if delta_memory[i]
                else reward_memory[i] + discount_factor * Q_targ_future[i]
                for i in range(len(reward_memory))
            ])
            Q_pred = Q_pred.to(self.dev)
            Q_targ = Q_targ.to(self.dev)
            # loss
            loss = F.mse_loss(Q_pred, Q_targ)
            # backpropogate
            loss.backward()
            self.optimizer.step()
        self.loss_memory.append(loss.to('cpu').detach().numpy())
        self.train_step += 1
        # soft update the target network
        if self.train_step % 1 == 0:
            self.__soft_update(self.Q, self.Q_target, 0.001)
        return

    def __soft_update(self, Q, Q_target, tau):
        """
        Soft update model parameters:
            θ_target = τ*θ_trained + (1 - τ)*θ_target;
        Q: weights will be copied from;
        Q_target: weights will be copied to;
        tau: interpolation parameter.
        """
        for q_target, q in zip(Q_target.parameters(), Q.parameters()):
            q_target.data.copy_(
                tau * q.data + (1.0 - tau) * q_target.data
            )
        return
    
    def plot_G(self, window=20, start_ind=0, sample=1, dir='', title="Average Return", 
                  TFD={}, close_me=False):
        """
        plot return using time window
        """
        G_plot = {}
        ind = window
        print("size of gmem: ", len(self.G_memory))
        while ind <= len(self.G_memory):
            # sample
            if ind % sample == 0:
                G_plot[ind - 1] = np.mean([
                    self.G_memory[i] for i in range(ind - window, ind, 1)
                ])
            ind += 1
        # plot
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
        ax.plot(
            list(G_plot.keys())[start_ind:],
            list(G_plot.values())[start_ind:],
            'b-'
        )
        ax.set_xlabel('Epochs')
        ax.set_ylabel('G')
        ax.set_title(title, fontdict=TFD)
        fig.tight_layout()
        fig.savefig('{}{}_G.png'.format(dir, self.name), dpi=600)
        if close_me:
            plt.close()
        return
    
    def collect_loss(self, window, sample, ):
        loss_plot = {}
        ind = window
        while ind <= len(self.loss_memory):
            # when we hit a sample size 
            # get the average over the size window 
            if ind % sample == 0:
                loss_plot[ind - 1] = np.mean([ # from the start of the window to me get the average
                    self.loss_memory[i] for i in range(ind - window, ind, 1)
                ])
            ind += 1
        return loss_plot
    
    def plot_loss(self, window=20, start_ind=0, sample=1, dir='', title="Loss", 
                  TFD={}, close_me=False, 
                  ):
        """
        plot train loss for agent
        """
        loss_plot = {}
        ind = window
        while ind <= len(self.loss_memory):
            # sample
            if ind % sample == 0:
                loss_plot[ind - 1] = np.mean([
                    self.loss_memory[i] for i in range(ind - window, ind, 1)
                ])
            ind += 1
        # plot
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
        ax.plot(
            list(loss_plot.keys())[start_ind:],
            list(loss_plot.values())[start_ind:],
            'b-'
        )
        ax.set_xlabel('Epochs')
        ax.set_ylabel('Loss')
        ax.set_title(title, fontdict=TFD)
        fig.tight_layout()
        fig.savefig('{}{}_loss.png'.format(dir, self.name), dpi=600)
        if close_me:
            plt.close()
        return


class DRL_Env:
    """
    Deep Reinforcement learning Environment.
    `name`: str, name of this instance;
    `agent`: Agent class;
    `initial state`: tuple, terminal state = 'Delta'!!!;
    `trans_func`: input state and action,output a new state;
    `reward_func`: input state and action, output a number;
    `memory_size`: int, size of memory;
    `sample_episodes`: size of the training data

    """

    def __init__(
        self, name, agent, initial_state, trans_func, reward_func,
        memory_size=1000, sample_episodes=100, **kwargs
    ):
        # input parameters
        self.name = name
        self.agent = agent
        self.initial_state = initial_state
        self.trans_func = trans_func
        self.reward_func = reward_func
        self.learn_ind = 1
        self.memory_size = memory_size
        self.sample_episodes = sample_episodes
        # initialize memory
        self.memory = Memory(
            memory_size=self.memory_size,
            sample_episodes=self.sample_episodes
        )

    def __Q_update(
        self, discount_factor,
        learn_step, write_log
    ):
        """
        one episode of Q-learning
        """
        # =================== initialize ===================
        # initialize
        G = 0
        state = self.initial_state
        # ======================= LOOP ========================
        epoch, learn_ind = 0, 0
        # until we get to the terminal state
        while state != 'Delta':
            # take action
            action = self.agent.take_action(state)
            # transition
            new_state = self.trans_func(epoch, list(state).copy(), action)
            
            # rewards
            R = self.reward_func(state, action, new_state)
            # delta
            delta = True if new_state == 'Delta' else False
            # update G
            G += R
            
            # --------------- output experience ----------------
            if write_log:
                # logging state, action and reward
                logging.info('    epoch: {}'.format(epoch))
                logging.info('    state: {}'.format(state))
                logging.info('    action: {}'.format(action))
                logging.info('    reward: {}'.format(R))
            # ---------------- memory control --------------------
            self.memory.update(
                state, delta, action, R,
                state if new_state == "Delta" else new_state
            )
            # ---------------- Learning --------------------
            # for each agent, provide data and train.
            if learn_ind % learn_step == 0:
                self.agent.learn(
                    memory=self.memory.sample(),
                    discount_factor=discount_factor
                )
            # ---------- on step, transit to new state -------------
            state = new_state
            epoch += 1
            learn_ind += 1
        # agent record G
        self.agent.G_memory.append(G)
        # print(G)
        return G

    def deep_Q_Network(
        self, episodes, discount_factor, learn_step,
        eps_init, eps_end, write_log, report_iter=100,
    ):
        """
        Deep Q-Network.
        - episodes: how many iterations to simulation in total.
        - alpha: learning rate;
        - discount factor: perspective of future.
        """
        # return
        G = []
        print(episodes)
        # ---------------------- Learning ----------------------
        if write_log:
            logging.info("Learning...")
        for iter in range(episodes):
            if iter % report_iter == 0:
                print("Iteration {}".format(iter))
            if write_log:
                logging.info("Iteration {}".format(iter))
            step_G = self.__Q_update(
                discount_factor, learn_step, write_log
            )
            # -------------- step control ---------------
            # record return
            G.append(step_G)
            # log return
            if write_log:
                logging.info("    return: {}".format(step_G))
            # set epsilon, 7-2.5, 10-5
            self.agent.epsilon = (eps_init - eps_end) * np.max([
                (episodes * 1 - iter) / (episodes * 1), 0
            ]) + eps_end
            if write_log:
                logging.info("    -----------------------")
        return G


class Memory():
    """
    Memory: remembers past information regarding state,
        action, reward and terminal;
    """
    def __init__(self, memory_size, sample_episodes):
        super().__init__()
        self.memory_max = memory_size
        self.sample_size = sample_episodes
        self.memory = {
            'state': [], 'delta': [], 'n_state': [],
            'action': [],
            'reward': [],
        }
        self.pointer = 0
        self.memory_size = 0

    # update, keep the most recent
    def update(self, state, delta, action, reward, new_state):
        """
        `state`: list, new state, do not remember 'Delta';
        `action`: int/str, action;
        `delta`: bool, whether the NEXT state is delta;
        `reward`: double, reward.
        """
        # not full
        if self.memory_size < self.memory_max:
            self.memory['state'].append(state)
            self.memory['delta'].append(delta)
            self.memory['n_state'].append(new_state)
            self.memory['action'].append(action)
            self.memory['reward'].append(reward)
            self.memory_size += 1
        # full
        else:
            self.memory['state'][self.pointer] = state
            self.memory['delta'][self.pointer] = delta
            self.memory['n_state'][self.pointer] = new_state
            self.memory['action'][self.pointer] = action
            self.memory['reward'][self.pointer] = reward
            self.pointer += 1
        # update pointer
        if self.pointer == self.memory_max - 1:
            self.pointer = 0
        return

    # smple from the entire memory, with large memory size
    def sample(self):
        """
        sample state, action, reward and delta
        """
        # indices
        if self.memory_size >= self.sample_size:
            choose_size = self.sample_size
        else:
            choose_size = self.memory_size
        sample_ind = np.random.choice(
            range(self.memory_size), size=choose_size, replace=False,
            p=[1/self.memory_size] * self.memory_size
        )
        # sample
        state_sample = [
            self.memory['state'][i] for i in sample_ind
        ]
        new_state_sample = [
            self.memory['n_state'][i] for i in sample_ind
        ]
        delta_sample = [
            self.memory['delta'][i] for i in sample_ind
        ]
        action_sample = [
            self.memory['action'][i] for i in sample_ind
        ]
        reward_sample = [
            self.memory['reward'][i] for i in sample_ind
        ]
        return (
            state_sample, new_state_sample, delta_sample,
            action_sample, reward_sample
        )
