import random
import string
import matplotlib.pyplot as plt
import pandas as pd

knapsack_size = 103

values = [78, 35, 89, 36, 94, 75, 74, 79, 80, 16]
weights = [18, 9, 23, 20, 59, 61, 70, 75, 76, 30]

#initiate a list of dict items containing the value and weight of each item
items = []
for i in range(len(values)):
    item = dict()
    item["value"] = values[i]
    item["weight"] = weights[i]
    items.append(item)


population_size = 50

crossover_rate = 0.8

mutation_rate = 0.1

tournamentK = 3

generations = 100

#generate a random population of strings, using characters given, of length given
def generate_population(size, value_length, characters):
    population = []
    for i in range(size):
        #create a random string of size value_length using characters 
        value = ''.join(random.choice(characters) for i in range(value_length))
        population.append(value)

    return population

# calculates the fitness of a value
def calc_fitness(value):
    global items, knapsack_size

    total_value = 0
    total_weight = 0 

    #convert the string value into a list of characters
    value_lst = [char for char in value]
    #for each character in the value, if it equals 1, we add the corresponding weight and value to total 
    for i in range(len(value_lst)):
        if value_lst[i] == '1':
            total_value += items[i]["value"]
            total_weight += items[i]["weight"]
    
    #if the weight is greater than the knapsack size we give it a fitness score of 0
    #else the fitness is the total value
    if total_weight > knapsack_size:
        fitness = 0
    else:
        fitness = total_value

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
    value = None
    for item in population:
        if item["fitness"] > max_fitness:
            max_fitness = item["fitness"]
            value = item
    return value

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
target_length = len(items)
character_pool = "01"
population = generate_population(population_size, target_length, character_pool)

#list to store average fitness for each generation
average_fitnesses = []
#list to store max fitness for each generation 
max_fitnesses = []
generation = 1

#create a list of dicts for the population including fitness for each member
population = create_population_dicts(population)
average_fitnesses.append({"generation":generation, "avg_fitness": get_average_fitness(population)})
max_fitnesses.append({"generation":generation, "max_fitness": get_max_fitness(population)["fitness"], "value" : get_max_fitness(population)["value"]})

for i in range(generations - 1):
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
    #append max fitness value to list
    max_fitnesses.append({"generation":generation, "max_fitness": get_max_fitness(population)["fitness"], "value" : get_max_fitness(population)["value"]})

#print best result found
total_generations = max_fitnesses[len(max_fitnesses)-1]["generation"]
best_value = max_fitnesses[len(max_fitnesses)-1]["value"]
best_fitness = max_fitnesses[len(max_fitnesses)-1]["max_fitness"]
print("After " + str(total_generations) + " generations, the best value found was: " + best_value + " with a score of: " + str(best_fitness))

#plot average fitnesses
df = pd.DataFrame(average_fitnesses)
df2 = pd.DataFrame(max_fitnesses)

plt.plot(df["generation"], df["avg_fitness"], label='Mean Fitness')
plt.plot(df2["generation"], df2["max_fitness"],label='Max Fitness')
plt.legend()
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.show()