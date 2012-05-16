import numpy as np

def stringtoarray(s):
   #Remove the return and split the string into a list of chars
   s = s[:len(s)-1]
   s = s.split(' ')

   #Convert each element of the list into integers, convert to numpy array
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
      if line[0] == '#': #Create a new list for a new event
         a = []
         pkg.append(a)
         L += 1
      else:
         pkg[L].append(stringtoarray(line)) #Append the array version of the string to the current list
   return pkg

