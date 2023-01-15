import random
import time

import numpy
import pybullet as p
import pybullet_data

import pyrosim.pyrosim as pyrosim

amplitudeBackLeg = numpy.pi / 6
frequencyBackLeg = 15
phaseOffsetBackLeg = numpy.pi / 8
amplitudeFrontLeg = numpy.pi / 6
frequencyFrontLeg = 15
phaseOffsetFrontLeg = 0

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = numpy.zeros(1000)
frontLeftSensorValues = numpy.zeros(1000)
targetAnglesBackLeg = amplitudeBackLeg * numpy.sin(frequencyBackLeg * numpy.linspace(0, 2 * numpy.pi, 1000) + phaseOffsetBackLeg)
targetAnglesFrontLeg = amplitudeFrontLeg * numpy.sin(frequencyFrontLeg * numpy.linspace(0, 2 * numpy.pi, 1000) + phaseOffsetFrontLeg)
# with open('data/targetAnglesBackLeg.npy', 'wb') as f:
#     numpy.save(f, targetAnglesBackLeg)
# with open('data/targetAnglesFrontLeg.npy', 'wb') as f:
#     numpy.save(f, targetAnglesFrontLeg)
# # exit()

for i in range(1000):
    time.sleep(1/100)
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLeftSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b"Torso_BackLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = targetAnglesBackLeg[i],
        maxForce = 20)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b"Torso_FrontLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = targetAnglesFrontLeg[i],
        maxForce = 20)
p.disconnect()

with open('data/backLegSensorValues.npy', 'wb') as f:
    numpy.save(f, backLegSensorValues)
with open('data/frontLegSensorValues.npy', 'wb') as f:
    numpy.save(f, frontLeftSensorValues)
