import gymnasium as gym
import numpy as np
from gymnasium.spaces import Discrete,MultiDiscrete

class babyrobot_v0(gym.Env):
    
    def __init__(self, **kwargs):
        super().__init__()
        # dimensions of the grid
        self.width = kwargs.get('width',3)
        self.height = kwargs.get('height',3)

        # define the maximum x and y values
        self.max_x = self.width - 1
        self.max_y = self.height - 1

        # there are 5 possible actions: move N,E,S,W or stay in same state
        self.action_space = Discrete(5)

        # the observation will be the coordinates of Baby Robot
        self.observation_space = MultiDiscrete([self.width, self.height])

        # Baby Robot's position in the grid
        self.x = 0
        self.y = 0

    def step(self, action):        
        obs = np.array([self.x,self.y]) 
        reward = -1            
        done = True
        truncated = False
        info = {}
        return obs, reward, done, truncated, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # reset Baby Robot's position in the grid
        self.x = 0
        self.y = 0
        info = {}
        return np.array([self.x,self.y]),info

    def render(self):
        pass