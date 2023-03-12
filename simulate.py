import sys

from simulation import SIMULATION

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]

if len(sys.argv) > 4:
    sleep = float(sys.argv[3])
    simulation = SIMULATION(directOrGUI, solutionID, sleep)
else:
    simulation = SIMULATION(directOrGUI, solutionID)

simulation.Run()
simulation.Get_Fitness()