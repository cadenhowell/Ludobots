#!/bin/bash

git clone https://github.com/cadenhowell/Ludobots.git
cd Ludobots
git checkout finalProject
python3 -m pip install -r requirements.txt
python3 search.py