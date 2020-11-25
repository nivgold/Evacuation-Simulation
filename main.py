from matplotlib import colors, cm
from matplotlib.ticker import PercentFormatter
from simulation import Simulation
import matplotlib.pyplot as plt
import numpy as np


def ex1():
    # 1.a:
    print("--------------------------------------------")
    print("1.a:")
    a = Simulation(num_individuals=1, num_steps=9000, v_des=1.5, random_loc=False, radii=0.2)
    a.run()

    print("evacuation time: " + str(a.evacuation_time))

    # x velocity graph:
    steps = int(a.evacuation_time/0.01)
    vel_x = a.v[0, 0, :][:steps]
    axis_time = np.array([x*0.01 for x in range(0, steps)])
    plt.scatter(axis_time, vel_x)
    plt.xlabel("time (s)")
    plt.ylabel("X velocity")
    plt.ylim(-0.1, 1.6)
    plt.title("V_x to time")
    plt.savefig('Vx_to_time.png')

    # y velocity graph:
    plt.figure()
    steps = int(a.evacuation_time / 0.01)
    vel_y = a.v[1, 0, :steps]
    plt.scatter(axis_time, vel_y)
    plt.ylim(-5, 5)
    plt.xlabel("time (s)")
    plt.ylabel("y velocity")
    plt.title("V_y to time")
    plt.savefig('Vy_to_time.png')

    # y to x graph
    plt.figure()
    y_vals = a.y[1, 0, :steps]
    x_vals = a.y[0, 0, :steps]
    plt.scatter(x_vals, y_vals)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(0, 15)
    plt.ylim(0, 15)
    plt.title("locations")
    plt.savefig('y_to_x_locations.png')

    print("--------------------------------------------")
    print("1.b:")
    lst_evac = []
    lst_locations = []
    for i in range(200):
        a = Simulation(num_individuals=1, num_steps=9000, v_des=1.5, random_loc=True, radii=0.2)
        a.run()
        lst_evac.append(a.evacuation_time)
        lst_locations.append(a.y)

    # print longest evacuation time:
    print("longest evacuation time: " + str(max(lst_evac)))

    # plot evacuation time distribution:
    plt.figure()
    fig, axs = plt.subplots(1, 1, tight_layout=True)
    axs.hist(lst_evac, bins=10, density=True)
    # Now we format the y-axis to display percentage
    axs.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    plt.xlabel("Evacuation Time Values")
    plt.ylabel("Percentage")
    plt.title("Evacuation Time Distribution")
    plt.savefig('1b_Evacuation_Time_hist.png')

    print("--------------------------------------------")
    print("1.c:")
    #  print how many collisions were: dist <= 0.5
    coll_counter = 0
    for step in range(9000):
        vec = []
        for y_mat in lst_locations:
            vec.append(y_mat[:, 0, step])
        for i in range(len(vec)):
            if np.all(vec[i] == 0):
                continue
            else:
                for j in range(i+1, len(vec)):
                    if np.linalg.norm(vec[i]-vec[j]) <= 0.5:
                        coll_counter += 1
    print("there were: " + str(coll_counter) + " mutual interceptions")


def ex2():
    pass


def ex3():
    pass


if __name__ == '__main__':
    ex1()
    # ex2()
    # ex3()

