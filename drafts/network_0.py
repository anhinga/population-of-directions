import neuron_types as nt

from utils import set_dict

import state_of_machine as state
                                                         
initial_output = {}

set_dict(initial_output, ['self', 'current matrix'], {'kind': 'matrix', 'repr': {}}) # this is where the network matrix sits 

matrix_repr = initial_output['self']['current matrix']['repr']

set_dict(matrix_repr, ['self', 'accum', 'self', 'current matrix'], 1) # this is the "main 1" of that matrix
                       
set_dict(matrix_repr, ['main_mouse', 'previous', 'main_mouse', 'current_mouse'], 1) # mouse neuron in the network matrix

set_dict(matrix_repr, ['image_mouse', 'accum', 'image_mouse', 'current_image_mouse'], 1) # accum connection for image_mouse neuron in the network matrix

set_dict(matrix_repr, ['image_mouse', 'current_mouse', 'main_mouse', 'current_mouse'], 1) # current_mouse connection for image_mouse neuron in the network matrix

set_dict(matrix_repr, ['image_mouse', 'previous_mouse', 'main_mouse', 'previous_mouse'], 1) # previous_mouse connection for image_mouse neuron in the network matrix
                                            
#print('initial_output: ', initial_output)

state.outputs[0] = initial_output
