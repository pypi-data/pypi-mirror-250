import numpy as np
import math 

def obtain_dx(x,r,n):
    dx = r*2*np.sqrt(1 - (x/r)**2)*np.sin(math.pi/n)
    return dx

def obtain_c(dx,c):
    c2 = dx/(dx/c - 1)
    return c2

def n_from_l(r,l):
    perimeter = 2*r*math.pi
    n = perimeter/l
    return n

def construct_lines(h, points):
    lines = []
    for i in range(0, len(points), 2):
        point1 = np.array([points[i],-h/2])
        try:
            point2 = np.array([points[i+1],-h/2])
        except IndexError:
            point2 = np.array([h/2,-h/2])
        point3 = np.array([point2[0],h/2])
        point4 = np.array([points[i],h/2])
        
        line = [list(point1), list(point2), list(point3), list(point4)]
        lines.append(line)
    return lines

def conform(r,l,c):
    n = n_from_l(r,l)
    points = [0.0]  # Inicializa points con el punto central
    x = 0
    while True:
        dx = obtain_dx(x, r, n)
        c2 = obtain_c(dx, c)
        
        x += c2
        if x >= r:
            break
        points.append(x)  # Añade el punto positivo
        points.insert(0, -x)  # Añade el punto negativo al principio de la lista

    #create the lines
    lines = construct_lines(2*r,points)
    return lines