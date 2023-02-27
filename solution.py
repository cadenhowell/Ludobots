import os
import random
import time
import math

import pyrosim.pyrosim as pyrosim
from morphology import Morphology


class SOLUTION:
    def __init__(self, nextAvailableID, seed=None):
        self.myID = nextAvailableID
        self.morphology = Morphology(seed)
        self.fitness = math.inf

    def Start_Simulation(self, directOrGUI, save=False):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py {directOrGUI} {self.myID} {save} 2&>1 &")


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
        pyrosim.End()


    def Create_Body(self):
        pyrosim.Start_URDF(f"body{self.myID}.urdf")

        for link in self.morphology.links:
            pyrosim.Send_Cube(name=link.name, pos=link.pos, size=link.size, isSensor=link.isSensor)

        for joint in self.morphology.joints:
            pyrosim.Send_Joint(name=joint.name, parent=joint.parent, child=joint.child, type=joint.type, position=joint.pos, jointAxis=joint.jointAxis)

        pyrosim.End()


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        for i, sensor in enumerate(self.morphology.sensors):
            pyrosim.Send_Sensor_Neuron(name = i, linkName = sensor)
            
        for i, joint in enumerate(self.morphology.joints):
            pyrosim.Send_Motor_Neuron(name = i + len(self.morphology.sensors), jointName = joint.name)
        
        for i, sensor in enumerate(self.morphology.sensors):
            for j, joint in enumerate(self.morphology.joints):
                pyrosim.Send_Synapse(sourceNeuronName = i , targetNeuronName = j + len(self.morphology.sensors), weight = self.morphology.weights[i][j])
                
        pyrosim.End()

    def Mutate(self):
        if random.random() < 0.5:
            self.morphology.Mutate_Brain()
        else:
            self.morphology.Mutate_Body()
