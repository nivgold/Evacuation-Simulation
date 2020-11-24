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

        # Room Container Parameters

        # room
        self.room = room