from matplotlib import colors, cm
from matplotlib.ticker import PercentFormatter
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
    plt.ylim(-2, 1)
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

    # print("--------------------------------------------")
    # print("1.b:")
    # lst_evac = []
    # for i in range(200):
    #     a = Simulation(num_individuals=1, num_steps=9000, v_des=1.5, random_loc=True)
    #     a.run()
    #     lst_evac.append(a.evacuation_time)
    #
    # # plot evacuation time distribution:
    # fig, axs = plt.subplots(1, 1, tight_layout=True)
    #
    # # N is the count in each bin, bins is the lower-limit of the bin
    # N, bins, patches = axs[0].hist(lst_evac, bins=20)
    #
    # # We'll color code by height, but you could use any scalar
    # fracs = N / N.max()
    #
    # # we need to normalize the data to 0..1 for the full range of the colormap
    # norm = colors.Normalize(fracs.min(), fracs.max())
    #
    # # Now, we'll loop through our objects and set the color of each accordingly
    # for thisfrac, thispatch in zip(fracs, patches):
    #     color = plt.cm.viridis(norm(thisfrac))
    #     thispatch.set_facecolor(color)
    #
    # # Now we format the y-axis to display percentage
    # axs[0].yaxis.set_major_formatter(PercentFormatter(xmax=1))
    # plt.savefig('1b_Evacuation_Time_hist.png')


def ex2():
    pass


def ex3():
    print("--------------------------------------------")
    print("3.a:")
    a = Simulation(num_individuals=50, num_steps=9000, random_loc=False, two_door_room=True, radii=0.25,)
    a.run()
    print("Evacuation time: " + str(a.evacuation_time))



if __name__ == '__main__':
    # ex1()
    # ex2()
     ex3()

