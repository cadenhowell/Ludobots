# 3D Morphology
Created for CS 396 - Artificial Life at Northwestern University

This project was built on top of Ludobots and Pyrosim. See links below for further details.

[r/ludobots](https://www.reddit.com/r/ludobots/)

[Pyrosim](https://github.com/ccappelle/pyrosim)
## Overview
To generate a 3D morphology, I recursively branched out constituent boxes with varying probability. Unlike my 1D morphology, I chose not to use spheres and arbitrarily rotated cylinders. In 3D they lead to too many cases where the morphology would be hard to connect and control. I also used revolute joints to connect the boxes, which are much easier to control than other joint types. The brain is a fully connected network from the sensors to the joints. The max number of segments is set to 10.

[Link to video](https://youtu.be/Xvd_xRGgUSE)

## Recursive Methodology
* For the dimension the box was branching out in, the box is between sizes 0.5 and 0.8. For the other two dimensions, the box is between sizes 0.2. and 0.4.
    * This gives the effect of the boxes being longer in one direction, creating more stick like structures and branches. This also reduces the chances of collisions.
* For a given box, 3 branches will come off it with probability 0.25, 2 with probability 0.25, and 1 with probability 0.5.
    * The direction of a branch is chosen in the current direction of travel with probability 0.4, and in other directions with probability 0.3.
* The joint axis is chosen to be revolute in the direction of travel.
    * After experimentation with other joint types and axis alignments, it was found they frequently caused odd behavior and collisions. Thus I chose to stick with revolute joints.
* A box is sensor with p=0.5.
* Joints are always placed in the center of a face

![Diagram](https://github.com/cadenhowell/Ludobots/blob/3DMorph/diagram.pdf)
## Motor
The motor power is set to 15 to reduce unrealistic behavior.
Joint motor range is multiplied by a desired motor range of 1, leaving it unaffected (for now).

## Brain
The brain is a fully connected neural network that connects all sensor inputs to all joint outputs.

## Fitness
Minimize the position in the x direction (unused for purposes of demonstrating morphology).

## Morphospace
The morphospace is a 3D collection of boxes which branch out in perpendicular directions. Since the revolute joints can modify these angles, the various branches can span a wider range of angles (more so than just the orthogonal directions). The brain connects every sensor to every joint, meaning that at sensor node can affect the movement of any joint. This allows for a wide range of behaviors. The most common was a jittery movement that propelled it in a direction (though it should be noted the morphologies have not yet been trained to a fitness function, the motion is all arbitrary). Generally, whenever the morphology grows to high, it loses balance and falls. 
## Running
Download ./main.sh and run it with execute privileges (chmod +x). This script will download Ludobots and all the requirements, then run search.py. Note that you need python3 and git to run this.

