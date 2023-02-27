import copy
import os
import pickle

import constants as c
from solution import SOLUTION


class PARALLEL_HILL_CLIMBER:
	def __init__(self):
		os.system('rm brain*.nndf')
		os.system('rm fitness*.txt')
		os.system('rm best_fitness.csv')
		os.system('rm body*.txt')
		self.parents = {}
		self.nextAvailableID = 0
		for i in range(c.populationSize):
			self.parents[i] = SOLUTION(self.nextAvailableID)
			self.nextAvailableID += 1
		

	def Evolve(self):
		self.Evaluate(self.parents)
		for currentGeneration in range(c.numberOfGenerations):
			self.Evolve_For_One_Generation()
				
	def Evolve_For_One_Generation(self):
		self.Spawn()
		self.Mutate()
		self.Evaluate(self.children)
		self.Print()
		self.Select()

	def Print(self):
		print()
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
		min_fitness = float('inf')
		for parentID in self.parents:
			if self.children[parentID].fitness < self.parents[parentID].fitness:
				self.parents[parentID] = self.children[parentID]

			if self.parents[parentID].fitness < min_fitness:
				min_fitness = self.parents[parentID].fitness
		
		with open('best_fitness.csv', 'a') as f:
			f.write(f'{str(min_fitness)}, ')

	def Show_Best(self):
		bestParent = None
		for parent in self.parents.values():
			if bestParent is None or parent.fitness < bestParent.fitness:
				bestParent = parent
		bestParent.Start_Simulation('GUI', save=True)

	def Evaluate(self, solutions):
		for solution in solutions.values():
			solution.Start_Simulation('DIRECT', save=False)
		for solution in solutions.values():
			solution.Wait_For_Simulation_To_End()