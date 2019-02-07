import json
import copy

import math
import random

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

map2 = mpimg.imread("map2.jpg")

with open('capitals.json', 'r') as capitals_file:
    capitals = json.load(capitals_file)
capitals_list = list(capitals.items())

def show_path(path, starting_city, title='map2', w=12, h=8):
    x, y = list(zip(*path))
    _, (x0, y0) = starting_city
    plt.imshow(map2)
    plt.plot(x0, y0, 'y*', markersize=15)
    plt.plot(x + x[:1], y + y[:1])
    plt.axis("off")
    fig = plt.gcf()
    fig.set_size_inches([w, h])
    fig.suptitle(title, fontsize=22, fontweight='normal')
    plt.show()

def simulated_annealing(problem, schedule):
    import sys
    current = problem
    for t in range(sys.maxsize):
        temperature = schedule(t)
        if temperature < 1e-10:
            return current
        neighbors = problem.successors()
        if not neighbors:
            return current
        next = random.choice(neighbors)
        delta_e = next.get_value() - current.get_value()
        clear_improvement = delta_e > 0
        choose_with_probability = math.exp(delta_e / temperature) > random.uniform(0.0, 1.0)
        if clear_improvement or choose_with_probability:
            current = next

class TravelingSalesmanProblem:    
    def __init__(self, cities):
        self.path = copy.deepcopy(cities)
    
    def copy(self):        
        new_tsp = TravelingSalesmanProblem(self.path)
        return new_tsp
    
    @property
    def names(self):        
        names, _ = zip(*self.path)
        return names
    
    @property
    def coords(self):        
        _, coords = zip(*self.path)
        return coords
    
    def successors(self):        
        new_problem_list = []
        for i in range(0, len(self.path)-1):
            new_problem = copy.deepcopy(self.path)
            temp = new_problem[i]
            new_problem[i] = new_problem[i+1]
            new_problem[i+1] = temp
            new_problem_list.append(TravelingSalesmanProblem(new_problem))
            
        new_problem = copy.deepcopy(self.path)
        temp = new_problem[0]
        new_problem[0] = new_problem[len(self.path)-1]
        new_problem[len(self.path)-1] = temp
        new_problem_list.append(TravelingSalesmanProblem(new_problem))
        return new_problem_list
            

    def get_value(self):        
        dist = 0.0
        for i in range(0, len(self.coords)-1):
            city1, city2 = self.coords[i], self.coords[i+1]
            dist +=(abs(city1[0] - city2[0]) ** 2 + abs(city1[1] - city2[1]) ** 2) ** 0.5
        
        city1, city2 = self.coords[0], self.coords[len(self.coords)-1]
        dist += (abs(city1[0] - city2[0]) ** 2 + abs(city1[1] - city2[1]) ** 2) ** 0.5
        return -dist

alpha = 0.95
temperature = 1e4

def schedule(time):
    return alpha ** time * temperature

num_cities = 100
capitals_tsp = TravelingSalesmanProblem(capitals_list[:num_cities])
starting_city = capitals_list[0]
dist = -capitals_tsp.get_value()
print("Initial path value: {:.2f}".format(dist))
print(capitals_list[:num_cities])
show_path(capitals_tsp.coords, starting_city, title='Initial Path\n(length = {:.2f})'.format(dist))

print('\nWorking ...\n')
alpha = 0.95
temperature=1e6
result = simulated_annealing(capitals_tsp, schedule)
dist = -result.get_value()
print("Final path length: {:.2f}".format(dist))
print(result.path)
show_path(result.coords, starting_city, title='Final Path\n(length = {:.2f})'.format(dist))
