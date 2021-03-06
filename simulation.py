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
    def __init__(self, num_individuals, num_steps, radii=0.2, tau=0.5, v_des=0.8, two_door_room=False, mass=80,
                 room_size=(15, 15), random_loc=True, is_distributed=False):

        self.evacuation_time = 0

        # Constants
        self.num_steps = num_steps  # number of steps for integration
        self.v_des = v_des

        # Agent information
        self.agents_escaped = 0  # number of agents escaped by timesteps
        self.death_proba = 0
        self.v = np.zeros((2, num_individuals, self.num_steps))  # Three dimensional array of velocity
        self.y = np.zeros(
            (2, num_individuals, self.num_steps))  # Three dimensional array of place: x = coordinates, y = Agent, z=Time

        # other
        self.room = Room(two_doors=two_door_room, size=room_size)  # kind of room the simulation runs in
        if random_loc:
            self.fill_room(radii, num_individuals, v_des)
        # update y, v matrices
        else:
            self.fill_center_room()
        self.entities = []
        for i in range(0, num_individuals):
            if not is_distributed:
                self.entities.append(Entity(self.room, self.y[:, i, 0], self.v[:, i, 0],
                                        mass, v_des, radii, tau=tau))  # initialize Entity
            else:
                if i < num_individuals / 2:
                    mass_sample = np.random.normal(loc=81.74, scale=0.25)
                    velocity_sample = np.random.normal(loc=0.8, scale=0.1)
                else:
                    mass_sample = np.random.normal(loc=79.23, scale=0.25)
                    velocity_sample = np.random.normal(loc=0.7, scale=0.1)
                self.entities.append(Entity(self.room, self.y[:, i, 0], self.v[:, i, 0],
                                        mass_sample, velocity_sample, radii, tau=tau))
        self.entities = np.array(self.entities)

        for entity in self.entities:
            entity.set_other_agents(set(self.entities))

    # function set_time, set_steps give the possibility to late change these variable when needed
    def set_steps(self, steps):
        self.num_steps = steps

    def dont_touch(self, i, x, radii):  # yields false if people don't touch each other and true if they do
        for j in range(i - 1):
            if np.linalg.norm(x - self.y[:, j, 0]) < 3 * radii:
                return True
        return False

    # fills the spawn zone with agents with random positions
    def fill_room(self, radii, num_individuals, v_des):
        radii = 0.1
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

        self.v[:, :, 0] = 0

        # for i in range(num_individuals):
        #     self.y[:, i, 0] = np.array([np.random.uniform(0.01, 14), np.random.uniform(0.01, 14)])
        #     self.v[:, i, 0] = np.array([0, 0])


    def fill_center_room(self):
        pos = [self.room.get_room_size()/2, self.room.get_room_size()/2]
        self.y[:, 0, 0] = pos
        self.v[:, :, 0] = 0

    def set_fog_conditions(self):
        for i in range(0, len(self.entities), 2):
            self.entities[i].set_fog_blind()

    def set_left_blind_conditions(self):
        for i in range(0, len(self.entities), 2):
            self.entities[i].set_left_blind()

    def set_elders_conditions(self):
        elder_v_des = self.v_des / 3
        for i in range(0, len(self.entities), 5):
            self.entities[i].v_0 = elder_v_des

    def run(self):
        for k in range(self.num_steps-1):
            if self.agents_escaped == len(self.entities):
                break
            # print every 5 seconds
            # if k % 500 == 0:
            #     print(k*0.01, "agent escaped:"+ str(self.agents_escaped))
            #     # print(self.y[:, :, k])
            for index, entity in enumerate(self.entities):
                if not entity.escaped:
                    dv_dt = entity.acceleration_calc()

                    # updating location and velocity
                    self.v[:, index, k+1] = (dv_dt * 0.01) + self.v[:, index, k]
                    self.y[:, index, k+1] = self.y[:, index, k] + self.v[:, index, k+1]*0.01

                    # updating entity location and velocity
                    entity.r = self.y[:, index, k+1]
                    entity.v = self.v[:, index, k+1]


                    if entity.check_escaped():
                        self.agents_escaped += 1

            # check if there are entities that are out of the room
            flag = True
            for i in range(len(self.entities)):
                if not self.entities[i].escaped:
                    if self.entities[i].r[0] < 0 or self.entities[i].r[1] < 0 or self.entities[i].r[0] > 15 or self.entities[i].r[1] > 15:
                        # location
                        self.y[:, i, k + 1] = np.array([np.random.uniform(0.01, 14), np.random.uniform(0.01, 14)])
                        self.entities[i].r = self.y[:, i, k + 1]
                        # velocity
                        self.v[:, i, k+1] = np.array([0, 0])
                        self.entities[i].v = self.v[:, i, k+1]


                        # if flag:
                        #     self.entities[i].set_escaped()
                        #     self.agents_escaped += 1
                        #     flag = False
                        # else:
                        #     self.entities[i].r = self.y[:, i, k]
                        #     flag = True
            # for i in range(len(self.entities)):
            #     if not self.entities[i].escaped:
            #         for j in range(i+1, len(self.entities)):
            #             if not self.entities[j].escaped:
            #                 if np.linalg.norm(self.entities[i].r - self.entities[j].r) <= 0.5:
            #                     i_distance = np.linalg.norm(self.entities[i].nearest_ext() - self.entities[i].r)
            #                     j_distance = np.linalg.norm(self.entities[j].nearest_ext() - self.entities[j].r)
            #                     if i_distance <= j_distance:
            #                         self.y[:, j, k+1] = self.y[:, j, k]
            #                         self.entities[j].r = self.y[:, j, k+1]
            #                     else:
            #                         self.y[:, i, k+1] = self.y[:, i, k]
            #                         self.entities[i].r = self.y[:, i, k+1]

        self.evacuation_time = 0.01 * (k+2)
        self.death_proba = 1 - (self.agents_escaped / len(self.entities))