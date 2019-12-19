## A directory for drafts

The system consists of 3 main components:

### 1. Control for the interactive evolution by population descent

(Should work according to what I specified in the main README. The [original hand-written design notes](https://github.com/anhinga/population-of-directions/tree/master/drafts/original-spec-draft) for this part of the system are posted.)

### 2. Interface for showing animations and taking mouse feedback

`anim_dmm.py` is a very rough `matplotlib` program demonstrating required capabilities and running one DMM cycle
per frame. Something along those lines can be used, at least at first.

Run `python anim_dmm.py` to see an animation of a small mouse-aware DMM.

### 3. An engine for mapping parameters into animations

I committed an initial draft of `typed_dmms.py` to be used for this purpose. 

All our experimental DMMs in
Clojure and in Processing were structured to use a single, sufficiently expressive **kind
of linear streams**. 

This new script, `typed_dmms.py`, is our first, very preliminary draft attempting to implement
a scheme with multiple kinds of linear streams from our May 2016 arxiv preprint.

Run `python using_typed_dmms.py` for initial testing.

### First refactoring

`anim-dmm.py` is split into `anim-dmm_0_2.py`, `state_of_machine.py`, `neuron_types.py`, and `network_0.py`
in order to detangle the network description and animation engine, and also to separate types and activation functions
(which are now in `neuron_types.py`) and the initial network matrix (and the rest of initial network output if required).

Run `python anim-dmm_0_2.py` to see an animation of a small mouse-aware DMM.

To add new primitives (that is, new types of neurons) extend `neuron_types.py` with more types
(currently it has three types). A type describes what kinds of linear streams are on inputs
of the neuron, and what is its built-in _activation function_.

To create new dmm network, write something instead of `network_0.py`.
