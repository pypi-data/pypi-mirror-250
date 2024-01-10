import numpy as np
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from mpl_toolkits.mplot3d import Axes3D
from datetime import date



class FeaturesExtra():
    
    def __init__(self, ax, alpha=1):
        self.ax = ax

        self.inclination_plot_color = "white"
        self.inclination_plot = False


    def inclinationObserver(self, semi_major_axis,
                            perihelion, eccentricity, 
                            longitude_of_ascending_node, 
                            inclination, argument_of_perihelion, 
                            actual_orbit, n_orbits, plot_steps):


        # Orbit with inclination set to 0 (projection)
        projected_orbit = pyasl.KeplerEllipse(a=float(semi_major_axis), per=float(perihelion), 
                                              e=float(eccentricity), Omega=float(longitude_of_ascending_node), 
                                              i=float(0), w=float(argument_of_perihelion))
        
        t_values = np.linspace(0, 4 * n_orbits, plot_steps)
        actual_positions = actual_orbit.xyzPos(t_values)
        projected_positions = projected_orbit.xyzPos(t_values)

    
        self.ax.plot(projected_positions[:,0], projected_positions[:,1], projected_positions[:,2], 
                     color=self.inclination_plot_color, alpha=self.alpha, linewidth=1)

        # Drawing lines more uniformly across the orbit
        num_lines = 300  # Adjust this number to control the density of lines
        step_size = len(actual_positions) // num_lines
        indices = np.linspace(0, len(actual_positions) - 1, num_lines, dtype=int)
        
        for i in indices:
            actual_pos = actual_positions[i]
            projected_pos = projected_positions[i]
            self.ax.plot([actual_pos[0], projected_pos[0]], 
                         [actual_pos[1], projected_pos[1]], 
                         [actual_pos[2], projected_pos[2]], 
                         color=self.inclination_plot_color, alpha=self.alpha, linewidth=1)

        self.ax.set_aspect('equal')