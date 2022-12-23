
import matplotlib.pyplot as plt
from random import randint
from time import sleep

def random_list(length, mn, mx):
	""" get random list of numbers from mn to mx """
	rl = []
	for i in range(0, length):
		rl.append(randint(mn, mx))
	return rl

num_points = 200
num = 4 # number of groups

# x and y values
x = random_list(num_points, 0, 100)
y = random_list(num_points, 0, 100)

# x and y values as points
points = []
for i in range(num_points):
	points.append([x[i], y[i]])

plt.plot(x, y, 'go')

plt.xlabel('X')
plt.ylabel('Y')

plt.axis([0, 100, 0, 100])

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

clusters = []
old_clusters = []

# get random centroids from points
choices = points
centroids = []
for k in range(num):
	centroids.append(choices.pop(randint(0, len(choices)-1)))

def update(*fargs):
	pass

animation = FuncAnimation(plt, )

plt.show()
