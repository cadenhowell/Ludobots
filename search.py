from parallelHillClimber import PARALLEL_HILL_CLIMBER
import os

for i in range(5):
    print(f'\nRun {i+1}')
    if os.path.exists(f'saved_morphs/{i+1}/best_fitness.csv'):
        os.system(f'rm saved_morphs/{i+1}/*')
    phc = PARALLEL_HILL_CLIMBER()
    phc.Evolve()
    phc.Show_Best()
    os.system(f'mv best_fitness.csv saved_morphs/{i+1}/')
    os.system(f'mv body*.urdf saved_morphs/{i+1}/')
    os.system(f'mv brain*.nndf saved_morphs/{i+1}/')
    print()