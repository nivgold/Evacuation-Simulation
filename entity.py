import numpy as np

class Entity:
    def __init__(self, room, m=80, v_0=1.5, radii=1, B=0.08, A=2*10**3, tau=0.5, k=1.2*10**5, kap=2.4*10**5):
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

        # location of the Entity (x,y) (m,m)
        self.r = np.zeros((2, 9000))
        # velocity of the Entity (v_x, v_y) (m/s, m/s)
        self.v = np.zeros((2, 9000))

        # Other Entities parameters
        self.other_agents = []

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

    def get_e_0(self):
        if self.room.two_doors == False:
            return (-self.r + self.room.door_location) / np.linalg.norm(-self.r + self.room.door_location)
        else:
            pass

    def set_other_agents(self, other_agents):
        self.other_agents = other_agents

    def f_agents(self):
        f_ij = []
        for other_agent in self.other_agents:
            f_ij.append(self.f_ij(other_agent))
        f_ij = np.array(f_ij)
        sum_f_ij = np.sum(f_ij, 1)
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
        f_walls = []
        for wall in self.room.walls:
            f_walls.append(self.f_iW(wall))
        f_walls = np.array(f_walls)
        sum_f_wall = np.sum(f_walls)
        return sum_f_wall

    def f_iW(self, wall):
        d_iW, n_iW, t_iW = self.wall_distance(wall)
        first_term = self.A * np.exp((self.radii - d_iW) / self.B) + self.k * self.g(self.radii - d_iW)
        second_term = self.kap * self.g(self.radii - d_iW) * self.v.dot(t_iW)
        f_iW = first_term * n_iW - second_term * t_iW

        return f_iW

    def wall_distance(self, wall):
        wall_vec = wall[1, :] - wall[0, :]
        distance_vec = self.r - wall[0, :]
        wall_len = np.linalg.norm(wall_vec)
        wall_unitvec = wall_vec / wall_len
        distance_vec_scaled = distance_vec / wall_len
        temp = wall_unitvec.dot(distance_vec_scaled)
        if temp < 0.0:
            temp = 0.0
        elif temp > 1.0:
            temp = 1.0
        nearest = wall_vec*temp
        dist = distance_vec - nearest
        nearest = nearest + wall[0, :]
        d_iW = np.linalg.norm(dist)
        n_iW = dist / d_iW
        t_iW = np.array([-n_iW[1], n_iW[0]])
        return d_iW, n_iW, t_iW


    def acceleration_calc(self):
        dv_dt = (self.v_0 * self.get_e_0() - self.v) / self.tau + self.f_agents() / self.m + self.f_walls() / self.m
        return dv_dt