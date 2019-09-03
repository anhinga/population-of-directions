# starting to test and use typed_dmms

import typed_dmms as dmms
import numpy as np
import copy

assert(dmms.new_zero_vector('matrix') == {'kind': 'matrix', 'repr': {}})

dmms.neuron_types['self'] = 'accum matrix'

assert(dmms.neuron_types == {'self': 'accum matrix'})

dmms.type_inputs['accum matrix'] = {'accum': 'matrix', 'delta':'matrix'}

assert(dmms.type_inputs == {'accum matrix': {'accum': 'matrix', 'delta': 'matrix'}})

dmms.type_functions['accum matrix'] = lambda accum, delta: dmms.add_nested_dict(copy.deepcopy(accum), delta)

