# https://docs.ray.io/en/master/ray-overview/index.html

import gym, ray
import numpy as np
from gym.spaces import Discrete, Box
from ray.rllib.algorithms import ppo

import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()
    
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

class GRIDEnv(gym.Env):
    def __init__(self, env_config, input_size=6, 
                 **kwargs):
        self.action_space = Discrete(3)
        if input_size == 6:
            self.observation_space = Box(low=np.array([0,   0,   0,   0,   0]), 
                                    #                   t,  m,   P,   D,   C, 
                                         high=np.array([24, 13, 1e7, 1e7,  1]), 
                                         dtype=np.float64)
        else:
            self.observation_space = Box(low=np.array([0, 0, 0, 0, 0, 0, 0]), 
                                    #      t,  m,   P,  D,  C, 
                                     high=np.array([24, 13, 1e7, 1e7, 1, 3]), 
                                     dtype=np.float64)
    
    def reset(self):
        return []
    def step(self, action):
        # return <obs>, <reward: float>, <done: bool>, <info: dict>
        return    [],      0.0, False,  dict()
    
env_config = {}
GRIDEnv(env_config=env_config, input_size=6)

print("DONE")

for i in range(3):
    print(i)