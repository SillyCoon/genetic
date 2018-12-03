import random


def _byfitness_key(element):
    return element['fitness']


class GeneticKnapsack:
    # Характеристики рюкзака
    knapsack = []
    # Данные о вещах
    data = []
    # Количество вещей (для удобства)
    quantity = 0

    QUANTITY_OF_INDIVIDUALS = 200
    GENERATIONS = 500

    _result = []

    def __init__(self, knapsack, data):
        self.knapsack = knapsack
        self.data = data
        self.quantity = len(data)

    def _step(self, population, counter=0):

        # Проверяем условие выхода
        if counter == 500 or not self._convergence(population):
            self._result = population
            return population

        # Отобрали от 1 до 10 штук для дальнейшей селекции
        selected_ids = self._selection(population)
        selected_individuals = []

        # Найдем по номерам хромосомы выбранных особей
        for id in selected_ids:
            selected_individuals.append(population[id])

        # Скрестим выбранных особей и получим детей
        children = self._crossbreading(selected_individuals)
        # 10% популяции мутирует
        mutated_population = self._mutation(population)
        # Сформируем новую популяцию
        new_population = self._form_new_population(mutated_population, children)
        counter += 1
        self._step(new_population, counter)

    def run(self):
        # Основная функция
        starting_population = self._starting_population()
        self._step(starting_population)

        return self._find_best_individual(self._result)

    def _starting_population(self):
        # Генерируем начальную популяцию

        population = []
        for i in range(0, self.QUANTITY_OF_INDIVIDUALS):
            individual = []
            for j in range(0, self.quantity):
                individual.append(random.getrandbits(1))
            population.append(individual)
        return population

    def _selection(self, population):
        # Отбор особей (рулетка), 10 попыток

        sum = 0
        # Получим первое приближение без 0 и сумму
        roulette = []
        i = 0
        for individual in population:
            fitness = self._fitness(individual)
            if fitness != 0:
                sum += fitness
                roulette.append({'id': i, 'fitness': fitness})
            i += 1

        # Рассчитаем вероятность выбора особи и разобьем на блоки от 0 до 1
        line = []

        line.append({'id': roulette[0]['id'], 'probability': roulette[0]['fitness'] / sum})

        for i in range(1, len(roulette)):
            line.append(
                {'id': roulette[i]['id'], 'probability': roulette[i]['fitness'] / sum + line[i - 1]['probability']})

        # 10 раз найдем случайное число от 1 до 10 и сравним его с промежутком
        # Если совпало, то выбираем особь из него
        result = []
        for j in range(0, 10):
            r = random.random()

            if r <= line[0]['probability']:
                result.append(line[0]['id'])

            for i in range(1, len(line)):
                if line[i - 1]['probability'] < r <= line[i]['probability']:
                    if result.count(i) == 0:
                        result.append(i)

        return result

    def _crossbreading(self, selected):
        # Скрестим каждую пару выбранных особей
        children = []
        for i in range(0, len(selected) // 2):
            children += self._three_points_crossbreading(selected[i], selected[len(selected) - 1 - i])
        return children

    def _three_points_crossbreading(self, ind1, ind2):
        # Трехточечное скрещивание двух особей, в результате получаем еще две
        points = []
        for i in range(0, 3):
            points.append(random.randint(1, self.quantity - 1))

        points.sort()

        first_child = ind1[0:points[0]] + ind2[points[0]:points[1]] + ind1[points[1]:points[2]] + ind2[points[2]:]
        second_child = ind2[0:points[0]] + ind1[points[0]:points[1]] + ind2[points[1]:points[2]] + ind1[points[2]:]

        return [first_child, second_child]

    def _mutation(self, population):
        # Производим мутации, к 10% особей добавляем случайную вещь
        ids = []

        for i in self._rand(0, self.QUANTITY_OF_INDIVIDUALS - 1, self.QUANTITY_OF_INDIVIDUALS // 10):
            flag = True
            counter = 0 # Чтобы исключить вариант, что у особи в наличии все вещиы
            while flag:
                p = random.randint(0, self.quantity - 1)
                if population[i][p] == 0:
                    population[i][p] = 1
                    flag = False
                if counter > self.quantity:
                    flag = False
                counter += 1
        return population

    def _form_new_population(self, old_population, children):
        worst = []
        # Находим худших по количеству детей
        for i in range(0, self.quantity):
            worst.append({'id': i, 'fitness': self._fitness(old_population[i])})

        worst = sorted(worst, key=_byfitness_key)[0:len(children)]

        # Заменяем худших на детей
        j = 0
        for individual in worst:
            old_population[individual['id']] = children[j]
            j += 1

        return old_population

    def _convergence(self, population):
        # Проверим популяцию на сходимость
        check = []
        for individual in population:
            check.append(self._fitness(individual))

        best = sorted(check, reverse=True)[0]

        for individual in check:
            if individual / best >= 0.1:
                False

        return True

    def _find_best_individual(self, population):
        check = []
        for individual in population:
            check.append({'fitness': self._fitness(individual), 'individual': individual})

        lel = sorted(check, key=_byfitness_key, reverse=True)

        return sorted(check, key=_byfitness_key, reverse=True)[0]

    def _fitness(self, individual):
        # Функция приспособленности

        weight, volume, price = 0, 0, 0
        for (selected, item) in zip(individual, self.data):
            if selected:
                weight += item[0]
                volume += item[1]
                price += item[2]
        if weight > self.knapsack[0] or volume > self.knapsack[1]:
            price = 0
        return price

    def _rand(self, start, stop, count):
        # Получаем неповторяющиеся случайные числа
        gamma = []
        for i in range(0, count):
            while True:
                item = random.randint(start, stop)
                if not gamma.count(item):
                    gamma.append(item)
                    yield item
                    break
