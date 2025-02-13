# Qualifying Autonomous Systems: Learning from Mario Kart for Robust Safety

## Members
- Kristy Sakano at kvsakano@umd.edu
- Alexis Chen, undergraduate research assistant
- Joe Mockler at jmockle1@umd.edu
- Dr. Mumu Xu at mumu@umd.edu

## Contents
This folder has submodules pointing to three different Githubs. 

1. [Stable Retro](https://github.com/Farama-Foundation/stable-retro) is maintained by Farama-Foundation. Follow the instructions in the ReadMe to install.

2. [Stable Retro Scripts](https://github.com/MatPoliquin/stable-retro-scripts) is maintained by Matt Poliquin. Follow the instructions in the ReadMe to install. This requires Stable Retro. 

3. [gym-SuperMarioKart-Snes](https://github.com/esteveste/gym-SuperMarioKart-Snes/tree/master/SuperMarioKart-Snes) is a repo that has the MarioKart ROM files. 

4. (TBA) Links to TELEX.

## How to Install

[This youtube video](https://www.youtube.com/watch?v=vPnJiUR21Og&t=423s&ab_channel=videogames.ai) created by Matt is very helpful for installing Stable Retro.

Reach out to one of the developers if you have any questions.

## Relevant Code

### Train the agent
1. Ensure that your reward structure in `mario-kart/stable-retro/retro/data/stable/SuperMarioKart-UMD/script.lua` is appropirate for the scenario you are trying to run.
2. Ensure that you have the right parameters set up for your model to start training in `mario-kart/stable-retro-scripts/models.py`.
3. Train your agent from the `mario-kart/stable-retro-scripts/` directory. Run `python3 model_trainer.py --env=SuperMarioKart-UMD --num_timesteps=[INSERT THE NUMBER OF TIMESTEPS YOU WANT] --num_env=[INSERT THE NUMBER OF ENVS YOU WANT] --play`
    1. We recommend using between 4-8 agents and at least 10,000 timesteps. A higher number of timesteps is necessary for training longer sections of the map.

### Test the agent & generate traces
1. Ensure that the model was trained sufficiently. You should see a new folder created called `mario-kart/OUTPUT` created after training the agent. Within it, you should have a new sub-folder titled `SuperMarioKart-UMD-[DATE]` and within it, a `.zip` file indicates that the model was trained successfully.
2. Run the `mario-kart/ppo_mariokart_evaluation.py` file. Make sure to change the input file to the model you are trying to generate a trace for.
3. Don't forget to copy your reward structure into the `mario-kart/OUTPUT/SuperMarioKart-UMD-[DATE]` folder.
4. Git add, commit, and push to Github with commentary, if applicable.

## Relevant Links
We also maintain a UMD Box link, accessible [here](https://umd.box.com/s/oiczfapf2b8jzxm2qamwohcay9aralsf). If you do not have access, contact one of the researchers listed above.


# Reward Shaping  
The agent is given intermediate rewards that are related to the task's ultimate goals. These rewards are designed to encourage the agent to take actions that are expected to lead to better outcomes in the long run.
