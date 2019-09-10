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
