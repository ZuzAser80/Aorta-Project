import matplotlib.pyplot as plt
import numpy as np
s = input("File name: ")
sepr = input("Input the separator: ")
x = input("Argument 1 (X): ")
y = input("Argument 2 (Y): ")
f = open(s, 'r').readline().rstrip().split(sepr)
ind_x = f.index(x)
ind_y = f.index(y)
points_x = []
points_y = []
with open(s, 'r') as f:
    for line in f:
        line = line.rstrip()
        params = line.split(sepr)
        points_x.append(params[ind_x])
        points_y.append(params[ind_y])
# print("X:", points_x)
# print("Y:", points_y)
plt.scatter(points_x, points_y)
plt.show()
