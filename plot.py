import matplotlib.pyplot as plt
import numpy as np

def main():
    # open csv in saved_morphs
    # plot fitness over generations
    data = np.zeros((5, 100))
    for i in range(5):
        with open(f'saved_morphs/{i+1}/best_fitness.csv', 'r') as f:
            data[i] = np.array(f.read().split(', ')[:-1]).astype(float)

    data = abs(data)
    plt.plot(data.T)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness over Generations')
    plt.legend(['Seed 1', 'Seed 2', 'Seed 3', 'Seed 4', 'Seed 5'])
    plt.show()

if __name__ == '__main__':
    main()