## January 2024

I want to use the [LTLf2DFA](https://pypi.org/project/ltlf2dfa/) package. I followed the pip instructions to install this package.

It is predicated on installing [MONA](https://www.brics.dk/mona/index.html) which requires a C compiler. Using WSL2, we don't need a C compiler and I was able to install it directly.

#### Basic Instructions on using WSL (Windows Subsystem for LInux)

1. Either open WSL or open Windows Powershell and "Alt +" Ubuntu to open it in a side-by-side
2. cd /mnt

#### LTLf2DFA
**INPUT TO LTLf2DFA**:  G( run_algorithm -> (F detected -> G start_mitigation))

**OUTPUT OF LTLf2DFA:** 

digraph MONA_DFA {
 rankdir = LR;
 center = true;
 size = "7.5,10.5";
 edge [fontname = Courier];
 node [height = .5, width = .5];
 node [shape = doublecircle]; 1; 2; 3; 5;
 node [shape = circle]; 1;
 init [shape = plaintext, label = ""];
 init -> 1;
 1 -> 1 [label="~run_algorithm"];
 1 -> 2 [label="run_algorithm & ~detected & ~start_mitigation"];
 1 -> 3 [label="run_algorithm & start_mitigation & ~detected"];
 1 -> 4 [label="detected & run_algorithm & ~start_mitigation"];
 1 -> 5 [label="detected & run_algorithm & start_mitigation"];
 2 -> 2 [label="~detected"];
 2 -> 4 [label="detected"];
 3 -> 2 [label="~detected & ~start_mitigation"];
 3 -> 3 [label="start_mitigation & ~detected"];
 3 -> 4 [label="detected & ~start_mitigation"];
 3 -> 5 [label="detected & start_mitigation"];
 4 -> 4 [label="true"];
 5 -> 4 [label="~start_mitigation"];
 5 -> 5 [label="start_mitigation"];
}

---
**NISE Project Pitch Ideas** 
1. Since we're creating a LTL -> automata -> Behavior Tree pipeline, consider the challenge of creating LTL prompts in the beginning.
	1. I've been using ChatGPT to generate LTL prompts from my casual English prompts, and minimally refining them. 
	2. Suggest: use a LLM (likely offline Llama-Recipes or Llama 2) to generate LTL prompts from casual English prompts for anomaly detection via formal methods (behavior trees)

## February 2024

### February 5th

**Pre-Meeting Thoughts**
I've spent a lot of time debugging the LTL2fDFA and in the end, I don't think the Deterministic Finite Automaton (DFA) is an appropriate automaton for the automaton. From my preliminary research, DFAs describe and recognize patterns in strings or sequences. I've considered switching to Buchi Automaton, and here's my rationale why:
- Buchi Automaton are used to handle infinite sequences of symbols, and express and verify temporal properties in systems. They have terminology to express and verify properties such as 'always', 'eventually', and 'until'
- Buchi Automatons' transition function can be non-deterministic, allowing for multiple possible transitions from a state based on the input symbol.
- DFAs are used in parsing and regular expression matching, or for modeling & recognizing patterns in languages. Buchi Automata is specifically for model checking, formal verification, and the analysis of reactive systems.
- CONS: Buchi automata are designed for infinite sequences of states and expressing temporal logic properties. Aka we aren't necessarily waiting 'until' something happens, we're more so looking at what happens over an infinite amount of time. They are suitable for capturing patterns where certain properties should occur infinite often in a sequence (and if we're doing anomaly detection, that doesn't usually happen).
	- Relies on the presence of specific states being visited infinitely often.

I'm also consider switching to a Rabin Automaton. Here's my rationale why:
- My LTL formula may include properties such as 'until' (U) or 'release' (R). 
	- Release (a R B) means that b is true until a becomes true, or b is true forever.
- They are more expressive and flexible, allowing for the specification of temporal logic properties that involve both 'eventually' and 'globally' conditions simultaneously.
- Sensor errors on perception level. 

**Post-Meeting Thoughts**
Regarding the presentation: Throw everything up on a set of slides to have a conversation & brainstorm ideas and future directions. Where do I think is the most beneficial? 
- Getting feedback is my primary goal.
- I know what are my next immediate steps, what makes that approach (or addressing this problem) an interesting problem that would advance the field. Consider providing the background about what makes it significant, and we can have a discussion about what makes it significant. 

Regarding research:
- Consider first moving to Rabin Automaton, but know that Mumu has more experience with Buchi Automaton.
- These three are the biggest automatons used right now, and there's not a good alternative to the three.
- Mumu has more experience with Buchi because Rabin Automaton experiences the synthesis problem - aka, during generation of Buchi automaton with LTL controls, it may not necessarily solve in polynomial time because of the # of state spaces exploding. 


### February 12th

**Pre-Meeting Notes**
Based on my brief exploration, I see there are two main LTL to deterministic Rabin automatons:
- Rabinizer3
- ltl2dstar 
- Both of which are commandline automaton translators

I did find one more, called ltl2tgba which is converting LTL to Buchi, and does have python integration. 

Summary, 1 paragraph, to Mumu by Monday. Talking about our research aims & goals for the rest of the year. Speak about next 5 years' worth of work.

I am creating a pipeline converting formal language logic - specifically Linear Temporal Language (LTL) - to behavior trees, with the intention of automating a behavior tree generator for safety detection of unmanned aircrafts. Behavior trees have been previously evaluated in simulation-driven case studies for anomaly detection, and as they are more intuitive and have less complex formulative (akin to human cognition), they are more interpretable by operators. The eventual goal is to leverage NLP and an operation-specific (mission-specific) LLM to convert human language from operators dictating mission and safety parameters into a Detection & Mitigation BT. The overall goal is to improve safety of the system during challenging unmanned missions such as operations in comms denied environments. This leads into my current research interests of verification & validation (V&V) and safety research of autonomous systems, including - but not limited to - task allocation, coverage and mapping, and anomaly detection and handling. 

- - -

Automating decision-making and Verification & Validation (V&V) algorithms may lead to more robust, reactive, and comprehensive analysis of autonomous flight systems across a myriad of fields. One such scenario of interest may be in a communications denied environment, in where operator-provided instructions may not be received by the autonomous UAV, or swarm of UAVs. Therefore, it is important to construct and deploy systems that are robustly evaluated through mathematically rigorous model testing, such as through Detection and Mitigation Behavior Trees, that can operate independently and autonomously from a human operator. As mission parameters may shift and update with new sensed data, multi-agent systems must continuously adapt and adjust their operations/goals to achieve mission success, or adjust their flight behavior to account for anomalous detections. Future research topics/areas for exploration may include dynamic task allocation of multi-agent systems, anomaly detection & handling, and formal verification of autonomous state systems.


### February 14th
*Note*: I presented my work titled Discussion #1 to the group to generate some feedback & thoughts. Majority of comments were from Mumu, and listed below:

- Consider a video game where you control a Mario character, and from the game, it generates a behavior tree.
	- There is no LTL but it involves a behavior tree.
	- We want to generate the LTL automatically (or come up with it ourselves) and use that to create the behavior tree.

Synthesis paper
- Summary: A comprehensive power management system for electrical aircraft. The summary is to maintain power levels for de-icing. A lot of the specifications are written in LTL.
	- Take the specifications as examples to drive my own behavior tree.
	- For now, ignore the mathematical part, but pay attention to the setup; balancing power for multi-variable constraint. Each sub-system has requirements, etc.
	- Write down all the specifications in this system.

CONOPS
- Consider a nominal scenario where something goes wrong, and write out what is going wrong.
	- Write out what is going wrong & what you would do in English, then we'll work together to write out a LTL.
	- What rules might there be? Can't fly over people, can't fly outside of bounded environment
	- Consider state variables of the scenario.
	- Consider the rules on the state variables.
	- Consider a takeoff or landing for collision-avoidance scenario.


### February 19th
We went over my Excalidraw mockup in the February 14th tab.

1. All variables need to be derived from the rules.
2. Rules may not be all encompassing; it may be an iterative process to refine & create new rules. This may cause smaller variables to pop up.

Next steps:
1. Discretize variables like in the paper.
2. Derive simple LTL examples from the discretized variables
	1. Consider LTL specifications for transitions of state variables as well
	2. Send to Mumu later this week?
3. Read the papers Mumu sent (ignore the receding horizon problem, but the multi-agent problem may be interesting)
4. Write up project pitch idea for NISE

Implementation of a LLM with behavior trees for generating LTL (Linear Temporal Logic) operators
- Maybe extraction of rules first?
- Then extraction to LTL format?

### February 26th & 28th
**What Happened**
- Proposal #1: It appears that the reference I sent (NL2TL: Transforming Natural Languages to Temporal Logics Using LLMs) is a helpful start! They were able to have a proof-of-concept that it is possible, and suggested a way to do model checking to ensure the LTL is correct
	- They did not apply the natural language to more casual language (ie: the interview -> rule generation part), nor to aerospace engineering-related principles.
	- There is still much to add to this problem space! New domain question, greater application to a larger scenario, validation in simulation.
	- Kyle's advice: Long Range Fires, Contested Logistics? Want more AI for mission operations, not business operations.
- Proposal #2: Would STL be better or Metric Temporal Logic (time diversion of LTL, similar to STL. People converge to STL more so than MTL. It's easier to deal with signals, versus next steps, which is baked into the language. )
	- If you have specifications that are more temporal than what LTL can cover
	- For multi-agent it could be a rendezvous, or anything with a hard temporal constraining (within 5 seconds, you need to do something, and if not, you do something else). They're hard to capture with LTL, but you can but you have to play tricks & assume delta time steps if you have multiple clocks going simultaneously.
	- multiple vehicles with different clocks (seconds, miliseconds, etc) whichever is the shortest delta T, everything has to march to that clock and it gets complicated.
	- combination of both will have to account for the small discretization. 
	- Kyle's advice: Contested Logistics, Robust Mission AI or Autonomy Assurance > Model Checking / Proof of Correctness
	- multi agent system, heterogeneous systems
- Proposal #3: robust ai, automatic task allocation. being able to fly at SOMD. which one submit to BAR versus WFD, it would be a strategic growth (time frame is roughly similar), pitching it as we need to build up our own in-house MARL. especially with airwing composition in the future. our case study is this scenario. flip that as a BAR, start with problem & then go to what we'll do. emphasize complex environment w/ a little bit of task allocation. 
- supporting my PhD research. 

Funding allocations: DP3 is $92/hr or $167K for a year and DP4 is $130/hour or $240K
- Project 1 is 0.4MY for me, a DP4. So I am requesting $96K
- Project 2 is the same
- Project 3 is 0.5MY for two DP3s ($167K) and 0.15MY for me, a DP4 ($36K) = $203K
	- RDT&E is $49k per MY


## March 2024
### March 11th

**Next Steps**
- Need to build an environmental conditions table
- Change to the shape notation, no letter notation (which is common in LTL formats)
- Need to specify if 'land' is a boolean or a state, and if so, create definitions for each of these variables/states/booleans.
- Express $[5,\infty]$ in LTL since it's currently not; try a 'next, next, next' as part of a lag.


![[LTL to Behavior Trees Research 2024-02-19 13.06.03.excalidraw]]


Windspeed Notes
- Windspeed depends on the specific weight/construction of the drone 
- [NOAA's National Weather Service](https://www.weather.gov/pqr/wind) breaks down wind speed into 12 categories
- The example in Wongpiromsarn et al. suggest 4 or fewer categories

**The table of altitude as a function of power and windspeed**

![[LTL to Behavior Trees Research 2024-02-26 13.08.59.excalidraw]]

![[LTL to Behavior Trees Research 2024-03-06 15.41.57.excalidraw]]

### March 25th & 27th, 2024
1. I applied to the Autonomy Summit on April 3rd. It coincides with our regular group meeting so the meeting was cancelled.
2. I have not heard back from the Formal Methods Workshop in late May/early June.
3. I'll be out of town the following week (Eclipse trip on April 8th), will attend group meeting on the 10th, but will be gone the rest of the week at a CRA-WP conference.
4. Goals for this week:
	1. Work on the extended abstract submission due April 4th for [SAIV 2024](https://www.aiverification.org/).
	2. Finish Mumu's edits
	3. Download the 1st of 3 packages to tinker with.


## April 2024

### April 15th
We skipped last week's meeting (04/08) because of a solar eclipse! The past few weeks were spent writing an extended abstract for SAIV 2024.

Current goals: re-write the Landing Problem Setup according to the email sent on March 19th with feedback, and start parsing one of the automaton translators.

Group meeting is on for this week & next week, but cancelled after that. Same with one-on-ones.

### April 22nd & 24th
- Was able to get Rabinizer 4 working!
- Next Steps: Understand what Rabin automata actually means :)
	- Notify Mumu via text, get responses via email (her phone: 951-534-4615)
	- Reach out to UMD Matrix Laboratory regarding flight tests
	- Build a script to stop command line running arguments
	- Wait for SAIV 2024 and also full proposals to come through!