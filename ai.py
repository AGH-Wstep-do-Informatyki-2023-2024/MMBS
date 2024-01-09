import numpy as np
import math
import random
import copy
import os


# rozkład normalny, używane do wyliczenia mutacji

def distrib(val, mean, scale):
    res = math.exp(-((val-mean)**2)/(2 * scale**2))
    res /= (scale * (2*math.pi)**(1/2))
    if val < 0:
        return -res
    return res


class Neural_network:

    # sieć neuronowa
    # weitghts - wagi danych połączeń w sieci
    # bias stały wektor dodawany podczas oceniania najlepszego ruchu
    # score aktualna ocena sieci

    def __init__(self, weights=[], bias=[]):
        self.input = np.matrix([])
        self.weights = np.matrix(weights)
        self.bias = np.matrix(bias)

    # zapisuje sieć w pliku, z opcją 'a' dopisuje do pliku z opcją 'w' nadpisuje
    def save_to_file(self, name, option='w'):  # 'w' lub 'a'
        file = open(name, option)
        for nums in self.weights.tolist():
            for weight in nums:
                file.write(str(weight)+" ")
            file.write('\n')
        for b in self.bias.tolist():
            file.write(str(b[0])+" ")
        file.write('\n')
        file.close()

    # wczytuje sieć z pliku id służy do odczytywania w przypadku kiedy wczytywanie jest z pliku generacji - wskazuje na początek wczytywanej sieci
    def load_from_file(self, name, input_size=54, output_size=13, id=0):
        file = open(name, "r")
        x = file.read().split()
        new_bias = []
        new_weights = []
        for i in range(0, output_size):
            new_weights.append([])
            for j in range(0, input_size):
                new_weights[i].append(float(x[id]))
                id += 1
        self.weights = np.matrix(new_weights)
        for i in range(0, output_size):
            new_bias.append([float(x[id])])
            id += 1
        self.bias = np.matrix(new_bias)
        file.close()
        return id

    # tworzy mutacje sieci parent ## MOŻNA SIĘ POBWAIĆ STAŁYMI

    def mutate_from(self, parent):
        par_weigh = parent.weights.tolist()
        mine_weigh = []
        par_bias = parent.bias.tolist()
        mine_bias = []
        for i in range(0, len(par_weigh)):
            mine_weigh.append([])
            for j in range(0, len(par_weigh[i])):
                x = random.randint(-1200, 1200)/100
                x = distrib(x, 0, 2)
                mine_weigh[i].append(par_weigh[i][j] + x)
        self.weights = np.matrix(mine_weigh)

        for i in range(0, len(par_bias)):
            x = random.randint(-1200, 1200)/100
            x = distrib(x, 0, 2)
            mine_bias.append([par_bias[i][0] + x])
        self.bias = np.matrix(mine_bias)

    # tworzy losowa siec

    def setrandom(self, input_size=54, output_size=13):
        ran = []
        for j in range(0, output_size):
            ran.append([])
            for i in range(0, input_size):
                r = 2*random.random()-1
                ran[j].append(r)
        self.weights = np.matrix(ran)
        bis = []
        for j in range(0, output_size):
            r = 2*random.random()-1
            bis.append([r])
        self.bias = np.matrix(bis)

    # resetuje ocenę sieci
    def reset_score(self):
        self.score = 0

    # zmienia ocenę sieci
    def add_score(self, x):
        self.score += x

    # nie wiem po co?
    def print_input(self):
        print(self.input)

    # przekazanie inputu
    def get_input(self, input):
        self.input = np.matrix(input)

    # normalizacja danych
    def sigmoid(self, x):
        return 1 / (1+math.exp(-x))

    # ocenia ruchy
    def eval(self):
        layer1 = np.matmul(self.weights, self.input) + self.bias
        layer2 = np.matrix([self.sigmoid(i[0]) for i in layer1.tolist()])
        self.predicts = layer2
        return layer2

    # zwraca indeks najlepszego ruchu
    def pick_best(self, size):
        predicts = self.predicts.tolist()[0][0:size]
        imax = 0
        maxs = -10000
        for i in range(0, size):
            if predicts[i] > maxs:
                maxs = predicts[i]
                imax = i
        return imax


class Generation:
    def __init__(self, size=100, predefined_agents=[], input_size=54, output_size=13):
        if len(predefined_agents) <= size:
            self.input_size = input_size
            self.output_size = output_size
            self.size = size
            self.agents = copy.deepcopy(predefined_agents)
            left = size-len(predefined_agents)
            for i in range(0, left):
                ai = copy.deepcopy(Neural_network())
                ai.setrandom(input_size, output_size)
                self.agents.append(copy.deepcopy(ai))
        return

    def save_to_file(self, name):
        file = open(name, 'w').close()
        for agent in self.agents:
            agent.save_to_file(name, 'a')

    def load_from_file(self, name):
        id = 0
        for agent in self.agents:
            id = agent.load_from_file(
                name, self.input_size, self.output_size, id)

    def draw(self):
        for agent in self.agents:
            print(agent.weights)

    def print_scores(self):
        for agent in self.agents:
            print(agent.score)

    def get_best(self):
        max = -1000
        best = 0
        for agent in self.agents:
            if agent.score > max:
                max = agent.score
                best = agent
        return best
