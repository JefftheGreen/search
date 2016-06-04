# /usr/bin/env python
# -*- coding: utf-8 -*-

import random
from abc import ABCMeta, abstractmethod

from utilities.variables import Identifier


class Evolver(metaclass=ABCMeta):

    # Default selection methods.
    #   TOP:            Use the top n% of the population to reproduce,
    #                   irrespective of the relative fitness of those selected.
    #   COEFFICIENT:    Use a number selected randomly with a chance
    #                   proportional to fitness.
    #   TOP_COEFF:      Use the top n% of the population to reproduce,
    #                   proportional to fitness.
    TOP, COEFFICIENT, TOP_COEFF = (Identifier(x) for x in ['top',
                                                           'coefficient',
                                                           'top_coefficient'])

    def __init__(self, pop_size):
        self.population = []
        self.pop_size = pop_size
        self.new_population()

    # Change population size and create a new population.
    def reset(self, pop_size):
        self.pop_size = pop_size
        self.new_population()

    def run(self, iterations, select_type, mu, cross_chance, s=1):
        for i in range(iterations):
            self.iterate(i, select_type, mu, cross_chance, s)

    def population_fitness(self):
        return sum([self.fitness(individual)
                    for individual in self.population]) / self.pop_size

    def iterate(self, iteration, select_type, mu, cross_chance, s):
        self.mutate(mu)
        self.select(select_type, s)
        self.reproduce(cross_chance)

    @abstractmethod
    def mutate(self, mu):
        pass

    @abstractmethod
    def new_population(self):
        pass

    def select(self, select_type, s=1):
        if select_type == self.TOP:
            self.population = sorted(self.population, key=self.fitness)
            surviving = max(int(self.pop_size * s), 1)
            self.population = self.population[0:surviving]
        elif select_type == self.COEFFICIENT:
            gene_pool = []
            fitnesses = {i: self.fitness(self.population[i])
                         for i in range(len(self.population))}
            scale = 1/min(fitnesses.values())
            if scale > 1:
                fitnesses = {i: fitnesses[i] * scale for i in fitnesses}
            for i in fitnesses:
                for n in range(int(fitnesses[i])):
                    gene_pool.append(self.population[i])
            new_pop = []
            for n in range(self.pop_size):
                new_pop.append(random.choice(gene_pool))
            self.population = new_pop
        elif select_type == self.TOP_COEFF:
            self.select(self.TOP, s)
            self.select(self.COEFFICIENT)

    @abstractmethod
    def fitness(self, individual):
        pass

    @abstractmethod
    def reproduce(self):
        pass