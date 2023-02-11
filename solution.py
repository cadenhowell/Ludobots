import os
import random
import time

import numpy

import pyrosim.pyrosim as pyrosim


class SOLUTION:
    def __init__(self, nextAvailableID, parentSeed=None):
        self.myID = nextAvailableID
        self.numSegments = random.randint(2, 5)
        self.numSensors = random.randint(1, self.numSegments)
        self.weights = 2 * numpy.random.rand(self.numSensors, self.numSegments - 1) - 1
        self.parentSeed = time.time() if parentSeed is None else parentSeed

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py 'GUI' {self.myID} 2&>1 &")

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


    def random_features(self, min_length, max_length, max_height, rotation_types):
        shape = random.choice(["cube", "cylinder", "sphere"])

        length = random.random() * (max_length - min_length) + min_length

        rpy = '0 0 0'
        if shape == 'cylinder':
            rpy = random.choice(list(rotation_types.values()))

        limit_length_cases = [
            shape == 'cylinder' and rpy == rotation_types["roll"],
            shape == 'sphere'
        ]
        if any(limit_length_cases):
            length = random.random() * (max_height - min_length) + min_length

        return shape, length, rpy


    def Create_Body(self):
        pyrosim.Start_URDF(f"body{self.myID}.urdf")

        random.seed(self.parentSeed)

        width, height = 1, 1
        min_length, max_length = 0.5, 2
        
        rotation_types = {
            'none': '0 0 0',
            'roll': f'{str(numpy.pi / 2)} 0 0',
            'pitch': f'0 {str(numpy.pi / 2)} 0'
        }

        self.sensors = list(map(str, random.sample(range(self.numSegments), self.numSensors)))
        self.joints = [f'{i}_{i+1}' for i in range(self.numSegments - 1)]

        def create_cube(name, length, isSensor, isRoot):
            pos = [-1 * length / 2, 0, 0]
            size = [length, width, height]

            if isRoot:
                pos[2] = height / 2
                
            pyrosim.Send_Cube(name=name, pos=pos, size=size, isSensor=isSensor)

        def create_cylinder(name, length, rpy, isSensor, isRoot):
            pos = [-1 * length / 2, 0, 0]
            size = [0, 0, 0]
            
            if rpy == rotation_types["none"]:
                size = [height, length / 2]

                if isRoot:
                    pos[2] = height / 2

            elif rpy == rotation_types["roll"]:
                size = [width, length / 2]

                if isRoot:
                    pos[2] = length / 2

            elif rpy == rotation_types["pitch"]:
                size = [length, height / 2]

                if isRoot:
                    pos[2] = height / 2

            pyrosim.Send_Cylinder(name=name, pos=pos, size=size, rpy=rpy, isSensor=isSensor)

        def create_sphere(name, length, isSensor, isRoot):
            pos = [-1 * length / 2, 0, 0]
            size = [length / 2]

            if isRoot:
                pos[2] = length / 2

            pyrosim.Send_Sphere(name=name, pos=pos, size=size, isSensor=isSensor)

        def create_joint(i, length, isRoot):
            position = [-1 * length, 0, 0]

            if isRoot:
                position[2] = height / 2

            pyrosim.Send_Joint(name=f'{i}_{i+1}', parent=str(i), child = str(i+1), type="revolute", position=position, jointAxis = "0 1 0")

        for i in range(self.numSegments):
            shape, length, rpy = self.random_features(min_length, max_length, height, rotation_types)

            name = str(i)
            if shape == 'cube':
                create_cube(name, length, name in self.sensors, i == 0)
            elif shape == 'cylinder':
                create_cylinder(name, length, rpy, name in self.sensors, i == 0)
            elif shape == 'sphere':
                create_sphere(name, length, name in self.sensors, i == 0)
            
            if self.numSegments > 1 and i < self.numSegments - 1:
                create_joint(i, length, i == 0)  

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        for i, sensor in enumerate(self.sensors):
            pyrosim.Send_Sensor_Neuron(name = i, linkName = sensor)
        for i, joint in enumerate(self.joints):
            pyrosim.Send_Motor_Neuron(name = i + len(self.sensors), jointName = joint)
        
        for i, sensor in enumerate(self.sensors):
            for j, joint in enumerate(self.joints):
                pyrosim.Send_Synapse(sourceNeuronName = i , targetNeuronName = j + self.numSensors, weight = self.weights[i][j])
        pyrosim.End()

    def Mutate(self):
        random.seed()
        randomRow = random.randint(0, len(self.sensors) - 1)
        randomColumn = random.randint(0, len(self.joints) - 1)
        self.weights[randomRow][randomColumn] = 2 * random.random() - 1