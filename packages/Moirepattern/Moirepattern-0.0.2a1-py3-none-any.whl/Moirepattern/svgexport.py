def write(fp, points):
    if not points:
        return
    
    if isinstance(points, (list, tuple)):
        pass
    else:
        
        return
    if len(points) > 2:
        
        x, y = points[0]
    else:
       
        return
    data = 'M{},{} ' .format(x, y)
    for p in points[1:]:
        x, y = p
        data += 'L{},{} ' .format(x, y)
    data += 'Z'  # Agrega el comando 'Z' al final para cerrar el trazado
    fp.write('<path d="{}" fill="Black" stroke="none" />\n'.format(data))


def export(geo, xsize, ysize, filename):
    with open(filename, 'w') as fp:
        fp.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fp.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{}" height="{}" viewBox="{} {} {} {}">\n'.format(xsize, ysize,-xsize/2, - ysize/2, xsize, ysize))
        fp.write('<defs>\n')
        fp.write('</defs>\n')
        for points in geo:
            
            write(fp, points)   
        fp.write('</svg>')