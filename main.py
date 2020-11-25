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

    def ex2a():
        # 2.a:
        print("2.a:")
        print("--------------------------------------------")
        simulation_2a20 = Simulation(num_individuals=20, num_steps=9000, random_loc=True)
        simulation_2a20.run()
        print(f'Evacuation Time with 20 agents: {simulation_2a20.evacuation_time}s, agents escaped: {simulation_2a20.agents_escaped}')
        print(simulation_2a20.y[:, :, int(simulation_2a20.evacuation_time/0.01) - 2])

        simulation_2a50 = Simulation(num_individuals=50, num_steps=9000, random_loc=True)
        simulation_2a50.run()
        print(f'Evacuation Time with 50 agents: {simulation_2a50.evacuation_time}s, agents escaped: {simulation_2a50.agents_escaped}')
        print(simulation_2a50.y[:, :, int(simulation_2a50.evacuation_time / 0.01) - 1])

        simulation_2a100 = Simulation(num_individuals=100, num_steps=9000, random_loc=True)
        simulation_2a100.run()
        print(f'Evacuation Time with 100 agents: {simulation_2a100.evacuation_time}s')
        print(simulation_2a100.y[:, :, int(simulation_2a100.evacuation_time / 0.01) - 1])

        simulation_2a200 = Simulation(num_individuals=200, num_steps=9000, random_loc=True)
        simulation_2a200.run()
        print(f'Evacuation Time with 200 agents: {simulation_2a200.evacuation_time}s')
        print(simulation_2a200.y[:, :, int(simulation_2a200.evacuation_time / 0.01) - 1])

    def ex2b():
        # 2.b:
        print("2.b:")
        print("--------------------------------------------")
        simulation_v_1_5 = Simulation(num_individuals=20, num_steps=9000, random_loc=True, v_des=1.5)
        simulation_v_1_5.run()
        print(f'Evacuation Time with 20 agents and desired speed of 1.5: {simulation_v_1_5.evacuation_time}s')

        simulation_v_2 = Simulation(num_individuals=20, num_steps=9000, random_loc=True, v_des=2)
        simulation_v_2.run()
        print(f'Evacuation Time with 20 agents and desired speed of 2: {simulation_v_2.evacuation_time}s')

        simulation_v_3 = Simulation(num_individuals=20, num_steps=9000, random_loc=True, v_des=3)
        simulation_v_3.run()
        print(f'Evacuation Time with 20 agents and desired speed of 3: {simulation_v_3.evacuation_time}s')

        simulation_v_0_8 = Simulation(num_individuals=20, num_steps=9000, random_loc=True, v_des=0.8)
        simulation_v_0_8.run()
        print(f'Evacuation Time with 20 agents and desired speed of 0.8: {simulation_v_0_8.evacuation_time}s')

        simulation_v_0_5 = Simulation(num_individuals=20, num_steps=9000, random_loc=True, v_des=0.5)
        simulation_v_0_5.run()
        print(f'Evacuation Time with 20 agents and desired speed of 0.5: {simulation_v_0_5.evacuation_time}s')

    def ex2c():
        # 2.c:
        print("2.c:")
        print("--------------------------------------------")
        simulation_20 = Simulation(num_individuals=20, num_steps=9000, random_loc=True)
        simulation_20.set_elders_conditions()
        simulation_20.run()
        print(f'Evacuation Time with 20 agents while 4 are elders: {simulation_20.evacuation_time}s')

        simulation_50 = Simulation(num_individuals=50, num_steps=9000, random_loc=True)
        simulation_50.set_elders_conditions()
        simulation_50.run()
        print(f'Evacuation Time with 50 agents while 10 are elders: {simulation_50.evacuation_time}s')

        simulation_75 = Simulation(num_individuals=75, num_steps=9000, random_loc=True)
        simulation_75.set_elders_conditions()
        simulation_75.run()
        print(f'Evacuation Time with 75 agents while 15 are elders: {simulation_75.evacuation_time}s')

        simulation_100 = Simulation(num_individuals=100, num_steps=9000, random_loc=True)
        simulation_100.set_elders_conditions()
        simulation_100.run()
        print(f'Evacuation Time with 100 agents while 20 are elders: {simulation_100.evacuation_time}s')

        simulation_150 = Simulation(num_individuals=150, num_steps=9000, random_loc=True)
        simulation_150.set_elders_conditions()
        simulation_150.run()
        print(f'Evacuation Time with 150 agents while 30 are elders: {simulation_150.evacuation_time}s')


    ex2a()
    ex2b()
    ex2c()



def ex3():
    print("--------------------------------------------")
    print("3.a (for 50 entities):")
    a = Simulation(num_individuals=50, num_steps=9000, random_loc=False, two_door_room=True, radii=0.2)
    a.run()
    print("Evacuation time: " + str(a.evacuation_time))
    a = None  # free space

    print("--------------------------------------------")
    print("3.b (for 50 entities):")
    b = Simulation(num_individuals=50, num_steps=9000, random_loc=False, two_door_room=True, radii=0.2)
    b.set_left_blind_conditions()
    b.run()
    print("Evacuation time: " + str(b.evacuation_time))
    b = None  # free space

    print("--------------------------------------------")
    print("3.c (for 50 entities):")
    c = Simulation(num_individuals=50, num_steps=9000, random_loc=False, two_door_room=True, radii=0.2)
    c.set_fog_conditions()
    c.run()
    print("Evacuation time: " + str(c.evacuation_time))
    print("Dying probability: " + str(c.death_proba))
    c = Simulation(num_individuals=50, num_steps=9000, random_loc=False, two_door_room=False, radii=0.2)
    c.set_fog_conditions()  # TODO support one door with fog case
    c.run()
    print("Evacuation time with only one door: " + str(c.evacuation_time))
    print("Dying probability with only one door: " + str(c.death_proba))
    c = None  # free space




if __name__ == '__main__':
    # ex1()
    # ex2()
     ex3()

