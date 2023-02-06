import os

os.system('git clone https://github.com/cadenhowell/Ludobots.git')
os.system('cd Ludobots')
os.system('git checkout finalProject')
os.system('python3 -m pip install -r requirements.txt')
os.system('python3 search.py')