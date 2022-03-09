from __future__ import print_function
import enum
from operator import attrgetter
from gaps import image_helpers
from gaps.selection import roulette_selection
from gaps.crossover import Crossover
from gaps.individual import Individual
from gaps.image_analysis import ImageAnalysis
from gaps.plot import Plot
from gaps.progress_bar import print_progress
from pathlib import Path
import os
import glob


class GeneticAlgorithm(object):

    TERMINATION_THRESHOLD = 10

    def __init__(self, image, piece_size, population_size, generations, elite_size=2):
        self._image = image
        self._piece_size = piece_size
        self._generations = generations
        self._elite_size = elite_size
        pieces, rows, columns = image_helpers.flatten_image(image, piece_size, indexed=True)
        self._population = [Individual(pieces, rows, columns) for _ in range(population_size)]
        self._pieces = pieces

    def start_evolution(self, verbose):
        print("=== Pieces:      {}\n".format(len(self._pieces)))
        sol_path = "./puzzle_solutions"
        Path(sol_path).mkdir(parents=True, exist_ok=True) #create dir if it doesn't exist
        
        #remove contents from solutions folder 
        files = glob.glob('%s/*'%sol_path)
        for f in files: os.remove(f)

        if verbose:
            plot = Plot(self._image)

        ImageAnalysis.analyze_image(self._pieces)

        fittest = None
        best_fitness_score = float("-inf")
        termination_counter = 0

        for N,generation in enumerate(range(self._generations)):
            print_progress(generation, self._generations - 1, prefix="=== Solving puzzle: ")

            new_population = []

            # Elitism
            elite = self._get_elite_individuals(elites=self._elite_size)
            new_population.extend(elite)

            selected_parents = roulette_selection(self._population, elites=self._elite_size)

            for first_parent, second_parent in selected_parents:
                crossover = Crossover(first_parent, second_parent)
                crossover.run()
                child = crossover.child()
                new_population.append(child)

            fittest,  partial_population = self._best_individual() #partial_population=n*100% of the population (currently n=0.2)

            if fittest.fitness <= best_fitness_score:
                termination_counter += 1
            else:
                best_fitness_score = fittest.fitness

            if termination_counter == self.TERMINATION_THRESHOLD:
                print("\n\n=== GA terminated")
                print("=== There was no improvement for {} generations".format(self.TERMINATION_THRESHOLD))
                return fittest

            self._population = new_population

            if verbose:
                #plot.show_fittest(fittest.to_image(), "Generation: {} / {}".format(generation + 1, self._generations), file_name="%s/%s.jpg"%(sol_path,N))
                #print(partial_population.__dict__)
                #save the partial pulation as images
                for idx, pop in enumerate(partial_population):
                  print(pop._fitness)
                  plot.show_fittest(pop.to_image(), "Generation: {} / {}".format(generation + 1, self._generations), file_name="%s/%s_%s.jpg"%(sol_path, N, idx))


        return fittest

    def _get_elite_individuals(self, elites):
        """Returns first 'elite_count' fittest individuals from population"""
        return sorted(self._population, key=attrgetter("fitness"))[-elites:]

    def _best_individual(self):
        """Returns the fittest individual from population"""
        return max(self._population, key=attrgetter("fitness")), sorted(self._population, key=attrgetter("fitness"))[-1:] #round(0.05*len(self._population))
