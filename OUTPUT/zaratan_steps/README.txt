This folder comprises of a few models trained on Zaratan. The purpose of this is to see if the number of steps the model trains for has a significant effect on the trace output(s). Specifically, what is the minimum number of steps we need to train for our scenario to have a reasonable output?

Specifically, we are training: 100k steps, 500k steps, 1 million steps, and 1.5 million steps.


After 500k steps, we implemented a callback to save the best model (EvalCallback) in addition to the PPO2 returned model.
