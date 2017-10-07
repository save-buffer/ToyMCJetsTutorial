import random

random.seed();

print("random numbers")
for i in range(1000):
    print(random.random())

print("random numbers on [5,15]")
for i in range(1000):
    print(random.random() * 10 + 5)

print("gaussian mu=5, sigma=2")
for i in range(1000):
    print(random.gauss(5,2)) #5 = mu, 2 = sigma

print("gaussian mu=5, sigma=2, range=[0,10]")
i = 0
while i < 1000:
    x = random.gauss(5,2)
    if(x < 0 or x > 10):
        continue
    i += 1
    print(x)
        
