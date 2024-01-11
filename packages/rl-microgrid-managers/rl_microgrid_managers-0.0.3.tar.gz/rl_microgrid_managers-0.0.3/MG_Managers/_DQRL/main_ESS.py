"""
IE-608 DQN example.
"""

# import
import logging
import numpy as np
from DRL import Agent, DRL_Env, ess_action_filter
from matplotlib import pyplot as plt


def main():
    """
    main
    """
    # --------- parameters -----------

    # horizon
    T = 16   # hours we need to cover
    K = 1    # number of potential sky conditions
    soc = 4  # number of consecutive discharge hours

    # ------------ MDP --------------

    # initial state: t, condition
    initial_state = (0, 0, 0, soc)

    # number of actions
    # actions = range(num_plans)
    actions = [0, 1, 2]
    epsi = .1              # percentage 
    action_weights = [1, -epsi, 0]    # used to control ESS supply effect

    ##################################
    #### Set up test environment
    ##################################
    seed = 13
    np.random.seed(seed)
   

    demand_min = 10
    demand_max = 50
    demands = np.random.default_rng().choice(list(np.arange(demand_min, demand_max+10, 10)), size=T)

    # set ouput max below demands to make sure there are cased when we will not meet demand
    outputs =  np.random.default_rng().choice(list(np.arange(demand_min, demand_max, T)), size=T)

    unmet = outputs - demands
    
    t = list(range(1, T+1))


    # use max unmet to set ESS output for testing
    ess_out = max(np.abs(unmet))*.80
    ess_out = max(np.abs(unmet))*2
    ess_unmet = outputs+ess_out - demands
    print(ess_out)
    
    ##################################
    ##################################
     # make some quick evaluators
    abs_reward = lambda x: -abs(x)  # just use abs val
    
    def fulfillment_specialist(x):
        if x < 0:
            return x
        return 0
    
    def fulfillment_specialist2(x):
        if x < 0:
            return x*under_weight
        return x*over_weight
    
    def linear(x):
        return x
    
    def recursive_average(new, x, t):
        if t == 0:
            return x
        return x + (1/t)(new-x)
        
    
    def trans_funcESS(t, s, a):
        """_summary_

        Args:
            t: epoch
            s: rest of state: [h,k,soc, F]
            a: [0(discharge), 1(charge), 2(idle)]
        """
        s = list(s).copy()
        if s[0] + 1 >= T:
            return "Delta"
        
        # unpack the state
        s[0] += 1 
        k = s[1]
        # sc = s[2]
        F = s[-1]
        
        pv_out = outputs[t]
        dem = demands[t]   
        
        if a == 0:
            # increment up to max value
            # s[2] = min(s[2] + 1, s[-1])
            s[2] =s[2] + 1
        elif a == 1:
            # s[2] = max(s[2] - 1, 0)
            s[2] = s[2] - 1
        
        return s
            
    def store_sample(samplev, storageV):
        storageV.append(np.mean(samplev))
            
    
    svals = []
    savgs = []
    sample = 500

    # def reward_funcESS(s, a, s_next, base_eval=linear, #):
    # def reward_funcESS(s, a, s_next, base_eval=fulfillment_specialist, #):
    # def reward_funcESS(s, a, s_next, base_eval=fulfillment_specialist2, #):
    def reward_funcESS(s, a, s_next, base_eval=abs_reward, 
                    #    ess_logic=True):
                       ess_logic=True):
        """_summary_

        Args:
            s: current state tuple (t, k, soc, F)
            a: action to be taken one of
            s_next:   state the given action would leave the system in
        Returns:
            _type_: some numeric value derived by base_eval function 
                    and current difference between DG output and Demand
        """
        s = list(s)
        t = s[0]       # current time
        k = s[1]
        sc = s[2]
        F = s[-1]      # get max SOC
        pv_out = outputs[t]
        dem = demands[t]
        
        if ess_logic:
            # punish bad actions
            if (sc >= F) and a==0:  # punish discharge when empty
                return -1e1
            if (sc <=0) and a == 1: # punish full charging
                return -1e1
            
            # punish inaction
            if (sc == F) and a == 2: # punish not charging on empty
                return -1e1
            if (sc == 0) and a == 2:  # not discharge when full
                return -1e1
        
        # use action to determine the ESS output 
        # also based on SOC and action filter used
        if a == 0 or a == 2:
            ess_con = action_weights[a]*ess_out
        else:
            # ess_con = action_weights[a]*pv_out
            ess_con = -.1*pv_out
        
        O = pv_out + ess_con 
        S = O - dem
        
        # if len(svals) > 2:
        #     # normalize?
        #     S = (S-np.min(svals))/(np.max(svals) - np.min(svals))
        
        svals.append(S)
        if len(svals)%sample == 0 and t > 0:
            # print(len(svals))
            store_sample(svals, savgs)
            svals.clear()
        
        
        return base_eval(S)


    def reward_funcESSOG(s, a, s_next, base_eval=abs_reward):
        """_summary_

        Args:
            s: current state tuple (t, k, soc, F)
            a: action to be taken one of
            s_next:   state the given action would leave the system in
        Returns:
            _type_: some numeric value derived by base_eval function 
                    and current difference between DG output and Demand
        """
        s = list(s)
        t = s[0]       # current time
        k = s[1]
        F = s[-1]      # get max SOC
        pv_out = outputs[t]
        dem = demands[t]
        
        # use action to determine the ESS output 
        # also based on SOC and action filter used
        ess_con = action_weights[a]*ess_out
        
        S = pv_out + ess_con - dem
        
        return base_eval(S)
             

    # learning params
    
    ##############################3################
    #####                Agent  params
    ##############################3################
    episodes=1200
    hidden_layers = [100, 100]
    lr = 1e-4 
    lr = 1e-4 
    learn_epoch = 1
    epsilon = .1   
    # agent
    manager = Agent(
        name="ESS_manager",
        actions=actions,
        input_size=len(initial_state),
        hidden_layers=hidden_layers,
        output_size=len(actions),
        learning_rate=lr, 
        learn_epoch=learn_epoch, 
        epsilon=epsilon,
        action_filter=ess_action_filter,
    )

    # define problem
    ################################### 
    # create the problem environment 
    # this requires the agent, the transition logic function, and the reward function
    mem_size = 5000
    samples_ep = 500
    
    problem = DRL_Env(
        name="maintenance",
        agent=manager,
        initial_state=initial_state,  # start at t=1
        trans_func=trans_funcESS,
        reward_func=reward_funcESS,
        memory_size=mem_size,
        sample_episodes=samples_ep,
    )

    ###################################################
    ##############       logging
    ###################################################
    logging.basicConfig(
        filename='maintenanceESS.log', filemode='w+',
        format='%(levelname)s - %(message)s', level=logging.INFO
    )

    ################################################
    ###########              DQN
    ################################################
    DQ_episodes = 1200
    gamma = .9
    DG_learn_step = 1
    eps_init = 1
    eps_end= 0
    write_log = False
    
    # call the Q network to optimze the problem
    G = problem.deep_Q_Network(
        episodes=DQ_episodes,
        discount_factor=gamma,
        learn_step=DG_learn_step,
        eps_init=eps_init,
        eps_end=eps_end,
        write_log=write_log,
    )


    
    # plot
    manager.plot_loss(window=20, start_ind=0, sample=1, dir='./figs',
                      title="My LOSS", TFD={"size": 20})
    # plt.show()
    
    manager.plot_G(window=20, start_ind=0, sample=1, dir='./figs',
                      title="Expected Return", TFD={"size": 20})
    plt.show()

    def generate_all_states(T, K, soc):
        states = list()
        for t in range(T):
            for k in K:
                for sc in range(soc+1):
                    states.append([t, k, sc, soc])
        return states
    
    def generate_quick_run(T, soc):
        states = list()
        for t in range(T):
            # for sc in range(soc+1):
            states.append([t, 0, 0, soc])
        return states
    
    statesAll = generate_all_states(T, K=[0], soc=soc)
    select_states = generate_quick_run(T, soc)
    
    # show policy?
    policy = problem.agent.generate_policy(states=statesAll)
    check_policy = problem.agent.generate_policy(states=select_states)
    sky_conds = {
        0:"sunny",
        1:'cloudy',
        2: 'overcast',
    }
    
    ESSM_Action_labels = {
        0: "discharge",
        1: "charge",
        2: "Idle",
    }
    xticklabels = list()
    c = 0
    print(len(select_states))

    for s in select_states:
        print(s)

    for s in select_states:
        s[2] = c
        s = "-".join([str(sv) for sv in s[:-1]])
        sp = s.split("-")
        t = int(sp[0]) + 1
        k = sky_conds[int(sp[1])]
        soc = int(sp[2])
        a = policy[s]
        Action = ESSM_Action_labels[a]
        if a == 0: # discharge
            c += 1
        elif a == 1: # charge
            c -= 1
        xticklabels.append(Action[0].upper())
        print("------------------------------------------------------------")
        print("State: time:{}\nsky condition: {}\nSOC: {}".format(t, k, c))
        print("\t\tAction: {}".format(Action))
        print("------------------------------------------------------------\n")
    
                
    fig, ax = plt.subplots(1)
    print("ESS-out: ", ess_out)
    print(demands)
    print(outputs)
    xl = range(len(outputs))
    ax.bar(xl, demands, color="red", label="Unmet")
    ax.bar(xl, outputs, color='green', alpha=.5, label="Exceeds")
    ax.bar(1, 0, color="brown", label="Meet")
    ax.set_xticks(xl)
    ax.set_xticklabels(xticklabels, fontdict={"rotation":90})
    plt.legend()
    plt.show()

    fig, ax = plt.subplots(1)
    
    print(savgs)
    ax.plot(savgs, label="averaged Supplied values")
    # ax.set_xticks(xl)
    # ax.set_xticklabels(xticklabels, fontdict={"rotation":90})
    plt.legend()
    plt.show()
    return

if __name__ == "__main__":
    print("Hi, it's a me, Jonesy!")
    main()
