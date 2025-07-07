![[Offline and Online Learning of STL Formulae using Decision Trees.pdf]]

### Introduction & Related Works

**Paper Objective**
- Learning high-level description of a system from its execution traces.
	- System is described using Signal Temporal Logic
	- Inferred formulae can be used for classification, monitoring, or control

**Where They Hope To Address Limitations (Of Current Formalisms)**
- STL Formulae have precise meaning & allow for a rich specification of the behaviors that is interpretable by human experts.
- ML methods applied to time-series data are either a) model-based & require a good model of the system or b) black-box models such as deep neural networks.
- Classical ML methods are overly specific to the task and do not offer insights into other aspects of the system in which they're applied (little to no knowledge discovery)

**The Solution**
- Two-class classification problem: build a temporal logic formula that can distinguish traces belonging to 1 of 2 possible classes (either a fault or not)
	- The dataset is a finite set of pairs of system traces (signals & labels)
	- Each label indicates whether the respective trace exhibits some desired system behavior, aka supervised learning.
	- To conduct a discriminating formula (aka determining whether it is A or B), they used a decision-tree based framework
		- Each node of the tree contains a test associated with the satisfaction of a simple formula
		- These trees are binary, used for classification purposes.
- Online learning problem: new data arrives over time & the model should be updated to accommodate it.
	- Provides a formulae early during the signal collection process
		- Refines it continuously as signals come in
	- Removes the separation between building & deployment phase

**Parameter Mining**
- What are the optimal parameters for a formula when a formula structure is given?
	- Formula template: "The engine speed settles below $v$ m/s within $\tau$ seconds"
	- An optimization procedure finds values for $v$ and $\tau$. 
- The designer of the system must have a good domain knowledge & awareness of properties of interest.
- Solution: parameters for the formula are selected such that the resulting formula barely or strongly satisfies the input signals.

**Supervised Two-Class Classification Problem**
- Goal: construct a formula, both structure & parameters, that can distinguish between two sets of signals.
	- Define a fragment of STL called inference parametric signal temporal logic (iPSTL). This is a subset within STL.
		- This fragment admits a partial order among formulae, in the sense of language inclusion, and with respect to the robustness degree.
			- **Partial Order**: a way of arranging elements where some elements can be compared to each other in a specific order, but not all elements are necessarily comparable. Likely a hierarchy but not a strict linear order.
			- **Language Inclusion**: one iPSTL formula can be considered as encompassing another. If formula A includes formula B, then any signal that satisfies A also satisfies B. 
			- **Robustness Degree**: How strongly a signal satisfies a given formula. A higher robustness degree means the signal satisfies the formula more strongly.
	- The TL;DR is that the authors defined a specific subset of STL called iPSTL. 
		- Because of partial order, we can arrange iPSTL formulas in a hierarchy based on language inclusion (some formulas can be seen as more general or encompassing others) and robustness degree (some signals satisfy certain formulas more strongly than others).
		- The hierarchy or ordering of iPSTL formulas can be represented as an infinite DAG.
			- Each node represents an iPSTL formula.
			- Directed edges show the inclusion relationship and robustness ordering.
			- No cycles exist! You can't start at one formula and return to it by following the edges.
- We can then formulate the classification problem as an optimization problem. The objective function involves the robustness degree. It can be solved in two cyclic steps
	- Optimize the formula structure by exploring the DAG and growing/pruning it
	- Optimize the formula parameters for a fixed structure, using a nonlinear optimization algorithm.

### Signal Temporal Logic

- A generalization of LTL, where time is continuous and the predicates are defined over real values.
- Has been used in formal verification of hybrid systems where it is used to state & monitor requirements.
- Evaluation of STL formulas typically fall in two categories
	- Satisfaction: whether a signal satisfies an STL formula depends on whether the conditions specified by the formula are met the appropriate times.
	- Robustness: This measures how strongly a signal satisfies/violates an STL formula, used in quantitative analysis & optimization. 
- Is defined using a dense-time semantics & natively supports predicates over reals.
	- In practice, its monitoring algorithms work with sampled data & assume that the signals are piece wise constant.


### Signal Classification
- Goal: find a STL formula that separates traces produced by a system that exhibit some desired property from other undesired properties of the same system.
	- Positives or targets are the normal working conditions.
	- Anomalies or negatives are the non-conforming patterns.
- Given a dataset of labeled signals, the goal is to find a STL formula such that the misclassification rate is minimized. 
	- The authors built a decision tree that classifies signals & maps the constructed tree to an STL formula.
		- The proposed idea is to split the signals using a simple formula at each node, chosen from a finite set of PSTL formulae, called *primitives*. They are atomic predicates with parameters and basic temporal operators with parameterized intervals. These primitives should be building blocks and easy to understand.

#### Building a Decision Tree
- The idea is to start with a fragment of STL and build a decision tree (that classifies signals)
	- Then, we want to traverse the decision tree to find the optimal values for each parameter in the model.
		- Past approaches used a greedy approach, where locally optimal decisions are taken at each node. 
		- The selection of the *primitives* was based on its *impurity measure*, which essentially tries to pass on children that are more pure aka have more objects belonging to the same class.
		- *Impurity measure* is of two components, *information gain (IG)* and also *Misclassification gain (MG)*
- The components for doing *Parameterized Learning Algorithm* (for inferring temporal logic from data) is a bunch of meta-parameters, defined as a) PSTL primitives and b) impurity measures and c) set of stopping conditions
	- If the stopping condition is not met, then the algorithm finds the optimal STL formula over all PSTLs using the impurity measure, which measures the quality of the partition.
	- After the tree is made, we then use an algorithm to traverse the tree & keep track of the paths
- When do we stop building a decision tree?
	- Technically, we can achieve perfect classification on the training data if we allow the algorithm to go to the maximum depth of the tree.
	- However, this takes a lot of time and over-fits the data. Rather, we can introduce more restrictive stopping conditions & prune unnecessary parts of the tree.
		- Post-completion pruning (aka pruning after the tree is built) can be done with a cost-complexity pruning algorithm. We assign a cost to a tree and 
	- We can also stop after the algorithm reaches a certain fixed depth.

### Online Learning
- This would occur when signals arrive over time & the inference system needs to be updated to accommodate it.
	- We want to build & update the STL formula used for data classification
- The general idea is to update leaves based on the new data. To select the right leaf, we look at the majority of the labels of the signals falling on that leaf.
	- Step 1: find the optimal parameters for each primitive in the set according to the impurity measure
	- Step 2: evaluate the status of the leaf whether to keep as is, or create a new non-terminal node (aka make more leaf-babies)
	- Step 3 (Potential): If so, the leaf is transformed into a non-terminal node & associated with the optimal formula. Leaf children are added.
	- Step 4 (Potential): Signals are partitioned according, and for each outcome, the corresponding partition is passed to the appropriate leaf