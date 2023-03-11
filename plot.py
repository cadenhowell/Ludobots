import matplotlib.pyplot as plt
import numpy as np
import constants as c

def main():
    # open csv in saved_morphs
    # plot fitness over generations
    data = np.zeros((c.num_runs, c.numberOfGenerations + 1))
    for i in range(c.num_runs):
        with open(f'saved_morphs/{i+1}/fitness_curve_data.csv', 'r') as f:
            data[i] = np.array(f.read().split(', ')[:-1]).astype(float)

    data = abs(data)
    plt.plot(data.T)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness over Generations')
    plt.legend([f'Seed {i+1}' for i in range(c.num_runs)])
    plt.show()

if __name__ == '__main__':
    main()