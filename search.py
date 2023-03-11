import argparse
import glob
import math
import os

from parallelHillClimber import PARALLEL_HILL_CLIMBER


def main():
    parser = argparse.ArgumentParser(description='Run a simulation')

    parser.add_argument('-s', '--seed', default=22, type=int, help='The random simulation seed')
    parser.add_argument('-r', '--runs', default='1-10', type=str, help='The run numbers to search')
    parser.add_argument('--reset', action='store_true', help='Reset the saved morphs directory')

    args = parser.parse_args()

    run_numbers = []
    for run in args.runs.split(','):
        if '-' in run:
            run_numbers += list(range(int(run.split('-')[0]), int(run.split('-')[1]) + 1))
        else:
            run_numbers.append(int(run))

    if args.reset:
        if os.path.exists('saved_morphs/'):
            os.system(f'rm -r saved_morphs/')
        os.system(f'mkdir saved_morphs/')

    clean_up()

    best_fitness = math.inf
    best_run = 0
    for i in run_numbers:
        if os.path.exists(f'saved_morphs/{i}'):
            os.system(f'rm -r saved_morphs/{i}')
            
        print(f'\nRun {i}')

        os.system(f'mkdir saved_morphs/{i}')
        phc = PARALLEL_HILL_CLIMBER(run_number = i, seed = args.seed ^ (i * 197299))
        phc.Evolve()

        if phc.get_best_and_min_fitness()[1] < best_fitness:
            best_fitness = phc.get_best_and_min_fitness()[1]
            best_run = i

        phc.Show_Best()

    with open('saved_morphs/best_run.txt', 'w+') as f:
        f.write(f'{best_run}')

    clean_up()


def clean_up():
    if glob.glob('fitness*.txt'):
        os.system('rm fitness*.txt')

    if glob.glob('brain*.nndf'):
        os.system('rm brain*.nndf')

    if glob.glob('body*.urdf'):
        os.system('rm body*.urdf')

    if glob.glob('world*.sdf'):
        os.system('rm world*.sdf')


if __name__ == '__main__':
    main()
