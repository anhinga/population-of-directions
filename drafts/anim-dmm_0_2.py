import typed_dmms as dmms
import neuron_types as nt
import network_0 as dmm_net

import state_of_machine as state

import matplotlib.pyplot as plt

import matplotlib.animation as animation

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure( figsize=(12,9), facecolor = 'gray' )

def onclick(event):
    state.pressed.pressed = True
    state.base_coords.base_xdata = event.xdata
    state.base_coords.base_ydata = event.ydata
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
           
def onrelease(event):
    state.pressed.pressed = False
    print('mouse release: , x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.x, event.y, event.xdata, event.ydata))
           
def onmove(event):
    state.main_mouse.base_xdata = event.xdata if event.xdata != None else -1000.0
    state.main_mouse.base_ydata = event.ydata if event.ydata != None else -1000.0
    print('mouse move: , x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.x, event.y, event.xdata if event.xdata != None else -1000.0, 
                             event.ydata if event.ydata != None else -1000.0))           

cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid2 = fig.canvas.mpl_connect('motion_notify_event', onmove)
cid3 = fig.canvas.mpl_connect('button_release_event', onrelease)

im = plt.imshow(dmms.new_zero['color image'](), interpolation='none', aspect='auto', vmin=0, vmax=1)

def animate_func(i):
    state.step.count = state.step.count + 1
    
    # We currently store the sequence of network states
    # (we don't have to do that, we currently just do that for convenience
    #  while we can afford it memory-wise)
    
    state.inputs[state.step.count] = dmms.down_movement(state.outputs[state.step.count-1])
    #print('inputs[',step.count,']=', inputs[step.count])
    state.outputs[state.step.count] = dmms.up_movement(state.inputs[state.step.count]) 
    #print('outputs[',step.count,']=', outputs[step.count])    

    if i % state.fps == 0:
        #print( '.') #, end ='' )
        print(i, state.count.count)
        
    j = i%150    

    #if (j < 50):
    #    a[j+count.count,j,0] = 255*j//50
    #else:
    #    if (j < 100):
    #        a[j+count.count,j,1] = 255*(j-50)//50 
    #    else:
    #        if (j < 150):
    #            a[j+count.count,j,2] = 255*(j-100)//100            
    im.set_data(state.outputs[state.step.count]['image_mouse']['current_image_mouse']['repr'])    
    #im.set_array(snapshots[i])
    if i % (state.fps*state.nSeconds) == 0:
        state.count.count = state.count.count + 1
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