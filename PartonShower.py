import random
import math
import Tkinter as tk
initial = [1, 1, 1, 1]

e_thresh = 0.01

def pdf(x):
    return 1 / (1 + x)

def theta(x):
    return math.pi / (2 * x + 2)

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

def simulate_shower(particle):
    if particle[0] < e_thresh:
        return [particle]
    length = math.sqrt(particle[1] ** 2 + particle[2] ** 2 + particle[3] ** 2)
    rand = random.random()
    th = theta(rand)
    ph = phi(rand)
    z = pdf(rand)
    new_length = length * math.sqrt(z)
    rad = [z * particle[0], particle[1], particle[2], particle[3]]
    rad = scale_to_length(rad, new_length)
    rad = rotate_towards_j(th, rad)
    rad = rotate_towards_k(ph, rad)
    fin = [particle[0] - rad[0], particle[1] - rad[1], particle[2] - rad[2], particle[3] - rad[3]]
    return [particle, simulate_shower(rad), simulate_shower(fin)]

def print_single_particle(particle):
    print("{ \"E\": " + str(particle[0]) + ", \"x\": " + str(particle[1]) + ", \"y\": " + str(particle[2]) + ", \"z\": " + str(particle[3]) + " }")
def print_particles(particles, tabs):
    print "\t" * tabs + "{"
    print "\t" * (tabs + 1) + "\"initial\" : ",
    print_single_particle(particles[0])
    if len(particles) == 1:
        print("\t" * tabs + "}")
        return
    print "\t" * (tabs + 1) + ","
    print "\t" * (tabs + 1) + "\"rad\" : ",
    print_particles(particles[1], tabs + 1)
    print "\t" * (tabs + 1) + ","
    print "\t" * (tabs + 1) + "\"fin\" : ",
    print_particles(particles[2], tabs + 1)
    print("\t" * tabs + "}")
    

final_particles = simulate_shower(initial)
    
#print_particles(final_particles, 0)

root = tk.Tk()
canvas = tk.Canvas(root, width=1000, height=1000)
canvas.pack()
scale = 20

camera_position = [0, 0, 1]

def convert_to_2d(x, y, z):
    depth = math.sqrt(camera_position[0] ** 2 + camera_position[1] ** 2 + camera_position[2] ** 2)
    return x / depth, y / depth, 1 / depth
    
    
def draw(particles, x, y, z):
    final_x = x + scale * particles[0][1]
    final_y = y + scale * particles[0][2]
    final_z = z + scale * particles[0][3]

    _x, _y, thick1 = convert_to_2d(x, y, z)
    _final_x, _final_y, thick2 = convert_to_2d(final_x, final_y, final_z)
    thick = (thick1 + thick2) / 2.0
    thick = max(thick, 1)
    canvas.create_line(_x, 1000 - _y, _final_x, 1000 - _final_y, width = thick)
    if len(particles) == 1:
        return
    draw(particles[1], final_x, final_y, final_z)
    draw(particles[2], final_x, final_y, final_z)
    
draw(final_particles, 500, 500, 0)
root.mainloop()

