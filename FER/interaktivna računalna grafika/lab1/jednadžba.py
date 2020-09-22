import numpy as np

var=input()
s=var.split(",")
s=np.array(s,int)

a = np.array([[s[0], s[1], s[2]], [s[4], s[5], s[6]], [s[8], s[9], s[10]]])
b = np.array([s[3], s[7], s[11]])
x = np.linalg.solve(a, b)
print("[x y z] = ",x)
