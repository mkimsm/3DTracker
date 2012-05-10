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

