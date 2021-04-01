## The only difference between this script and one_max.py is the calc_fitness function
##
##

import random
import string
import matplotlib.pyplot as plt
import pandas as pd

target = "10110110110110010111"

population_size = 100

crossover_rate = 0.8

mutation_rate = 0.1

tournamentK = 3

#generate a random population of strings, using characters given, of length given
def generate_population(size, value_length, characters):
    population = []
    for i in range(size):
        #create a random string of size value_length using characters 
        value = ''.join(random.choice(characters) for i in range(value_length))
        population.append(value)

    return population

#calculate the fitness of a value by using the hamming distance between the target and the value
def calc_fitness(value):
    global target
    hamming_distance = 0
    #for each character in the two term, check if they are equal
    for x,(i,j) in enumerate(zip(target,value)):
        if i!=j:
            hamming_distance += 1
    
    fitness = len(target) - hamming_distance

    return fitness

# given a list of population values and the fitness metric,
# will calculate fitness for each value and return a list of dict items
def create_population_dicts(population):
    population_fitness = []
    for item in population:
        value = dict()
        fitness = calc_fitness(item)
        value["value"] = item
        value["fitness"] = fitness
        population_fitness.append(value)
    return population_fitness

#takes list of dict items and returns the average of the fitness values in the list
def get_average_fitness(population):
    fitnesses = []
    for item in population:
        fitnesses.append(item["fitness"])
    total = 0
    for i in fitnesses:
        total += i
    return total/(len(fitnesses))

# given the population, will return the highest fitness value
def get_max_fitness(population):
    max_fitness = 0
    for item in population:
        if item["fitness"] > max_fitness:
            max_fitness = item["fitness"]
    return max_fitness

#given a list of values, will return the value with the highest fitness
def get_higher_fitness(values):
    best_value = values[0]
    for value in values:
        if value["fitness"] > best_value["fitness"]:
            best_value = value
    return best_value

#selection process using tournament selection between "tournamentK" number of values
def selection(population):
    global population_size, tournamentK
    new_population = []
    for i in range(population_size):
        values = []
        for i in range(tournamentK):
            value = random.choice(population)
            values.append(value)
        better_value = get_higher_fitness(values)
        new_population.append(better_value)
    
    return new_population

# perform crossover on some random values
def crossover(population):
    global crossover_rate

    new_population = []

    # iterate throught the population choosing 2 values to perform crossover on
    while len(population) > 1:
        #choose 2 random values and then remove them from old population
        value1 = random.choice(population)
        population.remove(value1)
        value2 = random.choice(population)
        population.remove(value2)

        child1, child2 = value1.copy(), value2.copy()

        if random.random() < crossover_rate:
            #get a random crossover point
            crossover_point = random.randint(1, len(value1["value"])-1)
            child1["value"] = value1["value"][:crossover_point] + value2["value"][crossover_point:]
            child2["value"] = value2["value"][:crossover_point] + value1["value"][crossover_point:]
        new_population.append(child1)
        new_population.append(child2)
    
    return new_population

# function to randomly flip a bit using mutation rate
def mutation(population):
    new_population = []
    for value in population:
        if random.random() < mutation_rate:
            mutation_bit = random.randint(0, len(value["value"])-1)
            s = list(value["value"])
            if s[mutation_bit] == '1':
                s[mutation_bit] = '0'
            else:
                s[mutation_bit] = '1'
            value["value"] = "".join(s)
            new_population.append(value)
        else:
            new_population.append(value)
    return new_population

#function to turn dict back into a list of values to remove fitness value
def remove_old_fitness(population):
    #create a list that just contains the values for each population item
    new_population = []
    for value in population:
        new_population.append(value["value"])
    return new_population


#create a random population
target_length = len(target)
character_pool = "01"
population = generate_population(population_size, target_length, character_pool)

#list to store average fitness for each generation
average_fitnesses = []
generation = 1

#create a list of dicts for the population including fitness for each member
population = create_population_dicts(population)
average_fitnesses.append({"generation":generation, "avg_fitness": get_average_fitness(population)})

#while get_max_fitness(population) < target_length:
for i in range(50):
    #perform selection
    population = selection(population)
    #perform crossover
    population = crossover(population)
    #perform mutation
    population = mutation(population)
    #remove old fitnesses from population
    population = remove_old_fitness(population)
    #calculate fitnesses for new population
    population = create_population_dicts(population)

    generation +=1
    #append average fitness value to list
    average_fitnesses.append({"generation":generation, "avg_fitness": get_average_fitness(population)})


#plot average fitnesses
df = pd.DataFrame(average_fitnesses)

plt.plot(df["generation"], df["avg_fitness"])
plt.show()

    