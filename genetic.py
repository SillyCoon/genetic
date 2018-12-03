from pyeasyga import pyeasyga
import json
import  MyAlgorythm as gen

# Read file to list

FNAME = "3.txt"
OUTNAME = "result.json"

with open(FNAME) as f:
    content = f.readlines()

content = [x.strip() for x in content]

knapsack = [float(n) for n in content.pop(0).split()]

data = []

for x in content:
    data.append([float(n) for n in x.split()])


# First task
ga = pyeasyga.GeneticAlgorithm(data)  # initialise the GA with data
ga.population_size = 500


def fitness(individual, data):
    weight, volume, price = 0, 0, 0
    for (selected, item) in zip(individual, data):
        if selected:
            weight += item[0]
            volume += item[1]
            price += item[2]
    if weight > knapsack[0] or volume > knapsack[1]:
        price = 0
    return price


ga.fitness_function = fitness
ga.run()

result = ga.best_individual()

weight = 0.0
volume = 0.0
json_result = {}
item_numbers = []

i = 0
for x in data:
    if result[1][i] != 0:
        item_numbers.append(i)
        weight += x[0]
        volume += x[1]
    i += 1

json_result = {"value": int(result[0]), "weight": int(weight), "volume": round(volume, 1), "items": item_numbers}

# *************************************************************************
# Second Task
my_algorythm = gen.GeneticKnapsack(knapsack, data)
second_task_result = my_algorythm.run()
second_item_numbers = []
second_json_result = {}

weight = volume = 0
i = 0
for x in data:
    if second_task_result['individual'][i] != 0:
        second_item_numbers.append(i)
        weight += x[0]
        volume += x[1]
    i += 1

second_json_result = {"value": int(second_task_result['fitness']), "weight": int(weight), "volume": round(volume, 1), "items": second_item_numbers}

final_result = {'1': json_result, '2': second_json_result }


final_dump = json.dumps(final_result, sort_keys=False, indent=2, separators=(',', ':'))

with open(OUTNAME, 'w+') as f:
    f.write(final_dump)
