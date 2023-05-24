################################################# IMPORTS ###########################################################
import matplotlib.pyplot as plt
import math as m
from vectors import Vector
import itertools
import numpy as np
############################################### GLOBAL CONSTANTS ####################################################
Iz = np.array([0,0,400])
Iy = np.array([0,400,0])
Ix = np.array([400,0,0])
#################################################### INPUTS #########################################################
r = (200, -150, 250)
v = (5, 0, 0)
h = np.cross(r,v)
N = np.cross(Iz,h)

class SolarSystem:
    def __init__(self, size):
        self.size = size
        self.bodies = []

        self.fig, self.ax = plt.subplots(
            1,
            1,
            subplot_kw={"projection": "3d"},
            figsize=(self.size / 50, self.size / 50),
        )
        self.fig.tight_layout()
        # self.ax.view_init(0, 0)

    def add_body(self, body):
        self.bodies.append(body)

    def update_all(self):
        for body in self.bodies:
            body.move()
            body.draw()
        
            
    def draw_all(self):
        origin = np.array([[0, 0, 0],[0, 0, 0],[0, 0, 0]]) # origin point
        self.ax.set_xlim((-self.size , self.size ))
        self.ax.set_xlabel("x")
        self.ax.set_ylim((-self.size , self.size ))
        self.ax.set_ylabel("y")
        self.ax.set_zlim((-self.size , self.size ))
        self.ax.set_zlabel("z")
        self.ax.quiver(*origin,Ix,Iy,Iz,color='black')
        plt.pause(0.001) # controls speed of simulation
        self.ax.clear()

    def calculate_all_body_interactions(self):
        bodies_copy = self.bodies.copy()
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                first.accelerate_due_to_gravity(second)
    


class SolarSystemBody:
    min_display_size = 10
    display_log_base = 1.3
    def __init__(
        self,
        solar_system,
        mass,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
    ):
        self.solar_system = solar_system
        self.mass = mass
        self.position = position
        self.velocity = Vector(*velocity)
        self.display_size = max(
            m.log(self.mass, self.display_log_base),
            self.min_display_size,
        )
        self.colour = "black"
        self.solar_system.add_body(self)

    def move(self):
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
            self.position[2] + self.velocity[2],
        )
    
    def draw(self):
        self.solar_system.ax.plot(
            *self.position,
            marker="o",
            markersize= self.display_size,
            # markersize=self.display_size + self.position[0] / 50, # changes the size depending on distance from viewer, it is arbitrary
            color=self.colour
        )
    
    def accelerate_due_to_gravity(self, other):
        distance = Vector(*other.position) - Vector(*self.position)
        distance_mag = distance.get_magnitude()
        force_mag = self.mass * other.mass / (distance_mag ** 2)
        force = distance.normalize() * force_mag
        reverse = 1
        for body in self, other:
            acceleration = force / body.mass
            body.velocity += acceleration * reverse
            reverse = -1

class Earth(SolarSystemBody):
    def __init__(
            self,
            solar_system,
            mass=10_000, 
            position=(0, 0, 0), 
            velocity=(0, 0, 0)
            ):
        super(Earth,self).__init__(solar_system, mass, position, velocity)
        self.colour = "blue"

class Sun(SolarSystemBody):
    def __init__(
        self,
        solar_system,
        mass=10_000,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
    ):
        super(Sun, self).__init__(solar_system, mass, position, velocity)
        self.colour = "yellow"

        
class Planet(SolarSystemBody):
    colours = itertools.cycle([(0, 0, 0), (1, 0, 0), (0, 0, 1)])
    def __init__(
        self,
        solar_system,
        mass=10,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
    ):
        super(Planet, self).__init__(solar_system, mass, position, velocity)
        self.colour = next(Planet.colours)



############################################### RUN INPUTS ####################################################

solar_system = SolarSystem(400)
earth = Earth(solar_system)
# sun = Sun(solar_system)
# planets = (
#     Planet(
#         solar_system,
#         position=(-150, -50, 0),
#         velocity=(0, 5, 5),
#     ),
#     Planet(
#         solar_system,
#         mass=20,
#         position=(-200, -150, 150),
#         velocity=(5, 0, 0)
#     )
# )
planet = Planet(
                solar_system, 
                mass= 1,
                position=r, 
                velocity=v)

while True:
    solar_system.calculate_all_body_interactions()
    solar_system.update_all()
    solar_system.draw_all()
# for _ in range(100):
#     solar_system.update_all()
#     solar_system.draw_all()

# plt.show()  # if not using interactive mode