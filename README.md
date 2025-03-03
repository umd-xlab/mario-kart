# Qualifying Autonomous Systems: Learning from Mario Kart for Robust Safety

## Members
- Kristy Sakano at kvsakano@umd.edu
- Alexis Chen, undergraduate research assistant
- Joe Mockler at jmockle1@umd.edu
- Dr. Mumu Xu at mumu@umd.edu


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
    2. num_timesteps is equivalent to total_timesteps. [This stack overflow answer](https://stackoverflow.com/questions/56700948/understanding-the-total-timesteps-parameter-in-stable-baselines-models) details why we sometimes go over the expected number here.
    3. Also, *"PPO/A2C and derivates collect n_steps * n_envs of experience before performing an update, so if you want to have exactly total_timesteps you will need to adjust those values"* from [this response on Github](https://github.com/DLR-RM/stable-baselines3/issues/1150).

### Test the agent & generate traces
1. Ensure that the model was trained sufficiently. You should see a new folder created called `mario-kart/OUTPUT` created after training the agent. Within it, you should have a new sub-folder titled `SuperMarioKart-UMD-[DATE]` and within it, a `.zip` file indicates that the model was trained successfully.
2. Run the `mario-kart/ppo_mariokart_evaluation.py` file with this command `python3 ppo_mariokart_evaluataion.py --date=[MM-DD_HH-MM-SS] --steps=[STEPS]`. Please fill in the boxes and remove the brackets with the appropirate date and number of steps.
    1. The current reward structure will be copied and saved into the output directory.
    2. The default number agents of agents used in the test will be 8. This can be edited in LIne 118.
4. Git add, commit, and push to Github with commentary, if applicable.

### Training Evaluation with Tensorboard
We're using Tensorboard to evaluate the training post-hoc. With a given training .tfevents data set, you can check the cumulative rewards / episode to ensure convergence. To install and run...
1. Install tensorflow (contains tensorboard) if not already done. `pip install tensorflow`
2. Put the .tfevents file in an accessible folder with NO spaces in the file path
3. Open your python (or cmd) terminal and run `tensorboard.main --logdir`
4. Then open `http://localhost:6006/` (or whatever localhost is recommended by tensorboard) in your browser. This should be the board to inspect data!

## External Links

### Relevant Repositories
This project uses contributions from three different repositories. Installation instructions are found in their respective repositories. Please add these directories to the `mario-kart` repository, but add both `stable-retro` and `stable-retro-scripts` to your `.gitignore`. 

1. [Stable Retro](https://github.com/Farama-Foundation/stable-retro) is maintained by Farama-Foundation. Follow the instructions in the ReadMe to install.

2. [Stable Retro Scripts](https://github.com/MatPoliquin/stable-retro-scripts) is maintained by Matt Poliquin. Follow the instructions in the ReadMe to install. This requires Stable Retro. 

3. [gym-SuperMarioKart-Snes](https://github.com/esteveste/gym-SuperMarioKart-Snes/tree/master/SuperMarioKart-Snes) is a repo that has the MarioKart ROM files. 

4. (TBA) Links to TELEX.

### Relevant Documentation

1. [StableBaselines3 PPO webpage](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html) details the PPO algorithm we are using within our RL agent. They have example links to other websites and examples that are worth checking out.
    1. [OpenAI also has a blog on PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html) which is pretty handy. 
2. [Gymnasium Documentation](https://gymnasium.farama.org/) is the interface we are using. It was originally called Gym and maintained by OpenAI, but they semi-retired the project and Farama Foundation picked it up to provide long-term support and maintenance. It's important to note that we are still using v0.21 and not v1.0.0 so some of the documentation might be slightly different, so if you notice anything strange, check out their Migration Guide.
    1. You can also read OpenAI's gym documentation, but it is out-of-date and the website recommends reading the Gymnasium documentation instead.
3. [Stable-Retro documentation](https://stable-retro.farama.org/main/getting_started/) is also very useful. Gymnasium hosts a bunch of different software but this one is the one we're using; it emulates older video games & let's us train them with RL.

## Relevant Links
We also maintain a UMD Box link, accessible [here](https://umd.box.com/s/oiczfapf2b8jzxm2qamwohcay9aralsf). If you do not have access, contact one of the researchers listed above.

## Useful packages
See the `requirements.txt` for relevant packages.

## Q&A

**"Do you know how to change stuff like the discount factor and epsilon in the RL training?"** 
This information is encoded within models.py  between lines 41-50. The entropy coefficient determines the exploration-exploitation trade-off. The default discount factor/gamma is set to be 0.99 but can be edited/added in this snippet to be altered. PPO doesn't have an epsilon per se, but there is a clipping parameter that prevents excessively large policy updates. It is set to a default of 0.2 but can also be edited/added in this snippet to be something different.

**"When the agent is evaluated, which NN controller is actually evaluated? I'm assuming the one achieving the highest reward during training?"** 
From my understanding, PPO does not track and save the 'best' model in terms of reward. Instead, it uses the most recent or current policy network, which isn't necessarily the one that achieved the highest reward during training. We can change this though - we can use a callback during training tos ave models whenever a new highest reward is reached. See Callback documentation here.
- Note: callbacks aren't common in PPO because it is an on-policy algorithm ie the the policy is always being updated, and older models aren't always useful as they're used on out-of-date information. PPO is focused on stability over immediate high scores, trying to find a balance between learning stability and performance. The highest observed reward might be because of lucky exploration rather than a reliable strategy. I suppose this matters more in dynamic environments versus our static environment, but still something to consider.
- We also want to avoid overfitting our model to the data, which is when our model is REALLY good at operating on the data we're feeding into the AI, but when you give it something slightly different, it struggles to adapt.