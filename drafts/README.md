## A directory for drafts

The system consists of 3 main components:

### 1. Control for the interactive evolution by population descent

(Should work according to what I specified in the main README. A fairly detailed hand-written design exists.)

### 2. Interface for showing animations and taking mouse feedback

(A very rough `matplotlib` program demonstrating required capabilities exists in my local backup.
Something along those lines can be used, at least at first.)

### 3. An engine for mapping parameters into animations

I committed `typed-dmms.py` to be used for this purpose. 

All our experimental DMMs in
Clojure and in Processing were structured to use a single, sufficiently expressive **kind
of linear streams**. 

This new script, `typed-dmms.py`, is our first, very preliminary draft attempting to implement
a scheme with multiple kinds of linear streams from our May 2016 arxiv preprint.
