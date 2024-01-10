from babyrobot_v0 import babyrobot_v0

# create an instance of our custom environment
env = babyrobot_v0()

# use the Gymnasium 'check_env' function to check the environment
# - returns nothing if the environment is verified as ok
from gymnasium.utils.env_checker import check_env
check_env(env)

print(f"Action Space: {env.action_space}")
print(f"Action Space Sample: {env.action_space.sample()}")

print(f"Observation Space: {env.observation_space}")
print(f"Observation Space Sample: {env.observation_space.sample()}")
