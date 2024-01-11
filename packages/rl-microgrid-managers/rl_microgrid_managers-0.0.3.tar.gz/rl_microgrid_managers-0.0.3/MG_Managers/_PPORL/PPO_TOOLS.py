# modified from original here: https://github.com/philtabor/Youtube-Code-Repository/blob/master/ReinforcementLearning/PolicyGradient/PPO/torch/ppo_torch.py
import os
import numpy as np
import torch as T
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions.categorical import Categorical
import matplotlib.pyplot as plt





base_sunlight_hours = {
        1:  [7,17],
        2:  [7,17],
        3:  [7,17],
        4:  [6,18],
        5:  [6,19],
        6:  [6,19],
        7:  [6,19],
        8:  [7,19],
        9:  [7,18],
        10: [7,18],
        11: [7,17],
        12: [7,17],
    }

def action_filter(state, F=4, 
                  sunlight_hours_dict=base_sunlight_hours, **kwargs):
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
        #        actions         D   C   I
        #                        0   1   2  Max hours
        # ESS directives values [1, -.c, 0, F]
        # G = 1 if connected to grid, 0 otherwise
        # State: 
        #   * 7 dimension:=[time, month_v, S, P, D, connection, weather_v]
        #   * 6 dimension:=[time, month_v, S, P, D,  connection]
        # look at the current SOC for the ESS and decide potential states
        
        month_v = state[1]
        if "needed" not in kwargs:
            print("no needed")
            needed = 0
        else:
            needed = kwargs["needed"]
        buyBack=False
        if "buyBack" in kwargs:
            buyBack = kwargs["buyBack"]
            
        PVsufficient = state[3] >= state[4]  # PV >= Demand
        state = list(state)
        SOC = state[2]
        Fx = F
        sunrise = sunlight_hours_dict[month_v][0]
        sunset = sunlight_hours_dict[month_v][1]
        sunlight_hours = list(range(sunrise, sunset+1))
        # needed =  ((self.ess_cap*F/F)*self.ess_ceff)/1000
        #  Catch Isolated Grid condition
        # if state[5] != 1 and int(state[0]) not in sunlight_hours:
        charge_possible = state[3] >= needed
        
        #  when isolated
        if state[5] != 1:
            #  we it can't charge and meet demand
            if state[3] - needed < state[4]:
                # print(f"outside sunlight in isolation t: {state[0]}")
                # print(f'{sunlight_hours}')
                # if isolated and not fully discharged 
                # we can discharge (0) or remain idle
                if SOC < Fx and SOC >= 0:
                    return [0, 2]
                # other wise the PV can't output with no sun so we can't charge
                # when fully discharged (SOC >= FX), thus we idle
                return [2]
            else:
                if SOC < Fx and SOC > 0:
                    if PVsufficient:
                        return [1, 2]
                    return [0, 1, 2]
                # if fully discharged 
                elif SOC == Fx:
                    if charge_possible:
                        return [1, 2]
                    # print("empty and idle")
                    return [2]
                # if fully charged 
                else:
                # elif SOC == 0:
                    if PVsufficient:
                        return [2]
                    return [0, 2]

        state = tuple(state)
        if SOC < Fx and SOC > 0:
            #  if connected or there is enough from PV to charge
            #  do what ever
            if state[5] == 1 or charge_possible:
            # if state[5] == 1 o:
                if PVsufficient and not buyBack:
                    return [1, 2]
                else:
                    return [0, 1, 2]
            else:
                return [0, 2]

        # if fully discharged 
        elif SOC == Fx:
            if state[5] == 1 or charge_possible:
                return [1, 2]
            # print("empty and idle")
            return [2]
        # if fully charged 
        elif SOC == 0:
            if PVsufficient and not buyBack:
                return [2,]
            return [0, 2]

def action_filterOMGA(state, F=4, 
                                sunlight_hours_dict=base_sunlight_hours, **kwargs):
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
        #        actions         D   C   I
        #                        0   1   2  Max hours
        # ESS directives values [1, -.c, 0, F]
        # G = 1 if connected to grid, 0 otherwise
        # State: 
        #   * 7 dimension:=[time, month_v, S, P, D, connection, weather_v]
        #   * 6 dimension:=[time, month_v, S, P, D,  connection]
        # look at the current SOC for the ESS and decide potential states
        
        month_v = state[1]
        if "needed" not in kwargs:
            print("no needed")
            needed = 0
        else:
            needed = kwargs["needed"]
        
        state = list(state)
        SOC = state[2]
        Fx = F
        sunrise = sunlight_hours_dict[month_v][0]
        sunset = sunlight_hours_dict[month_v][1]
        sunlight_hours = list(range(sunrise, sunset+1))
        # needed =  ((self.ess_cap*F/F)*self.ess_ceff)/1000
        #  Catch Isolated Grid condition
        # if state[5] != 1 and int(state[0]) not in sunlight_hours:
        charge_possible = state[3] >= needed
        if state[5] != 1:
            #  we it can't charge and meet demand
            if state[3] - needed < state[4]:
                # print(f"outside sunlight in isolation t: {state[0]}")
                # print(f'{sunlight_hours}')
                # if isolated and not fully discharged 
                # we can discharge (0) or remain idle
                if SOC < Fx and SOC >= 0:
                    return [0, 2]
                # other wise the PV can't output with no sun so we can't charge
                # when fully discharged (SOC >= FX), thus we idle
                return [2]
            else:
                if SOC < Fx and SOC >= 0:
                    return [0, 1, 2]
                # if fully discharged 
                elif SOC == Fx:
                    if charge_possible:
                        return [1, 2]
                    # print("empty and idle")
                    return [2]
                # if fully charged 
                else:
                # elif SOC == 0:
                    return [0, 2]

        state = tuple(state)
        if SOC < Fx and SOC > 0:
            #  if connected or there is enough from PV to charge
            #  do what ever
            if state[5] == 1 or charge_possible:
            # if state[5] == 1 o:
                return [0, 1, 2]
            else:
                return [0, 2]

        # if fully discharged 
        elif SOC == Fx:
            if state[5] == 1 or charge_possible:
                return [1, 2]
            # print("empty and idle")
            return [2]
        # if fully charged 
        elif SOC == 0:
            return [0, 2]

class Hippocampus:
    """Represents the memory of the agent(s) as the experience the environment"""
    def __init__(self, memory_size, end_sentinel="Done", sample_size=None, **kwargs):
        self.memory = dict({
            "states": list(),
            "actions": list(),
            "rewards": list(),
            "probs": list(),
            "vals": list(),
            "episode_ends": list()
        })
        if sample_size is not None and sample_size <= memory_size:
            self.sample_size = sample_size
        else:
            self.sample_size = int(memory_size/2)
        self.end_sentinel = end_sentinel
        self.memory_size = memory_size
    
    def observe(self, state, action, probs, val, reward, end, **kwargs):
        # print("action type: ", type(action))
        # print("probs type: ", type(probs))
        # print("vals type: ", type(val))
        self.memory['states'].append(state)
        self.memory["probs"].append(probs)
        self.memory["actions"].append(action)       
        self.memory["rewards"].append(reward)       
        self.memory["vals"].append(val)        
        self.memory["episode_ends"].append(end)
        
    def recallBatched(self, randomize=True):
    # def recallBatched(self, randomize=False):
        n_episodes = len(self.memory['states'])
        batch_indices = np.arange(0, n_episodes, self.sample_size)
        
        indices = np.arange(n_episodes, dtype=np.int64)
        
        # get a randomized sample if desired
        if randomize:
            np.random.shuffle(indices)
        # get batched samples from memory by getting a list of
        # indices each the size of a memory batch
        memories = [indices[i:i+self.sample_size] for i in batch_indices]
        return np.array(self.memory['states']),\
               np.array(self.memory["actions"]),\
               np.array(self.memory['rewards']),\
               np.array(self.memory['probs']),\
               np.array(self.memory["vals"]), np.array(self.memory['episode_ends']), memories    
       
    def clear_memory(self, ):
        self.forget()     
    
    def forget(self,):
        for it in self.memory:
            self.memory[it].clear()
            
            
            
            
class ActorNetwork(nn.Module):
    """The actor part of an actor critic network"""
    def __init__(self, state_shape, actions_shape, hidden_layers=[100, 100],
                 lr=.002, betas=(.9, .999), seed=0, dev=None):
        super(ActorNetwork, self).__init__()
        self.input_shape = state_shape
        self.output_shape=actions_shape
        self.hidden_layers = hidden_layers
        self.lr = lr
        self.betas = betas
        self.layers = None
        self.dev=dev
        self.generate_network()
        
    def generate_network(self, ):
        self.layers = nn.Sequential()
        
        self.layers.add_module("Linear_In", nn.Linear(self.input_shape, self.hidden_layers[0]))
        # add the activation for the just added layer
        self.layers.add_module("Act_In", nn.ReLU())
        for i in range(1, len(self.hidden_layers)):
            self.layers.add_module(
                f"Linear_{i}", nn.Linear(self.hidden_layers[i-1], self.hidden_layers[i]),
            )
            # add layers activation
            self.layers.add_module(
                f"Linear_{i}_Act", nn.ReLU(),
            )
            
        # now handle the output layer
        self.layers.add_module(
            "Actions_Out", nn.Linear(self.hidden_layers[-1], self.output_shape),
        )
        
        # add final activation, should log softmax
        self.layers.add_module(
            "Actions_Out_Act", nn.LogSoftmax(dim=0),
        )
        
        # set up optimizer
        self.optimizer = optim.Adam(self.parameters(), lr=self.lr, betas=self.betas)
        
        if self.dev is None:
            self.dev = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.dev)
        
    def forward(self, state):
        dist = self.layers(state)
        # dist = Categorical(dist)
        return dist
    
    
class CriticNetwork(ActorNetwork):
    def __init__(self, input_shape, output_shape=1, hidden_layers=[100, 100],
                 lr=.002, betas=(.9, .999), seed=0, dev=None):
        super().__init__(input_shape, output_shape, hidden_layers=hidden_layers,
                 lr=lr, betas=betas, seed=seed, dev=dev)
        
    def forward(self, state):
        value = self.layers(state)
        return value
    
  

class PPO_Agent:
    def __init__(self, 
              state_size, actions_size=3, actions=[0, 1, 2],
              actor_layers=[100, 100], critic_layers=[10, 10],
              actor_lr=.0002, actor_betas=(.9, .999), 
              critic_lr=.0002, critic_betas=(.9, .999), 
            #   learn_epochs = 150, 
            #   learn_epochs = 100, 
            #   learn_epochs = 100, 
            #   learn_epochs = 10, 
            #   learn_epochs = 50, 
            #   learn_epochs = 30, 
              learn_epochs = 20, 
              memory_size=30, 
              learn_interval = 15,
              storage_path="./", 
              load_model=False, 
              discount=.9, gae_lambda=.75, 
              sample_size=10,
              clip=.2,
              action_filter=action_filter, 
              **kwargs,
              ):
        self.memory = Hippocampus(memory_size=memory_size, sample_size=sample_size)
        self.discount = discount
        self.gamma = discount
        self.gae_lambda=gae_lambda
        self.clip=clip
        self.actions = actions
        self.n_epoch=learn_epochs
        self.learn_interval = learn_interval
        self.epoch = 0
        self.action_filter = action_filter
        self.actor_loss = list()
        self.critic_loss = list()
        if torch.cuda.is_available():
            self.dev = "cuda:0"
        else:
            self.dev = "cpu"
        self.name = "PPO_EMS"
        self.log_probs = list()
        self.V_pred = list()
        self.actor_layers = actor_layers
        self.critic_layers = critic_layers
        self.actor_hidden_layers =actor_layers
        self.actor_lr = actor_lr
        self.actor_betas = actor_betas
        
        self.critic_hidden_layers = critic_layers
        self.critic_lr = critic_lr
        self.critic_betas = critic_betas
        self.train_step = 0
        self.actor_loss = []
        self.critic_loss = []
        self.total_loss = []
        
        if load_model:
            print(f"Attempting to load model: {load_model}")
            # self.load_model(storage_path)
            self.load_model_checkpoint(storage_path)
        
        self.actor = ActorNetwork(state_shape=state_size, actions_shape=actions_size, 
                                  hidden_layers=self.actor_layers, lr=self.actor_lr, betas=self.actor_betas, dev=self.dev)
        self.critic = CriticNetwork(input_shape=state_size, hidden_layers=self.critic_hidden_layers, lr=critic_lr, 
                                    betas=critic_betas, dev=self.dev)  
        if load_model:
            self.load_networks()
    # def load_model(self, pth):
    #     self.load_model_checkpoint(pth)
    #     self.load_networks()
        
    
    def store_trained_model(self, actor_path, critic_path=None, epoch=None):
        print(f"Storing model to {actor_path}")
        torch.save(
            { 
            #  Actor Network
              "actor_network": self.actor.state_dict(),
              "actor_optimizer": self.actor.optimizer,
              "actor_optimizer_dict": self.actor.optimizer.state_dict(),
              "actor_loss": self.actor_loss,
              "actor_hidden_layers": self.actor_layers,
              "actor_lr": self.actor.lr,
              "actor_betas": self.actor.betas,
            
            #  Critic Network
              "critic_network": self.critic.state_dict(),
              "critic_optimizer": self.critic.optimizer,
              "critic_optimizer_dict": self.critic.optimizer.state_dict(),
              "critic_loss": self.critic_loss,
              "critic_hidden_layers": self.critic_layers,
              "critic_lr": self.critic.lr,
              "critic_betas": self.critic.betas,
            
              "gamma": self.gamma,
              "gae_lambda": self.gae_lambda,
            
            # Progress
              "train_step": self.epoch,
              "actor_loss": self.actor_loss,
              "critic_loss": self.critic_loss,
             }, actor_path)
        return

    
    def load_model_checkpoint(self, a2c_path):
        print(f"loading a2c from: {a2c_path}")
        self.check_point = torch.load(a2c_path)
        
        self.actor_hidden_layers = self.check_point["actor_hidden_layers"]
        self.actor_lr = self.check_point["actor_lr"]
        self.actor_betas = self.check_point["actor_betas"]
        
        self.critic_hidden_layers = self.check_point["critic_hidden_layers"]
        self.critic_lr = self.check_point["critic_lr"]
        self.critic_betas = self.check_point["critic_betas"]
        self.train_step = self.check_point["train_step"]
        self.actor_loss = self.check_point["actor_loss"]
        self.critic_loss = self.check_point["critic_loss"]   
        self.gamma = self.check_point["gamma"] 
        self.gae_lambda = self.check_point["gae_lambda"] 
    
    
    def load_networks(self, ):
        # ----------------- construct network --------------------
        if self.check_point is not None and "actor_network" in self.check_point and "critic_network" in self.check_point:
            self.actor.load_state_dict(self.check_point["actor_network"])
            self.critic.load_state_dict(self.check_point["critic_network"])
        
        
        if self.check_point is not None and "actor_optimizer_dict" in self.check_point and "critic_optimizer_dict" in self.check_point:
            print("Loading optimizers....")
            self.actor.optimizer.load_state_dict(self.check_point["actor_optimizer_dict"])
            print("actor done.")
            self.critic.optimizer.load_state_dict(self.check_point["critic_optimizer_dict"])
            print("critic done.")
    

    def learn(self, ):
        """
            train the network with the experiences in memory
        """
        # print("Epochs: ", self.n_epoch)
        for _ in range(self.n_epoch):
#             s, a, r, p, v, e, mem = Hippo.recallBatched()
            # Recall Batched Memories
            states, actions, rewards, probs, values, dones_arr, mem_batches = self.memory.recallBatched()
            # set up list of predicted advantages
            advantage = np.zeros(len(rewards), dtype=np.float32)
            # store calculated discounted advantage values
            for t in range(len(rewards)-1):
                discount = 1
                adv = 0
                for k in range(t, len(rewards)-1):
                    adv += discount*(rewards[k] + self.gamma*values[k+1] - values[k])
                    discount *= self.gamma*self.gae_lambda
                advantage[t] = adv

            advantage = T.tensor(advantage).to(self.dev)
            values = T.tensor(values).to(self.dev)  # predicted values
            # print(f"size of mem batches: {len(mem_batches)}")
            for memory in mem_batches:
                stateB = T.tensor(states[memory], dtype=T.float).to(self.dev)
                # print(f"len of stateB: {len(stateB)}")
                actionB = T.tensor(actions[memory], dtype=T.float).to(self.dev)
                old_probsB = T.tensor(probs[memory], dtype=T.float).to(self.dev)

                dist = self.actor(stateB)
                dist = Categorical(dist)
                critic_value = self.critic(stateB)
                critic_value = T.squeeze(critic_value)
                new_probs = dist.log_prob(actionB)
                ratio = new_probs.exp()/old_probsB.exp()
                weighted_probs = advantage[memory]*ratio
                weighted_clipped_probs = T.clamp(ratio, 1-self.clip, 1+self.clip) * advantage[memory]
                actor_loss = -T.min(weighted_probs, weighted_clipped_probs).mean()

                returnss = advantage[memory] + values[memory]

                critic_loss = (returnss-critic_value)**2
                critic_loss = critic_loss.mean()

                total_loss = actor_loss + .5*critic_loss
                
                self.actor.optimizer.zero_grad()
                self.critic.optimizer.zero_grad()

                total_loss.backward()
                self.actor.optimizer.step()
                self.critic.optimizer.step()
                # print("appending")
                self.actor_loss.append(actor_loss.to('cpu').detach().numpy())
                self.critic_loss.append(critic_loss.to('cpu').detach().numpy())
                self.total_loss.append(total_loss.to("cpu").detach().numpy())
        # if len(self.memory.memory["states"]) >= self.memory.memory_size:
        self.memory.clear_memory()  
        return
            
            
    # get the action for this state
    def get_stateValueActionProbs(self, state, **kwargs):
        # make state to tensor
        input_seq = torch.FloatTensor(state).to(self.dev)
        
        # make a prediction, with grad
        policy_dist = self.actor(input_seq)
        
        value = self.critic(input_seq)
        
        dist = policy_dist.to('cpu').detach().numpy()
        
        # valid_actions
        if self.action_filter is not None:
            valid_actions = self.action_filter(state, **kwargs)
        else: 
            valid_actions = self.actions
        # choose action
        action_pr = np.array([
            np.exp(dist[i]) if self.actions[i] in valid_actions
            else 0 for i in range(len(self.actions))
        ])
        
        
        if np.sum(action_pr) == 0:
            action_pr = np.array([
                1 if self.actions[i] in valid_actions
                else 0 for i in range(len(self.actions))
            ])
        action_pr = action_pr / np.sum(action_pr)
        action_ind = np.random.choice(
            range(len(self.actions)), 1, False, action_pr
        )[0]
        
        # log prob
        log_prob = policy_dist.squeeze(0)[action_ind]
        
        # entropy
#         self.entropy += -1 * np.sum(np.mean(np.exp(dist)) * dist)
        # return
        return value,  log_prob
    
    def observeTakeAction(self, state, **kwargs):
        return self.take_action(state, **kwargs)
    
    # get the action for this state
    def take_action(self, state, **kwargs):
        # make state to tensor
        input_seq = torch.FloatTensor(state).to(self.dev)
        
        # make a prediction, with grad
        policy_dist = self.actor(input_seq)
        dist = policy_dist.to('cpu').detach().numpy()
        policy_dist = Categorical(policy_dist)
        value = self.critic(input_seq)
        
        # value, distribution
        self.V_pred.append(value)
        
        
        
        
        # valid_actions
        if self.action_filter is not None:
            valid_actions = self.action_filter(state, **kwargs)
        else: 
            valid_actions = self.actions
        # choose action
        # if action not valid set probablity to zero
        action_pr = np.array([
            np.exp(dist[i]) if self.actions[i] in valid_actions
            else 0 for i in range(len(self.actions))
        ])
        
        # if none chosen set equal prob for either
        if np.sum(action_pr) == 0:
            action_pr = np.array([
                1 if self.actions[i] in valid_actions
                else 0 for i in range(len(self.actions))
            ])
        # make sure it looks like a prob (i.e. sums to 1)
        action_pr = action_pr / np.sum(action_pr)
        
        # randomly choose index
        action_ind = np.random.choice(
            range(len(self.actions)), 1, False, action_pr
        )[0]
        
        # log prob
        # self.log_probs.append(policy_dist.squeeze(0)[action_ind])
        action = self.actions[action_ind]
        nact = T.tensor(action, dtype=T.int).to(self.dev)
        # print("tth: ", policy_dist.log_prob(nact))
        self.log_probs.append(T.squeeze(policy_dist.log_prob(nact)).item())
        # entropy
        # self.entropy += -1 * np.sum(np.mean(np.exp(dist)) * dist)
        # return
        
        # print(f"action: {action}")
        return action
    
    def observe(self, state, action, probs, val, reward, end=False, **kwargs):
        self.memory.observe(state, action, probs, val, reward, end)
        # print(f"stored memories: {len(self.memory.memory['states'])}")
    
    def memorize(self, state, action, nstate, R, G, epoch):
        # print(f"Month: {epoch}")
        # print(f"self.epoch: {self.epoch}")
        # print("interval: ", self.learn_interval)
        # print(self.log_probs[-1].detach().numpy())
        # print(f"interval: {self.learn_interval}")
        # self.observe(state, action, self.log_probs[-1].detach().numpy(), self.V_pred[-1].detach().numpy(), R, self.epoch)
        # self.observe(state, action, self.log_probs[-1], self.V_pred[-1].detach().numpy(), R, self.epoch)
        # self.epoch = epoch
        # if self.epoch%self.learn_interval == 0 and self.epoch != 0:
        mem_len = len(self.memory.memory["states"])
        if mem_len%self.learn_interval == 0 and mem_len != 0:
            print("\n\nlearning...")
            print(f"self.epoch: {self.epoch}")
            print(f"stored memories: {len(self.memory.memory['states'])}")
            print("interval: ", self.learn_interval, "\n\n")
            self.learn()
            self.log_probs.clear()
            self.V_pred.clear()
        else:
            # print(self.log_probs[-1].detach().numpy())
            # print(f"interval: {self.learn_interval}")
            # self.observe(state, action, self.log_probs[-1].detach().numpy(), self.V_pred[-1].detach().numpy(), R, self.epoch)
            self.observe(state, action, self.log_probs[-1], self.V_pred[-1].detach().numpy(), R, self.epoch)
            
        self.epoch += 1 
        return 
    
    def simulate_action(self, state, max_charge=4, **kwargs):
        """
        take action (for simulation), based on the input state.
        """
        # make state to tensor
        # state = np.array(state)
        input_seq = torch.FloatTensor(list(state)).to(self.dev)
        # make a prediction, without grad
        self.actor.eval()
        with torch.no_grad():
            dist = self.actor(input_seq).to('cpu').numpy()
        self.actor.train()
        
        # valid_actions
        valid_actions = self.action_filter(state, **kwargs)
        
        # choose action
        action_pr = np.array([
            np.exp(dist[i]) if self.actions[i] in valid_actions
            else 0 for i in range(len(self.actions))
        ])
        if np.sum(action_pr) == 0:
            action_pr = np.array([
                1 if self.actions[i] in valid_actions
                else 0 for i in range(len(self.actions))
            ])
        action_pr = action_pr / np.sum(action_pr)
        action_ind = np.argmax(action_pr)
        return self.actions[action_ind]
    
    def plot_loss(self, window=20, start_ind=0, 
                  sample=1, dir='', 
                  titles=['Actor Loss','Critic Loss', "Total_loss" ], colors=['b-', 'r-', 'g-'],
                  TFD={}, close_me=False, fileName=None):
        """
        plot train loss for agent
        dir: 'directory/'
        """
        savename = self.name
        print(f"len actorloss: {len(self.actor_loss)}, len criticloss: {len(self.critic_loss)}")
        self.total_loss = np.array(self.total_loss).flatten().tolist()
        print(f"total loss samples: {len(self.total_loss)}")
        if fileName is not None:
            savename = fileName
        
        for nn in range(3):
            if nn == 0:
                loss_memory = self.actor_loss
                savenamefull = savename + "_Actor"
            elif nn == 1:
                loss_memory = self.critic_loss
                savenamefull = savename + "_Critic"
            else:
                loss_memory = self.total_loss
                savenamefull = savename + "_Total"
            # savenamefull = savename + "_Actor" if nn == 0 else savename + "_Critic"
            loss_plot = {}
            ind = window
            while ind <= len(loss_memory):
                # sample
                if ind % sample == 0:
                    loss_plot[ind - 1] = np.mean([
                        loss_memory[i] for i in range(ind - window, ind, 1)
                    ])
                ind += 1
            # plot
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
            ax.plot(
                list(loss_plot.keys())[start_ind:],
                list(loss_plot.values())[start_ind:],
                colors[nn],  label=titles[nn], 
            )
            ax.set_xlabel('Epochs')
            ax.set_ylabel('Loss')
            ax.set_title(titles[nn], fontdict=TFD) 
            
            fig.tight_layout()
        
            plt.legend()    
            fig.savefig(f'{dir}{savenamefull}_loss.png', dpi=600)
        return            
            
      
class A2C_Agent(PPO_Agent):
    def __init__(self, state_size, 
                 actions_size=3, 
                 actions=[0, 1, 2], 
                 actor_layers=[100, 100], 
                 critic_layers=[10, 10], 
                 actor_lr=0.0002, actor_betas=(0.9, 0.999), 
                 critic_lr=0.0002, critic_betas=(0.9, 0.999), 
                 learn_epochs=50, 
                 memory_size=30, learn_interval=15, 
                 storage_path="./", 
                 load_model=False, discount=0.9, gae_lambda=0.75, sample_size=10, clip=0.2, action_filter=action_filter, **kwargs):
        super().__init__(state_size, actions_size, actions, actor_layers, critic_layers, actor_lr, actor_betas, critic_lr, critic_betas, learn_epochs, memory_size, learn_interval, storage_path, load_model, discount, gae_lambda, sample_size, clip, action_filter, **kwargs)      
            
            
            
            
            
            
            
            
            