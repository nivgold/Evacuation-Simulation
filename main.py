from simulation import Simulation
import matplotlib.pyplot as plt
a = Simulation(num_individuals=1, num_steps=9000, v_des=1.5)

a.run()

print(a.y[:, :, 0])
print(a.evacuation_time)