import pybullet as p
import time

physicsClient = p.connect(p.GUI)
for i in range(1000):
    time.sleep(1/100)
    p.stepSimulation()
    print(i)
p.disconnect()