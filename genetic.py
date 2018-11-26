from pyeasyga import pyeasyga
import json

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
json_result = []
item_numbers = []

i = 0
for x in data:
    if result[1][i] != 0:
        item_numbers.append(i)
        weight += x[0]
        volume += x[1]
    i += 1

json_result.append({"value": int(result[0])})
json_result.append({"weight": int(weight)})
json_result.append({"volume": round(volume, 1)})
json_result.append({"items": item_numbers})

json_dump = json.dumps(json_result, sort_keys=True, indent=2, separators=(',', ':'))

with open(OUTNAME, 'w+') as f:
    f.write(json_dump)
