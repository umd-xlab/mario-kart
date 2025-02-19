# Qualifying Autonomous Systems: Learning from Mario Kart for Robust Safety

## Members
- Kristy Sakano at kvsakano@umd.edu
- Alexis Chen, undergraduate research assistant
- Joe Mockler at jmockle1@umd.edu
- Dr. Mumu Xu at mumu@umd.edu

## Contents
This project uses contributions from three different repositories. Installation instructions are found in their respective repositories. Please add these directories to the `mario-kart` repository, but add both `stable-retro` and `stable-retro-scripts` to your `.gitignore`. 

1. [Stable Retro](https://github.com/Farama-Foundation/stable-retro) is maintained by Farama-Foundation. Follow the instructions in the ReadMe to install.

2. [Stable Retro Scripts](https://github.com/MatPoliquin/stable-retro-scripts) is maintained by Matt Poliquin. Follow the instructions in the ReadMe to install. This requires Stable Retro. 

3. [gym-SuperMarioKart-Snes](https://github.com/esteveste/gym-SuperMarioKart-Snes/tree/master/SuperMarioKart-Snes) is a repo that has the MarioKart ROM files. 

4. (TBA) Links to TELEX.

## How to Install

[This youtube video](https://www.youtube.com/watch?v=vPnJiUR21Og&t=423s&ab_channel=videogames.ai) created by Matt is very helpful for installing Stable Retro.

Reach out to one of the developers if you have any questions.

### Common Installation Issues
1. `No module named retro._retro`: Consider re-running `pip install -e .` in the stable-retro directory.
2. `AttributeError: module 'retro' has no attribute 'Actions'`: Try removing the repository and and recloning it from Github. Do a clean install with `pip3 install -e .`.
    1. Alternatively, `pip3 install git+https://github.com/Farama-Foundation/stable-retro.git` may have worked; code taken from Stable-Retro's recommendations.

## Relevant Code

### Examine the game in interactive mode
1. In `mario-kart/stable-retro`, run `./gym-retro-integration`
2. In the Game drop-down menu, click **Load Game** navigate to your `SuperMarioKart-UMD` folder and select `rom.sha `.
3. You can start the game from the beginning loading screen, or you can load in the game at a specified start location (after the loading screen). This is known as a **state**. To do the latter, in the Game drop-down menu, click **Load State** and navigate to the state you'd like to open within the `SuperMarioKart-UMD` folder. Look for a file with the suffix `.state`.
4. The old reward structure was able to be edited within this GUI. You can edit it by opening the Data drop-down menu and clicking **Load Scenario**. However, we switched to scripting the reward structure and you can edit it outside of the GUI. (I recommend using VS Code or another similar code editor to edit the reward file directly. It is called `script.lua`.)
5. You can examine the various variables with the right-hand menu. It may also be useful to observe when the scenario is 'Done' for the ending condition. 

### Train the RL agent
1. Ensure that your reward structure in `mario-kart/stable-retro/retro/data/stable/SuperMarioKart-UMD/script.lua` is appropirate for the scenario you are trying to run.
2. Ensure that you have the right parameters set up for your model to start training in `mario-kart/stable-retro-scripts/models.py`.
3. Train your agent from the `mario-kart/stable-retro-scripts/` directory. Run `python3 model_trainer.py --env=SuperMarioKart-UMD --num_timesteps=[INSERT THE NUMBER OF TIMESTEPS YOU WANT] --num_env=[INSERT THE NUMBER OF ENVS YOU WANT] --play`
    1. We recommend using between 4-8 agents and at least 10,000 timesteps. A higher number of timesteps is necessary for training longer sections of the map.

### Test the agent & generate traces
1. Ensure that the model was trained sufficiently. You should see a new folder created called `mario-kart/OUTPUT` created after training the agent. Within it, you should have a new sub-folder titled `SuperMarioKart-UMD-[DATE]` and within it, a `.zip` file indicates that the model was trained successfully.
2. Run the `mario-kart/ppo_mariokart_evaluation.py` file with this command `python3 ppo_mariokart_evaluataion.py --date=[MM-DD_HH-MM-SS] --steps=[STEPS]`. Please fill in the boxes and remove the brackets with the appropirate date and number of steps.
3. Don't forget to copy your reward structure into the `mario-kart/OUTPUT/SuperMarioKart-UMD-[DATE]` folder.
4. Git add, commit, and push to Github with commentary, if applicable.

### Training Evaluation with Tensorboard
We're using Tensorboard to evaluate the training post-hoc. With a given training .tfevents data set, you can check the cumulative rewards / episode to ensure convergence. To install and run...
1. Install tensorflow (contains tensorboard) if not already done. `pip install tensorflow`
2. Put the .tfevents file in an accessible folder with NO spaces in the file path
3. Open your python (or cmd) terminal and run `tensorboard.main --logdir`
4. Then open `http://localhost:6006/` (or whatever localhost is recommended by tensorboard) in your browser. This should be the board to inspect data!

## Relevant Links
We also maintain a UMD Box link, accessible [here](https://umd.box.com/s/oiczfapf2b8jzxm2qamwohcay9aralsf). If you do not have access, contact one of the researchers listed above.

## Useful packages
See the `requirements.txt` for relevant packages.

# Reward Shaping  
The agent is given intermediate rewards that are related to the task's ultimate goals. These rewards are designed to encourage the agent to take actions that are expected to lead to better outcomes in the long run.
