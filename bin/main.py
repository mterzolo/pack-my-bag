import genetic_functions as gf

items_dict = {

    'sleeping bag': {'weight': 12, 'survival points': 16},
    'rope': {'weight': 5, 'survival points': 7},
    'pocket knife': {'weight': 2, 'survival points': 10},
    'torch': {'weight': 15, 'survival points': 5},
    'bottle': {'weight': 7, 'survival points': 8},
    'glucose': {'weight': 6, 'survival points': 12},
    'map': {'weight': 2, 'survival points': 7},
    'hiking boots': {'weight': 10, 'survival points': 4},
    'compass': {'weight': 1, 'survival points': 4},
    'rain jacket': {'weight': 3, 'survival points': 11}

}

max_weight = 40

def main():
    """
    Main function that will find the optimal bag combo
    :return: items in bag, weight, score, and the score over the generations
    """
    # create the first population
    population = gf.generate_first_population(20, items_dict)

    progress = []

    for i in range(0, 20):

        # calculate the score of each individual in the population
        sorted_perf_pop = gf.compute_perf_population(population, items_dict, max_weight)

        # select the individuals that survive in the population
        next_generation = gf.select_from_population(sorted_perf_pop, items_dict, 8, 2)

        # create children from those survivors
        children = gf.create_children(next_generation, 6)

        # mutate the children and save as next population
        population = gf.mutate_population(children, .15)

        # track progress of best solution
        best_solution = gf.compute_perf_population(population, items_dict, max_weight)[0]
        progress.append(best_solution[1][1])

    return best_solution, progress


if __name__ == '__main__':
    main()