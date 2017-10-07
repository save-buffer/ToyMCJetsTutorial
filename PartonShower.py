import random
import math

initial = [[0, 0, 0, 0]]

e_thresh = 0.001

def pdf(x):
    return 1 / (1 + x)

def theta(x):
    return math.pi / (2 * x + 2)

def phi(x):
    return math.pi * x


def simulate_shower(shower):
    for i in shower:
        dist = math.sqrt(i[1] ** 2 + i[2] ** 2 + i[3] ** 2)
        x = random.random()
        th = theta(x)
        ph = phi(x)
        z = pdf(x)
        
