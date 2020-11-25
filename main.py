from simulation import Simulation
import matplotlib.pyplot as plt
import numpy as np


def ex1():
    # 1.a:
    print("--------------------------------------------")
    print("1.a:")
    a = Simulation(num_individuals=1, num_steps=9000, v_des=1.5, random_loc=False)

    a.run()

    print("starting point: " + str(a.y[:, :, 0][0][0]) + "," + str(a.y[:, :, 0][1][0]))
    print("evacuation time: " + str(a.evacuation_time))

    # print x velocity graph:
    steps = int(a.evacuation_time/0.01)
    vel_x = a.v[0, 0, :steps]
    axis_time = np.array([x*0.01 for x in range(0, steps)])

    plt.scatter(axis_time, vel_x)
    plt.xlabel("time (s)")
    plt.ylabel("X velocity")
    plt.savefig('1a_Xvelocity.png')

def ex2():
    pass

def ex3():
    pass

if __name__ == '__main__':
    ex1()
    # ex2()
    # ex3()

