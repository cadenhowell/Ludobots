import numpy
import pybullet as p

import pyrosim.pyrosim as pyrosim


class MOTOR:
    def __init__(self, jointName, amplitude, frequency, phaseOffset):
        self.jointName = jointName
        self.amplitude = amplitude
        self.frequency = frequency
        self.phaseOffset = phaseOffset
        self.motorValues = self.amplitude * numpy.sin(self.frequency * numpy.linspace(0, 2 * numpy.pi, 1000) + self.phaseOffset)

    def Set_Value(self, robotId, desiredAngle):
        pyrosim.Set_Motor_For_Joint(
                bodyIndex = robotId,
                jointName = self.jointName,
                controlMode = p.POSITION_CONTROL,
                targetPosition = desiredAngle,
                maxForce = 20)

    def Save_Values(self):
        with open('data/MotorValues.npy', 'wb') as f:
            numpy.save(f, self.motorValues)