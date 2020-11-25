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

    # x velocity graph:
    steps = int(a.evacuation_time/0.01)
    vel_x = a.v[0, 0, :][:steps]
    axis_time = np.array([x*0.01 for x in range(0, steps)])
    plt.scatter(axis_time, vel_x)
    plt.xlabel("time (s)")
    plt.ylabel("X velocity")
    plt.title("V_x to time")
    plt.savefig('Vx_to_time.png')
    plt.close()

    # y velocity graph:
    steps = int(a.evacuation_time / 0.01)
    vel_y = a.v[1, 0, :steps]
    axis_time = np.array([x * 0.01 for x in range(0, steps)])
    plt.scatter(axis_time, vel_y)
    plt.xlabel("time (s)")
    plt.ylabel("y velocity")
    plt.title("V_y to time")
    plt.savefig('Vy_to_time.png')
    plt.close()

    # y to x graph
    y_vals = a.v[1, 0, :]
    x_vals = a.v[0, 0, :]
    plt.scatter(x_vals, y_vals)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("locations")
    plt.savefig('y_to_x_locations.png')
    plt.close()










def ex2():
    pass

def ex3():
    pass

if __name__ == '__main__':
    ex1()
    # ex2()
    # ex3()

