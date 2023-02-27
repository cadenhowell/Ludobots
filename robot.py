import os
import math 
import pybullet as p

import constants as c
import pyrosim.pyrosim as pyrosim
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
import math

class ROBOT:
    def __init__(self, solutionID, save=False):
        self.solutionID = solutionID
        self.robotId = p.loadURDF(f"body{self.solutionID}.urdf")
        if not save:
            os.system(f'rm body{self.solutionID}.urdf')
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK(f"brain{self.solutionID}.nndf")
        print(save)
        if not save:
            os.system(f'rm brain{self.solutionID}.nndf')

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, i):
        for linkName in self.sensors:
            self.sensors[linkName].Get_Value(i)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName).encode('utf-8')
                desiredAngle = c.motorJointRange * self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)

    def Think(self):
        self.nn.Update()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = math.inf if math.isnan(basePosition[0]) else basePosition[0]
        
        with open(f"tmp{self.solutionID}.txt", "w") as f:
            f.write(str(xPosition))
        os.system(f'mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt')
        
