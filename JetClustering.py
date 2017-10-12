import random
import math
#import matplotlib.pyplot as plt


##LHC-SCALE ENERGY LEVELS (very slow, expect 15ish minutes on a mid-spec 2016 MacBook Pro)
##About 13 TeV collision, 3 MeV threshold, negligible mass
#e_thresh = 0.001
#e_collision = 3529.411
#mass = 0.000001

##Smaller scale collision. Smaller shower, much faster simulation (< 1 sec)
##About 3 GeV collision, 3 MeV threshold, negligible mass
e_thresh = 0.001
e_collision = 1
mass = 0.00001

def pdf(x):
    return 1 / (1 + x)

def theta(x):
    return (math.pi / 2) * x

def phi(x):
    return math.pi * x

def rotate_towards_j(th, to_rotate):
    x = to_rotate[1]
    y = to_rotate[2]
    z = to_rotate[3]
    length = math.sqrt(z ** 2 + x ** 2);
    rx = -x * y / length
    ry = (x ** 2 + z ** 2) / length
    rz = -z * y / length
    x = math.cos(th) * x
    y = math.cos(th) * y
    z = math.cos(th) * z
    rx = math.sin(th) * rx
    ry = math.sin(th) * ry
    rz = math.sin(th) * rz
    return [to_rotate[0], x + rx, y + ry, z + rz]

def rotate_towards_k(th, to_rotate):
    x = to_rotate[1]
    y = to_rotate[2]
    z = to_rotate[3]
    length = math.sqrt(y ** 2 + x ** 2);
    rx = -x * z / length
    ry = -y * z / length
    rz = (y ** 2 - x ** 2) / length
    x = math.cos(th) * x
    y = math.cos(th) * y
    z = math.cos(th) * z
    rx = math.sin(th) * rx
    ry = math.sin(th) * ry
    rz = math.sin(th) * rz
    return [to_rotate[0], x + rx, y + ry, z + rz]

def scale_to_length(vector, target):
    length = math.sqrt(vector[1] ** 2 + vector[2] ** 2 + vector[3] ** 2)
    return [vector[0], target * vector[1] / length, target * vector[2] / length, target * vector[3] / length];

def simulate_shower(particle, final_array):
    if particle[0] < e_thresh:
        final_array.append(particle)
        return
    length = math.sqrt(particle[1] ** 2 + particle[2] ** 2 + particle[3] ** 2)
    rand = random.random()
    th = theta(rand)
    ph = phi(rand)
    z = pdf(rand)
    e_k = z * particle[0] - mass
    new_length = math.sqrt(2 * mass * e_k)
#    new_length = math.sqrt(z) * length
    rad = [z * particle[0], particle[1], particle[2], particle[3]]
    rad = scale_to_length(rad, new_length)
    rad = rotate_towards_j(th, rad)
    rad = rotate_towards_k(ph, rad)
    fin = [particle[0] - rad[0], particle[1] - rad[1], particle[2] - rad[2], particle[3] - rad[3]]
    simulate_shower(rad, final_array)
    simulate_shower(fin, final_array)

def print_single_particle(particle):
    print("{ \"E\": " + str(particle[0]) + ", \"x\": " + str(particle[1]) + ", \"y\": " + str(particle[2]) + ", \"z\": " + str(particle[3]) + " }")    

def generate_event(energy):
    alpha = 0.1
    e = math.e ** -alpha * random.random()
    ph = random.random() * 2 * math.pi
    th = random.random() * math.pi
    p = math.sqrt(2 * mass * (e - mass));
    a = rotate_towards_j(th, [e, p, 0, 0])
    a = rotate_towards_k(ph, a)
    b = [energy - e, p - a[1], -a[2], -a[3]]
    return a, b

def calculate_eta(vector):
    p = math.sqrt(vector[1] ** 2 + vector[2] ** 2 + vector[3] ** 2)
    p_t = math.sqrt(vector[2] ** 2 + vector[3] ** 2)
    th = math.asin(p_t / p)
    return -math.log(math.tan(th / 2.0))

def calculate_phi(vector):
    p = math.sqrt(vector[1] ** 2 + vector[2] ** 2 + vector[3] ** 2)
    p_b = math.sqrt(vector[1] ** 2 + vector[2] ** 2)
    phi = math.asin(p_b / p)
    return phi

#IMPORTANT NOTE: THE BEAM AXIS IS THE X AXIS IN MY SIMULATION, SO THE TRANSVERSE MOMENTUM
#IS p_y^2 + p_z^2 INSTEAD OF p_x^2 + p_y^2
#THIS ALSO MEAN THAT PHI IS THE ROTATION FROM THE X AXIS TOWARDS THE Z AXIS, INSTEAD OF
#THE OPPOSITE

#beam distances
def calculate_d_bs(pseudo_jets):
    d_b = []
    for i in pseudo_jets:
        p_t = math.sqrt(i[2] ** 2 + i[3] ** 2)
        p = math.sqrt(p_t ** 2 + i[1] ** 2)
        try:
            d_b.append(p_t ** (2 * p))
        except:
            print_single_particle(i)
            print p_t
            print p
            quit()
    return d_b

def calculate_d_ijs(pseudo_jets, R, n):
    d_ij = []
    for i in range(len(pseudo_jets)):
        d_ij.append([])
        for j in range(i + 1, len(pseudo_jets)):
            p_t_i = math.sqrt(pseudo_jets[i][2] ** 2 + pseudo_jets[i][3] ** 2)
            p_t_j = math.sqrt(pseudo_jets[j][2] ** 2 + pseudo_jets[j][3] ** 2)
            eta_i = calculate_eta(pseudo_jets[i])
            eta_j = calculate_eta(pseudo_jets[j])
            phi_i = calculate_phi(pseudo_jets[i])
            phi_j = calculate_phi(pseudo_jets[j])
            delta_ij = math.sqrt((phi_i - phi_j) ** 2 + (eta_i - eta_j) ** 2)
            p_t = min(p_t_i, p_t_j)
            d_ij[i].append((p_t ** (2 * n)) * (delta_ij / R))
    return d_ij

def cluster_jets(pseudo_jets, R, n):
    if len(pseudo_jets) == 0:
        return []
    removed = []
    for i in range(len(pseudo_jets)):
        removed.append(False)
    new_pseudo_jets = []
    jets = []
    d_b = calculate_d_bs(pseudo_jets)
    d_ij = calculate_d_ijs(pseudo_jets, R, n)
    for i in range(len(pseudo_jets) - 1):
        if removed[i]:
            continue
        min_j = 0
        for j in range(len(d_ij[i])):
            if d_ij[i][j] < d_ij[i][min_j]:
                if not removed[j + i + 1]:
                    min_j = j
        v1 = pseudo_jets[i]
        v2 = pseudo_jets[min_j]

        if d_ij[i][min_j] < d_b[i]:
            new_v = [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2], v1[3] + v2[3]]
            new_pseudo_jets.append(new_v)
            removed[min_j + i + 1] = True
        else:
            jets.append(pseudo_jets[i])
        removed[i] = True
    if not removed[len(pseudo_jets) - 1]:
        jets.append(pseudo_jets[len(pseudo_jets) - 1])
    return jets + cluster_jets(new_pseudo_jets, R, n)

# a, b = generate_event(e_collision)
# a_shower = []
# b_shower = []
# simulate_shower(a, a_shower)
# simulate_shower(b, b_shower)
# a_jets = cluster_jets(a_shower, 0.5, 1)
# print len(a_jets)

rs = [0.01, 0.05, 0.1, 0.5, 1.0]
ns = [-1, 0, 1]

a_showers = []
b_showers = []
for i in range(10):
    a, b = generate_event(e_collision)
    a_shower = []
    b_shower = []
    simulate_shower(a, a_shower)
    simulate_shower(b, b_shower)
    a_showers.append(a_shower)
    b_showers.append(b_shower)

num_jets = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]
for i in range(len(rs)):
    print "I: " + str(i)
    for j in range(len(ns)):
        print "J: " + str(j)
        for k in a_showers:
            print "clustering jets"
            a_jets = cluster_jets(k, rs[i], ns[j])
            num_jets[i][j] += len(a_jets)
        for k in b_showers:
            b_jets = cluster_jets(k, rs[i], ns[j])
            num_jets[i][j] += len(b_jets)

#plt.hist(num_jets)
#plt.show()
    



