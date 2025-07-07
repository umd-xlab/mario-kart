Christel Baier and Joost-Pieter Katoen

**Why formal methods?** To provide formalisms, techniques, and tools that enable the efficient design of correct & well-functioning systems despite their complexity.
- The 'applied mathematics for modeling and analyzing Information and Communications Technology' (<font color="#00b050">Chapter 1.1</font>)

**What is model checking?** A formal verification technique which allows for desired behavioral properties of a given system to be verified on the basis of a suitable model of the system through systematic inspection of all states of the model. (<font color="#00b050">Foreward</font>)
- Assessing functional properties of information and communication systems.
- Requires a model of the system, a desired property, and then checks whether the model satisfies the property.
- Goal is to check the absence of errors (aka property violations) and can be an effective debugging technique

![[Principles of Model Checking 2024-07-22 13.41.57.excalidraw|1000]]

# Chapter 1: System Verification

**System Verification Definition**: Used to establish that the design/product under consideration possesses certain properties. The properties to be validated are obtained from the system's specification, which prescribes what the system has to do and what not. 
- A defect is found once the system does not fulfill one of the specification's properties.
- The system is found to be 'correct' when it satisfies all properties obtained from its specification.

Two types of **software verification**:
1. Peer Review - uncompiled code is not executed, but analyzed statically.
2. Software testing - testing the software under consideration and providing its compiled code with inputs, called tests. An exhaustive testing of all execution paths is infeasible; in practice, only a small subset of these paths are examined. Testing can only show the presence of errors, not their absence. 

Model-based verification techniques are based on models describing the possible system behavior in a mathematically precise & unambiguous manner.
- These models are accompanied by algorithms that systematically explore all states of the system model.
- Model checking is a verification technique that explores all possible system states in a brute force manner.
	- Given a finite-state model of a system and a formal property, it systematically checks whether this property holds for (a given state in) that model.

1. **Modeling Phase**
	1. Model the system under consideration using the model description language of the model checker at hand
	2. Formalize the property to be checked using the property specification language.
	3. Expressed using finite-state automata, consisting of a finite set of states & a set of transitions
		1. States comprise information about the current values of variables, the previously executed statement, etc.
		2. Transitions describe how the system evolves from one state into another. 
2. **Running Phase**
	1. Run the model checker to check the validity of the property in the system model.
		1. Property specification languages can be temporal logic (an extension of traditional propositional logic with operators that refer to the behavior of systems over time).
3. **Analysis Phase**
	1. Is the property satisfied?
	2. Is the property violated?
	3. Out of memory?

Things that can be checked with temporal specifications:
1. Functional correctness: "Does the system do what it is supposed to do?"
2. Reachability: "Is it possible to end up in a deadlock state?"
3. Safety: "Something bad never happens"
4. Liveness: "Something good will eventually happen"
5. Fairness: "Does, under certain conditions, an event occur repeatedly?"
6. Real-time properties: "Is the system acting in time?"

Types of error:
1. Modeling Error: The model does not reflect the design of the system. We have to get a new model & restart verification, including the previous properties checked by the old model.
2. Design Error: Verification has a negative result and the design (and its model) has to be improved.
3. Property Error: The property does not reflect the informal requirement that it has to be validated. 

# Chapter 2: Modelling Concurrent Systems

### Chapter 2.1 Transition Systems

Transition systems are models that describe the behavior of systems; aka directed graphs where nodes are states and edges are transitions/state changes.

**Remarks on notation**
- Transitions are called 'action names' and denoted with the Greek alphabet $\alpha, \beta, \gamma$
- States are called 'atomic propositions' and denoted with Arabic letters $x, y, z$

A transition system *TS* is a tuple $( S, Act, \rightarrow , I, AP, L )$ where
- *S* is a set of states
- *Act* is a set of actions
- $\rightarrow \subseteq S \times Act \times S$  is a transition relation
- $I \subseteq S$ is a set of initial states
- $AP$ is a set of atomic propositions (which is a smaller subset of $S$ and only pertains to the relevant states in the specific property we're testing)
- $L: S \rightarrow 2^{AP}$ is a labeling function (it relates a set $L(s)$ of atomic propositions to any state $s$.)
And we know that *TS* is finite if *S, Act* and *AP* are finite

Notes: Actions are only necessary for modeling communication mechanisms. IN cases where action are irrelevant, we just use the symbol $\tau$. 

Nondeterministic (aka random) choices serve to model the parallel execution of independent activities by interleaving and to model the conflict situations that arise, such a a scenario where two processes are trying to simultaneously access a shared resource.
- Interleaving: the nondeterministic/random choice of the order in which the order of actions of the processes that run in parallel are executed.
- Nondeterminism is important for abstraction purposes (?), underspecification (early design phases where a coarse model of the system is provided that represents several options of possible behaviors), and to model the interface with an unknown (ie: human user!)

There are two approaches to formalize the visible behavior of a transition system:
1. **Action-based approach**: only the executed actions are observable from outside
2. **State-based approach**: relies on the atomic propositions that hold in the current state to be visible.

The transition relation is defined using the Structured Operational Semantics (SOS) notation. It looks like $\frac{premise}{conclusion}$ and read as if the top proposition holds, then the bottom proposition holds as well. 
- Think of an 'if ..., then ...'

### Chapter 2.2 Parallelism and Communication

Most hardware & software systems have parallel systems in which messages can be transferred either synchronously or asynchronously. 

We want to define an operator $TS = TS_1 \| TS_2 \| ... \| TS_n$ that is a transition system that specifies the behavior of the parallel composition of transition systems $TS_1$ through $TS_n$. 

*Interleaving*: the idea where we weave or interleave independent components with other independent components. The idea is based on a single processor being available on which the actions of the processes are interlocked. It is displayed as ||| or three vertical bars. 

It's important to note that $TS(PG_1 ||| PG_2)$ does not equal $TS(PG_1)||| TS(PG_2)$. 
- This is because  $TS(PG_1 ||| PG_2)$  takes into account the interleaving of program graphs $PG_1$ and $PG_2$. It considers & accounts for actions in these programs that may conflict/interfere with each other when accessing shared variables.
- The latter $TS(PG_1)||| TS(PG_2)$ represents the Cartesian product of the individual transitions systems of $PG_1$ and $PG_2$. It combines the states without accounting for potential conflicts due to shared variables. This can lead to inconsistent or incorrect states.
- Shared variables are often called 'global' variables. 

- **Critical Actions**: Access (inspect or modify) shared variables.
	- *Contention Resolution*: when critical actions from both systems are enabled, the system must resolve which action occurs first.
	- Critical actions cannot execute simultaneously. The order of the execution will affect the outcome.
	- Simultaneous reading can be allowed, but simultaneous modification introduces conflict that must be managed.
- **Noncritical Actions**: Do not affect shared variables, only local variables.
	- Interleaving of noncritical actions can be done without any conflicts!

**Interleaving**: Processes evolve completely autonomously.
Note: To model a parallel system using the interleaving operator for program graphs, it is crucial that the actions (denoted as α and belonging to the set Act) are indivisible. This means that each action cannot be broken down into smaller parts.
- You have to make sure these steps happen sequentially w/o being interrupted by other processes. Like if you're using multiple variables across multiple steps, they can't be interrupted or changed in the middle. 
- You can mark these steps with a single, indivisible action by putting them together under one label. 

**Shared-Variable Programs**: Processes 'communicate' via shared variables. You basically have a variable 'x' that changes values (ie: the domain(x) = {1,2} and depending on which value x is at, indicates which process should go first)

**Handshaking**: Concurrent processes interact, and must do so in a synchronous fashion.
- In this book, we don't focus on the content of the handshake, but much more the communication (aka the synchronization) of actions that represent the occurrence of a handshake.
- When the set $H$ of handshake actions is empty, all actions of the participating processes can take place autonomously. 

**Channel Systems**: Another system where processes/parallel programs can communicate via channels. These are FIFO buffers that hold messages. These channels are useful for describing communication protocols (but not particularly relevant to what I am doing, I think).
- Each channel has a capacity, finite or infinite. This refers to the maximum number of messages it cans tore. When the capacity is zero, communication is instantaneous and handshakes are simultaneously happening (sending & receiving simultaneously)
- When a channel has a nonzero capacity, there's a delay between sending & receiving messages. This is called asynchronous communication.

### Chapter 2.3 The State-Space Explosion Problem
Cardinality: the number of states in these models/transition systems.
- Verification techniques are based on systematically analyzing these transition systems.
- The runtime are determined by the number of states that need to be analyzed.
	- The number of states grow exponentially with the number of variables in the program graph. This is known as the state-space explosion problem. 

- The number of atomic propositions to represent program graphs are extremely large.
	- However, in practice, only a small fragment of the possible atomic propositions is needed.
	- An explicit representation of the labeling function is mostly not necessary, as the truth-values of the atomic formulae are typically derived from the state information.

# Chapter 3: Linear Time Properties

### Chapter 3.1 Deadlock
In some programs, a terminal state is undesirable (ie: a parallel system) and represents design error. This is a *deadlock*, which occurs if the complete system is in a terminal state, with at least 1 component in a non-terminal system.
- The whole system has to stop, but 1 component has the possibility to continue to operate.
- A classic example is when components mutually wait for each other to progress.

Another definition for deadlock: two computer programs sharing the same resource are preventing each other from accessing the resource, resulting in both programs ceasing to function.

### Chapter 3.2 Linear Time Behavior
This book focuses on using the state-based approach which abstracts from actions & only labels the state sequences.
- Kristy's note - this is similar to graph theory in traditional CS

Let $TS = (S, Act, \rightarrow, I, AP, L)$ be a transition system.

The state graph of $TS$ with the notation $G(TS)$ is the digraph $(V,E)$ with vertices $V=S$ and edges $E$. 
- There exists a vertex for each state in $TS$ and an edge between vertices whenever there is some action $\alpha$. 
- Multiple transitions with different action labels are represented with a single edge.

A path is denoted by $\pi$. We can also define the pre-nodes and the post-nodes around a node $s$ like a directed graph.
- A maximal path fragment is either a finite path fragment that ends in a terminal state, or an infinite path fragment.
- A path fragment is called *initial* if it starts in an initial state. If it's just a chunk of the path without including the initial state, it does not qualify.

**Trace:** a sequence that records the sets of atomic propositions (or properties) that hold true at each state along a state path. The emphasis is on the *observable properties or propositions of the states* (rather than the transitions/states themselves)
- Used to understand the behavior of the system in terms of the properties that are true along the execution path.
- Useful in model checking where we are interested in ensuring certain properties hold throughout the execution.
- In general, transition systems do not have any terminal states, so we're usually looking at infinite traces.

*Reachability Analysis*: Before checking properties, a reachability analysis can identify terminal states in a transition system. 
- We can also extend transition systems with terminal states by adding a self-loop to the terminal state. 

**Linear Time Property**: A subset of $(2^{AP})^\omega$ over the set of atomic propositions $AP$
- We assume a fixed set of propositions $AP$
- These are requirements on the traces of a transition system.
- The $(2^{AP})^\omega$ denotes the set of words that arise from the infinite concatenation of symbols from the alphabet $2^{AP}$
- Therefore, a LT property is a language/set of infinite words over the alphabet $2^{AP}$
- Kristy's notes: you can think of these as rules in a LTL example. "The Light 1 is infinitely often green" or something like that.

The mutual exclusion property ensures that at most 1 process can be in its critical section at any given time. (Aka both or >1 process can't be at critical simultaneously!

### Chapter 3.3 Safety Properties and Invariants
Safety properties are written such that 'nothing bad should happen'.

**Invariants**: LT properties that are given by a condition $\phi$ for the states and require that $\phi$ holds for all reachable states.
- They are a special type of safety property that must hold in every reachable state of a transition system.
	- We can use BFS or DFS to search all states reachable from the initial state(s). If one state does not hold, then the invariance is violated.
- They are state properties that can be verified by examining all reachable states.
- Example: ensuring mutual exclusion in a system.

**Safety properties** are not invariants (they are not state properties). They are defined as an LT property over $AP$ such that any infinite word $\sigma$ where P does not hold contains a $bad prefix$. 
- May impose requirements on finite path fragments rather than just states.
- They cannot be verified by considering only reachable states; it requires analysis of path fragments.
- Example: money is withdrawn from an ATM after the correct PIN is entered.

General facts about Traces & Safety Properties
1. **Infinite Trace Inclusion**: If one transition system $TS$ is a subset of the traces of another transition system $TS'$, then $TS'$ satisfies all LT properties that $TS$ satisfies.
2. **Finite Trace Equivalence**: The same applies to safety properties. If There is a set of safety properties in $TS$, and $TS$ is a subset within $TS'$, then any safety properties valid for $TS$ are also valid for $TS'$.
3. **Finite Trace Inclusion**: If all finite traces of one system are included in another, then the safety properties of the latter are satisfied by the former.

### Chapter 3.4 Liveness Properties

The opposite of safety properties (which specify 'something bad never happens'), liveness properties state 'something good' will happen in the future.
- **Definition of Liveness Property**: To force progress in the system, or by stating 'doing nothing is not an option'
- Liveness properties require a certain condition on the infinite behaviors. Example: certain events occur infinitely often.

Liveness Properties: Ensuring that there is always a way to continue from any finite sequence to eventually satisfy the property.
- No matter what happens in the short term (finite sequence), there is always a way to satisfy the liveness property in the long term (infinite sequence)
- Ensures that certain desirable outcomes will eventually occur, regardless of the intermediate states.
- There are three typical examples (see page 122 for equation examples):
	- *Eventually* each process will eventually enter its critical section. 
	- *Repeated eventually* each process will enter its critical section infinitely often. 
	- *Starvation freedom* each waiting process will eventually enter its critical section.

Every LT property can be decomposed. Here's an example: "The machine provides beer infinitely often after initially providing soda three times in a row."
- Part 1: Beer must be provided infinitely often. It is a liveness property!
- Part 2: The first three drinks must be soda. This is a safety property, since if the first three drinks are not soda (aka are beer), it is violated!
- Therefore, this property is a combination of both a safety and liveness property!

### Chapter 3.5: Fairness

The goal is to rule out infinite behaviors that are unrealistic & assist in liveness properties.
- Remove biases: we do not want to consistently ignore a possible option. No one process can be perpetually neglected.
- Rule out computations that are considered to be unreasonable for the system under consideration.

Process Fairness: the fair scheduling of the execution of processes. Used in proving starvation freedom.

Flavors of Fairness Constraints:
1. *Unconditional fairness*: Every process gets it turn infinitely often. Aka "impartiality"
	1. Does not take into account whether a process is enabled or ready to execute a transition. It simply ensures that every process will get a chance to execute repeatedly over time.
	2. Example: a round robin-scheduler for CPU processes. Every process in the scheduler gets a time slice infinitely often, regardless of their state (enabled or not)
2. *Strong fairness*: Every process that is enabled infinitely often gets it turn infinitely often. Aka "compassion"
	1. If there are opportunities for a process to execute, the process will eventually execute infinitely often. This prevents situations where a process is enabled again & again but never gets a chance to execute.
	2. Example: a shared printer with multiple computers. If a computer sends print jobs infinitely often (even if there are periods where it does not send print jobs), it will be get its turn to use the printer infinitely often.
3. *Weak fairness*: Every process that is continuously enabled from a certain time instant gets its turn infinitely often. Aka "justice"
	1. It only requires that if a process remains enabled continuously without interruption, it will eventually execute infinitely often. It prevents situation where a process is always ready to execute but never gets a chance to do so after a certain point in time. 
	2. Example: a traffic light system. If a traffic light is continuously enabled (aka there are cars coming from its direction regularly) from a certain point in time, it will eventually turn green infinitely often, ensuring cars can pass through.
	3. A great example is the traffic light scenario; it ensures that a process will infinitely often request to enter the critical section. To do this, each process has to leave the noncritical section infinitely often.
4. Unconditional A-fair executions is a subset of all strong A-fair executions, which is a subset of all weak A-fair executions. 
	1. Unconditional fairness rules out more behaviors than strong fairness, and strong fairness excludes more behaviors than weak fairness.
Note: 'enabled' means a process is ready to execute, aka the conditions for its execution are met. 
- 'gets its turn' means that the process actually executes.
- Something that is 'A-fair' means its actions are fair.
- A fairness constraint imposes a requirement on all actions in a set A. 
	- A fairness assumption is the application of different fairness constraints on different action sets within a system.
- A *realizable fairness assumption* is valid in a transition system *TS* whenever in any reachable state, at least one fair execution is possible.
	- They are irrelevant for verifying safety properties. "Something bad **never** happens". Safety is concerned with the impossibility of undesirable states/events.
	- They are used for ensuring liveness of a system. "Something good **eventually** happens". Fairness is concerned with the frequency or inevitability of certain events/actions.

# Chapter 4: Regular Properties

**Regular Properties Definition**: Safety properties whose bad prefixes constitute a regular language, and hence can be recognized by finite automaton.
- The algorithm to check a safety property $P_{safe}$ for a given finite transition system $TS$ relies on a reduction to the invariant-checking problem for $TS$ with a finite automaton that recognizes the bad prefixes of $P_{safe}$ .
- This automaton-based verification algorithm can be generalized to a larger class of linear-time properties, called $\omega$-regular properties.

Goals of this chapter: We want to understand algorithms that are used to verify safety, liveness, and other linear-time properties in finite transition systems. We want to reduce our safety property to an invariant-checking problem. This is done with a finite automaton, which an example of is the Buchi automata. 
- Buchi automata should let us verify certain state conditions hold continuously (persistence checking)

### Chapter 4.1 Automata on Finite Words
A non-deterministic finite automaton (NFA) is a theoretical model of computation similar to a deterministic finite automaton (DFA) but differs in such that it allows for multiple possible transitions fora  given state and input signal. 
- non-determinism allows multiple potential paths through the state transitions.

If we have $\delta(a,A) = \oslash$ the automaton is stuck and no further progress can be made -> this is known as a *rejection*.\
- The system will continue to read the input, but when it gets to the end, it *accepts* whatever the current state is as an accept state, and rejects otherwise. 
- For any input, there might be several possible behaviors/runs; some may be accepting and some may be rejection.
	- If at least one of its run is accepting (ie runs the whole input and ends in a final state), the input is accepted by $A$. 
	- If all runs ends in rejection, then it is the 'emptiness problem'. 

Fun fact: we can convert a NFA (non-deterministic finite automaton) to a DFA (deterministic finite automaton) using a subset construction (also known as a powerset construction).

### Chapter 4.2 Model-Checking Regular Safety Properties
Goal: Explain how NFAs can be used to check the validity of an important class of safety properties. The specific class is that all their bad prefixes constitute a regular language. 

**Vocabulary Refresher**
- **Safety Property**: a condition that must always hold during the execution of a system. 
- **Bad Prefixes:** Sequences that (if extended further) could never satisfy the property again. They demonstrate a violation of the safety condition.
- **Invariant**: a condition that must always hold in all reachable states.
- **Regular Language**: a set of strings that can be recognized by a finite automaton, such as DFA or NFA. They are described by regular expressions and use operations like union, intersection, complementation, etc.
- **Regular Safety Property**: a safety property whose set of bad prefixes forms a regular language. This means that there exists a finite automaton (DFA or NFA)

Example 1: Invariant conditions
- Let's assume an invariant condition that should hold in every reachable state of a system (ie: the humidity must be below 0.5).
- Let $\phi$ be a state condition (a propositional formula, ie: humidity $\leq 0.5$ )
- The language of bad prefixes are sequences where at least one state does not satisfy $\phi$. (ie: a state where the humidity is 0.7)
- This can be expressed with a regular expression and recognized by a finite automaton

Example 2: Mutual Exclusion
- The safety property here may be "at most one process can be in its critical section at any time".
- The bad prefixes would be where two processes are in their critical sections simultaneously. (ie: $sect_1 = crit$ and $sect_2 = crit$ at $t=10$)

Note: there's another type of language called *context-free language*. This is not covered in this chapter, but it requires nested structures and counting. 
- An example of this would be "The number of inserted coins is always at least the number of dispensed drinks." This is because we have to count 'coins' and 'drinks' separately and a finite automaton cannot keep track of these counts, as it has no memory mechanism.
- Rather, a stack-based recognition program can keep track of 'coins' events and decrement the stack for each 'drink' event.

**How to Verify Safety of a TS (transition system) by using a NFA (non-deterministic finite automaton)**
1. Translate the safety rule into a machine (NFA called $A$) that knows all the 'bad prefixes'
2. Define the system as a TS.
3. Perform an intersection check between the NFA and TS. This ensures that there is no overlap in the two lists, and no action sequence performed by TS is a bad prefix.

Example: A vending machine that should never dispense a drink unless a coin is inserted.
1. Safety Rule:($P_{safe}$) The machine should not give out a drink without a coin being inserted first.
2. Bad Prefix: Any sequence where a drink is dispensed without a coin.
3. NFA ($A$): A machine that knows all the sequences where a drink is dispensed without a coin.
4. System Behavior ($TS$): The vending machine's actions (inserting coins and dispensing drinks)

We intersect the vending machine's actions ($TS$) and the bad prefix checker ($A$) and see if there are any sequences of actions that exist where a drink is dispensed w/o a coin. 
- If none exist, our vending machine is verified safe :)

Definition 4.16 details the guidelines of a product of a transition system ($TS$) and a NFA. This product, seen as $TS \otimes A$ can detail the combined behavior of the $TS$ and the automaton $A$ (which has the specification within it).
- This lets us reduce the problem of verifying a specification to a much simpler problem of checking properties in the product.
- So we check if the product will reach any bad states; if not, then the system satisfies the safety property $A$.
- If it fails, we get a counterexample, and we can read the exact sequence of events leading to the violation. This makes it easier to debug and fix!
#### Chapter 4.3: Automata on Infinite Words

Consider variants of nondeterministic finite automatons (NFAs) called nondeterministic Buchi automata (NBA) which are accepts for languages of infinite words.
- If we are given a nondeterministic Buchi automaton $A$ that specifies the "bad traces", then a graph analysis in the product of $TS \otimes A$ will either establish or disprove $TS \models P$. 
- The specific problems we'll be addressing are persistence properties, which will necessitate graph algorithms.
	- For regular safety properties, invariant checking / depth first search is all we would need.
	- Persistence problems ensure that certain conditions hold after a certain point.

**$\omega$-regular languages** can handle infinite sequences of symbols from $\sum$ and can include infinite repetition as A, B, A, B, A, B, ....
- We can denote this as $(AB)^\omega$. 

Example 1: $G = AB.(C)^\omega + (A).(BC)^\omega$ has two components:
- Finite sequence $AB$ followed by an infinite repetition of $C$. This looks like $A, B, C, C, C, ...$
- Finite sequence $A$ followed by an infinite repetition of $BC$. This looks like $A, B, C, B, C, B, C,...$

Example 2: $(A+B)^*A(AAB+C)^\omega$ 
- $(A+B)^*$ means any sequence of As and Bs, including the empty sequence. The $^*$ means any number of repetitions (including zero) of the expression inside the parenthesis.
- $A$ specifies that after the sequence of As and Bs, there must be an A.
- $(AAB + C)^\omega$ indicates infinite repetition of either the sequence $AAB$ or $C$.
- Example solution: $A, A, A, C, C, C,...$ or $B, B, A, A, A, B, A, A, B, A, A, B...$
- 

Start on page 172 ! :D