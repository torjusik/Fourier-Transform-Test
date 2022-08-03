from cmath import sqrt, tan
from math import ceil, cos, pi, sin
from turtle import pos
from numpy import angle, array, float64, ndarray
from pygame.draw import line, circle
class Vector():
    def __init__(self, offsetFromParent, parentVector=array((1920/2, 1080/2), dtype=float64)):
        
        self.offsetFromParent = array(offsetFromParent)
        self.complex = complex(offsetFromParent[0], offsetFromParent[1])
        self.parentVector = parentVector
        tangentSqr = self.offsetFromParent[0]**2 + self.offsetFromParent[1]**2
        self.hypotenus = ceil(sqrt(tangentSqr).real)
        self.arrowsize = self.hypotenus * 0.2

        if type(parentVector) != ndarray:
            self.pos = self.parentVector.pos + self.offsetFromParent
            self.radian = parentVector.radian + angle(self.complex)
        else: 
            self.radian = angle(self.complex)
            self.pos = self.parentVector + self.offsetFromParent

    def update(self):
        self.pos = self.parentVector.pos + self.offsetFromParent
    
    def set_rad(self, radian):
        self.radian = radian
        self.offsetFromParent[0] =  self.hypotenus * cos(self.radian).real
        self.offsetFromParent[1] = self.hypotenus * sin(self.radian).real
        self.complex = complex(self.offsetFromParent[0], self.offsetFromParent[1])
        if type(self.parentVector) != (ndarray):
            self.pos = self.parentVector.pos + self.offsetFromParent
        else: self.pos = self.parentVector + self.offsetFromParent
    

    def draw(self, screen):
        line(screen, (255, 255, 255), self.pos - self.offsetFromParent, self.pos, width=5)
        if type(self.parentVector) != ndarray:
            circle(screen, (255, 255, 255), self.parentVector.pos, self.hypotenus, width = 2)
            self.parentVector.draw(screen)
        else: circle(screen, (255, 255, 255), self.parentVector, self.hypotenus, width=2)
            
        """ rad1 = self.radian + 3*pi/4
            rad2 = self.radian - 3*pi/4
        else: 
            rad1 = self.radian + 3*pi/4
            rad2 = self.radian - 3*pi/4
        xaxis1 = cos(rad1) * self.arrowsize
        yaxis1 = sin(rad1) * self.arrowsize
        
        xaxis2 = cos(rad2) * self.arrowsize
        yaxis2 = sin(rad2) * self.arrowsize

        arr1 = array((xaxis1, yaxis1), dtype=float64)
        arr2 = array((xaxis2, yaxis2), dtype=float64)
        line(screen, (255, 255, 0), self.pos, self.pos + arr1, width=5)
        line(screen, (255, 255, 0), self.pos, self.pos + arr2, width=5)"""    

if __name__ == '__main__':
    vector = Vector(array((-2, 0), dtype=float64))
    print(vector.radian)
