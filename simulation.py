import time

import pybullet as p
import pybullet_data

import constants as c
from robot import ROBOT
from world import WORLD


class SIMULATION:
	def __init__(self, directOrGUI, solutionID, sleep_time = 0.001):
		self.directOrGUI = directOrGUI
		self.sleep_time = sleep_time
		if directOrGUI == "DIRECT":
			self.physicsClient = p.connect(p.DIRECT)
		else:
			self.physicsClient = p.connect(p.GUI)
		p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
		p.setAdditionalSearchPath(pybullet_data.getDataPath())
		p.setGravity(0,0,-9.8)
		self.world = WORLD()
		self.robot = ROBOT(solutionID)

	def Run(self):
		for i in range(c.simulation_steps):
			if self.directOrGUI == "GUI":
				time.sleep(self.sleep_time)
			p.stepSimulation()
			self.robot.Sense(i)
			self.robot.Think()
			self.robot.Act()
			self.robot.Get_Fitness(writeToFile=False)

	def Get_Fitness(self):
		self.robot.Get_Fitness()
		
	def __del__(self):
		p.disconnect()