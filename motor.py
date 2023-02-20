import numpy
import pybullet as p

import pyrosim.pyrosim as pyrosim


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName

    def Set_Value(self, robotId, desiredAngle):
        pyrosim.Set_Motor_For_Joint(
                bodyIndex = robotId,
                jointName = self.jointName,
                controlMode = p.POSITION_CONTROL,
                targetPosition = desiredAngle,
                maxForce = 15)

    def Save_Values(self):
        with open('data/MotorValues.npy', 'wb') as f:
            numpy.save(f, self.motorValues)