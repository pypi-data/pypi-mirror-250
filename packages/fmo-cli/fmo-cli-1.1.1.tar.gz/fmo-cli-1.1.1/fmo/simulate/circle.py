import matplotlib.pyplot as plt
from random import randrange

from fmo.simulate.bcurve import BezierCurve

import math

class Circle:
    def __init__(self, radius, center=(0, 0),x_stretch = 2, y_stretch = 1, circle_number = 25, pathpoints = [(-2,0),(-9,12),(10,6),(6,10)]):
        self.radius = radius
        self.center = center
        self.x_stretch = x_stretch
        self.y_stretch = y_stretch
        self.circlenumber = circle_number
        self.path =  BezierCurve(pathpoints)
    
    def get_point(self, t, noise):
        x,y = self.center
        self.center = self.path.get_point(t/self.circlenumber)

        x = self.center[0] + self.radius * math.cos(2 * math.pi * t)*(self.x_stretch+ max(0.1,math.sin(t))) + noise*(randrange(0,100)-50)
        y = self.center[1] + self.radius * math.sin(2 * math.pi * t)*(self.y_stretch+ max(0.1,math.sin(t))) + noise*(randrange(0,100)-50)
        return (x, y)

    def outputCircles(self, circlenumber= 10, fidelity = 1000, noise = 0):
        num_points = fidelity
        return [self.get_point(t*circlenumber / num_points,noise) for t in range(num_points)]

if __name__== "__main__":
# Create a circle with radius 1 and center (0, 0)
    circle = Circle(1, pathpoints=[(-1, 1), (-4, 1), (-4, 2), (-14, 2)])

    # Traverse the circle and plot the points
    points = circle.outputCircles()
    x_vals, y_vals = zip(*points)
    plt.plot(x_vals, y_vals)
    plt.axis('equal')
    plt.show()