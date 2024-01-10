import math


def makeSimpleMoire(Moire, extra = 1):


    angle = math.radians(Moire.angle)
    dl = Moire.d
    c = Moire.c
    
    min_x = extra * -Moire.xsize/2
    min_y = extra * -Moire.ysize/2
    max_x = extra * Moire.xsize/2
    max_y = extra * Moire.ysize/2
    actual_pos = min_x
    sinb = math.sin(angle) #So we aren't calculating it every time like a retard
    cosb = math.cos(angle)
    c2 = 1/(1/c - sinb/dl) # dx/(dx/c-1) can be 0 and m = dy/c2
    paircheck = 1
    
    points = []
    lines = []
    Moire.first_pos = actual_pos
    while True:
        x_f_max = (cosb*max_y/dl)/(1/c - sinb/dl) + actual_pos  
        x_f_min = (cosb*min_y/dl)/(1/c - sinb/dl) + actual_pos #elegant as fuck

        actual_pos += c2
            
                

        pt1 = [x_f_max, max_y]
        pt2 = [x_f_min, min_y]

        points.append(pt1)
        points.append(pt2)
            
        if paircheck == 2:
            lines.append([pt2, pt1, points[-4], points[-3]]) #order is important
            if pt2[0] >= max_x:
                Moire.last_pos = actual_pos
                break
            paircheck = 0
            
        paircheck += 1

            
    Moire.poly = lines
    Moire.gap = c2
    Moire.first_pos = min_x