import typed_dmms as dmms
import numpy as np
import copy
from utils import set_dict

import matplotlib.pyplot as plt

import matplotlib.animation as animation

from skimage.draw import line, line_aa


class BaseCoords:
    def __init__(self):
        self.base_xdata = 0.0
        self.base_ydata = 0.0

base_coords = BaseCoords()

main_mouse = BaseCoords()

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
                                                          'repr': {'xdata': main_mouse.base_xdata,
                                                                   'ydata': main_mouse.base_ydata}},
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

outputs = {}

outputs[0] = initial_output

inputs = {}
                          


fps = 30
nSeconds = 5

#a = np.zeros((dmms.image_height, dmms.image_width, 3), dtype = np.uint8)

# the kosher thing is to have a separate output neuron,
# but let's just use the output['image_mouse']['current_image_mouse']['repr'] for now

class Pressed:
    def __init__(self):
        self.pressed = False
        

pressed = Pressed()

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure( figsize=(12,9), facecolor = 'gray' )

def onclick(event):
    pressed.pressed = True
    base_coords.base_xdata = event.xdata
    base_coords.base_ydata = event.ydata
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
           
def onrelease(event):
    pressed.pressed = False
    print('mouse release: , x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.x, event.y, event.xdata, event.ydata))
           
def onmove(event):
    main_mouse.base_xdata = event.xdata if event.xdata != None else -1000.0
    main_mouse.base_ydata = event.ydata if event.ydata != None else -1000.0
    if pressed.pressed:
        pass # instead of what is commented out
        # draw line
        # print(type(base_coords.base_xdata), type(event.xdata))
        # rr, cc = line(int(round(base_coords.base_xdata)), int(round(base_coords.base_ydata)),
        #               int(round(event.xdata)), int(round(event.ydata)))
        #print("DEBUG MOUSE: ", len(rr), len(cc))
        #dd = np.zeros(len(rr), dtype=np.int64)
        #print(rr.dtype, cc.dtype, dd.dtype)
        #a[cc, rr, dd] = 255 # 1.0
        #base_coords.base_xdata = event.xdata
        #base_coords.base_ydata = event.ydata
    print('mouse move: , x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.x, event.y, event.xdata if event.xdata != None else -1000.0, 
                             event.ydata if event.ydata != None else -1000.0))           

cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid2 = fig.canvas.mpl_connect('motion_notify_event', onmove)
cid3 = fig.canvas.mpl_connect('button_release_event', onrelease)

#a = snapshots[0]

class Count:
    def __init__(self):
        self.count = 0

count = Count()

step = Count()

im = plt.imshow(dmms.new_zero['color image'](), interpolation='none', aspect='auto', vmin=0, vmax=1)

def animate_func(i):
    step.count = step.count + 1
    
    # We currently store the sequence of network states
    # (we don't have to do that, we currently just do that for convenience
    #  while we can afford it memory-wise)
    
    inputs[step.count] = dmms.down_movement(outputs[step.count-1])
    #print('inputs[',step.count,']=', inputs[step.count])
    outputs[step.count] = dmms.up_movement(inputs[step.count]) 
    #print('outputs[',step.count,']=', outputs[step.count])    

    if i % fps == 0:
        #print( '.') #, end ='' )
        print(i, count.count)
        
    j = i%150    

    #if (j < 50):
    #    a[j+count.count,j,0] = 255*j//50
    #else:
    #    if (j < 100):
    #        a[j+count.count,j,1] = 255*(j-50)//50 
    #    else:
    #        if (j < 150):
    #            a[j+count.count,j,2] = 255*(j-100)//100            
    im.set_data(outputs[step.count]['image_mouse']['current_image_mouse']['repr'])    
    #im.set_array(snapshots[i])
    if i % (fps*nSeconds) == 0:
        count.count = count.count + 1
    #return [im]

anim = animation.FuncAnimation(
                               fig, 
                               animate_func, 
                               #frames = nSeconds * fps,
                               #init_func = init_func_dummy,
                               interval = 1 # 1000 / fps, # in ms
                               )

#anim.save('test_anim.mp4', fps=fps, extra_args=['-vcodec', 'libx264'])

#print('Done!')

plt.show()  # Not required, it seems (only if you are in Jupyter)

print('Done!')