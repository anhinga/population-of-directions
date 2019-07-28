### Experiments with "population coordinate descent"

Population coordinate descent was described in https://github.com/jsa-aerial/DMM/blob/master/design-notes/Early-2017/population-coordinate-descent.md

We are planning to implement an interactive evolution setup, similar to one used by people for CPPN experiments: https://en.wikipedia.org/wiki/Compositional_pattern-producing_network

The user is given several directions of change selected from the current set of possible directions according to the current probability distribution over that set, and can pick one or two directions of change to try as a step of coordinate descent.

When 2 directions of are picked by a user, we'll have a 2D slider similar to 2D sliders used in our interactive shaders in June 2019: https://github.com/anhinga/2019-python-drafts/tree/master/vispy/atparty-2019

In that case, the descent will effectively happen over a linear combination of these two directions, and this linear combination will be added to the current set of possible directions.

We'll experiment with rules for (and interactive adjustment of) probabilities over the maintained set of directions.

