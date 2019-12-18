import typed_dmms as dmms
import numpy as np
import copy
from utils import set_dict

from skimage.draw import line, line_aa

import state_of_machine as state

assert(dmms.new_zero_vector('matrix') == {'kind': 'matrix', 'repr': {}})

dmms.neuron_types['self'] = 'accum matrix'

assert(dmms.neuron_types == {'self': 'accum matrix'})

dmms.type_inputs['accum matrix'] = {'accum': 'matrix', 'delta':'matrix'}

assert(dmms.type_inputs == {'accum matrix': {'accum': 'matrix', 'delta': 'matrix'}})

dmms.type_functions['accum matrix'] = lambda inputs: {'current matrix': 
                                                         {'kind': 'matrix',
                                                          'repr':  dmms.add_nested_dict(copy.deepcopy(inputs['accum']['repr']), 
                                                                                        inputs['delta']['repr'] if 'delta' in inputs
                                                                                                                else {})}}

dmms.neuron_types['main_mouse'] = 'smart_mouse'

dmms.type_inputs['smart_mouse'] = {'previous': 'mouse'}

dmms.type_functions['smart_mouse'] = lambda inputs: {'current_mouse':
                                                         {'kind': 'mouse',
                                                          'repr': {'xdata': state.main_mouse.base_xdata,
                                                                   'ydata': state.main_mouse.base_ydata}},
                                                     'previous_mouse':
                                                         inputs['previous']}

dmms.neuron_types['image_mouse'] = 'image_mouse_type'

dmms.type_inputs['image_mouse_type'] = {'accum': 'color image', 'current_mouse': 'mouse', 'previous_mouse': 'mouse'}

def draw_a_line_on_image(inputs):
    current_x = int(round(inputs['current_mouse']['repr']['xdata']))
    current_y = int(round(inputs['current_mouse']['repr']['ydata']))
    previous_x = int(round(inputs['previous_mouse']['repr']['xdata']))
    previous_y = int(round(inputs['previous_mouse']['repr']['ydata']))
    if current_x >= 0 and current_y >= 0 and previous_x >=0 and previous_y >= 0:    
        rr, cc = line(previous_x, previous_y, current_x, current_y)
        dd = np.zeros(len(rr), dtype=np.int64)
        #print(rr.dtype, cc.dtype, dd.dtype)
        # NEED TO EITHER COPY THIS IMAGE, OR ASSUME NON-SHARING (CURRENTLY THIS HOLDS)
        inputs['accum']['repr'][cc, rr, dd] = 1.0 # 255
    return {'current_image_mouse': inputs['accum']}
        
dmms.type_functions['image_mouse_type'] = draw_a_line_on_image
                                                         
initial_output = {}

set_dict(initial_output, ['self', 'current matrix'], {'kind': 'matrix', 'repr': {}}) # this is where the network matrix sits 

set_dict(initial_output['self']['current matrix']['repr'], 
                       ['self', 'accum', 'self', 'current matrix'], 1) # this is the "main 1" of that matrix
                       
set_dict(initial_output['self']['current matrix']['repr'], 
                       ['main_mouse', 'previous', 'main_mouse', 'current_mouse'], 1) # mouse neuron in the network matrix

set_dict(initial_output['self']['current matrix']['repr'], 
                       ['image_mouse', 'accum', 'image_mouse', 'current_image_mouse'], 1) # accum connection for image_mouse neuron in the network matrix

set_dict(initial_output['self']['current matrix']['repr'], 
                       ['image_mouse', 'current_mouse', 'main_mouse', 'current_mouse'], 1) # current_mouse connection for image_mouse neuron in the network matrix

set_dict(initial_output['self']['current matrix']['repr'], 
                       ['image_mouse', 'previous_mouse', 'main_mouse', 'previous_mouse'], 1) # previous_mouse connection for image_mouse neuron in the network matrix
                                            
#print('initial_output: ', initial_output)

state.outputs[0] = initial_output
