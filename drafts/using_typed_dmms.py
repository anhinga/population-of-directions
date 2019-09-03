# starting to test and use typed_dmms

import typed_dmms as dmms
import numpy as np
import copy
from utils import set_dict

assert(dmms.new_zero_vector('matrix') == {'kind': 'matrix', 'repr': {}})

dmms.neuron_types['self'] = 'accum matrix'

assert(dmms.neuron_types == {'self': 'accum matrix'})

dmms.type_inputs['accum matrix'] = {'accum': 'matrix', 'delta':'matrix'}

assert(dmms.type_inputs == {'accum matrix': {'accum': 'matrix', 'delta': 'matrix'}})

dmms.type_functions['accum matrix'] = lambda accum, delta: {'current matrix': 
                                                                {'kind': 'matrix',
                                                                 'repr':  dmms.add_nested_dict(copy.deepcopy(accum), delta)}}

initial_output = {}

set_dict(initial_output, ['self', 'current matrix'], {'kind': 'matrix', 'repr': {}}) # this is where the network matrix sits 

set_dict(initial_output['self']['current matrix']['repr'], 
                       ['self', 'accum', 'self', 'current matrix'], 1) # this is the "main 1" of that matrix

print('initial_output: ', initial_output)
                          
initial_input = dmms.down_movement(initial_output)

print(initial_input)                          

