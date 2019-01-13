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

my_algorythm = gen.GeneticKnapsack(knapsack, data)
task_result = my_algorythm.run()
item_numbers = []
json_result = {}

weight = volume = 0
i = 0
for x in data:
    if task_result['individual'][i] != 0:
        item_numbers.append(i)
        weight += x[0]
        volume += x[1]
    i += 1

json_result = {"value": int(task_result['fitness']), "weight": int(weight), "volume": round(volume, 1), "items": item_numbers}

final_result = {'result': json_result }


final_dump = json.dumps(final_result, sort_keys=False, indent=2, separators=(',', ':'))

with open(OUTNAME, 'w+') as f:
    f.write(final_dump)
