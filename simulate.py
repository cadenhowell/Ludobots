import time

import numpy
import pybullet as p
import pybullet_data

import pyrosim.pyrosim as pyrosim

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = numpy.zeros(500)
frontLeftSensorValues = numpy.zeros(500)
for i in range(500):
    time.sleep(1/60)
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLeftSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
p.disconnect()
with open('data/backLegSensorValues.npy', 'wb') as f:
    numpy.save(f, backLegSensorValues)
with open('data/frontLegSensorValues.npy', 'wb') as f:
    numpy.save(f, frontLeftSensorValues)
