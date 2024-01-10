import gymnasium as gym

###########################################
#         Stage 1 - Initialization
###########################################

# create the cartpole environment
env = gym.make('CartPole-v1', render_mode="human")

# run for 10 episodes
for episode in range(10):

  # put the environment into its start state
  env.reset()

###########################################
#            Stage 2 - Execution
###########################################

  # run until the episode completes
  terminated = False
  while not terminated:

    # show the environment
    env.render()

    # choose a random action
    action = env.action_space.sample()

    # take the action and get the information from the environment
    observation, reward, terminated, truncated, info = env.step(action)


###########################################
#           Stage 3 - Termination
###########################################

# terminate the environment
env.close()