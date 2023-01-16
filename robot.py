import pybullet as p

import constants as c
import pyrosim.pyrosim as pyrosim
from motor import MOTOR
from sensor import SENSOR


class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

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
            if jointName == b'Torso_BackLeg':
                print(jointName)
                self.motors[jointName] = MOTOR(jointName, c.amplitudeBackLeg, c.frequencyBackLeg, c.phaseOffsetBackLeg)
            else:
                self.motors[jointName] = MOTOR(jointName, c.amplitudeBackLeg, 0.5 * c.frequencyBackLeg, c.phaseOffsetBackLeg)

    def Act(self, i):
        for jointName in self.motors:
            self.motors[jointName].Set_Value(self.robotId, i)