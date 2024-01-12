#############################################
# * purpose: set of classes that define an Energy grid manager object
# * created on: 12/24/22
# * Creator: Gerald Jones, UTK, ISE
#############################################
import torch
import torch.nn.functional as F
import torch.optim as optim
from ._DQRL.Q_MLP import Q_MLP
from ._A2CRL.ActorCritic import Actor, Critic
import matplotlib.pyplot as plt
import numpy as np


class ANYLOGICAGENT:
    """Generic agent object to be used within anylogic with pyComms
    
    """
    def __init__(self, init_state: list or np.array or set or None, 
                       actions: list or np.array or None, 
                       action_filter: None or function , 
                       **kwargs):
        self.init_state = init_state
        self.actions = actions
        self.action_filter=action_filter
        self.init_agent(**kwargs)
    
    
    def init_agent(self, **kwargs):
        return
    
    def memorize(self, state, **kwargs):
        return

    def observeTakeAction(self, state, **kwargs):
        return np.random.default_rng().choice(self.actions, 1, )[0]
    
    def observePerformance(self, 
                           learn_step, learn_interval, 
                           State, NextState, 
                           performance,
                           **kwargs):
        self.memorize(learn_step, State, NextState, performance)    
        if learn_step%learn_interval == 0:
            self.learn()
        return
    
    def learn(self, **kwargs):
        return np.random.default_rng().choice(self.actions, 1, )[0]

    def simulate_observation(self, state, **kwargs):
        return 


class GA_Agent(ANYLOGICAGENT):
    """ Agent that will perform some form of GA operation
    Args:
        ANYLOGICAGENT (_type_): _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, 
                 init_state: list or np.array or set or None, 
                 actions: list or np.array or None, 
                 action_filter: None or function or None, 
                 population_size: int or 10, 
                 generations: int or 10,
                 chromosome_length: int or 2,
                 chromosome_shape: list or tuple or None,
                 **kwargs):
        self.population_size=population_size
        self.generations = generations
        self.chromosome_length = chromosome_length
        self.chromosome_shape = chromosome_shape
        self.performance_dict = {0:0 for i in range(self.population_size)}
        
        super().__init__(init_state, actions, action_filter, **kwargs)
        
    
    def observePerformance(self, performance_score, **kwargs):
        """Observe performance of current chromosome based on returned "state
        """    
        self.performance_dict[kwargs["chromosome"]] = performance_score
        
    def rank_performance(self, **kwargs):
        self.performance_dict = dict(sorted(self.performance_dict.items(), 
                                            key=lambda x:[1]))
    
    
    def cross_over(self, parent_a, parent_b, **kwargs):
        # get random cross over point
        cp = np.random.default_rng().choice(range(1, self.chromosome_length), 1)[0]
        
        # create children
        kid_a = list(parent_a)[0:cp] + list(parent_b)[cp:] 
        kid_b = list(parent_b)[0:cp] + list(parent_a)[cp:] 
        return kid_a, kid_b
    
    def mutate(self, agent, **kwargs):
        mp1 = np.random.default_rng().choice(range(1, self.chromosome_length), 1)[0]
        mp2 = np.random.default_rng().choice(range(1, self.chromosome_length), 1)[0]
        tmp = agent[mp1]
        agent[mp1] = agent[mp2]
        agent[mp2] = tmp
        return agent
        
    def childrenMutation(self, kid_a, kid_b, mutation, **kwargs):
        #  do random mutation for each child
        for i in range(2):
            if np.random.default_rng().random() <= mutation:
                if i == 0:
                    kid_a = self.mutate(kid_a)
                else:
                    kid_b = self.mutate(kid_b)
        return kid_a, kid_b
    
    def breed_pair(self, parent_a, parent_b, cross_over, mutation, **kwargs):
        if np.random.default_rng().random() <= cross_over:
            kid_a, kid_b = self.cross_over(parent_a, parent_b) 
        else: 
            kid_a, kid_b =  parent_a, parent_b
       
        return self.childrenMutation(kid_a, kid_b, mutation)


    def select_breeding_pair(self, **kwargs):
        #  generate probablity of selection for each 
        # chromsome based on performance
        self.rank_performance()
        
        fittness = list(self.performance_dict.values())
        fittness_sum = np.sum(fittness)

class RL_AGENT(ANYLOGICAGENT):
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
    
    def __init__(self, 
                 init_state: list or np.array or set or None, 
                 actions: list or np.array or None, 
                 action_filter: None or function, 
                 discount: float or .9,
                 name: str or "RL-AGENT",
                 **kwargs):
        super().__init__(init_state, actions, action_filter, **kwargs)
        self.input_size = len(self.init_state)
        self.output_size = len(len(self.actions))
        
        self.discount=discount
        self.loss_memory = []
        self.G_memory = []
        # self.action_logic = lambda x:x
        if self.action_filter is None:
            self.action_logic=self.ess_action_filter_TKSPD
        else:
            self.action_logic = self.action_logic
        self.name=name
        
    def ess_action_filter_TKSPD(self, state, F=4, 
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
        # print(f"PV: {state[3]}")
        # print(f"needed: {needed}")
        # charge_possible = state[3] >= needed
        # charge_possible = state[3] - needed - state[4] >= 0
        # charge_possible = state[3] - needed - state[4] >= 0
        # print(f"charge possible: {charge_possible}")
        # print(f"SOC{SOC}, Fx: {Fx}, state[5]{state[5]}") 
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
                  TFD={}, close_me=False, fileName=None,
                  ):
        """
        plot train loss for agent
        """
        
        savename = self.name
        if fileName is not None:
            savename = fileName
        
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
        fig.savefig('{}{}_loss.png'.format(dir, savename), dpi=600)
        if close_me:
            plt.close()
        return    


class A2C_AGENT(RL_AGENT):
    def __init__(self, 
                init_state: list or np.array or set or None, 
                actions: list or np.array or None, 
                action_filter: None or function, 
                discount: float or 0.9, 
                name: str or "RL-AGENT", 
                hlayers: list or list([10, 10]),
                lr: float or 1e-3,
                b1: float or 1e-3,
                b2: float or 1e-3,
                seed: float or 0,
                learn_epoch: int or 1,
                epsilon: float or .9,
                min_epsilon: float or .1,
                callbacks: None or list or function,
                loggers: None or function,
                epsilon_update_interval: int or np.inf,
                epScale: float or int or 1,
                q_network_path: str or "DQ_agent.pt",
                optimizer: None or torch.optim,
                **kwargs):
        super().__init__(init_state, actions, action_filter, discount, name, **kwargs)
        self.hlayers = hlayers
        self.lr=lr
        self.b1=b1
        self.b2=b2
        self.seed=seed
        self.learning_epoch=learn_epoch
        self.epsilon=epsilon
        self.init_eps = epsilon
        self.callbacks = callbacks
        self.loggers = loggers
        self.epsilon_update = epsilon_update_interval
        self.min_epsilon = min_epsilon
        self.epScale = epScale
        self.kwargs = kwargs
        self.ep_steps = 1

       
        self.optimizerObj = None
        self.checkpoint = None
        
 
        self.episode = 0

        self.dev, self.Q, self.Q_target = None, None, None
        
        #################################################################
        #################################################################
        # set up training and learning behavior and initialize memory
        self.train_step = 1
        self.learn_epoch = learn_epoch
        self.loss_memory = []
        self.G_memory = []
        self.q_network_path=q_network_path

        
        
        self.init_network(optimizer)
       
    
    
    
    def init_networks(self, optimizer):
        if optimizer is None:
                self.optimizer = torch.optim.Adam(lr=self.lr, betas=[self.b1, self.b2])




# Base agent object, put the generic stuff here
class ESS_AGENT:
    """ Base class for ESS managers
        Represents an agent intended to manage an ESS unit
    """
    
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
    
    def __init__(self, actions, 
                 ess_cap,  ess_ceff,
                 discount=.90,
                 action_logic=None, name="ESS Agent",
                 **kwargs):
                
        """_summary_

        Args:
                        initial_state(vector): starter state for agent
                              actions(array/vector): int vector representing potential actions
                action_logic (method): logic function that returns 
                                       a set of potential action
                         name (string or int): string or number used to ID agent
                      **kwargs: any other needed key word arguments 
        """

        self.ess_cap=ess_cap
        self.ess_ceff=ess_ceff
        self.discount=discount
        self.actions = actions
        self.loss_memory = []
        self.G_memory = []
        # self.action_logic = lambda x:x
        if action_logic is None:
            self.action_logic=self.ess_action_filter_TKSPD
        self.name=name
          
    def set_state(self, state):
        self.current_state=state 

    def ess_action_filter_TKSPD(self, state, F=4, 
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
        # print(f"PV: {state[3]}")
        # print(f"needed: {needed}")
        # charge_possible = state[3] >= needed
        # charge_possible = state[3] - needed - state[4] >= 0
        # charge_possible = state[3] - needed - state[4] >= 0
        # print(f"charge possible: {charge_possible}")
        # print(f"SOC{SOC}, Fx: {Fx}, state[5]{state[5]}") 
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
            'b-',
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
                  TFD={}, close_me=False, fileName=None,
                  ):
        """
        plot train loss for agent
        """
        
        savename = self.name
        if fileName is not None:
            savename = fileName
        
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
        fig.savefig('{}{}_loss.png'.format(dir, savename), dpi=600)
        if close_me:
            plt.close()
        return    

    
        
        

# DQ RL Based Manager
class DQ_EMS(ESS_AGENT):
    def __init__(self, 
                 input_size, actions, 
                 ess_cap, ess_ceff,
                 discount=.9,
                 action_logic=None, name="DQ-ESS Agent",
                 hidden_layers=[10, 10],
                 lr=1e-3, learn_epoch=1, epsilon=.5, 
                 seed=1, optimizer=None,
                 betas=(.9, .999),
                 callbacks=None, loggers=None, epsilon_update=np.inf, min_epsilon=.1, epScale=1, 
                 q_network_path=None, qtarget_network_path=None,
                 training=True,
                 **kwargs):
        super().__init__(actions, 
                         ess_cap, ess_ceff,
                         discount,
                         action_logic, name, **kwargs)
        
        self.input_size=input_size
        self.actions=actions
        self.output_size = len(self.actions)
        self.action_filter = self.action_logic
        self.seed=seed
        print(actions)
        self.epsilon=epsilon
        self.init_eps = epsilon
        self.callbacks = callbacks
        self.loggers = loggers
        self.epsilon_update = epsilon_update
        self.min_epsilon = min_epsilon
        self.epScale = epScale
        self.kwargs = kwargs
        self.ep_steps = 1
        self.training=training
        ###########################################################
        # ----------------- construct network --------------------
        self.hidden_layers = hidden_layers
        self.optimizer = optimizer
        self.optimizerObj = None
        self.checkpoint = None
        
        self.lr = lr
        self.betas = betas
        self.episode = 0
        self.input_size, self.output_size = input_size, len(actions)
        self.dev, self.Q, self.Q_target = None, None, None
        
        #################################################################
        #################################################################
        # set up training and learning behavior and initialize memory
        self.train_step = 1
        self.learn_epoch = learn_epoch
        self.loss_memory = []
        self.G_memory = []
        self.q_network_path=q_network_path
        self.qtarget_network_path=qtarget_network_path
        self.init_Qnetworks()
        
    
    def load_model_checkpoint(self, checkpoint_path):
        training = self.training
        print(f"Loading model check point from {checkpoint_path}")
        check_point = torch.load(checkpoint_path)
        print(f"loaded checkpoint: {len(check_point)}")
        self.checkpoint = check_point
        self.hidden_layers = check_point["hidden_layers"]
        self.optimizer.load_state_dict(check_point["Optimizer"])
        self.min_epsilon = check_point["min_epsilon"]
        if not training:
            self.epsilon = 0
            print(f"epsilon {self.epsilon}")
        else:
            self.epsilon = check_point["epsilon"]
            self.ep_steps = check_point["epsilon_step"]
            self.train_step = check_point["train_step"]
            pass
        self.epsilon_update = check_point["epsilon_update"]
        self.lr = check_point["lr"]
        self.learn_epoch = check_point["learn_epoch"]
        self.betas = check_point["betas"]
        self.loss_memory = list(check_point["loss"])
        
    
    def create_network_objects(self,):
        # prediction network
        self.Q = Q_MLP(
            hidden_layer_shape=self.hidden_layers,
            input_size=self.input_size,
            output_size=self.output_size,
            seed=self.seed
        )
        self.Q.to(self.dev)
        
        # target network
        self.Q_target = Q_MLP(
            hidden_layer_shape=self.hidden_layers,
            input_size=self.input_size,
            output_size=self.output_size,
            seed=self.seed
        )
        
        
        self.Q_target.to(self.dev)
        
        for p in self.Q.parameters():
            p.data.fill_(0)
        for p in self.Q_target.parameters():
            p.data.fill_(0)    

        if self.checkpoint is not None:
            print("loading networks")
            checkpoint = self.checkpoint
            self.Q.load_state_dict(checkpoint["Q_network"])
            self.Q_target.load_state_dict(checkpoint["Qtarget_network"])
            self.Q.eval()
            self.Q_target.eval()        

        self.optimizer = optim.Adam(self.Q.parameters(), lr=self.lr, 
                                    betas=self.betas,)
       
        if self.checkpoint is not None and "Optimizer" in self.checkpoint:
            print("loading optimizer")
            self.optimizer.load_state_dict(self.checkpoint["Optimizer"])

    
    def init_Qnetworks(self, ):
        # ------------------- GPU ----------------
        if torch.cuda.is_available():
            self.dev = "cuda:0"
        else:
            self.dev = "cpu"
       
        if self.q_network_path:
            self.load_model_checkpoint(self.q_network_path)
        else:
            print("No Loaded networks by Agent...")
        
        self.create_network_objects()
        # if self.checkpoint is not None:
        #     self.load_trained_model()
        # # prediction network
        # self.Q = Q_MLP(
        #     hidden_layer_shape=self.hidden_layers,
        #     input_size=self.input_size,
        #     output_size=self.output_size,
        #     seed=self.seed
        # )
        # self.Q.to(self.dev)
        
        # # target network
        # self.Q_target = Q_MLP(
        #     hidden_layer_shape=self.hidden_layers,
        #     input_size=self.input_size,
        #     output_size=self.output_size,
        #     seed=self.seed
        # )
        
        
        # self.Q_target.to(self.dev)
        # for p in self.Q.parameters():
        #     p.data.fill_(0)
        # for p in self.Q_target.parameters():
        #     p.data.fill_(0)
        # load previous parameters
        # if 'Q_path' in self.kwargs:
        # if self.q_network_path is not None and self.qtarget_network_path is not None:
        #    self.load_trained_model(self.q_network_path, self.qtarget_network_path)
            # self.Q.load_state_dict(torch.load(self.kwargs['Q_path']))
            # self.Q.eval()
        
        # optimizer
        # https://pytorch.org/docs/stable/optim.html
        
        # if "Optimizer" in self.checkpoint:
        #     self.optimizer.state_dict(self.checkpoint["Optimizer"])
        return
       
       
    def store_trained_model(self, pathQ="DQ_network.pt", pathQ_target="DQ_target.pt", **kwargs):
        # store the models param dict
        print(f"Storing DQ models check point to ./{pathQ}")
        torch.save({"Q_network":self.Q.state_dict(),
                    "Qtarget_network": self.Q_target.state_dict(),
                    "input_size": self.input_size,
                    "output_size": self.output_size,
                    "actions": self.actions,
                    "Optimizer": self.optimizer.state_dict(),
                    "epsilon": self.epsilon,
                    "epsilon_step": self.ep_steps,
                    "train_step": self.train_step,
                    "hidden_layers": self.hidden_layers,
                    "min_epsilon": self.min_epsilon,
                    "epsilon_update": self.epsilon_update,
                    "lr": self.lr,
                    "learn_epoch": self.learn_epoch,
                    "betas": self.betas,
                    "loss": self.loss_memory,
                    }, pathQ) 
        # torch.save(self.Q_target.state_dict(), pathQ_target)
        # torch.save(self.optimizer.state_dict(), "Optimizer_" + pathQ)
        return 
    
    def load_trained_model(self, checkpoint, pathQ="DQ_network.pt", pathQ_target="DQ_target.pt", **kwargs):
        # load the trained model params
        # checkpoint = torch.load(pathQ)
        self.Q.load_state_dict(checkpoint["Q_network"])
        self.Q_target.load_state_dict(checkpoint["Qtarget_network"])
        self.optimizer.load_state_dict(checkpoint["Optimizer"])
        self.Q.eval()
        self.Q_target.eval()
    
        # self.Q.load_state_dict(torch.load(pathQ))
        # self.Q.eval()
        # self.Q_target.load_state_dict(torch.load(pathQ_target))
        # self.Q_target.eval()
        # self.optimizer.load_state_dict(torch.load(), "Optimizer_" + pathQ)
        return                  


            
    def load_parameter(self, Q_path, Qtarget_path):
        """
        Load network parameter from path
        """
        self.Q.load_state_dict(torch.load(Q_path))
        self.Q_target.load_state_dict(torch.load(Qtarget_path))
        return    
    def store_parameter(self, Q_path, Qtarget_path, epoch):        
        torch.save(
            { "":epoch, 
              "model_state_dict": self.Q.state_dict(),
              "optimizer_state_dict": self.optimizer,
              "loss": self.loss,
             }, Q_path)   
        # torch.save(
        #     { "":epoch, 
        #       "model_state_dict": self.Q.state_dict(),
        #       "optimizer_state_dict": self.optimizer,
        #       "loss": self.actor_loss,
        #      }, Qtarget_path)   
        
        return 
    
    def take_action(self, state, **kwargs):
        """
        take action (make prediction), based on the input state.
        """
        # print("DQ taking action")
        # make state to tensor
        input_seq = torch.tensor(
            state, dtype=torch.float, device=self.dev
        )
        # make a prediction
        self.Q.eval()
        with torch.no_grad():
            output_seq = list(self.Q(input_seq))
        self.Q.train()

        # get only valid ESS commands based on state
        valid_actions = self.action_filter(state, **kwargs)

        # get a random number between 0, 1
        # will be true(Greedy) 1-epsilon% of the time
        if np.random.random() > self.epsilon:
            # print("Greedy epsilon: ", self.epsilon)
            return valid_actions[np.argmax([
                output_seq[self.actions.index(i)]
                for i in valid_actions
            ])]
        else:
            # print("Random")
            return valid_actions[np.random.choice(
                range(len(valid_actions)), size=1, replace=False,
                p=[1 / len(valid_actions)] * len(valid_actions)
            )[0]]
            
                   
    def simulate_action(self, state, **kwargs):
        """
        take action (for simulation), based on the input state.
        """
        print("in learning DQ")
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
        print("filtering actions in DQ learning")
        valid_actions = self.action_filter(state, **kwargs)

        return valid_actions[np.argmax([
            output_seq[self.actions.index(i)]
            for i in valid_actions
        ])]
        
        
    def learn(self, memory, discount_factor=None, inter=.001,
              update_target_interval=1, **kwargs):
        """
        train the network
        every Q_share training steps copy into target 
        using inter as the tau factor
        """
        if discount_factor is None:
            discount_factor = self.discount
        
        # print("in DG learn")
        # memories
        state_memory = memory[0]
        new_state_memory = memory[1]
        delta_memory = memory[2]
        action_memory = memory[3]
        reward_memory = memory[4]
        # print(f"Memory state size: {len(state_memory)}")
        # action index
        action_ind = torch.tensor([
            [self.actions.index(a)] for a in action_memory
        ], device=self.dev)  # .flatten()
        # print(f'370 learn epoch: {self.learn_epoch}')
        # print(f'reward mem length: {len(reward_memory)}')
        # 
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
        if self.train_step % update_target_interval == 0:
            self.__soft_update(self.Q, self.Q_target, inter)
        
        # if self.train_step % self.epsilon_update == 0:
        #     # print("min eps ", self.min_epsilon)
        #     self.epsilon = self.epsilon_decay(self.epsilon, self.min_epsilon, self.ep_steps, self.epScale)
        #     # print(f"Epsilon: {self.epsilon}")
        #     self.ep_steps += 1
        
        self.epsilon = self.epsilon_update_base(self.init_eps, self.min_epsilon,
                                               self.ep_steps, self.epsilon_update)
        self.ep_steps += 1
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
    
    def epsilon_decay(self, epsilon, min_ep, t, scl=1):
        return max(epsilon/(t*scl), min_ep)
    
    def epsilon_update_base(self, eps_init, eps_end, iters, episodes):
            # set epsilon, 7-2.5, 10-5
            self.epsilon = (eps_init - eps_end) * np.max([
                (episodes * 1 - iters) / (episodes * 1), 0
            ]) + eps_end
             
            return self.epsilon
       
#################################
 #      A2C RL based manager  
#################################
class A2C_EMS(ESS_AGENT):
    def __init__(self, 
                 input_size, actions,
                 ess_cap, ess_ceff, 
                 actor_hidden_layers, critic_hidden_layers,
                 discount=.7,  
                 action_logic=None, name="A2C-ESS Agent",
                 actor_lr=.001, critic_lr=.001,
                 actor_betas=(.9, .999), critic_betas=(.9, .999),
                 callbacks=None, loggers=None, optimizer=None,
                 a2c_path=None,
                 training=True,
                 **kwargs):
        super().__init__(actions, 
                         ess_cap, ess_ceff,
                         discount,
                         action_logic, name, **kwargs)           
    
        self.input_size=input_size
        self.actions=actions
        self.action_filter = self.action_logic
        

        self.callbacks = callbacks
        self.loggers = loggers
        self.kwargs = kwargs
        self.training = training
         ###########################################################
        # ----------------- construct network --------------------
        self.actor_hidden_layers = actor_hidden_layers
        self.critic_hidden_layers = critic_hidden_layers
        self.optimizer = optimizer
        self.actor_lr = actor_lr
        self.critic_lr = critic_lr
        self.actor_betas = actor_betas
        self.critic_betas = critic_betas
        self.input_size, self.output_size = input_size, len(actions)
        self.dev, self.actor, self.critic = None, None, None
        self.check_point=None
        self.a2c_path=a2c_path
        self.train_step = 1
        self.actor_loss = []
        self.critic_loss = []
        self.init_networks()
        
        
        self.reward_memory = []
        self.log_prob = []
        self.V_pred = []
        self.G_memory = []
        self.entropy = 0
        
    
    def create_networks(self, ):
        # ----------------- construct network --------------------
        # actor
        self.actor = Actor(
            hidden_layers=self.actor_hidden_layers,
            input_size=self.input_size, output_size=self.output_size
        )
        self.actor.to(self.dev)
        # critic
        self.critic = Critic(
            hidden_layers=self.critic_hidden_layers, 
            input_size=self.input_size
        )
        self.critic.to(self.dev)
        
        
        if self.check_point is not None and "actor_network" in self.check_point and "critic_network" in self.check_point:
            self.actor.load_state_dict(self.check_point["actor_network"])
            self.critic.load_state_dict(self.check_point["critic_network"])
        
        self.actor_optimizer = optim.Adam(
            self.actor.parameters(), lr=self.actor_lr,
            betas=self.actor_betas,
        )
        self.critic_optimizer = optim.Adam(
            self.critic.parameters(), lr=self.critic_lr,
            betas=self.critic_betas,
        )
        
        if self.check_point is not None and "actor_optimizer" in self.check_point and "critic_optimizer" in self.check_point:
            # self.actor_optimizer.load_state_dict(self.check_point["actor_optimizer"])
            # self.critic_optimizer.load_state_dict(self.check_point["critic_optimizer"])
            self.actor_optimizer = self.check_point["actor_optimizer"]
            self.critic_optimizer = self.check_point["critic_optimizer"]
        
    
    def init_networks(self,):
         # ------------------- GPU ----------------
        if torch.cuda.is_available():
            self.dev = "cuda:0"
        else:
            self.dev = "cpu"
        if self.a2c_path is not None:
            self.load_model_checkpoint(self.a2c_path)
        self.create_networks()
        
        
        
 
        # # ----------------- construct network --------------------
        # # actor
        # self.actor = Actor(
        #     hidden_layers=self.actor_hidden_layers,
        #     input_size=self.input_size, output_size=self.output_size
        # )
        # self.actor.to(self.dev)
        # # critic
        # self.critic = Critic(
        #     hidden_layers=self.critic_hidden_layers, 
        #     input_size=self.input_size
        # )
        # self.critic.to(self.dev)
        # ------------------------ optimizer ----------------------------
        # https://pytorch.org/docs/stable/optim.html
        self.actor_optimizer = optim.Adam(
            self.actor.parameters(), lr=self.actor_lr,
            betas=self.actor_betas,
        )
        self.critic_optimizer = optim.Adam(
            self.critic.parameters(), lr=self.critic_lr,
            betas=self.critic_betas,
        )
        
        
    def load_parameter(self, actor_path, critic_path):
        """
        Load network parameter from path
        """
        self.actor.load_state_dict(torch.load(actor_path))
        self.critic.load_state_dict(torch.load(critic_path))
        return    
    
    def store_trained_model(self, actor_path, critic_path=None, epoch=None):
        print(f"Storing model to {actor_path}")
        torch.save(
            { 
            #  Actor Network
              "actor_network": self.actor.state_dict(),
            #   "actor_optimizer": self.actor_optimizer,
              "actor_optimizer": self.actor_optimizer.state_dict(),
              "actor_loss": self.actor_loss,
              "actor_hidden_layers": self.actor_hidden_layers,
              "actor_lr": self.actor_lr,
              "actor_betas": self.actor_betas,
            #  Critic Network
              "critic_network": self.critic.state_dict(),
              "critic_optimizer": self.critic_optimizer.state_dict(),
              "critic_loss": self.critic_loss,
              "critic_hidden_layers": self.critic_hidden_layers,
              "critic_lr": self.critic_lr,
              "critic_betas": self.critic_betas,
            # Progress
              "train_step": self.train_step,
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
        
        self.actor_optimizer = self.check_point["actor_optimizer"]
        self.critic_optimizer = self.check_point["critic_optimizer"]
        
        self.actor_optimizer = torch.optim.adam
        
        self.actor_optimizer = self.check_point["actor_optimizer"]
        self.critic_optimizer = self.check_point["critic_optimizer"]
    
    
    def store_parameter(self, actor_path, critic_path, epoch):
        torch.save(
            { "":epoch, 
              "model_state_dict": self.actor.state_dict(),
              "optimizer_state_dict": self.actor_optimizer,
              "loss": self.actor_loss,
             }, actor_path)
        
        torch.save(
            { "":epoch, 
              "model_state_dict": self.critic.state_dict(),
              "optimizer_state_dict": self.critic_optimizer,
              "loss": self.critic_loss,
             }, critic_path)
        return
        
      
      
    def take_action(self, state, max_charge=4, **kwargs):
        """
        take action (make prediction), based on the input state.
        """
        # make state to tensor
        input_seq = torch.FloatTensor(state).to(self.dev)
        # make a prediction, with grad
        policy_dist = self.actor(input_seq)
        value = self.critic(input_seq)
        # value, distribution
        self.V_pred.append(value[0])
        dist = policy_dist.to('cpu').detach().numpy()
        
        # valid_actions
        valid_actions = self.action_filter(state, max_charge=4, **kwargs)
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
        self.log_prob.append(policy_dist.squeeze(0)[action_ind])
        # entropy
        self.entropy += -1 * np.sum(np.mean(np.exp(dist)) * dist)
        # return
        return self.actions[action_ind]

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
        valid_actions = self.action_filter(state, max_charge=4, **kwargs)
        
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

    def learn(self, discount_factor, V_future=0):
        """
        train the network
        """
        # set zero grad
        self.actor_optimizer.zero_grad()
        self.critic_optimizer.zero_grad()
        # print(f"length of reward mem: {len(self.reward_memory)}")
        # target values
        V_targ = np.zeros(len(self.V_pred))
        for t in range(len(self.reward_memory) - 1, -1, -1):
            V_future = self.reward_memory[t] + discount_factor * V_future
            V_targ[t] = V_future
        # make tensors
        V_pred = torch.stack(self.V_pred)
        V_targ = torch.FloatTensor(V_targ).to(self.dev)
        log_prob = torch.stack(self.log_prob)
        # print("After making tensors..")
        # loss
        advantage = V_targ - V_pred
        actor_loss = (-1 * log_prob * advantage.detach()).mean()
        critic_loss = advantage.pow(2).mean()
        # back propagate
        actor_loss.backward()
        critic_loss.backward()
        self.actor_optimizer.step()
        self.critic_optimizer.step()
        # save loss
        self.actor_loss.append(actor_loss.to('cpu').detach().numpy())
        self.critic_loss.append(critic_loss.to('cpu').detach().numpy())
        # clear memory
        self.log_prob = []
        self.V_pred = []
        self.reward_memory = []
        return
    
    def plot_G(self, window=20, start_ind=0, sample=1, dir='', 
               title="G", TFD={}, close_me=False):
        """
        plot return using time window
        dir: 'directory/'
        """
        G_plot = {}
        ind = window
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
    
    def plot_loss(self, window=20, start_ind=0, 
                  sample=1, dir='', 
                  titles=['Actor Loss','Critic Loss' ], colors=['b-', 'r-'],
                  TFD={}, close_me=False, fileName=None):
        """
        plot train loss for agent
        dir: 'directory/'
        """
        savename = self.name
        if fileName is not None:
            savename = fileName
        
        for nn in range(2):
            loss_memory = self.actor_loss if nn == 0 else self.critic_loss
            savenamefull = savename + "_Actor" if nn == 0 else savename + "_Critic"
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
  
        
        