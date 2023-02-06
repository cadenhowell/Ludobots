import os
import random
import time

import numpy

import constants as c
import pyrosim.pyrosim as pyrosim


class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = 2 * numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons) - 1

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py {directOrGUI} {self.myID} 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{self.myID}.txt"):
            time.sleep(0.01)
        with open(f"fitness{self.myID}.txt", "r") as fitnessFile:
            self.fitness = float(fitnessFile.read())
        os.system(f"rm fitness{self.myID}.txt")

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        sx, sy = 4, 1
        px, py = sx, sx
        dx, dy = 0, 1.5
        z, dz = 0.1, 0.1
        for j in range(8):
            pyrosim.Send_Cube(name=f"stair_{j}", pos=(dx, dy + sy / 2, z / 2), size=(sx, sy, z))
            z += dz
            dy += sy
        pyrosim.Send_Cube(name=f"platform_1", pos=(dx, dy + py / 2, z / 2), size=(px, py, z))
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1] , size=[1, 2, 0.5])
        
        pyrosim.Send_Joint(name = "Torso_BL" , parent= "Torso" , child = "BL" , type = "revolute", position = [-0.5, -0.9, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BL", pos=[-0.1, 0, -0.5] , size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name = "Torso_BR" , parent= "Torso" , child = "BR" , type = "revolute", position = [0.5, -0.9, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BR", pos=[0.1, 0, -0.5] , size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name = "Torso_FL" , parent= "Torso" , child = "FL" , type = "revolute", position = [-0.5, 0.9, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FL", pos=[-0.1, 0, -0.5] , size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name = "Torso_FR" , parent= "Torso" , child = "FR" , type = "revolute", position = [0.5, 0.9, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FR", pos=[0.1, 0, -0.5] , size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name = "Torso_BW" , parent= "Torso" , child = "BW" , type = "revolute", position = [0, -1, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BW", pos=[0, -0.65, 0] , size=[0.1, 1.3, 0.1])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "BL")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FL")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "BW")

        pyrosim.Send_Motor_Neuron(name = 3 , jointName = "Torso_BL")
        pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_FL")
        pyrosim.Send_Motor_Neuron(name = 5 , jointName = "Torso_BW")

        
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])
        pyrosim.End()
        pass

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow][randomColumn] = 2 * random.random() - 1