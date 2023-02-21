import os
import random
import time

import numpy

import pyrosim.pyrosim as pyrosim


class SOLUTION:
    def __init__(self, nextAvailableID, parentSeed=None):
        self.myID = nextAvailableID
        self.maxNumSegments = 10
        self.parentSeed = time.time() if parentSeed is None else parentSeed


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
        pyrosim.End()


    def random_features(self, min_length, max_length, direction):
        is_sensor = random.random() < 0.5

        size = [0, 0, 0]
        for i in range(3):
            if i == direction:
                new_min_length = 0.5
                size[i] = random.random() * (max_length - new_min_length) + new_min_length
            else:
                new_max_length = 0.4
                size[i] = random.random() * (new_max_length - min_length) + min_length

        joint_axis = [0, 0, 0]
        joint_axis[direction] = 1
        joint_axis = ' '.join(map(str, joint_axis))

        return size, is_sensor, joint_axis


    def create_cube(self, name, size, direction, isSensor, isRoot):
        pos = [0, 0, 0]
        pos[direction] = size[direction] / 2

        if isRoot:
            pos[2] = size[2] / 2
            
        pyrosim.Send_Cube(name=name, pos=pos, size=size, isSensor=isSensor)



    def create_joint(self, parent_idx, child_idx, size, old_direction, new_direction, isRoot, jointAxis):
        pos = [0, 0, 0]

        if isRoot:
            pos[2] = size[2] / 2
        else:
            pos[old_direction] += size[old_direction] / 2
        pos[new_direction] += size[new_direction] / 2

        pyrosim.Send_Joint(name=f'{parent_idx}_{child_idx}', parent=str(parent_idx), child=str(child_idx), type="revolute", position=pos, jointAxis = jointAxis)
        self.joints.append(f'{parent_idx}_{child_idx}')


    def build_node(self, queue):
        child_queue = []

        while len(queue) > 0:
            node = queue.pop(0)
            direction = node[0]
            i = node[1]

            min_d, max_d = 0.2, 0.8
            size, is_sensor, joint_axis = self.random_features(min_d, max_d, direction)

            self.create_cube(
                name = str(i), 
                size = size, 
                direction = direction, 
                isSensor = is_sensor, 
                isRoot = i == 0
            )
                
            if is_sensor:
                self.sensors.append(str(i))
        
            k = random.choices([1, 2, 3], weights=[0.5, 0.25, 0.25])[0]

            weights = [0.3] * 3
            weights[direction] = 0.4

            directions = numpy.random.choice([0, 1, 2], size=k, replace=False, p=weights)

            for new_direction in directions:
                if len(self.joints) < self.maxNumSegments - 1:
                    child_idx = len(self.joints) + 1

                    self.create_joint(
                        parent_idx=i, 
                        child_idx=child_idx, 
                        size=size, 
                        old_direction=direction,
                        new_direction=new_direction, 
                        isRoot=i == 0,
                        jointAxis=joint_axis
                    )

                    child_queue.append((new_direction, child_idx))

        if len(child_queue) > 0:
            self.build_node(child_queue)


    def Create_Body(self):
        pyrosim.Start_URDF(f"body{self.myID}.urdf")
        self.sensors = []
        self.joints = []

        random.seed(26)
        
        self.build_node([(random.choice([0, 1, 2]), 0)])

        pyrosim.End()


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        if not hasattr(self, 'weights'):
            self.weights = 2 * numpy.random.rand(len(self.sensors), len(self.joints)) - 1

        for i, sensor in enumerate(self.sensors):
            pyrosim.Send_Sensor_Neuron(name = i, linkName = sensor)
        for i, joint in enumerate(self.joints):
            pyrosim.Send_Motor_Neuron(name = i + len(self.sensors), jointName = joint)
        
        for i, sensor in enumerate(self.sensors):
            for j, joint in enumerate(self.joints):
                pyrosim.Send_Synapse(sourceNeuronName = i , targetNeuronName = j + len(self.sensors), weight = self.weights[i][j])
        pyrosim.End()

    def Mutate(self):
        random.seed()
        randomRow = random.randint(0, len(self.sensors) - 1)
        randomColumn = random.randint(0, len(self.joints) - 1)
        self.weights[randomRow][randomColumn] = 2 * random.random() - 1