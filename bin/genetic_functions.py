import random


def fitness(combo, items_dict):
    """

    This function will score a particular item combination
    :param combo: A selected combination of items in the bag
    :param items_dict: dictionary describing the weight and survival points of all items
    :return: tuple that contains the weight and the survival points of a combo
    """
    weight = 0
    surv_score = 0

    for i in combo:
        if combo[i] == 1:
            weight += items_dict[i]['weight']
            surv_score += items_dict[i]['survival points']

    return weight, surv_score


def generate_combo(items_dict):
    """

    Creates a new combination of items from all possible items
    :param items_dict: dictionary describing the weight and survival points of all items
    :return: dictionary that tells what possible items are included in a combo
    """
    items = [i for i in items_dict]
    combo = {i: random.randint(1, 2) - 1 for i in items}

    return combo


def generate_first_population(size_population, items_dict):
    """

    Create many different individuals that will make the first population
    :param size_population: how many individuals in the population
    :param item_dict: dictionary describing the weight and survival points of all items
    :return: list of combo dictionaries
    """
    population = []
    i = 0
    while i < size_population:
        population.append(generate_combo(items_dict))
        i += 1

    return population


def compute_perf_population(population, items_dict, max_weight):
    """

    Score the population and sort the individuals by total survival points
    :param population: a list of combo dictionaries
    :param items_dict: dictionary describing the weight and survival points of all items
    :return: sorted list of tuples containing the items selected, total weight, and total survival points
    """
    population_perf = {}
    for combo in population:
        title = [i for i in combo if combo[i] == 1]
        population_perf[', '.join(title)] = fitness(combo, items_dict)

        # exclude individuals that weigh more than we allow
        population_perf = {k: v for (k, v) in population_perf.items() if v[0] < max_weight}
        sorted_perf_pop = sorted(population_perf.items(), key=lambda x: x[1][1], reverse=True)

    return sorted_perf_pop


def select_from_population(sorted_perf_pop, items_dict, darwins_bunch, lucky_few):
    """

    Choose which individuals from a given generation will survive
    :param sorted_perf_pop: sorted list of tuples containing the items selected, total weight, and total survival points
    :param items_dict: dictionary describing the weight and survival points of all items
    :param darwins_bunch: number of individuals that survive because they are the strongest
    :param lucky_few: number of individuals that survive due to chance
    :return: the sames sorted list of tuples, this time only containing those that survived
    """
    next_generation = []

    #select the strong survivors
    for i in range(darwins_bunch):
        next_generation.append(sorted_perf_pop[i][0])

    #select the ones that survive due to chance
    for i in range(lucky_few):
        next_generation.append(random.choice(sorted_perf_pop)[0])
    random.shuffle(next_generation)
    final_out = []
    for i in next_generation:
        items = [g for g in items_dict]
        next_gen_dict = {g: (1 if g in i.split(", ") else 0) for g in items}
        final_out.append(next_gen_dict)

    return final_out


def create_child(individual1, individual2):
    child = {}
    for i in individual1:
        if int(100 * random.random()) < 50:
            child[i] = individual1[i]
        else:
            child[i] = individual2[i]
    return child


def create_children(breeders, number_of_child):
    next_population = []
    for i in range(len(breeders) // 2):
        for j in range(number_of_child):
            next_population.append(create_child(breeders[i], breeders[len(breeders) - 1 - i]))
    return next_population


def mutate_combo(combo):
    key_mod = random.choice(list(combo.keys()))
    if combo[key_mod] == 0:
        combo[key_mod] = 1
    else:
        combo[key_mod] = 0
    return combo


def mutate_population(population, chance_of_mutation):
    for i in range(len(population)):
        if random.random() * 100 < chance_of_mutation:
            population[i] = mutate_combo(population[i])
    return population
