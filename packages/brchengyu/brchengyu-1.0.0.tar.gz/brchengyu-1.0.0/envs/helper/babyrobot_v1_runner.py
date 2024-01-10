import gymnasium as gym
import numpy as np
import babyrobot_01

# create the environment
# env = gym.make('BabyRobotEnv-v2')
env = gym.make('br-v1')

# initialize the environment
env.reset()
env.render()

terminated = False
while not terminated:  

  # choose a random action
  action = env.action_space.sample()   

  # take the action and get the information from the environment
  new_state, reward, terminated, truncated, info = env.step(action)
  
  # show the current position and reward
  env.render(action=action, reward=reward) 