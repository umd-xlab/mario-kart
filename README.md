# Qualifying Autonomous Systems: Learning from Mario Kart for Robust Safety
Data processing and STL analysis script as apart of broader project to strategically design RL systems for requirement-based regulation. This branch performs two main functions:
1.  It accepts the RL system output data (csv with list entries),converts it to a csv, and is processed in MATLAB. This processing computes pertinent state data from the extracted time series, plots the data, and outputs as a new csv that may be accepted by TeLEx.
2.  This local copy of TeLEx reads the csv and determines STL parameters fitting a provided formula template using a tightness metric. This is an implementation of Jha et al.'s work: [*TeLEx: learning signal temporal logic from positive examples using tightness metric*](https://link.springer.com/article/10.1007/s10703-019-00332-1), 2019.

## Steps to extract STL formulae
1.  First, run the RL algorithm on the other branches and evaluate the DNN controller; the result should be a csv of lists. See other branches for successfully training and running the RL algorithm.
2.  Now, put the data in `.\Analysis\Data Processing\Data` folder and rename line 10 of `csv.parse.py` with the updated data file name.
    1.  Run this script.
    2.  The data will be split into the individual evaluations and dumped into `parsed_agent_data` subfolder as csv's with individual entries.
    3.  This OVERWRITES the existing data in `parsed_agent_data`!
3.  Open MATLAB set the working directory to the pwd. Run the script.
    1.  Plots showcasing the state data and the processed state data (velocity, heading angle, accelerations) are created. Time derivatives are taken with 2nd order schemes, and heading angle is computed from a smoothed velocity.
    2.  Script also calculates the expected reward from the trace, but confirm that the `reward_calc.m` file corroborates your reward script first for an accurate calculation!
    3.  Finally, the processed data is exported to a TeLEx-friendly format with `export_telex.m`. You must supply this function with the data you plan to use in the STL mining. Similarly, you provide csv headers for the STL mining, so confirm these match the parameters you plan to reason over in step 4!
4.  Mining the STL parameters.
    1.  Set your working directory to the SUBFOLDER TeLEX
    2.  Put the exported telex csv file (step 3.3) in the subfolder `udacityData`. Rename this file to `steering1p.csv` and delete the existing file
    3.  Open `test_udacity.py` and run the script!
    4.  You can confirm your implementation (using the provided `steering1p.csv` file) against the results below. Optimization time may vary slightly, but should be in appropriate order of magnitude:
```
G[0, 72] ( ((phidot > 0.5)|(phidot < -0.5)) -> speed < a? 0;80)
 Synthesized STL formula: G[0.0,72.0](((phidot > 0.5)  Synthesized STL formula: G[0.0,72.0](((phidot > 0.5)  S S Synth S S Synthesized STL formula: G[0.0,72.0](((phidot > 0.5) | (phidot < -0.5)) => (speed < 39.619140625))
 Optimization time: 0.04790210723876953
 Optimization time: 0.04790210723876953

Test result of synthesized STL on each trace: [True]
 Robustness Metric Value: [0.002574920654296875]
```

