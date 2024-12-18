import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculateReward(speed):
    if speed > 900: #above speed limit
        return 0 # no additional reward beyond limit
    elif speed > 600: # gives good reward
        return 1
    elif speed >= 400 & speed <= 600: # penalty for moderate speed
        return -0.25
    else: # penalty for low speed
        return -0.5

file = 'speeds.csv'
speedData = pd.read_csv(file).to_numpy().flatten()

incrementalRewards = np.array([calculateReward(speed) for speed in speedData])
cumulativeRewards = np.cumsum(incrementalRewards)

time = np.arange(len(speedData))

fig, axes = plt.subplots(2,1)

axes[0].plot(time,cumulativeRewards,label='Cumulative Reward', color = 'blue')
axes[0].set_title('Cumulative Reward vs. Time')
axes[0].set_xlabel('Time')
axes[0].set_ylabel('Cumulative Reward')
axes[0].grid(True)
axes[0].legend()

axes[1].plot(time, incrementalRewards, label='Incremental Reward', color='red')
axes[1].set_title('Incremental Reward vs. Time')
axes[1].set_xlabel('Time')
axes[1].set_ylabel('Incremental Reward')
axes[1].grid(True)
axes[1].legend()

plt.tight_layout()
plt.show()
