from matplotlib import colors, cm
from matplotlib.ticker import PercentFormatter
from simulation import Simulation
import matplotlib.pyplot as plt
import numpy as np


def ex1():
    plt.style.use('ggplot')

    def ex1a():
        print("--------------------------------------------")
        print("1.a:")

        a = Simulation(num_individuals=1, num_steps=9000, random_loc=False)
        a.run()
        print("evacuation time: " + str(a.evacuation_time))
        # x velocity graph:
        max_step = int(a.evacuation_time/0.01)
        vel_x = a.v[0, 0, :][:max_step-1]
        axis_time = np.array([x*0.01 for x in range(0, max_step-1)])
        plt.plot(axis_time, vel_x)
        plt.xticks(axis_time[::50])
        plt.xlabel("time (s)")
        plt.ylabel("X Velocity (m/s)")
        plt.ylim(0-0.1, 1.6)
        plt.xlim(0-0.1, (max_step-2)*0.01)
        plt.title("Velocity of x axis by time")
        plt.savefig('./out/Vx_to_time.png')

        # y velocity graph:
        plt.figure()
        max_step = int(a.evacuation_time / 0.01)
        vel_y = a.v[1, 0, :][:max_step-1]
        plt.plot(axis_time, vel_y)
        plt.xticks(axis_time[::50])
        plt.ylim(-5, 5)
        plt.xlim(0, (max_step-2)*0.01)
        plt.xlabel("time (s)")
        plt.ylabel("Y Velocity (m/s)")
        plt.title("Velocity of y axis by time")
        plt.savefig('./out/Vy_to_time.png')

        # y to x graph
        plt.figure()
        y_vals = a.y[1, 0, :][:max_step-1]
        x_vals = a.y[0, 0, :][:max_step-1]
        plt.plot(x_vals, y_vals)
        plt.xlabel("X Coordinate (m)")
        plt.ylabel("Y Coordinate (m)")
        plt.xlim(0, 14.5)
        plt.ylim(0, 15)
        plt.title("Location")
        plt.savefig('./out/y_to_x_locations.png')

    def ex1b():
        print("--------------------------------------------")
        print("1.b:")
        lst_evac = []
        lst_locations = []
        for i in range(200):
            a = Simulation(num_individuals=1, num_steps=9000, random_loc=True)
            a.run()
            lst_evac.append(a.evacuation_time)
            lst_locations.append(a.y)

        # print longest evacuation time:
        print("Longest evacuation time: " + str(max(lst_evac)) + "s")

        # plot evacuation time distribution:
        plt.figure()
        fig, axs = plt.subplots(1, 1, tight_layout=True)
        axs.hist(lst_evac, bins=30, density=True, facecolor='g', alpha=0.75)
        # Now we format the y-axis to display percentage
        plt.xlabel("Evacuation Time (s)")
        plt.ylabel("Probability")
        plt.title("Evacuation Time Distribution")
        plt.savefig('./out/Evacuation_Time_hist.png')

        return lst_locations

    def ex1c(lst_locations):
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

    # ex1a()
    locations = ex1b()
    # ex1c(locations)

def ex2():

    def ex2a():
        # 2.a:
        print("2.a:")
        print("--------------------------------------------")
        simulation_2a20 = Simulation(num_individuals=20, num_steps=9000, random_loc=True)
        simulation_2a20.run()
        print(f'Evacuation Time with 20 agents: {simulation_2a20.evacuation_time}s, agents escaped: {simulation_2a20.agents_escaped}')

        # simulation_2a50 = Simulation(num_individuals=50, num_steps=9000, random_loc=True)
        # simulation_2a50.run()
        # print(f'Evacuation Time with 50 agents: {simulation_2a50.evacuation_time}s, agents escaped: {simulation_2a50.agents_escaped}')

        simulation_2a100 = Simulation(num_individuals=100, num_steps=9000, random_loc=True)
        simulation_2a100.run()
        print(f'Evacuation Time with 100 agents: {simulation_2a100.evacuation_time}s')

        simulation_2a200 = Simulation(num_individuals=200, num_steps=9000, random_loc=True)
        simulation_2a200.run()
        print(f'Evacuation Time with 200 agents: {simulation_2a200.evacuation_time}s')

    def ex2b():
        # 2.b:
        print("2.b:")
        print("--------------------------------------------")
        plt.style.use('ggplot')

        evacuation_time = []
        desired_velocity = np.arange(0.5, 5, 0.2)
        for v_des in desired_velocity:
            print(f'run with {v_des} velocity')
            simulation = Simulation(num_individuals=50, num_steps=9000, random_loc=True, v_des=v_des, radii=0.1)
            simulation.run()
            print(simulation.evacuation_time)
            evacuation_time.append(simulation.evacuation_time)

        plt.figure()
        plt.plot(desired_velocity, evacuation_time)
        plt.xlabel("Desired Velocity (m/s)")
        plt.ylabel("Evacuation Time (s)")
        plt.xlim(0, 5.5)
        plt.ylim(0, 91)
        plt.title("Evacuation Time to Desired Velocity for 50 People")
        plt.savefig('./out/Evacuation_time_to_desired_velocity.png')

    def ex2c():
        # 2.c:
        print("2.c:")
        print("--------------------------------------------")
        plt.style.use('ggplot')

        plt.figure(figsize=(10, 8))
        for num_people in [20, 50, 75, 100]:
            evacuation_time = []
            desired_velocity = np.arange(0.5, 5, 0.2)
            for v_des in desired_velocity:
                print(f'run with {num_people} people and {v_des} velocity')
                simulation = Simulation(num_individuals=num_people, num_steps=9000, random_loc=True, v_des=v_des)
                simulation.set_elders_conditions()
                simulation.run()
                evacuation_time.append(simulation.evacuation_time)

            plt.plot(desired_velocity, evacuation_time, label=f"{num_people} People")


        plt.xlabel("Desired Velocity (m/s)")
        plt.ylabel("Evacuation Time (s)")
        plt.xlim(0, 5.5)
        plt.ylim(0, 91)
        plt.legend()
        plt.title("Evacuation Time to Desired Velocity for Simulations with 20% are Elders")
        plt.savefig('./out/Evacuation_time_to_desired_velocity_elders.png')


    # ex2a()
    # ex2b()
    ex2c()

def ex3():

    def ex3a():
        print("--------------------------------------------")
        print("3.a 20 entities with two doors:")
        a = Simulation(num_individuals=20, num_steps=9000, random_loc=True, two_door_room=True)
        a.run()
        print("Evacuation time: " + str(a.evacuation_time))
        print(f"escaped: {a.agents_escaped}")

        print("3.a 50 entities with two doors:")
        a = Simulation(num_individuals=50, num_steps=9000, random_loc=True, two_door_room=True)
        a.run()
        print("Evacuation time: " + str(a.evacuation_time))
        print(f"escaped: {a.agents_escaped}")

        print("3.a 75 entities with two doors:")
        a = Simulation(num_individuals=75, num_steps=9000, random_loc=True, two_door_room=True)
        a.run()
        print("Evacuation time: " + str(a.evacuation_time))
        print(f"escaped: {a.agents_escaped}")

        print("3.a 100 entities with two doors:")
        a = Simulation(num_individuals=100, num_steps=9000, random_loc=True, two_door_room=True)
        a.run()
        print("Evacuation time: " + str(a.evacuation_time))
        print(f"escaped: {a.agents_escaped}")

    def ex3b():
        print("--------------------------------------------")
        print("3.b 20 entities with two doors and half are left-door blinded:")
        b = Simulation(num_individuals=20, num_steps=9000, random_loc=True, two_door_room=True)
        b.set_left_blind_conditions()
        b.run()
        print("Evacuation time: " + str(b.evacuation_time))

        print("3.b 50 entities with two doors and half are left-door blinded:")
        b = Simulation(num_individuals=50, num_steps=9000, random_loc=True, two_door_room=True)
        b.set_left_blind_conditions()
        b.run()
        print("Evacuation time: " + str(b.evacuation_time))

        print("3.b 75 entities with two doors and half are left-door blinded:")
        b = Simulation(num_individuals=75, num_steps=9000, random_loc=True, two_door_room=True)
        b.set_left_blind_conditions()
        b.run()
        print("Evacuation time: " + str(b.evacuation_time))

        print("3.b 100 entities with two doors and half are left-door blinded:")
        b = Simulation(num_individuals=100, num_steps=9000, random_loc=True, two_door_room=True)
        b.set_left_blind_conditions()
        b.run()
        print("Evacuation time: " + str(b.evacuation_time))

    def ex3c():
        print("--------------------------------------------")
        print("Two Doors with Fog:")
        print("20 entities with two doors and fog:")
        c = Simulation(num_individuals=20, num_steps=9000, random_loc=True, two_door_room=True, v_des=0.8)
        c.set_fog_conditions()
        c.run()
        print("Evacuation time: " + str(c.evacuation_time))
        print("Dying probability: " + str(c.death_proba))

        print("50 entities with two doors and fog:")
        c = Simulation(num_individuals=50, num_steps=9000, random_loc=True, two_door_room=True, v_des=0.9)
        c.set_fog_conditions()
        c.run()
        print("Evacuation time: " + str(c.evacuation_time))
        print("Dying probability: " + str(c.death_proba))

        print("75 entities with two doors and fog:")
        c = Simulation(num_individuals=75, num_steps=9000, random_loc=True, two_door_room=True, v_des=0.9)
        c.set_fog_conditions()
        c.run()
        print("Evacuation time: " + str(c.evacuation_time))
        print("Dying probability: " + str(c.death_proba))

        print("100 entities with two doors and fog:")
        c = Simulation(num_individuals=100, num_steps=9000, random_loc=True, two_door_room=True, v_des=0.5)
        c.set_fog_conditions()
        c.run()
        print("Evacuation time: " + str(c.evacuation_time))
        print("Dying probability: " + str(c.death_proba))

        print("--------------------------------------------")
        print("One Door with Fog:")
        print("20 entities with one door and fog:")
        c = Simulation(num_individuals=20, num_steps=9000, random_loc=True, two_door_room=False, v_des=0.8)
        c.set_fog_conditions()
        c.run()
        print("Evacuation time with only one door: " + str(c.evacuation_time))
        print("Dying probability with only one door: " + str(c.death_proba))

        print("50 entities with one door and fog:")
        c = Simulation(num_individuals=50, num_steps=9000, random_loc=True, two_door_room=False, v_des=0.8)
        c.set_fog_conditions()
        c.run()
        print("Evacuation time with only one door: " + str(c.evacuation_time))
        print("Dying probability with only one door: " + str(c.death_proba))

        print("75 entities with one door and fog:")
        c = Simulation(num_individuals=75, num_steps=9000, random_loc=True, two_door_room=False, v_des=0.5)
        c.set_fog_conditions()
        c.run()
        print("Evacuation time with only one door: " + str(c.evacuation_time))
        print("Dying probability with only one door: " + str(c.death_proba))

        print("100 entities with one door and fog:")
        c = Simulation(num_individuals=100, num_steps=9000, random_loc=True, two_door_room=False, v_des=0.5)
        c.set_fog_conditions()
        c.run()
        print("Evacuation time with only one door: " + str(c.evacuation_time))
        print("Dying probability with only one door: " + str(c.death_proba))

    ex3a()
    ex3b()
    ex3c()

def second_3():
    print("--------------------------------------------")
    print("Simulations with one door:")

    agents = 20
    simulation = Simulation(num_individuals=agents, num_steps=9000, two_door_room=False, random_loc=True,
                            is_distributed=True)
    simulation.run()
    print(f'           Evacuation time: {simulation.evacuation_time}s')
    print(f'{agents} Agents: ')
    print('           Death Probability: {:2.2f}%\n'.format(simulation.death_proba*100))

    agents = 50
    simulation = Simulation(num_individuals=agents, num_steps=9000, two_door_room=False, random_loc=True,
                            is_distributed=True)
    simulation.run()
    print(f'           Evacuation time: {simulation.evacuation_time}s')
    print(f'{agents} Agents: ')
    print('           Death Probability: {:2.2f}%\n'.format(simulation.death_proba * 100))

    agents = 75
    simulation = Simulation(num_individuals=agents, num_steps=9000, two_door_room=False, random_loc=True,
                            is_distributed=True)
    simulation.run()
    print(f'           Evacuation time: {simulation.evacuation_time}s')
    print(f'{agents} Agents: ')
    print('           Death Probability: {:2.2f}%\n'.format(simulation.death_proba * 100))

    agents = 100
    simulation = Simulation(num_individuals=agents, num_steps=9000, two_door_room=False, random_loc=True,
                            is_distributed=True)
    simulation.run()
    print(f'           Evacuation time: {simulation.evacuation_time}s')
    print(f'{agents} Agents: ')
    print('           Death Probability: {:2.2f}%\n'.format(simulation.death_proba * 100))

    print("--------------------------------------------")
    print("Simulations with two doors:")

    agents = 20
    simulation = Simulation(num_individuals=agents, num_steps=9000, two_door_room=True, random_loc=True,
                            is_distributed=True)
    simulation.run()
    print(f'           Evacuation time: {simulation.evacuation_time}s')
    print(f'{agents} Agents: ')
    print('           Death Probability: {:2.2f}%\n'.format(simulation.death_proba * 100))

    agents = 50
    simulation = Simulation(num_individuals=agents, num_steps=9000, two_door_room=True, random_loc=True,
                            is_distributed=True)
    simulation.run()
    print(f'           Evacuation time: {simulation.evacuation_time}s')
    print(f'{agents} Agents: ')
    print('           Death Probability: {:2.2f}%\n'.format(simulation.death_proba * 100))

    agents = 75
    simulation = Simulation(num_individuals=agents, num_steps=9000, two_door_room=True, random_loc=True,
                            is_distributed=True)
    simulation.run()
    print(f'           Evacuation time: {simulation.evacuation_time}s')
    print(f'{agents} Agents: ')
    print('           Death Probability: {:2.2f}%\n'.format(simulation.death_proba * 100))

    agents = 100
    simulation = Simulation(num_individuals=agents, num_steps=9000, two_door_room=True, random_loc=True,
                            is_distributed=True)
    simulation.run()
    print(f'           Evacuation time: {simulation.evacuation_time}s')
    print(f'{agents} Agents: ')
    print('           Death Probability: {:2.2f}%\n'.format(simulation.death_proba * 100))


if __name__ == '__main__':
    # ex1()
    ex2()
    # ex3()
    # second_3()
