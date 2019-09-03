# typed DMMs with kinds of linear streams ( https://arxiv.org/abs/1605.05296 )

# first draft (*** don't take this design too seriously ***)

import numpy as np
import copy

# vector consists of "kind" and "repr" (representation) 

# let's start with 5 kinds, "number", "image", "color image", "matrix", "mouse"
# add them as needed

new_zero = {'number': lambda: 0,
            'image': lambda: np.zeros((300, 400)),
            'color image': lambda: np.zeros((300, 400, 3)),     
            'matrix': lambda: {}, # let's implement 'matrix' via nested dicts at the moment
            'mouse': lambda: {'xdata': 0.0, 'ydata': 0.0}
           }
    
neuron_types = {} # dictionary mapping neuron names to type names

type_functions = {} # dictionary mapping type names to activation functions

type_inputs = {} # dictionary mapping type names to maps from input names to input kinds
                 # dictionary mapping type names to maps from output names to output kinds can be omitted

def new_zero_vector(kind):
    return {'kind': kind,
            'repr': new_zero[kind]()
           }

def mult_number_nested_dict_in_place(coef, dict): # leaves must be numbers
    for key, value in dict.items():
        if type(value) == type({}):
            mult_number_nested_dict_in_place(coef, value)
        else:
            dict[key] = coef*value 
    return dict            
           
def mult_number_nested_dict(coef, old_dict): # new copy
    new_dict = copy.deepcopy(old_dict)
    return mult_number_nested_dict_in_place(coef, new_dict)
           
def mult_number_vector(kind, coef, vector):
    # assumes that something outside established that
    # vector[kind] = kind
    if kind in ['number', 'image', 'color image']:
        return {'kind': kind,
                'repr': coef * vector['repr']
               }
    if kind in ['matrix', 'mouse']:
        print('DEBUG 2', coef, vector)
        return {'kind': kind,
                'repr': mult_number_nested_dict(coef, vector['repr'])
               }

def add_nested_dict(old_dict, new_dict): # in place, adding to old_dict
    for key, value in new_dict.items():
        if key in old_dict:
            old_value = old_dict[key]
            if type(value) == type({}) and type(old_value) == type({}):
                old_dict[key] = add_nested_dict(old_value, value)
            if type(value) == type({}) and type(old_value) != type({}):
                old_dict[key] = add_nested_dict({'number': old_value}, value)
            if type(value) != type({}) and type(old_value) == type({}):
                old_dict[key] = add_nested_dict(old_value, {'number': value})
            else: # no check for data being numerical !
                old_dict[key] = old_value+value
        else:
            old_dict[key] = copy.deepcopy(value) # if we had a warranty that new_dict is not reused this can be improved
                                                 # right now there are no reuse plans (revisit this)
    return old_dict
                                                 
def add_vectors(kind, old_sum, new_vector):
    # assumes that something outside established that
    # old_sum[kind] == new_vector[kind] = kind
    # *** MODIFIES old_sum ***
    if kind in ['number', 'image', 'color image']:
        old_sum['repr'] += new_vector['repr']
    if kind in ['matrix', 'mouse']:
        print('DEBUG 3: ', old_sum)
        print('DEBUG 4: ', new_vector)
        add_nested_dict(old_sum['repr'], new_vector['repr'])
    return old_sum             
      
def add_term(kind, old_sum, coef, new_vector): # *** MODIFIES old_sum ***
    if kind == old_sum['kind'] and kind == new_vector['kind']:
        # need to compute and return old_sum+coef*new_vector
        # where + and * are interpreted according to kind
        return add_vectors(kind, old_sum, mult_number_vector(kind, coef, new_vector))
    else:
        # can add diagnostics or just ignore
        # this is not supposed to happen
        # but OK to interpret as adding zero
        return old_sum     


# this cycle remains:
#
# next_input = down_movement (current_output)
# next_output = up_movement (next_input)

def up_movement(next_input): # next_input here is next_matrix returned from down_movement
    next_output = {}
    for neuron_name, neuron_inputs in next_input.items():
        neuron_type = neuron_types[neuron_name]
        print('DEBUG 5: ', neuron_type, neuron_name, neuron_inputs)
        next_output[neuron_name] = type_functions[neuron_type](neuron_inputs) # apply activation function
    return next_output # can be used as current_output on the next cycle

def down_movement (current_output):
    next_input = {}
    next_matrix = current_output['self']['current matrix']
    assert(next_matrix['kind'] == 'matrix')
    for neuron_name, neuron_matrix_rows in next_matrix['repr'].items():
        neuron_type = neuron_types[neuron_name]
        next_input[neuron_name] = {}
        for input_name, matrix_row in neuron_matrix_rows.items():
            input_kind = type_inputs[neuron_type][input_name]
            print('DEBUG: ', neuron_name, input_kind, input_name, matrix_row)
            next_input[neuron_name][input_name] = apply_matrix_row_typed(input_kind, matrix_row, current_output)
    return next_input # can be used as next_input by the up_movement
    
def apply_matrix_row_typed(input_kind, matrix_row, current_output):
    result = new_zero_vector(input_kind)
    for neuron_name, group_of_elements in matrix_row.items():
        for output_name, coef in group_of_elements.items():
            output = current_output[neuron_name][output_name]
            result = add_term(input_kind, result, coef, output)    
    return result

