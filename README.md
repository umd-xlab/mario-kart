# Qualifying Autonomous Systems: Learning from Mario Kart for Robust Safety

## Contributors
- **Kristy Sakano (Developer)**  
- **Joe Mockler**  
- **Alexis Chen (Developer)**  

## Semester
**Fall 2024**

## Project Overview
**Reward shaping** is a technique used in reinforcement learning (RL) to modify or "shape" the reward signal that an agent receives during training. The goal is to make learning more efficient by providing additional feedback that guides the agent toward desired behavior.  
  
The agent is given intermediate rewards that are related to the task's ultimate goals. These rewards are designed to encourage the agent to take actions that are expected to lead to better outcomes in the long run.

## Files in the Repository

### 1. `speeds.csv`
This csv file contains speed data used for reward calculation.

### 2. `speedlimit.py`
This script defines the reward shaping strategy and visualizes the rewards overtime using graphs as an output.

#### Key functions:
**`calculateReward(speed)`**: Calculates the incremental and cumulative reward based on the speed data in the speeds.csv file.  
**Visualization**: Plots both incremental and cumulative rewards over time.

### 3. `speedsandterrain.csv`
This csv file contains both speed and terrain data used for reward calculation.

### 4. `speedandterrain.py`
This script builds onto speedlimit.py and incorporates terrain data as a part of the reward shaping strategy. It also visualizes the rewards using graphs as an output.

#### Key functions:
**`calculateReward(speed, terrain)`**: Calculates the incremental and cumulative reward based on speed and terrain data in the speedsandterrain.csv file.  
**Visualization**: Plots both incremental and cumulative rewards over time.
