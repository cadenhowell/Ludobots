import argparse
import os
import pickle

import constants as c

parser = argparse.ArgumentParser(description='View a simulation')

parser.add_argument('-c', '--compare', default=False, action='store_true', help='Compare the best solution to the original solution in the lineage')

parser.add_argument('-r', '--run', default='best', type=str, help='The run number')
parser.add_argument('-g', '--generation', default=c.numberOfGenerations, type=int, help='The generation number')
parser.add_argument('-s', '--solution', default='best', type=str, help='The solution ID')

parser.add_argument('-t', '--sleep', default=0.002, type=float, help='The slowness of the simulation')

args = parser.parse_args()

run_number = args.run
if run_number == 'best':
    with open('saved_morphs/best_run.txt', 'r') as f:
        run_number = f.read()

solution = args.solution
if solution == 'best':
    with open(f'saved_morphs/{run_number}/gen_{args.generation}/best_solution.txt', 'r') as f:
        solution = f.read()

if args.compare:

    with open(f'saved_morphs/{run_number}/gen_{args.generation}/lineage.txt', 'r') as f0:

        original_parent_id = None
        new_lines = f0.readlines()
        for line in new_lines:
            if line.split(' ')[-1].strip() == solution:
                original_parent_id = line.split(' ')[1][:-1]
                break
        for i in range(0, args.generation+1, 100):

            original_solution = None
            with open(f'saved_morphs/{run_number}/gen_{i}/lineage.txt', 'r') as f1:
                old_lines = f1.readlines()
                for line in old_lines:
                    if line.split(' ')[1][:-1] == original_parent_id:
                        original_solution = line.split(' ')[-1].strip()
                        break

            with open(f'saved_morphs/{run_number}/gen_{i}/solution{original_solution}.pkl', 'rb') as run_file:
                loaded_solution = pickle.load(run_file)
                loaded_solution.Start_Simulation('GUI', sleep = args.sleep)
                while not os.path.exists(f'fitness{original_solution}.txt'):
                    pass
                os.system(f'rm fitness{original_solution}.txt')

else:
    with open(f'saved_morphs/{run_number}/gen_{args.generation}/solution{solution}.pkl', 'rb') as f:
        loaded_solution = pickle.load(f)
        loaded_solution.Start_Simulation('GUI', sleep = args.sleep)
        while not os.path.exists(f'fitness{solution}.txt'):
            pass
        os.system(f'rm fitness{solution}.txt')
