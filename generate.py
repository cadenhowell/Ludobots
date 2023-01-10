import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")
length, width, height = 1, 1, 1
x0, y0, z0 = 0, 0, 0.5
for i in range(5):
    for j in range(5):
        for k in range(10):
            pyrosim.Send_Cube(name="Box", pos=[x0 + i * length, y0 + j * width, z0 + k * height] , size=[length * 0.9 ** k, width * 0.9 ** k, height * 0.9 ** k])
pyrosim.End()