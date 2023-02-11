# 1D Morphology
## Overview
There are several possible 1D morphologies, but the constituent components are a sphere, cylinder, and box. These can be oriented arbitrarily. The constraint is that they can only vary their length in the x direction and are limited in height such that they do not phase through the floor. The fitness function is set to move in the -x direction (though for the sake of demonstration of the morphologies, they only trained for 1 generation).

## Paramaters
* A body has between 2 and 5 segments
* At least 1 segment must be a sensor
* Joints are between each segment
* The width and height are set to 1
* The length can vary between 0.5 and 2.
    * In the case of a sphere, or cylinder in some orientations, the length is limited such that the body does not exceed the preset height and phase through the floor when connected at joint to other segments.

## Fitness
Minimize the position in the x direction
## Running
Download ./main.sh and run it with execute privileges (chmod +x). This script will download Ludobots and all the requirements, then run search.py. Note that you need python3 and git to run this.

