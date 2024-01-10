from . import simple
from . import bool
from . import svgexport as svg
from . import visualizator as vis
from . import cylinder as cyl
import math
#Moire class
class Moire:
    def __init__(self,d,c,angle):
        self.d = d
        self.c = c
        self.angle = angle
        self.poly = []
        self.base = []
        self.type = ""
        self.parts = [self]
        self.structure = [1] #this will be a matrix with the shape of the structure; Zeroes in every pos unless is the corresponding part
        self.rows = 1
        self.cols = 1
    
    def setsize(self, x , y):
        self.xsize = x
        self.ysize = y
        
        
    def make(self,type, extra = 1.0):
        self.type = type
        if self.type == "Simple":
            simple.makeSimpleMoire(self, extra)
        elif self.type == "Cylinder":
            
            self.poly = cyl.conform(min(self.xsize,self.ysize)/2,self.d,self.c)
        else:
            print("Not implemented yet // Not a valid type")
    
    def base_make(self):
        c = self.c
        p1 = [-self.xsize/2,-self.ysize/2]
        p2 = [-self.xsize/2 + c,-self.ysize/2]
        p3 = [-self.xsize/2 + c,self.ysize/2]
        p4 = [-self.xsize/2,self.ysize/2]
        export = [p1,p2,p3,p4]
        self.base = []
        while True:
            self.base.append(export)
            p1 = [p1[0] + 2*c,p1[1]]
            p2 = [p2[0] + 2*c,p2[1]]
            p3 = [p3[0] + 2*c,p3[1]]
            p4 = [p4[0] + 2*c,p4[1]]
            export = [p1,p2,p3,p4]
            if p1[0] >= self.xsize/2:
                break
            
    def export(self,filename):
        to_export = []
        parts = len(self.parts)
        for i in range(parts):
            x_size = self.xsize
            y_size = self.ysize
            #create a box with the size of the part
            box = [[-x_size/2,-y_size/2],[-x_size/2,y_size/2],[x_size/2,y_size/2],[x_size/2,-y_size/2]] #ill be adjusting the points positions when some part is added
            #iterate through the lines and check if they intersect with the box
            #if they do, add the intersection points to the list
            for line in self.poly:
                if bool.intersect(line,box)[0] != False:
                    to_export.append(bool.intersect(line,box))
            to_export = [sublist[0] for sublist in to_export]
            
            svg.export(to_export,x_size,y_size,filename)
            
    def export_base(self,filename):
        self.base_make()
        svg.export(self.base,self.xsize,self.ysize,filename)
        
    def view(self):
        vis.visualize(self)
        
    def add(self,other, extra = 1.2, autody = True):
        #check if the angle is 0
        if hasattr(self , "is_comp"):
            print("This is a compound Moire, please use add_compound")
            return
        if autody:
            if self.angle % 180 == 0:
                print("Please use autody = False, as the angle is 0")     
            l1 = self.d
            l1_angle = self.angle
            l2 = other.d
            l2_angle = other.angle
            l1_angle = math.radians(l1_angle)
            l2_angle = math.radians(l2_angle)
            l2 = l1 * math.cos(l2_angle)/math.cos(l1_angle)
            other.d = l2
        other.make("Simple", extra)     
        extra_c2 = extra *10 / 2 #super crappy way to get the extra c2
        self.parts.append(other)
        self.structure.append(0)
        self.cols += 1
        self.rows = max(self.rows,1)
        #other structure must have a 1 on the end of the list and 0s in the rest
        
        other.structure = [0 for i in range(len(self.structure)-1)]
        other.structure.append(1) 
        other.cols = self.cols
        
        #adjust the position of the points
        xsize_new = self.xsize + other.xsize
        #view last point of self
        last_point = self.last_pos - self.gap * extra_c2 
        print("Last point")
        print(last_point)
        #move to self.xsize/2
        difference = (self.xsize/2 - last_point) 
        
        #move all self points by difference in x
        for line in self.poly:
            for point in line:
                point[0] += difference
        
        
        
        #crop self to his size:
        #create box
        box = [[-self.xsize/2,-self.ysize/2],[-self.xsize/2,self.ysize/2],[self.xsize/2,self.ysize/2],[self.xsize/2,-self.ysize/2]]
        #iterate through the lines and check if they intersect with the box
        #if they do, add the intersection points to the list
        new_selfpoly = []
        for line in self.poly:
            if bool.intersect(line,box)[0] != False:
                new_selfpoly.append(bool.intersect(line,box))
        new_selfpoly = [sublist[0] for sublist in new_selfpoly]
        self.poly = new_selfpoly
        
        #adjust the position of the points considering the new size
        #assumes that last point is now in self.xsize/2
        for i, line in enumerate(self.poly):
            self.poly[i] = [list(point) for point in line]
        difference = -xsize_new/2 + self.xsize/2
        for line in self.poly:
            for point in line:
                point[0] += difference
        
                
        #we must have now self in place
        #now we work with other
        #adjust the position of the points
        #view first point of other
        first_point = other.first_pos +  other.gap * extra_c2
        new_last_point = other.last_pos - other.gap * extra_c2 #this is the new last point of the whole structure
        print("Last point2")
        print(other.last_pos)
        print(new_last_point)
        
        #move to -other.xsize/2
        for i, line in enumerate(other.poly):
            other.poly[i] = [list(point) for point in line]
        difference = (-other.xsize/2 - first_point)
        #move all other points by difference in x
        for line in other.poly:
            for point in line:
                point[0] += difference
        #crop other to his size:
        #create box
        new_last_point = new_last_point + difference
        print(new_last_point)
        box = [[-other.xsize/2,-other.ysize/2],[-other.xsize/2,other.ysize/2],[other.xsize/2,other.ysize/2],[other.xsize/2,-other.ysize/2]]
        #iterate through the lines and check if they intersect with the box
        #if they do, add the intersection points to the list
        new_otherpoly = []
        for line in other.poly:
            if bool.intersect(line,box)[0] != False:
                new_otherpoly.append(bool.intersect(line,box))
        new_otherpoly = [sublist[0] for sublist in new_otherpoly]
        other.poly = new_otherpoly
        #adjust the position of the points considering the new size
        #assumes that first point is now in -other.xsize/2
        other.poly = [[list(point) for point in line] for line in other.poly]

        difference = (xsize_new/2 - other.xsize) + other.xsize/2
        #move all other points by difference in x
        for line in other.poly:
            for point in line:
                point[0] += difference
        new_last_point = new_last_point + difference
        print(new_last_point)
        last_pt_sum = 0
        while True:
            c2 = other.gap
            last_pt_sum += c2
            if last_pt_sum > xsize_new/2:
                self.last_pos = last_pt_sum
                break
            
        #now we must combine the structures
        self.poly += other.poly
        #print poly
        print("Newpoly")
        
        self.xsize = xsize_new
        self.ysize = xsize_new
        self.is_comp = True
        self.gap = other.gap #store the last c2
        
    def add_compound(self,other, extra = 1.6):
        print("comp")
        print(self.last_pos)
        last_pos = self.last_pos
        new_size = self.xsize + other.xsize
        extra_c = extra * 10 / 2
        other.make("Simple", extra)
        #now we know that self is in the middle of the new structure, and we must move it to the left
        #move all self points by difference in x
        for line in self.poly:
            for point in line:
                point[0] -= other.xsize/2
        self.poly = [[list(point) for point in line] for line in self.poly]
        old_size = self.xsize
        self.xsize = new_size
        self.ysize = self.ysize
        #get the others poly
        other_poly = other.poly
        #other is in the middle of the new structure, and we must move it to the right, also we must consider last_pos
        
        if last_pos > self.xsize/2:
            last_pos -= self.gap
        last_pos -= other.xsize/2
        print(last_pos)
        first_pos = other.first_pos + other.gap* extra_c  - other.gap * 2*(self.cols-1)/2
        difference = last_pos - first_pos
        for line in other_poly:
            for point in line:
                point[0] += difference
        other.poly = [[list(point) for point in line] for line in other_poly]
        first_pos += difference
        #crop other to his size:
        #create box
        box = [[old_size/2 - other.xsize/2,-other.ysize/2],[old_size/2- other.xsize/2,other.ysize/2],[new_size/2,other.ysize/2],[new_size/2,-other.ysize/2]]
        #iterate through the lines and check if they intersect with the box
        #if they do, add the intersection points to the list
        new_otherpoly = []
        for line in other.poly:
            if bool.intersect(line,box)[0] != False:
                new_otherpoly.append(bool.intersect(line,box))
        new_otherpoly = [sublist[0] for sublist in new_otherpoly]
        other.poly = new_otherpoly
        #done, just add the poly
        self.poly += other.poly
        #determine new last_pos
        last_pt_sum = first_pos
        self.cols +=1
        c2 = other.gap
        while True:
            
            last_pt_sum += c2
            if last_pt_sum > new_size/2:
                self.last_pos = last_pt_sum 

                print("last pos")
                print(last_pt_sum)
                
                break
        
        self.gap = other.gap
        self.poly = [[list(point) for point in line] for line in self.poly]
        