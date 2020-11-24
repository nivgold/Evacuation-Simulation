import numpy as np
import sys
from room import Room
from entity import Entity

'''
class to put the hole thing together. Its main parts
are the Differential Equation, the rooms, and the method 
of integration. The Integration can be done by calling
the run function. If the integration is done the results 
are saved in self.y for later use for example to display
them with with the function "Show"'''


class Simulation:
    def __init__(self, num_individuals, num_steps, radii=1, tau=0.1, v_des=1.5, two_door_room=False, mass=80,
                 room_size=(15, 15)):

        self.evacuation_time = 0

        # Constants
        self.num_steps = num_steps  # number of steps for integration

        # Agent information
        self.agents_escaped = 0  # number of agents escaped by timesteps
        self.v = np.zeros((2, self.N, self.num_steps))  # Three dimensional array of velocity
        self.y = np.zeros(
            (2, self.N, self.num_steps))  # Three dimensional array of place: x = coordinates, y = Agent, z=Time

        # other
        self.room = Room(two_doors=two_door_room, size=room_size)  # kind of room the simulation runs in

        # update y, v matrices
        self.fill_room(radii, num_individuals, v_des)
        self.entities = []
        for i in range(0, num_individuals):
            self.entities.append(Entity(self.room, self.y[:, i, 0], self.v[:, i, 0],
                                        mass, v_des, radii, tau=tau))  # initialize Entity
        self.entities = np.array(self.entities)

    # function set_time, set_steps give the possiblity to late change these variable when needed
    def set_steps(self, steps):
        self.num_steps = steps

    def dont_touch(self, i, x, radii):  # yields false if people don't touch each other and true if they do
        for j in range(i - 1):
            if np.linalg.norm(x - self.y[:, j, 0]) < 3 * radii:
                return True
        return False

    # fills the spawn zone with agents with random positions
    def fill_room(self, radii, num_individuals, v_des):
        spawn = self.room.get_spawn_zone()
        len_right = spawn[0, 1] - spawn[0, 0]
        len_left = spawn[1, 1] - spawn[1, 0]
        max_len = max(len_left, len_right)

        # checks if the area is too small for the agents to fit in
        area_people = 0
        for i in range(num_individuals):
            area_people += 4 * radii ** 2
        if area_people >= 0.7 * max_len ** 2:
            sys.exit('Too much people! Please change the size of the room/spawn-zone or the amount of people.')
        # checks if the agent touches another agent/wall and if so gives it a new random position in the spawn-zone
        for i in range(num_individuals):
            # The pedestrians don't touch the wall
            x = len_right * np.random.rand() + spawn[0, 0]
            y = len_left * np.random.rand() + spawn[1, 0]
            pos = [x, y]

            # The pedestrians don't touch each other
            while self.dont_touch(i, x, radii):
                x = len_right * np.random.rand() + spawn[0, 0]
                y = len_left * np.random.rand() + spawn[1, 0]
                pos = [x, y]
            self.y[:, i, 0] = pos

        self.v[:, :, 0] = v_des * self.diff_equ.e_t(self.y[:, :, 0])

    # calls the method of integration with the starting positions, diffequatial equation, number of steps, and delta t = tau
    def run(self):
        self.y, self.agents_escaped, self.forces = self.method(self.y[:, :, 0], self.v[:, :, 0], self.diff_equ.f,
                                                               self.num_steps, self.tau, self.room)