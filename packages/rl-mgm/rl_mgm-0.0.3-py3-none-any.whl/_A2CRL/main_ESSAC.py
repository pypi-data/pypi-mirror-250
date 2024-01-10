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
    epsi = .1              # percentage of output taken to charge ess
    action_weights = [1, -epsi, 0]    # used to control ESS supply effect

    ##################################
    #### Set up test environment
    ##################################
    seed = 1911
    np.random.seed(seed)

    demand_min = 10
    demand_max = 50
    demands = np.random.default_rng().choice(list(np.arange(demand_min, demand_max+10, T)), size=T)

    # demands = (demands - demands.min())/(demands.max() - demands.min())

    # set ouput max below demands to make sure there are cased when we will not meet demand
    outputs =  np.random.default_rng().choice(list(np.arange(demand_min, demand_max, T)), size=T)

    # outputs = (outputs - outputs.min())/(outputs.max() - outputs.min())
    unmet = outputs - demands
   
    # time steps 
    t = list(range(1, T+1))


    # use max unmet to set ESS output for testing
    ess_out = max(np.abs(unmet))*.80
    ess_out = max(np.abs(unmet))*.5
    ess_unmet = outputs+ess_out - demands
    print(ess_out)
    
    ##################################
    ##################################
     # make some quick evaluators
    ##################################
    ##################################
    abs_reward = lambda x: -abs(x)  # just use abs val
    under_weight = 2
    over_weight = 1.5
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
        
        k = s[1]
        F = s[-1]      # get max SOC
        pv_out = outputs[t]
        dem = demands[t]    
        
        
        # unpack the state
        s[0] += 1 # increment time unit
        # k = s[1]
        # soc = s[2]
        # F = s[3]
        # if discharge increment discharge counter
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
                       ess_logic=True):
                    #    ess_logic=True):
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
                return -1e-1
            if (sc <=0) and a == 1: # punish full charging
                return -1e-1
            
            # punish inaction
            if (sc == F) and a == 2: # punish not charging on empty
                return -1e-1
            if (sc == 0) and a == 2:  # not discharge when full
                return -1e-1
        
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
            store_sample(svals, savgs)
            svals.clear()
        
        
        return base_eval(S)
             
        
     # agent
    manager = Agent(
        name="ESS_manager_AC",
        actions=actions,
        input_size=len(initial_state),
        actor_hidden_layers=[10],
        critic_hidden_layers=[10],
        output_size=len(actions),
        actor_lr=1e-2,
        critic_lr=1e-2,
    )

    # define problem
    problem = DRL_Env(
        name="maintenance",
        agent=manager,
        initial_state=initial_state,
        trans_func=trans_funcESS,
        reward_func=reward_funcESS,
    )    
         
  

    # logging
    logging.basicConfig(
        filename='maintenanceESS.log', filemode='w+',
        format='%(levelname)s - %(message)s', level=logging.INFO
    )

    # DQN
    # call the Q network to optimze the problem
       # DQN
    G = problem.advantage_actor_acritic(
        episodes=5000,
        # discount_factor=1,
        discount_factor=.10,
        # discount_factor=1.0,
        write_log=True
    )

    
    
    # plot
    manager.plot_loss(window=20, start_ind=0, sample=1, dir='./figs',
                      title="My LOSS", TFD={"size": 20})
    plt.show()
    
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
    
    states = generate_all_states(T, K=[0], soc=soc)
    select_states = generate_quick_run(T, soc)
    # show policy?
    policy = problem.agent.generate_policy(states=states)
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
    # for s in check_policy:
        s = "-".join([str(sv) for sv in s[:-1]])
        sp = s.split("-")
        t = int(sp[0]) + 1
        k = sky_conds[int(sp[1])]
        soc = int(sp[2])
        a = check_policy[s]
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
