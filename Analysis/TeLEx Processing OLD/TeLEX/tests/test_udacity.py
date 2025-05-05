### STL DATA MINING ###
# This script is used to extract the STL parameters from a given formula
# The formula goes in 'templogicdata' below, and follows the conventions from the attached paper
# You MUST put your data in a csv file with formatting from the outputted MATLAB script
# This csv file MUST be renamed to 'steering1p.csv' and put in udacityData subfolder
#######################

import sys
import os 
#sys.path.insert(0, "C:\\Users\Joseph Mockler\Documents\GitHub\mario-kart\Analysis\TeLEx Processing\TeLEX")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import telex
import pandas

# Runs paper example 1 - these formulae were given
#templogicdata =  [
#     'G[0, 220046461440] ( ((angle > 0.2) | (angle < -0.2)) -> (speed < a? 15;25) )',
#     'G[0, 220046461440] ( ((angle > 0.2) | (angle < -0.2)) -> ( (speed < a? 15;25) & (speed > b? -25;-15) ) )',
#]

# Runs paper example 2 - my implementation to check if true
# Upon running - looks like it matches!
# templogicdata = ['G[0, 220046461440] ( ((torque > 1.6)|(torque < -1.6)) -> speed < a? 15;25)']

# Runs paper example 3 - CANNOT reproduce, but by inspection of the data,
# it's not possible to reproduce their results. Maybe they used a different formula/test set?
# templogicdata = ['G[0, 220046461440] ( (angle > 0.06) -> torque > b? -1.5;2)']

# JM - attempt to do STL on our data
# test case 1
templogicdata = ['G[0, 72] ( ((phidot > 0.5)|(phidot < -0.5)) -> speed < a? 0;80)']

# test case 2
#templogicdata = ['F[0, a? 1;70]( speed > 20 )']

# test case 3
#templogicdata = ['G[a? 0;60, b? 10;72](phidot < -0.5)']

def test_stl(tlStr):
    print(tlStr)
    try:
        (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "./tests/udacityData", "gradient")
    except ValueError:
        (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "./tests/udacityData", "nogradient")
    print(" Synthesized STL formula: {}\n Theta Optimal Value: {}\n Optimization time: {}\n".format(stlsyn, value, dur))
    (bres, qres) = telex.synth.verifySTL(stlsyn, "./tests/udacityData")
    print("Test result of synthesized STL on each trace: {}\n Robustness Metric Value: {}\n".format(bres, qres))


def main():
    for templ in templogicdata:
        test_stl(templ)

if __name__ == "__main__":
    main()

