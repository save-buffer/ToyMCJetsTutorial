import random

def falls_in_circle(x, y):
    return (x ** 2 + y ** 2) < 0.25

in_circle = 0
total = 100000
for i in range(total):
    x = random.random() - 0.5
    y = random.random() - 0.5
    if falls_in_circle(x, y):
        in_circle += 1

pi = 4.0 * in_circle / total
print(pi)
