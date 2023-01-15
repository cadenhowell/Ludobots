import matplotlib.pyplot as plt
import numpy

backLegSensorValues = None
with open('data/backLegSensorValues.npy', 'rb') as f:
    backLegSensorValues = numpy.load(f)

frontLegSensorValues = None
with open('data/frontLegSensorValues.npy', 'rb') as f:
    frontLegSensorValues = numpy.load(f)

plt.plot(backLegSensorValues, label='Back Leg', linewidth=3.0)
plt.plot(frontLegSensorValues, label='Front Leg')
plt.legend()
plt.show()

targetAnglesBackLeg = None
with open('data/targetAnglesBackLeg.npy', 'rb') as f:
    targetAnglesBackLeg = numpy.load(f)

targetAnglesFrontLeg = None
with open('data/targetAnglesFrontLeg.npy', 'rb') as f:
    targetAnglesFrontLeg = numpy.load(f)

plt.plot(targetAnglesBackLeg, label='Back Leg')
plt.plot(targetAnglesFrontLeg, label='Front Leg')
plt.legend()
plt.show()