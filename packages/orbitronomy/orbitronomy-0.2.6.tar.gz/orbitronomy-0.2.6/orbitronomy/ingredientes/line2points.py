# import numpy as np
# from PyAstronomy import pyasl
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from matplotlib.animation import PillowWriter
# from mpl_toolkits.mplot3d import Axes3D
# from datetime import date


# class DrawLine:
    
#     def __init__(self, ax, draw=True):
#         self.ax = ax

#         self.color = "green"
#         self.draw = draw

#     def drawLineTwoPoints(self, point1, point2):

#         self.point1 = point1
#         self.point2 = point2

#         xs = [self.point1[0], self.point2[0]]
#         ys = [self.point1[1], self.point2[1]]
#         zs = [self.point1[2], self.point2[2]]

#         self.ax.plot(xs, ys, zs, color=self.color)
#         return xs, ys, zs
    
#     def drawLineTwoPointsName(self, name):
#         self.object_positions[name]

#         # get the coordinates of the object and draw a line from the sun to the object
#         self.drawLineTwoPoints([0, 0, 0], self.object_positions[name])


    
            