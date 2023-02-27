import sys

from simulation import SIMULATION

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
save = False if sys.argv[3] == "False" else True
simulation = SIMULATION(directOrGUI, solutionID, save)
simulation.Run()
simulation.Get_Fitness()