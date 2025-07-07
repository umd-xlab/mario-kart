
# August 2024

## August 26th, 2024

Objectives of Meeting:
- Inform Mumu that I left my job
	- Discuss past proposals and how I can recycle them for the future?
- Talk about my planned Fellowship applications
	- Pull up Excel Sheet with the three listed fellowships this fall.
	- Discuss the proposal for the NDSEG fellowship.
- Discuss the project structure and goals for this year
- Discuss the classes I'm taking and how I'm being funded this year (but would eventually like to pivot away from being a TA)

Look ahead to tasks:
- Send Mumu a copy of my fellowship applications within 1-2 weeks

# September 2024

## September 9th, 2024

Objectives of Meeting:
1. Go over NDSEG essay
	1. Give timeline for fellowship deadlines
		1. Point Foundation is due 10/24, but the webpage opens tomorrow with a list of requirements.
		2. PDSoros is due 10/30
		3. NDSEG is due 11/01
			1. Very clear about bullet points, in the beginning of the essay to make a clear statement: I want to focus on human-centered AI research in the beginning
		4. Amelia Earhart Fellowship is due 11/15
		5. Graduate Fellowship for STEM Diversity is due 12/27
		6. Link Foundation is due late January
2. Go over current research aims for the NAWCAD project
	1. Consider a meeting with Mumu, Joe, and myself to be on the same page before talking with George again
	2. Let's finalize a broad question we're asking this week after working through some of the comments from [[General Meeting Notes for FY24 & FY25#09/04/2024]]
		1. Then work on more specific questions, our objective, and lastly our approach by the end of October.
3. Mention that prescription safety glasses are available for all researchers through the Laboratory Safety program. 

I'm interested in the intersection of explainable AI, information communication, and system safety.
- Inspired by reading some papers in the Journal of System Safety (from the International System Safety Society)
- They make a great case for a risk assessment matrix on the 8th page of the 2023: Assessing the Safety of Intelligent Systems
	- *"A risk statement in place of a conventional risk value would likely be perceived differently by the stakeholder community. Some individuals, interpreting the risk to be important while others interpreting the risk as low consequence. Conventional risk rankings ensure all stakeholders interpret threats equally by use of an agreed to risk assessment matrix."*
- Relevant Links: https://jsystemsafety.com/index.php/jss/issue/archive (Journal of System Safety archive)

## September 16th & 18th
Objectives of Meeting
- Discuss the CNN paper & interactive page that I found.
- Go over Fellowship Essay(s)
	- Query: does Mumu prefer being addressed as Prof or Dr?
- Discuss our next research objective (after meeting with George)
# October 2024
Not much happened here. I presented to the group on October 9th, presentation below:

![[Oct 9th Presentation to Group Meeting.pptx]]

 We organized what our plan will be, and Joe claimed the "Identify Cascading Failures & Construct Local Specifications for Scenario" side of the circle, while I have the "Simulate Scenario & Collect Performance Data" side.

![[Pasted image 20241104142451.png|500]]

Alexis the undergraduate asked to join the project after my presentation, and I & Joe talked to her about the project & I sent her some material on Slack to start reading. We worked to get her set up with Github and she created our repository that we'll use for the project.

I started looking into getting a simulation engine up and running, and ran into a lot of roadblocks. I finally settled on OpenAI's Retro Games.

# November 2024

## November 4th and 6th
Great news, I ended up getting OpenAI's Retro Games -> Stable-Retro up and running on 11/04!
- It currently 'works' for a different game, so my next task is to get it up and running for Mario Kart
- I need to wipe the downstairs computer and install Stable-Retro on it (this will be done by 11/08 so I can show Alexis it, and show her how to push it to her own branch.)

I probably should make a write-up of everything I needed, but tbh, I patched so much I'm not even sure. I'll probably add it to our ReadMe at some point in the future.

Currently planning on attending the SOMD event (Autonomy Summit) on November 14th. 

Mumu asked me to give a lecture on Nov 18/20 about machine learning and aerospace engineering, as it pertains to our work here. I haven't put much thought into it but I'll get a copy of the slides draft to her by Monday Nov 11th!

I factory reset the Mac in the downstairs lab and created a new profile called 'X Lab' with a corresponding password 'xlab' (no spaces or dashes)
- It was originally at El Capitan, but I decided to update the OS. The internet suggested I update to High Sierra first, and then 

# December 2024
Meeting with Calin, Calin's grad student, Joe, and myself on 12/10/2024
- Goal: figure out what technical areas they want to do research in
- Maybe hypothesize motivation or project ideas? Mumu recommends starting with a scenario first

Scenario 1: ???
- Method: Statistical STL

Scenario 2: Experiencing Unknown-unknown or unknown-known hazards
- Method: Transfer Learning
- Mumu mentioned a recent discussion where they motivated transfer learning
- We could categorize theory (?) to create a framework of transfer of knowledge
- "If we train on rocks, will the system be able to adapt to avoid boulders?"

Scenario 3: Slowly changing environments over long periods of time
- Method: Generating Rules for Rules
- "If we live in Texas, do we need snow-related hazard rules? Or can we check much less frequently, and what frequency is appropriate?"

Scenario 4: Deploying an AI that updates its STL rules over time
- Method: Continuous learning
- "Our environment is constantly changing - can we update our STL rules while deployed?"

George Discussion:
1. Probability for risk analysis: We are likely advertising our product to NAVY operators who are acquiring contractor-based technology
2. "After hitting a rock, we know that 50% of the time we will recover, but 50% of the time, we'll go off a cliff."
3. Goal: merge probability distribution and specifications
4. By testing our system over a range of specifications (tightening and loosening them, such as varying speed limits), we can see a probability distribution of hazards, ie: the most hazards centered around 40 mph speed limits.

# February 2024

### 02/13/2025

**Inter-Group Meetings:** We've been meeting regularly with Dr. Calin Belta and his post-doc, Andy. The upcoming meeting this Friday (02/14/2025) will have them present to us (Mumu, George, Joe, and myself) current work that is being conducted in ML & STL. This was motivated by our last conversation, which was difficult when we didn't have any knowledge of current/ongoing work in this area. 

**Recent Literature:** Mumu asked me to look into some recent literature in the areas of specification mining in actual hardware (TurtleBots?) and NLP for translating human readable rules to STL (ChuChu Fan from MIT)
- The TurtleBots are maintained by UMD's MRC, and we'll need to complete training on it before we can execute.
- We'll also need ROS experience, which I currently lack.
- I'm going to self-evaluate this as a ❗/5.

**Bug Log:** Stable Retro is showing some bugs. For some reason, half of our agents are 'dying out' during training. This is truncating our training time. A good idea is to get TensorBoard up and running to record when training. This has an urgency of a ❗❗❗/5.

I updated the README with some new documentation on how to run this project. This was an urgency of ❗/5.

**Paper Submissions:** We recently submitted to ICUAS! We were able to successfully submit on 02/07/2025. Dr. Costello helped us with the submission process. The conference will be in Charlotte in early May.

Alexis (the undergraduate) and I have been working together to get the code up and running! We've been working together most Tu/Thur every week at 11 am.
- I'm hopeful that she'll be able to run the experiments for us in a few weeks. 
- She might also be interested in working on/with the hardware. 

The Github has been updated with our current code version. This was an urgency of ❗❗/5.

### 02/17/2025 & 02/19/2025
**Inter-Group Meetings**: I was asked to draft a presentation about explainability for the next meeting (02/28/2025).  George called and said he wanted to do a presentation on interpretability instead. I think it's a good idea to have a backup set of slides just in case, so I'll go ahead and draft something.

**Recent Literature**: Haven't gotten a chance to doing this yet T_T

**Bug Log & Coding Woes:** Joe figured out how to start logging things on Tensorboard. Great news! 
- I updated the post-processing script so Alexis can run it too. She recently got SuperMarioKart working on her computer (good news!) so she can now run experiments for us!
- The ReadMe has been updated with general info, but needs instructions on how to run the post-processing script.

**Grad Offer visit** on March 7th with two potential incoming PhD students
- One student will be able to attend, the other cannot.

**During weekly presentations:** Answer high vision questions (what is it/why do we care)
- Emphasizing motivation & explainability of project.
- Use this to track changes of wording/project over the course of the semester
- Make a webpage tutorial for everyone.

**Github Access Coin**: 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

#### 02/24/2025
**Inter-Group Meetings** I need to draft a talk on explainability and send it to Mumu by tomorrow evening

**Bug Log & Coding Woes**
- Need to figure out Tensorboard by 3 PM to teach it to Alexis
- Working on getting Lenny up and running
- Talk with Nitya/Nathalie about clusters