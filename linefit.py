import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as m3d
from numpy import *
   
# R is the set of arrays that the pattern recognition will spit out
# It should be in the same form that the event is in, just not all of the arrays, only a
# select number of them

# All this is based on the conclusion from 
# http://www.scribd.com/doc/31477970/Regressions-et-trajectoires-3D
n = len(R)		

# Sets up arrays of zeros for each value that is calculated in a for loop
x = [0] * n
y = [0] * n	
z = [0] * n
x_2 = [0] * n
y_2 = [0] * n
z_2 = [0] * n
xy = [0] * n
xz = [0] * n
yz = [0] * n

# This replaces the zeros in the x,y, and z vector with their respective values in each 
# array
for i in range(n):
	x[i] = R[i][1]
	y[i] = R[i][2]
	z[i] = R[i][3]

# Simple calculation of the values needed
X_m = (1/float(len(x)))*(sum(x))
Y_m = (1/float(len(y)))*(sum(y))
Z_m = (1/float(len(z)))*(sum(z))

# Same as previous for loop but does it for x^2 since it is needed in the summation in
# the equation
for i in range(len(x)):
    x_2[i] = (R[i][1])**2 
    y_2[i] = (R[i][2])**2 
    z_2[i] = (R[i][3])**2 
    
Sxx = -(X_m**2) + (1/float(len(x_2)))*(sum(x_2))
Syy = -(Y_m**2) + (1/float(len(y_2)))*(sum(y_2))
Szz = -(Z_m**2) + (1/float(len(z_2)))*(sum(z_2))

# Same as previous for loop but does it for x*y since it is needed in the summation in
# the equation
for i in range(len(x)):
    xy[i] = (R[i][1]) * (R[i][2])
    xz[i] = (R[i][1]) * (R[i][3]) 
    yz[i] = (R[i][2]) * (R[i][3])
    
Sxy = (-X_m*Y_m) + (1/float(len(xy)))*(sum(xy))
Sxz = (-X_m*Z_m) + (1/float(len(xz)))*(sum(xz))
Syz = (-Y_m*Z_m) + (1/float(len(yz)))*(sum(yz))

Theta = (arctan( (2*Sxy)/(Sxx-Syy) ) )/2

# Calculating all the k values
K11 = (Syy+Szz)*(cos(Theta)**2) + (Sxx+Szz)*(sin(Theta)**2) - (2*Sxy*cos(Theta)*sin(Theta))
K22 = (Syy+Szz)*(sin(Theta)**2) + (Sxx+Szz)*(cos(Theta)**2) + (2*Sxy*cos(Theta)*sin(Theta))
K12 = -Sxy*((cos(Theta)**2) - (sin(Theta)**2)) + (Sxx - Syy)*cos(Theta)*sin(Theta)
K10 = Sxz*cos(Theta) + Syz*sin(Theta)
K01 = -Sxz*sin(Theta) + Syz*cos(Theta)
K00 = Sxx + Syy

# Coefficients
c2 = -K00 - K11 -K22
c1 = K00*K11 + K00*K22 + K11*K22 - (K01**2) - (K10**2)
c0 = (K01**2)*K11 + (K10**2)*K22 - (K00*K11*K22)

p = c1 - ((c2**2)/3)
q = ((2.0/27.0)*(c2**3)) - ((c1*c2)/3) + c0
R = ((q**2)/4) + ((p**3)/27)

# See the document I listed above
if R>0:
    d2m = (-c2/3) + (((-q/2) + (R**(1.0/2.0)))**(1.0/3.0)) + (((-q/2) - (R**(1.0/2.0)))**(1.0/3.0))
    Pp = 0
    phi = 0
else:
    Pp = (-(p**3)/27)**(1.0/2.0)
    phi = arccos(-q/(2*Pp)) #fix this
    d2m1 = (-c2/3) + 2*(Pp**(1.0/3.0))*cos(phi/3)
    d2m2 = (-c2/3) + 2*(Pp**(1.0/3.0))*cos((phi+2*pi)/3)
    d2m3 = (-c2/3) + 2*(Pp**(1.0/3.0))*cos((phi+4*pi)/3)
    d2m = min(d2m1,d2m2,d2m3)
    
a = (-K10/(K11-d2m))*cos(Theta) + (K01/(K22-d2m))*sin(Theta)
b = (-K10/(K11-d2m))*sin(Theta) + (-K01/(K22-d2m))*cos(Theta)

# These are the values of the second point to graph that gives you the slope of the best
# fit line
u = (1/float((1+(a**2)+(b**2)))) * (((1+(b**2))*X_m) - (a*b*Y_m) + a*Z_m)
v = (1/float((1+(a**2)+(b**2)))) * ((-a*b*X_m) + ((1+(a**2))*Y_m) + b*Z_m)
w = (1/float((1+(a**2)+(b**2)))) * ((a*X_m) + (b*Y_m) + (((a**2)+(b**2))*Z_m))

# This is the line that needs to be plotted along with the data
# See the github commit for what the issue is
X = [u,X_m]
Y = [v,Y_m]
Z = [w,Z_m]

