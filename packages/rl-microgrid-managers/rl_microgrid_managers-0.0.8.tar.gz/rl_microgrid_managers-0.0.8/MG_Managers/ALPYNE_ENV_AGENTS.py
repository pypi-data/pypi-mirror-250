from logging import DEBUG
import torch
import logging
# from alpyne.client import alpyne_client
# from alpyne.client.alpyne_client import AlpyneClient
# from alpyne.client.utils import histogram_outputs_to_fake_dataset, limit
# from alpyne.data.constants import RunStatus
# from alpyne.data.spaces import Number, Observation

# from .Memories import *

import numpy as np
import matplotlib.pyplot as plt

from .ESM_AGENTS import DQ_EMS, A2C_EMS

TERMINAL_STATE="Delta"
class AlPyESM:
    action_dict = {0:"discharge", 1:"charge", 2:"idle"}
    action_d = {0:"D", 1:"C", 2:"I"}
    weather_dict = {1:"sunny", 2:"cloudy", 3:"overcast"}
    weather_d = {1:"s", 2:"c", 3:"o"}
    
    
    def __init__(self, 
                 manager,
                 al_model_path, 
                 days=30,
                 seed=13,
                 method='DQ',
                 memory_size=30,
                 sample_episodes=21,
                 DG_Table="dg_toy", NODE_Table="demand_nodes5",
                 port=51550,
                 **kwargs):
        self.agent=manager
        self.model = self.load_model(al_model_path, port=port)       # load connection to anylogic model
        print(f"Model loaded from: {al_model_path}")
        self.config = self.model.create_default_rl_inputs # get reference to model configs
        self.config.UseAgent=True
        self.DG_Table=DG_Table
        self.NODE_Table=NODE_Table
        self.config.DG_TABLE=DG_Table
        self.config.NODE_TABLE=NODE_Table
        self.action_temp = self.model.action_template
        self.seed=seed
        self.port=port
        self.TotalDays=days
        self.method=method
        self.config.engine_seed = self.seed
        self.memory_size=memory_size
        self.sample_episodes = sample_episodes
        self.max_charge = 4
        self.kpis = {
            "pv_out":[],
            "ess_out":[],
            "demand":[],
            "supply":[],
            "time":[],
            "weather":[],
            "costs": [],
            }
        
        # get instance of microgram simulation 
        self.microgrid = self.model.create_reinforcement_learning(self.config).run()
        self.memory = Memory(
            memory_size=self.memory_size,
            sample_episodes=self.sample_episodes
        )
        
    
    def init_grid(self,):
        self.config.UseAgent=True
        self.config.DG_TABLE=self.DG_Table
        self.config.NODE_TABLE=self.NODE_Table
        self.kpis = {
            "pv_out":[],
            "ess_out":[],
            "demand":[],
            "supply":[],
            "time":[],
            "weather":[],
            }
        self.model = self.load_model()
    
        
    def load_model(self, al_model_path, blocking=True, verbose=True, port=51550):
        # return AlpyneClient(r"Exported\StockManagementGame\model.jar", blocking=True, verbose=True)
        print("Loading Model...")
        # return AlpyneClient(al_model_path, blocking=blocking, verbose=verbose, port=port)
    
    def display_configs(self,):
        print(self.model.configuration_template)
        print(self.model.observation_template)
        print(self.model.action_template)
        print(self.model.output_name)
        
    def simulate(self, T):
        
        
        # get state, store state, 
        status, info = self.microgrid.last_state
        observation = self.microgrid.get_observation()
            
        state = np.array([
            observation.time,
            observation.skyCondition,
            observation.SOC,
            observation.PVout,
            observation.Demand,
        ])
        
        
        # iterate through T time steps using 
        # the AL to get PV/ESS outputs, Demands each time 
        # step using the given network to provide
        # the policy
        while not self.microgrid.is_terminal():
            
            
            # get action and perform it
            action_v = action = self.agent.simulate_action(state)
            self.action_temp.action = action_v
            self.microgrid.take_action(action=self.action_temp)
            
            # get state, store state, 
            status, info = self.microgrid.last_state
            observation = self.microgrid.get_observation()
                
            self.kpis['pv_out'].append(observation.PVout)
            self.kpis['ess_out'].append(observation.ESSout)
            self.kpis['demand'].append(observation.Demand)
            self.kpis['supply'].append(observation.Supply)
            self.kpis['time'].append(observation.time) 
            self.kpis['weather'].append(observation.skyCondition)
            self.kpis['costs'].append(observation.hourlyCosts)
            self.kpis['action'].append(observation.hourlyCosts)
            
            state = np.array([
                observation.time,
                observation.skyCondition,
                observation.SOC,
                observation.PVout,
                observation.Demand,
            ])
    
    
    def plot_simulation(self, title="MG Simulation", 
                        xlabel="time/Action", xlablfd={}, xtickfd={},
                        ylabel="Power", ylablfd={}, ytickfd={},
                        colors=['red', 'blue', 'green'], 
                        ax=None, figsize=(20, 20),
                        **kwargs):
        
        if ax is None:
            f, ax = plt.subplots(2, figsize=figsize)
        weathers = self.kpis['weather']
        time = self.kpis['time']
        costs = self.kpis['costs']
        pvOut = self.kpis['pv_out']
        essOut = self.kpis['ess_out']
        demand = self.kpis['demand']
        supply = self.kpis['supply']
        xticks = [f"{t}\n{w}" for t,w in zip(time, weathers)]
        
        # without policy
        ax[0].bar(time, weathers, )
            
 
 
class AlPyESM_SIM:
    action_dict = {0:"discharge", 1:"charge", 2:"idle"}
    action_d = {0:"D", 1:"C", 2:"I"}
    weather_dict = {1:"sunny", 2:"cloudy", 3:"overcast"}
    weather_d = {1:"s", 2:"c", 3:"o"}
    
    
    def __init__(self, 
                 manager,
                 memory_size=30,
                 sample_episodes=21,
                 max_charge=4,
                learn_step=10, discount_factor=.6, inter=.001, 
                update_target_interval=10,
                write_log=False,
                network_path1=None,
                network_path2=None,
                # write_log=True,
                 **kwargs):
        self.agent=manager
        
        self.memory_size=memory_size
        self.sample_episodes = sample_episodes
        self.max_charge = max_charge
        self.learn_ind = 0
        self.learn_step = learn_step
        self.discount_factor=discount_factor
        self.inter=inter
        self.write_log=write_log
        self.update_target_interval=update_target_interval
        self.kpis = {
            "pv_out":[],
            "ess_out":[],
            "demand":[],
            "supply":[],
            "time":[],
            "weather":[],
            "costs": [],
            }
        self.Gs=[]
        self.G=0
        self.first_run=True
        # get instance of microgram simulation 
        
        self.memory = Memory(
            memory_size=self.memory_size,
            sample_episodes=self.sample_episodes
        )

    def reinitialize(self,):
        self.learn_ind = 0
        self.Gs.append(self.G)
        self.G=0
        self.kpis = {
            "pv_out":[],
            "ess_out":[],
            "demand":[],
            "supply":[],
            "time":[],
            "weather":[],
            "costs": [],
            }
 
 
    def observeTakeAction(self, state, **kwargs):
        action = self.agent.take_action(state, **kwargs)
        return action
    
    def simulate_action(self, state, **kwargs):
        # print(f"kwargs: {kwargs}")
        action = self.agent.simulate_action(state, **kwargs)
        return action
    
    
    def update_kpis(self, p, e, d, s, t, w, c):
        self.kpis["pv_out"].append(p)
        self.kpis["ess_out"].append(e)
        self.kpis["demand"].append(d)
        self.kpis["supply"].append(s)
        self.kpis["time"].append(t)
        self.kpis["weather"].append(w)
        self.kpis["costs"].append(c)
        
    
    def memorize(self, state, action, new_state, R, G, epoch,):
                #  learn_ind, learn_step, discount_factor, inter, update_target_interval):
        if self.write_log:
                # logging state, action and reward
                logging.info('    epoch: {}'.format(epoch))
                logging.info('    state: {}'.format(state))
                logging.info('    action: {}'.format(action))
                logging.info('    reward: {}'.format(R))
        
        delta=False
        # if days == self.TotalDays:
        #     new_state = TERMINAL_STATE
        #     delta=True    
        # ---------------- memory control --------------------
        # store that step of the episode
        self.memory.update(
            state, delta, action, R,
            state if new_state == TERMINAL_STATE else new_state
        )
        
        self.timeToLearn()
        # if self.learn_ind % self.learn_step == 0:
        #     # print("learning....2")
        #     self.agent.learn(
        #             memory=self.memory.sample(),
        #             discount_factor=self.discount_factor,
        #             inter=self.inter,
        #             update_target_interval=self.update_target_interval,
        #     )
        # self.learn_ind += 1
        # agent record G
        self.agent.G_memory.append(G)
        
        
    def timeToLearn(self,):
        # print(f'learn index: {self.learn_ind}, learn step: {self.learn_step}')
        if self.learn_ind % self.learn_step == 0:
            # print(f"learning...., learn_indx: {self.learn_ind}")
            self.agent.learn(
                    memory=self.memory.sample(),
                    discount_factor=self.discount_factor,
                    inter=self.inter,
                    update_target_interval=self.update_target_interval,
            )
        self.learn_ind += 1
        return
      
            
    def simulate(self, T):
        
        
        # # get state, store state, 
        # status, info = self.microgrid.last_state
        # observation = self.microgrid.get_observation()
            
        state = np.array([
            observation.time,
            observation.skyCondition,
            observation.SOC,
            observation.PVout,
            observation.Demand,
        ])
        
        
        # iterate through T time steps using 
        # the AL to get PV/ESS outputs, Demands each time 
        # step using the given network to provide
        # the policy
        while not self.microgrid.is_terminal():
            
            
            # get action and perform it
            action_v = self.agent.simulate_action(state)
            self.action_temp.action = action_v
            self.microgrid.take_action(action=self.action_temp)
            
            # get state, store state, 
            status, info = self.microgrid.last_state
            observation = self.microgrid.get_observation()
                
            self.kpis['pv_out'].append(observation.PVout)
            self.kpis['ess_out'].append(observation.ESSout)
            self.kpis['demand'].append(observation.Demand)
            self.kpis['supply'].append(observation.Supply)
            self.kpis['time'].append(observation.time) 
            self.kpis['weather'].append(observation.skyCondition)
            self.kpis['costs'].append(observation.hourlyCosts)
            self.kpis['action'].append(observation.hourlyCosts)
            
            state = np.array([
                observation.time,
                observation.skyCondition,
                observation.SOC,
                observation.PVout,
                observation.Demand,
            ])
    
    
    def plot_simulation(self, title="MG Simulation", 
                        xlabel="time/Action", xlablfd={}, xtickfd={},
                        ylabel="Power", ylablfd={}, ytickfd={},
                        colors=['red', 'blue', 'green'], 
                        ax=None, figsize=(20, 20),
                        **kwargs):
        
        if ax is None:
            f, ax = plt.subplots(2, figsize=figsize)
        weathers = self.kpis['weather']
        time = self.kpis['time']
        costs = self.kpis['costs']
        pvOut = self.kpis['pv_out']
        essOut = self.kpis['ess_out']
        demand = self.kpis['demand']
        supply = self.kpis['supply']
        xticks = [f"{t}\n{w}" for t,w in zip(time, weathers)]
        
        # without policy
        ax[0].bar(time, weathers, )
 


 
class AlPyESM_DQ_SIM(AlPyESM_SIM):
    def __init__(self, manager, memory_size=30, sample_episodes=21, max_charge=4,
                 learn_step=10, discount_factor=.6, inter=.001, 
                 update_target_interval=10,
                 write_log=False,
                 **kwargs):
        super().__init__( manager,
                         memory_size=memory_size,
                         sample_episodes=sample_episodes,
                         max_charge=max_charge,
                         learn_step=learn_step, discount_factor=discount_factor, inter=inter, 
                         update_target_interval=update_target_interval,
                         write_log=write_log, 
                         **kwargs)
    
    def __Q_update(self, discount_factor, 
                   learn_step, write_log, inter=.001, 
                   update_target_interval=1):
        
        G = 0
        epoch, learn_ind = 1, 0
        delta = False
        status, info = self.microgrid.last_state
        observation = self.microgrid.get_observation()
            
        state = [
            observation.time,
            observation.skyCondition,
            observation.SOC,
            observation.PVout,
            observation.Demand,
        ]
        while not self.microgrid.is_terminal():
             
            # Take action based on seen state
            action_v = self.agent.take_action(state, max_charge=self.max_charge)
            self.action_temp.action = action_v
            self.microgrid.take_action(action=self.action_temp)
            
            status, info = self.microgrid.last_state
            observation = self.microgrid.get_observation()
            new_state = [
                observation.time,
                observation.skyCondition,
                observation.SOC,
                observation.PVout,
                observation.Demand,
            ]
            
            # get reward for action
            R = observation.hourlyCosts
            days = observation.Days
            G += R
            if write_log:
                # logging state, action and reward
                logging.info('    epoch: {}'.format(epoch))
                logging.info('    state: {}'.format(state))
                logging.info('    action: {}'.format(action_v))
                logging.info('    reward: {}'.format(R))
            
            if days == self.TotalDays:
                new_state = "Delta"
            
            # ---------------- memory control --------------------
            # store that step of the episode
            self.memory.update(
                state, delta, action_v, R,
                state if new_state == "omega" else new_state
            )
            
            
            # ---------------- Learning --------------------
            # at preset interval
            # for each agent, provide data and train.
            # train and update Q and targets 
            if learn_ind % learn_step == 0:
                self.agent.learn(
                    memory=self.memory.sample(),
                    discount_factor=discount_factor,
                    inter=inter,
                    update_target_interval=update_target_interval,
                )
            
            if new_state == "omega":
                break
            epoch += 1
            learn_ind += 1
            state = new_state
        
        # agent record G
        self.agent.G_memory.append(G)
        
        return G
    
    
    def process_episode(self, step_G, eps_init, eps_end, episodes):
        self.Gs.append(step_G)
        # log return
        if self.write_log:
            logging.info("    return: {}".format(step_G))
        
        self.epsilon_update_base(eps_init, eps_end, episodes)
        if self.write_log:
            logging.info("    -----------------------")

    def deep_Q_Network(
        self, episodes, discount_factor, learn_step,
        eps_init, eps_end, write_log, report_iter=100,
        inter=.001, update_target_interval=1, use_weather=None,
    ):
        """
        Deep Q-Network.
        - episodes: how many iterations to simulation in total.
        - alpha: learning rate;
        - discount factor: perspective of future.
        - learn_step: int, 
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
                discount_factor, learn_step, write_log, inter=inter,
                update_target_interval=update_target_interval, 
            )
            # -------------- step control ---------------
            # record return
            G.append(step_G)
            # log return
            if write_log:
                logging.info("    return: {}".format(step_G))
            
            self.epsilon_update_base(eps_init, eps_end, episodes)
            if write_log:
                logging.info("    -----------------------")
        return G  
    
    
    def epsilon_update_base(self, eps_init, eps_end, episodes):
            # set epsilon, 7-2.5, 10-5
            self.agent.epsilon = (eps_init - eps_end) * np.max([
                (episodes * 1 - iter) / (episodes * 1), 0
            ]) + eps_end
            return 
        
    def store_trained_model(self, pathQ="DQ_network.pt", pathQ_target="DQ_target.pt", **kwargs):
        # # store the models param dict
        # print(f"Storing DQ models at {pathQ} and {pathQ_target}")
        # torch.save(self.agent.Q.state_dict(), pathQ) 
        # torch.save(self.agent.Q_target.state_dict(), pathQ_target)
        self.agent.store_trained_model(pathQ, pathQ_target)
        return 
    
    def load_trained_model(self, pathQ="DQ_network.pt", pathQ_target="DQ_target.pt", 
                           training=True, **kwargs):
        # load the trained model params
        # self.agent.Q.load_state_dict(torch.load(pathQ))
        # self.agent.Q.eval()
        # self.agent.Q_target.load_state_dict(torch.load(pathQ_target))
        # self.agent.Q_target.eval()
        print("DO NOT SEE ME")
        self.agent.load_trained_model(pathQ, pathQ_target, training)
        return       

    def simulate_action22(self, state, **kwargs):
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

   
   
    
class AlPyESM_A2C_SIM(AlPyESM_SIM):
    def __init__(self, manager, memory_size=30, sample_episodes=21, max_charge=4,
                 learn_step=10, discount_factor=.6, inter=.001, 
                 update_target_interval=10,
                 write_log=False,
                 **kwargs):
        super().__init__(manager, 
                         memory_size, sample_episodes, 
                         max_charge=max_charge,
                         learn_step=learn_step, discount_factor=discount_factor, inter=inter, 
                         update_target_interval=update_target_interval,
                         write_log=write_log,  
                         **kwargs)
        self.G = 0
        self.epoch, self.V_future = 0, 0
        self.Gs = list()
        
        
    def __A2C_update(self, discount_factor, write_log, learn_step,
                     
                     use_weather=False):
        """
        one episode of A2C
        """
        self.G = 0
        self.epoch, self.V_future = 0, 0
        delta = False
        status, info = self.microgrid.last_state
        observation = self.microgrid.get_observation()
        print(f"status: {status}, info: {info}")
        state = np.array([
            observation.time,
            observation.skyCondition,
            observation.SOC,
            observation.PVout,
            observation.Demand,
        ])
        print(f"init: {state}")
        i = 0
        while not self.microgrid.is_terminal():
            
           # Take action based on seen state
            action_v = self.agent.take_action(state, max_charge=self.max_charge)
            self.action_temp.action = action_v
            self.microgrid.take_action(action=self.action_temp)
            
            status, info = self.microgrid.last_state
            observation = self.microgrid.get_observation()
            new_state = np.array([
                observation.time,
                observation.skyCondition,
                observation.SOC,
                observation.PVout,
                observation.Demand,
            ])
            
            # get reward for action
            R = observation.hourlyCosts
            days = observation.Days
            G += R
            
            if i%20 == 0:
                print(f"step: {i}, reward: {R}, days: {days}, state: {state} ")
            i += 1
            if write_log:
                # logging state, action and reward
                logging.info('    epoch: {}'.format(epoch))
                logging.info('    state: {}'.format(state))
                logging.info('    action: {}'.format(action_v))
                logging.info('    reward: {}'.format(R))
            # on step, transit to new state
            state = new_state
            epoch += 1
            if epoch >= learn_step:
                V_future = self.agent.critic(list(state.values))
                V_future = self.V_future.to('cpu').detach().numpy()[0]
                break
        
        
        # agent record G
        if V_future == 0:
            self.agent.G_memory.append(G)
        # ================ Learning =================
        self.agent.learn(
            V_future=V_future,
            discount_factor=discount_factor,
        )
        return G

    def advantage_actor_acritic(
        self, episodes, discount_factor=1, write_log=False,
        learn_step=100,
        report_interval=100,
    ):
        """
        Deep Q learning.
        - episodes: how many iterations to simulation in total.
        - alpha: learning rate;
        - discount factor: perspective of future.
        """
        G = []
        # ---------------------- Learning ----------------------
        if write_log:
            logging.info("Learning...")
        for iter in range(episodes):
            if iter % report_interval == 0:
                print("Iteration {}".format(iter))
            # if True:
            if write_log:
                logging.info("Iteration {}".format(iter))
            # run one update
            # try:
            step_G = self.__A2C_update(discount_factor, write_log, learn_step)
            # ---------------- step control --------------------
            # record return
            G.append(step_G)
            # log return
            if write_log:
                logging.info("    return: {}".format(step_G))
                logging.info("    -----------------------")
        return G    
           
    def memorize(self, state, action, new_state, R, G, epoch,):
                #  learn_ind, learn_step, discount_factor, inter, update_target_interval):
        if self.write_log:
                # logging state, action and reward
                logging.info('    epoch: {}'.format(epoch))
                logging.info('    state: {}'.format(state))
                logging.info('    action: {}'.format(action))
                logging.info('    reward: {}'.format(R))
        
        delta=False
        # if days == self.TotalDays:
        #     new_state = TERMINAL_STATE
        #     delta=True    
        # ---------------- memory control --------------------
        # store that step of the episode
        self.memory.update(
            state, delta, action, R,
            state if new_state == TERMINAL_STATE else new_state
        )
        
        
        # check for learning time
        self.timeToLearn()
       # remember the reward for this one
        self.agent.reward_memory.append(R) 
        # agent record G
        self.agent.G_memory.append(G)
        self.G = G
        self.state=state
    
    # used to have the networks learn
    def timeToLearn(self,):
        
        if self.epoch >= self.learn_step:
            print("learning...")
            print(f"learn step: {self.learn_step}, epoch: {self.epoch}")
            self.state = np.array(self.state)
            state = torch.FloatTensor(self.state).to(self.agent.dev)
            # print(f"state: {state}")
            
            self.V_future = self.agent.critic(state)
            self.V_future = self.V_future.to('cpu').detach().numpy()[0]
        
            # agent record G
            # if self.V_future == 0:
            # self.agent.G_memory.append(self.G)
            # print("Off to agent learn")
            # ================ Learning =================
            self.agent.learn(
                V_future=self.V_future,
                discount_factor=self.discount_factor,
                epochs=1,
            )
            self.record_episode(self.G)
            self.G = 0
            self.epoch, self.V_future = 0, 0
            self.agent.reward_memory=[]
        else:
            self.epoch += 1
        return
 
    def record_episode(self, step_G):
        self.Gs.append(step_G)
        # log return
        if self.write_log:
            logging.info("    return: {}".format(step_G))
            logging.info("    -----------------------")

    # https://pytorch.org/tutorials/beginner/saving_loading_models.html
    def store_trained_model(self, pathActor="Actor_network.pt", **kwargs):
        # store the models param dict
        # torch.save(self.agent.actor.state_dict(), pathActor) 
        # torch.save(self.agent.critic.state_dict(), pathCritic)
        self.agent.store_trained_model(pathActor)
        return 
    
    
    # https://pytorch.org/tutorials/beginner/saving_loading_models.html
    def load_trained_model(self, pathActor="Actor_network.pt", pathCritic="Critic_network.pt", **kwargs):
        print("Here?")
        self.agent.load_model_checkpoint(self, pathActor)
        # load the trained model params
        # self.agent.actor.load_state_dict(torch.load(pathActor))
        # self.agent.actor.eval()
        # self.agent.critic.load_state_dict(torch.load(pathCritic)) 
        # self.agent.critic.eval()
        return
 
    
        
class AlPyESM_PPO_SIM(AlPyESM_A2C_SIM):
    def __init__(self, manager, 
                 memory_size=30, sample_episodes=21, 
                 max_charge=4, learn_step=10, discount_factor=0.6, 
                 inter=0.001, update_target_interval=10, write_log=False, **kwargs):
        super().__init__(manager, memory_size, sample_episodes, 
                         max_charge, learn_step, discount_factor, 
                         inter, update_target_interval, 
                         write_log, **kwargs)
 
 
    # used to have the networks learn
    def timeToLearn(self,):
        if self.epoch >= self.learn_step:
            # print("learning...")
            # print(f"learn step: {self.learn_step}, epoch: {self.epoch}")
            self.state = np.array(self.state)
            state = torch.FloatTensor(self.state).to(self.agent.dev)
            # print(f"state: {state}")
            self.V_future = self.agent.critic(state)
            self.V_future = self.V_future.to('cpu').detach().numpy()[0]
        
            # agent record G
            # if self.V_future == 0:
            # self.agent.G_memory.append(self.G)
            # print("Off to agent learn")
            # ================ Learning =================
            self.agent.learn(
                memory=self.memory.sample(),
                V_future=self.V_future,
                discount_factor=self.discount_factor
            )
            self.record_episode(self.G)
            self.G = 0
            self.epoch, self.V_future = 0, 0
            self.agent.reward_memory=[]
        else:
            self.epoch += 1
        return 
 
 
 
        
class AlPyESM_DQ(AlPyESM):
    def __init__(self, manager, al_model_path, days=7, seed=13, 
                 method='DQ', memory_size=30, sample_episodes=21, 
                 DG_Table="dg_toy", NODE_Table="demand_nodes5",
                 port=51550,
                 **kwargs):
        super().__init__(manager, al_model_path, days, seed, method, memory_size, 
                         sample_episodes, 
                         DG_Table, NODE_Table, 
                         port,
                         **kwargs)
    
    def __Q_update(self, discount_factor, 
                   learn_step, write_log, inter=.001, 
                   update_target_interval=1):
        
        G = 0
        epoch, learn_ind = 1, 0
        delta = False
        status, info = self.microgrid.last_state
        observation = self.microgrid.get_observation()
            
        state = [
            observation.time,
            observation.skyCondition,
            observation.SOC,
            observation.PVout,
            observation.Demand,
        ]
        while not self.microgrid.is_terminal():
             
            # Take action based on seen state
            action_v = self.agent.take_action(state, max_charge=self.max_charge)
            self.action_temp.action = action_v
            self.microgrid.take_action(action=self.action_temp)
            
            status, info = self.microgrid.last_state
            observation = self.microgrid.get_observation()
            new_state = [
                observation.time,
                observation.skyCondition,
                observation.SOC,
                observation.PVout,
                observation.Demand,
            ]
            
            # get reward for action
            R = observation.hourlyCosts
            days = observation.Days
            G += R
            if write_log:
                # logging state, action and reward
                logging.info('    epoch: {}'.format(epoch))
                logging.info('    state: {}'.format(state))
                logging.info('    action: {}'.format(action_v))
                logging.info('    reward: {}'.format(R))
            
            if days == self.TotalDays:
                new_state = "Delta"
            
            # ---------------- memory control --------------------
            # store that step of the episode
            self.memory.update(
                state, delta, action_v, R,
                state if new_state == "omega" else new_state
            )
            
            
            # ---------------- Learning --------------------
            # at preset interval
            # for each agent, provide data and train.
            # train and update Q and targets 
            if learn_ind % learn_step == 0:
                self.agent.learn(
                    memory=self.memory.sample(),
                    discount_factor=discount_factor,
                    inter=inter,
                    update_target_interval=update_target_interval,
                )
            
            if new_state == "omega":
                break
            epoch += 1
            learn_ind += 1
            state = new_state
        
        # agent record G
        self.agent.G_memory.append(G)
        
        return G

    def deep_Q_Network(
        self, episodes, discount_factor, learn_step,
        eps_init, eps_end, write_log, report_iter=100,
        inter=.001, update_target_interval=1, use_weather=None,
    ):
        """
        Deep Q-Network.
        - episodes: how many iterations to simulation in total.
        - alpha: learning rate;
        - discount factor: perspective of future.
        - learn_step: int, 
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
                discount_factor, learn_step, write_log, inter=inter,
                update_target_interval=update_target_interval, 
            )
            # -------------- step control ---------------
            # record return
            G.append(step_G)
            # log return
            if write_log:
                logging.info("    return: {}".format(step_G))
            
            self.epsilon_update_base(eps_init, eps_end, episodes)
            if write_log:
                logging.info("    -----------------------")
        return G  
    
    
    def epsilon_update_base(self, eps_init, eps_end, episodes):
            # set epsilon, 7-2.5, 10-5
            self.agent.epsilon = (eps_init - eps_end) * np.max([
                (episodes * 1 - iter) / (episodes * 1), 0
            ]) + eps_end 
            return 
        
        
class AlPyESM_A2C(AlPyESM):
    def __init__(self, manager, al_model_path, 
                 days=7, seed=13, method='A2C', 
                 memory_size=30, sample_episodes=21, 
                  DG_Table="dg_toy", NODE_Table="demand_nodes5",
                 port=51550,
                 **kwargs):
        super().__init__(manager, al_model_path, 
                         days, seed, method, 
                         memory_size, sample_episodes, 
                         DG_Table, NODE_Table,
                         port,
                         **kwargs)
        
    def __A2C_update(self, discount_factor, write_log, learn_step,
                     
                     use_weather=False):
        """
        one episode of A2C
        """
        G = 0
        epoch, V_future = 0, 0
        delta = False
        status, info = self.microgrid.last_state
        observation = self.microgrid.get_observation()
        print(f"status: {status}, info: {info}")
        state = np.array([
            observation.time,
            observation.skyCondition,
            observation.SOC,
            observation.PVout,
            observation.Demand,
        ])
        print(f"init: {state}")
        i = 0
        while not self.microgrid.is_terminal():
            
           # Take action based on seen state
            action_v = self.agent.take_action(state, max_charge=self.max_charge)
            self.action_temp.action = action_v
            self.microgrid.take_action(action=self.action_temp)
            
            status, info = self.microgrid.last_state
            observation = self.microgrid.get_observation()
            new_state = np.array([
                observation.time,
                observation.skyCondition,
                observation.SOC,
                observation.PVout,
                observation.Demand,
            ])
            
            # get reward for action
            R = observation.hourlyCosts
            days = observation.Days
            G += R
            
            if i%20 == 0:
                print(f"step: {i}, reward: {R}, days: {days}, state: {state} ")
            i += 1
            if write_log:
                # logging state, action and reward
                logging.info('    epoch: {}'.format(epoch))
                logging.info('    state: {}'.format(state))
                logging.info('    action: {}'.format(action_v))
                logging.info('    reward: {}'.format(R))
            # on step, transit to new state
            state = new_state
            epoch += 1
            if epoch >= learn_step:
                V_future = self.agent.critic(list(state.values))
                V_future = V_future.to('cpu').detach().numpy()[0]
                break
        # agent record G
        if V_future == 0:
            self.agent.G_memory.append(G)
        # ================ Learning =================
        self.agent.learn(
            V_future=V_future,
            discount_factor=discount_factor
        )
        return G

    def advantage_actor_acritic(
        self, episodes, discount_factor=1, write_log=False,
        learn_step=100,
        report_interval=100,
    ):
        """
        Deep Q learning.
        - episodes: how many iterations to simulation in total.
        - alpha: learning rate;
        - discount factor: perspective of future.
        """
        G = []
        # ---------------------- Learning ----------------------
        if write_log:
            logging.info("Learning...")
        for iter in range(episodes):
            if iter % report_interval == 0:
                print("Iteration {}".format(iter))
            # if True:
            if write_log:
                logging.info("Iteration {}".format(iter))
            # run one update
            # try:
            step_G = self.__A2C_update(discount_factor, write_log, learn_step)
            # ---------------- step control --------------------
            # record return
            G.append(step_G)
            # log return
            if write_log:
                logging.info("    return: {}".format(step_G))
                logging.info("    -----------------------")
        return G    