import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def calculateReward(speed, terrain):
    #Speed reward
    if speed > 900: #above speed limit
        speed_reward = 0 #no additional reward beyond limit
    elif speed > 600: #good speed range
        speed_reward = 1 
    elif 400 <= speed <= 600: #moderate speed
        speed_reward = -0.25
    else: #low speed
        speed_reward = -0.5

    #Terrain reward
    if terrain == "road":
        terrain_reward = 1
    elif terrain == "grass":
        terrain_reward = -1
    else:
        terrain_reward = 0 #in case of anything else

    #Total reward is the sum of the speed and terrain-based rewards
    return speed_reward + terrain_reward

#setting up csv file and data that will be plotted
file = 'speedsandterrain.csv'

data = pd.read_csv(file, header=None, names=['speed', 'terrain'])
speedData = data['speed'].to_numpy()
terrainData = data['terrain'].to_numpy()

incrementalRewards = np.array([calculateReward(speed, terrain) for speed, terrain in zip(speedData, terrainData)])
cumulativeRewards = np.cumsum(incrementalRewards)

time = np.arrange(len(speedData))
fig, axes = plt.subplots(2, 1)

#cumulative reward
axes[0].plot(time, cumulativeRewards)
axes[0].set_title('Cumulative Reward vs. Time')
axes[0].set_xlabel('Time')
axes[0].set_ylabel('Cumulative Reward')
axes[0].grid(True)
axes[0].legend()

ax2 = axes[0].twinx()
ax2.plot(time, speedData, label='Speed', color='green', linestyle='--')
ax2.set_ylabel('Speed', color='green')
ax2.tick_params(axis='y', labelcolor='green')

#incremental reward
axes[1].plot(time, incrementalRewards, color='purple')
axes[1].set_title('Incremental Reward vs. Time')
axes[1].set_xlabel('Time')
axes[1].set_ylabel('Incremental Reward')
axes[1].grid(True)
axes[1].legend()

ax3 = axes[1].twinx()
ax3.plot(time, speedData, label='Speed', color='green', linestyle='--')
ax3.set_ylabel('Speed', color='green')
ax3.tick_params(axis='y', labelcolor='green')

#shading to indicate terrain type
for i in range(len(terrainData)):
    if terrainData[i] == "road":
        axes[1].axvspan(i-0.5, i+0.5, color='green', alpha=0.2)  # road in light green
    elif terrainData[i] == "grass":
        axes[1].axvspan(i-0.5, i+0.5, color='red', alpha=0.2)  # grass in light red

road_patch = mpatches.Patch(color='green', alpha=0.3, label='Road')
grass_patch = mpatches.Patch(color='red', alpha=0.3, label='Grass')
axes[1].legend(handles=[road_patch, grass_patch], loc='upper right')

plt.tight_layout()
plt.show()
