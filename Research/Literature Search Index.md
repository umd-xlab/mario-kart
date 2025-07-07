
**Donze, Alexandre. On Signal Temporal Logic. (2014) Lecture Notes**![[Donze, STL Berkeley Lecture.pdf]]
1. Most intuitive logic is Linear Temporal Logic (LTL) which pertains to discrete sequence of states.
	1. Evaluated on a sequence, e.g. $w = aaabbaaa....$ and at each step of $w$, we can define a truth value.
	2. ![[Pasted image 20231229192720.png|400]]
2. LTL formula is known as $\varphi$  , we evaluate it on a sequence $w$, and the atoms are symbols $a, b$. 
	1. We may also call $w$ as a system $M$ with a property $\varphi$. Then, we may have $M \rightarrow aaaabbbaa...$ and $\varphi \rightarrow 111000$. 
	2. Model-Checking (<font color="#00b050">Slide 6</font>) is to prove that $M \models \varphi$ aka M models $\varphi$, or that it semantically entails $\varphi$. 
	3. Monitoring is computing $\chi ^\varphi (w, 0)$ for finite sets of $w$
	4. Remark is statistics model checking, or doing statistics on $\chi ^\varphi (w, 0)$ for populations of $w$
3. We want to move from discrete-time discrete systems to hybrid (discrete-continuous) systems.
	1. Therefore, we move from LTL to STL. This is an extension of LTL with real-time and real-valued constraints. (<font color="#00b050">Slide 9</font>)
	2. LTL is $G(r \rightarrow F g)$ Boolean predicates, discrete-time
	3. STL is $G(x[t] > 0 \rightarrow F_{[0, 0.5s]} y[t] > 0)$ Predicates over real values, real-time
4. General syntax.... F means until, G means always.
5. Parametric STL uses stand-in variables like $\tau$ and $\pi$ in place of real numbers. (<font color="#00b050">Slide 30</font>)
	1. Example: After 2 seconds, the signal never goes above 3. After $\tau$ seconds, the signal never goes above $\pi$. 
	2. Tight valuation function: there exists a valuation $v'$ in a $\delta$-close neighborhood of $v$, with $\delta$ 'small' (within some tolerance)


----

**Puranik and Mavris. Anomaly Detection in General Aviation Operations Using Energy Metrics and Flight Data Records. (2018)**
![[Puranik, Anomaly detection in general aviation operation using energy metrics.pdf]]
1. Motivation: Previously, accidents are the triggers for identifying problems & developing mitigation strategies
	1. Industry desires a pro-active approach in which potential unsafe events are identified beforehand, and mitigation strategies are implemented.
	2. Defining the Method: energy state awareness and energy management
		1. Existing method: 'exceedances' - useful for pre-defined events but not for others.
		2. Consider: data mining for safety analysis, incident examination, and fault detection
		3. Combine clustering & one-class classification algorithms
	3. Note: anomalous or abnormal flights != unsafe flights. The main purpose is to identify the anomalies, not to determine/understand unsafe practices
2. Challenges: aviation data is unlabeled (consider unsupervised or semi-supervised)
	1. Authors considered clustering as it allows the possibility of multiple standard patterns
	2. One-class learning algorithms for outlier detection (Local Outlier Factor?)
3. Methodology:
	4. ![[Pasted image 20240106152044.png]]
4. Experiments: Verification was conducted through a simulated anomalous approach & landing.
	1. GA operations include heterogeneity due to uncertain weather conditions, but we cannot differentiate between purely weather-induced anomalies & those due to piloting procedures due to the unavailability of weather data.
5. How Can We Use This?
	1. The authors had access to multi-parametric time series data of a number of parameters (altitude, pitch angle, RPM, Kinetic Energy/Potential Energy/Total Energy) which is more than the flight paths we're given
	2. Anomalies were identified by different feature vector options but overlapped 
	3. The author provided a literature survey of other approaches (supervised & unsupervised)