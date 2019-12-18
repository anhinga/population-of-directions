# state of our machine

# accumulated dmm traces, mouse state, animation parameters, etc.

class BaseCoords:
    def __init__(self):
        self.base_xdata = 0.0
        self.base_ydata = 0.0

base_coords = BaseCoords()

main_mouse = BaseCoords()


outputs = {}

inputs = {}
                          
fps = 30
nSeconds = 5

class Pressed:
    def __init__(self):
        self.pressed = False
        

pressed = Pressed()

class Count:
    def __init__(self):
        self.count = 0

count = Count()

step = Count()

