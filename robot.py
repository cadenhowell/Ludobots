import os
import math 
import pybullet as p

import constants as c
import pyrosim.pyrosim as pyrosim
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR


class ROBOT:
    def __init__(self, solutionID):
        self.robotId = p.loadURDF("body.urdf")
        self.solutionID = solutionID
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK(f"brain{self.solutionID}.nndf")
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
                if neuronName == '5':
                    desiredAngle = self.nn.Get_Value_Of(neuronName)
                else:
                    desiredAngle = c.motorJointRange * self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
                if neuronName == '3':
                    self.motors[b'Torso_BR'].Set_Value(self.robotId, desiredAngle)
                if neuronName == '4':
                    self.motors[b'Torso_FR'].Set_Value(self.robotId, desiredAngle)

    def Think(self):
        self.nn.Update()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        yPosition = basePosition[1]
        zPosition = basePosition[2]
        with open(f"tmp{self.solutionID}.txt", "w") as f:
            f.write(str(yPosition * 0.1 + zPosition * 0.9))
        os.system(f'mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt')
        
