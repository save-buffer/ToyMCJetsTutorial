import random
import math

random.seed()

def pdf(x):
    return math.e ** -x

def cdf(x):
    return -math.e ** -x

def rand_range_pdf(mi, ma):
    x = -1
    while x < mi or x > ma:
        x = pdf(random.random() * -1.6094)
    return x

#for i in range(1000):
#    print(rand_range_pdf(0, 5))


print("ACCEPT-REJECT")
accepted = 0
for i in range(1000):
    x = random.random() * 5
    fx = math.e ** -x
    r = random.uniform(0, 1)
    if r > fx:
        continue
    accepted += 1
    print(x)

print("ACCEPTED:")
print(accepted / 1000.0)

print("INVERSE")
for i in range(1000):
    u = random.random()
    x = -math.log(u)
    print(x)
