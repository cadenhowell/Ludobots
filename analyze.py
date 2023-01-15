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