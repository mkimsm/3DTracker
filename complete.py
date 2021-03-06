import numpy as np

def stringtoarray(s):
   s = s[:len(s)-1]
   s = s.split(' ')

   i=0
   for num in s:
      s[i] = int(s[i])
      i += 1
   a = np.array(s)
   return a

   
def package(x):
   f = open(x)
   pkg = []
   L = -1
   for line in f:
      if line[0] == '#':
         a = []
         pkg.append(a)
         L += 1
      else:
         pkg[L].append(stringtoarray(line))
   return pkg
   
   

R = package('NIFFTE-alphas.dat')

k = raw_input('What event would you like to use?\n')
K = int(k)
this = R[K]

toli = raw_input('What would you like your tolerance to be?\n')
tol = int(toli)
good =[]
for i in range(len(R[K])):
	if R[K][i][4] >  tol:
		good.append(R[K][i])
		
n = len(good)
x = [0] * n
y = [0] * n
z = [0] * n
x_2 = [0] * n
y_2 = [0] * n
z_2 = [0] * n
xy = [0] * n
xz = [0] * n
yz = [0] * n
for i in range(n):
	x[i] = good[i][1]
	y[i] = good[i][2]
	z[i] = good[i][3]

X_m = (1/float(len(x)))*(sum(x))
Y_m = (1/float(len(y)))*(sum(y))
Z_m = (1/float(len(z)))*(sum(z))

for i in range(len(x)):
    x_2[i] = (good[i][1])**2 
    y_2[i] = (good[i][2])**2 
    z_2[i] = (good[i][3])**2 
    
Sxx = -(X_m**2) + (1/float(len(x_2)))*(sum(x_2))
Syy = -(Y_m**2) + (1/float(len(y_2)))*(sum(y_2))
Szz = -(Z_m**2) + (1/float(len(z_2)))*(sum(z_2))

for i in range(len(x)):
    xy[i] = (good[i][1]) * (good[i][2])
    xz[i] = (good[i][1]) * (good[i][3]) 
    yz[i] = (good[i][2]) * (good[i][3])
    
Sxy = (-X_m*Y_m) + (1/float(len(xy)))*(sum(xy))
Sxz = (-X_m*Z_m) + (1/float(len(xz)))*(sum(xz))
Syz = (-Y_m*Z_m) + (1/float(len(yz)))*(sum(yz))

Theta = (np.arctan( (2*Sxy)/(Sxx-Syy) ) )/2

K11 = (Syy+Szz)*(np.cos(Theta)**2) + (Sxx+Szz)*(np.sin(Theta)**2) - (2*Sxy*np.cos(Theta)*np.sin(Theta))
K22 = (Syy+Szz)*(np.sin(Theta)**2) + (Sxx+Szz)*(np.cos(Theta)**2) + (2*Sxy*np.cos(Theta)*np.sin(Theta))
K12 = -Sxy*((np.cos(Theta)**2) - (np.sin(Theta)**2)) + (Sxx - Syy)*np.cos(Theta)*np.sin(Theta)
K10 = Sxz*np.cos(Theta) + Syz*np.sin(Theta)
K01 = -Sxz*np.sin(Theta) + Syz*np.cos(Theta)
K00 = Sxx + Syy

c2 = -K00 - K11 -K22
c1 = K00*K11 + K00*K22 + K11*K22 - (K01**2) - (K10**2)
c0 = (K01**2)*K11 + (K10**2)*K22 - (K00*K11*K22)

p = c1 - ((c2**2)/3)
q = ((2.0/27.0)*(c2**3)) - ((c1*c2)/3) + c0
R = ((q**2)/4) + ((p**3)/27)

if R>0:
    d2m = (-c2/3) + (((-q/2) + (R**(1.0/2.0)))**(1.0/3.0)) + (((-q/2) - (R**(1.0/2.0)))**(1.0/3.0))
    Pp = 0
    phi = 0
else:
    Pp = (-(p**3)/27)**(1.0/2.0)
    phi = np.arccos(-q/(2*Pp)) #fix good
    d2m1 = (-c2/3) + 2*(Pp**(1.0/3.0))*np.cos(phi/3)
    d2m2 = (-c2/3) + 2*(Pp**(1.0/3.0))*np.cos((phi+2*np.pi)/3)
    d2m3 = (-c2/3) + 2*(Pp**(1.0/3.0))*np.cos((phi+4*np.pi)/3)
    d2m = min(d2m1,d2m2,d2m3)
    
a = (-K10/(K11-d2m))*np.cos(Theta) + (K01/(K22-d2m))*np.sin(Theta)
b = (-K10/(K11-d2m))*np.sin(Theta) + (-K01/(K22-d2m))*np.cos(Theta)

u = (1/float((1+(a**2)+(b**2)))) * (((1+(b**2))*X_m) - (a*b*Y_m) + a*Z_m)
v = (1/float((1+(a**2)+(b**2)))) * ((-a*b*X_m) + ((1+(a**2))*Y_m) + b*Z_m)
w = (1/float((1+(a**2)+(b**2)))) * ((a*X_m) + (b*Y_m) + (((a**2)+(b**2))*Z_m))


X = [u,X_m]
Y = [v,Y_m]
Z = [w,Z_m]
diffx = X_m - u
diffy = Y_m - v
diffz = Z_m - w
Xn = [X_m + diffx,X_m]
Yn = [Y_m + diffy,Y_m]
Zn = [Z_m + diffz,Z_m]
print(X)
print(Y)
print(Z)

import numpy
import mayavi
from mayavi.mlab import *


mayavi.mlab.figure(figure='Collision', bgcolor=(0,0,0), fgcolor=None, engine=None, size=(1200, 800))
points3d(x, y, z, scale_factor=.35, color=(.04,.85,.14))

mayavi.mlab.axes( color=(1,1,1), x_axis_visibility=True, xlabel='x', y_axis_visibility=True, ylabel='y', z_axis_visibility=True, zlabel='z')
mayavi.mlab.title('This is physics')
plot3d(X,Y,Z,tube_radius=0.1, color=(.94,1,0))
plot3d(Xn,Yn,Zn,tube_radius=0.1, color=(.94,1,0))


