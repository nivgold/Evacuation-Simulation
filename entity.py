import numpy as np


class Entity:
    def __init__(self, room, r, v, m=80, v_0=1.5, radii=1, B=0.08, A=2*10**3, tau=0.5, k=1.2*10**5, kap=2.4*10**5):
        # Individual Entity Parameters

        # weight
        self.m = m
        # desired velocity (m/s)
        self.v_0 = v_0
        # radius of observed entities (m)
        self.radii = radii
        # constant (m)
        self.B = B
        # constant (N)
        self.A = A
        # acceleration time (s)
        self.tau = tau
        # parameter (kg/s^2)
        self.k = k
        # parameter (kg/m*s)
        self.kap = kap
        # init location
        self.r = r
        # velocity of the Entity (v_x, v_y) (m/s, m/s)
        self.v = v
        # direction of the Entity
        random_destination = np.random.uniform(-1, 1, (2,))
        self.e_0 = random_destination

        # left - blind
        self.left_blind = False
        # fog - blind
        self.fog_blind = False
        # does escaped
        self.escaped = False

        # Other Entities parameters
        self.other_agents = set()

        # Room Container Parameters

        # room
        self.room = room

    def get_rij(self, other_agent):
        return self.radii + other_agent.radii

    def g(self, x):
        if x < 0:
            return 0
        else:
            return x

    def set_left_blind(self):
        self.left_blind = True

    def set_fog_blind(self):
        self.fog_blind = True

    def set_escaped(self):
        self.escaped = True

    def get_neighbors_directions(self):
        # not close to any door -> following the agents in the radius
        neighbors_directions = []
        for other_agent in self.other_agents:
            if np.linalg.norm(self.r - other_agent.r) < 5:
                neighbors_directions.append(other_agent.e_0)

        neighbors_directions = np.array(neighbors_directions)
        if len(neighbors_directions) == 0:
            return self.e_0
        direction = np.mean(neighbors_directions, axis=0)
        return direction

    def calculate_e_0(self):
        if not self.room.two_doors:
            # one door situation
            direction = (-self.r + self.room.door_location) / np.linalg.norm(-self.r + self.room.door_location)

            if self.fog_blind:
                # one door , fog situation
                distance = np.linalg.norm(-self.r + self.room.door_location)
                if distance > 5:
                    direction = self.get_neighbors_directions()

        else:
            # two doors situation
            if self.left_blind:
                # two doors situation, left-blind situation
                right_door_location = self.room.get_left_right_door_location()[1]
                direction = (-self.r + right_door_location) / np.linalg.norm(-self.r + right_door_location)
            elif self.fog_blind:
                # two doors situation, fog-blind situation
                right_door_location = self.room.get_left_right_door_location()[1]
                right_distance = np.linalg.norm(self.r - right_door_location)

                left_door_location = self.room.get_left_right_door_location()[0]
                left_distance = np.linalg.norm(self.r - left_door_location)

                if np.min(np.array([right_distance, left_distance])) > 5:
                    # not close to any door -> following the agents in the radius
                    direction = self.get_neighbors_directions()
                else:
                    # close to one door
                    if right_distance < left_distance:
                        # going to right door
                        direction = (-self.r + right_door_location) / np.linalg.norm(-self.r + right_door_location)
                    else:
                        # going to left door
                        direction = (-self.r + left_door_location) / np.linalg.norm(-self.r + left_door_location)
            else:
                # normal two doors situation
                right_door_location = self.room.get_left_right_door_location()[1]
                right_distance = np.linalg.norm(self.r - right_door_location)

                left_door_location = self.room.get_left_right_door_location()[0]
                left_distance = np.linalg.norm(self.r - left_door_location)

                if right_distance < left_distance:
                    # go to right door
                    direction = (-self.r + right_door_location) / right_distance
                else:
                    # go to left door
                    direction = (-self.r + left_door_location) / left_distance

        self.e_0 = direction

    def check_escaped(self):
        if not self.room.two_doors:
            door_location = self.room.get_door_location()
            distance = np.linalg.norm(self.r - door_location)
        else:
            if self.left_blind:
                right_door_location = self.room.get_left_right_door_location()[1]
                distance = np.linalg.norm(self.r - right_door_location)

            else:
                # including both the fog-blind and regular two-doors cases
                right_door_location = self.room.get_left_right_door_location()[1]
                right_distance = np.linalg.norm(self.r - right_door_location)

                left_door_location = self.room.get_left_right_door_location()[0]
                left_distance = np.linalg.norm(self.r - left_door_location)



                distance = np.min(np.array([right_distance, left_distance]))

        if distance < 0.5:
            # set entity to be escaped
            self.set_escaped()
            return True
        return False

    def set_other_agents(self, other_agents):
        self.other_agents = other_agents - {self}

    def f_agents(self):
        f_ij = []
        for other_agent in self.other_agents:
            if not other_agent.escaped:
                f_ij.append(self.f_ij(other_agent))
        f_ij = np.array(f_ij)
        if len(f_ij) == 0:
            return 0
        sum_f_ij = np.sum(f_ij, axis=0)
        return sum_f_ij

    def f_ij(self, other_agent):
        d_ij, n_ij, t_ij, dv_ij = self.agent_distance(other_agent)
        r_ij = self.get_rij(other_agent)
        first_term = self.A * np.exp((r_ij - d_ij) / self.B) + self.k * self.g(r_ij - d_ij)
        second_term = self.kap * self.g(r_ij - d_ij) * dv_ij
        f_ij = first_term * n_ij + second_term * t_ij
        return f_ij

    def agent_distance(self, other_agent):
        d_ij = np.linalg.norm(self.r - other_agent.r)
        n_ij = (self.r - other_agent.r) / d_ij
        t_ij = np.array([-n_ij[1], n_ij[0]])
        dv_ij = (other_agent.r - self.r).dot(t_ij)
        return d_ij, n_ij, t_ij, dv_ij

    def f_walls(self):
        f_walls = 0
        for wall in self.room.walls:
            f_walls += self.f_iW(wall)
        f_walls = np.array(f_walls)
        return f_walls

    def f_iW(self, wall):
        d_iW, n_iW, t_iW = self.wall_distance(wall)
        first_term = self.A * np.exp((self.radii - d_iW) / self.B) + self.k * self.g(self.radii - d_iW)
        second_term = self.kap * self.g(self.radii - d_iW) * self.v.dot(t_iW)
        f_iW = first_term * n_iW - second_term * t_iW

        return f_iW

    def wall_distance(self, wall):

        # need to find wall closest coordinates
        wall_p1 = wall[0, :]
        wall_p2 = wall[1, :]
        agent_point = self.r

        wall_vec = wall_p2 - wall_p1
        det = np.sum(wall_vec**2)
        a = np.sum(wall_vec * (agent_point - wall_p1)) / det
        wall_closest_point = wall_p1 + a * wall_vec

        d_iW = np.linalg.norm(agent_point - wall_closest_point)
        n_iW = (self.r - wall_closest_point) / d_iW
        t_iW = np.array([-n_iW[1], n_iW[0]])

        return d_iW, n_iW, t_iW



    def acceleration_calc(self):
        self.calculate_e_0()
        dv_dt = (self.v_0 * self.e_0 - self.v) / self.tau + self.f_agents() / self.m + self.f_walls() / self.m
        return dv_dt