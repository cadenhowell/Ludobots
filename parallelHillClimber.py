import copy
import os

import constants as c
from solution import SOLUTION

import math
class PARALLEL_HILL_CLIMBER:
	def __init__(self, run_number, seed):
		self.run_number = run_number
		self.seed = seed
		self.fitness_data = []
		self.parents = {}
		self.nextAvailableID = 0

		for i in range(c.populationSize):
			self.get_evaluated_solution(i)
			while self.parents[i].fitness == math.inf:
				self.get_evaluated_solution(i)

	def get_evaluated_solution(self, i):
		self.parents[i] = SOLUTION(nextAvailableID = self.nextAvailableID, seed = self.seed ^ (self.nextAvailableID * 43649))
		self.nextAvailableID += 1
		self.Evaluate({i: self.parents[i]})


	def Evolve(self):
		for currentGeneration in range(c.numberOfGenerations):
			if currentGeneration % 100 == 0:
				self.save(currentGeneration)

			min_fitness = self.get_best_and_min_fitness()[1]
			self.fitness_data.append(min_fitness)
			
			self.Evolve_For_One_Generation(currentGeneration)


		self.save(c.numberOfGenerations)

		with open(f'saved_morphs/{self.run_number}/fitness_curve_data.csv', 'a+') as f:
			for fitness in self.fitness_data:
				f.write(f'{fitness}, ')

	def save(self, currentGeneration):
		dir = f'saved_morphs/{self.run_number}/gen_{currentGeneration}'
		if not os.path.exists(dir):
			os.system(f'mkdir {dir}')
		self.save_all(dir)
		self.save_best(dir)
		self.save_lineage(dir)

	def get_best_and_min_fitness(self):
		min_fitness = math.inf
		for parentID in self.parents:
			if self.parents[parentID].fitness < min_fitness:
				min_fitness = self.parents[parentID].fitness
				best = self.parents[parentID]
		return best, min_fitness

	def save_all(self, dir):
		for parentID in self.parents:
			self.parents[parentID].save(dir)

	def save_best(self, dir):
		bestID = self.get_best_and_min_fitness()[0].myID
		with open(f'{dir}/best_solution.txt', 'w+') as f:
			f.write(f'{bestID}')
				
	def save_lineage(self, dir):
		with open(f'{dir}/lineage.txt', 'w') as f:
			for parentID in self.parents:
				f.write(f'Ancestor: {parentID}, Descendant: {self.parents[parentID].myID}\n')

	def Evolve_For_One_Generation(self, currentGeneration):
		self.Spawn()
		self.Mutate()
		self.Evaluate(self.children)
		self.Print(currentGeneration)
		self.Select()

	def Print(self, currentGeneration):
		
		print()
		print(f'Generation: {currentGeneration}')
		for parentID in self.parents:
			print(self.parents[parentID].fitness, self.children[parentID].fitness)
		print()

	def Spawn(self):
		self.children = {}
		for parentID in self.parents:
			self.children[parentID] = copy.deepcopy(self.parents[parentID])
			self.children[parentID].Set_ID(self.nextAvailableID)
			self.nextAvailableID += 1

	def Mutate(self):
		for child in self.children.values():
			child.Mutate()

	def Select(self):
		for parentID in self.parents:
			if self.children[parentID].fitness < self.parents[parentID].fitness:
				self.parents[parentID] = self.children[parentID]
		
	def Show_Best(self):
		bestParent = None
		for parent in self.parents.values():
			if bestParent is None or parent.fitness < bestParent.fitness:
				bestParent = parent
		bestParent.Start_Simulation('GUI')
		bestParent.Wait_For_Simulation_To_End()

	def Evaluate(self, solutions):
		for solution in solutions.values():
			solution.Start_Simulation('DIRECT')
		for solution in solutions.values():
			solution.Wait_For_Simulation_To_End()