import numpy as np

var=input("Unesi koordinate točke A,B,C i T odvojene zarezom\n")
s=var.split(",")
s=np.array(s,float)

a = np.array([[s[0], s[3], s[6]], [s[1], s[4], s[7]], [s[2], s[5], s[8]]])
b = np.array([[s[9]], [s[10]], [s[11]]])
try:
  a = np.linalg.inv(a)
except:
  print("Something went wrong")
else:
  print("Nothing went wrong")
  x = np.linalg.solve(a, b)
  print("[t1 t2 t3] = ", x.transpose())



