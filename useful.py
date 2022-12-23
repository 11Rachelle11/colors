
from math import sqrt

def second(item):
	""" return the second item in an iterable """
	return item[1]

def dicmax(dic):
	""" return the key with the greatest value """
	m = ((0, 0, 0), 0)
	for key in dic:
		if dic[key] > m[1]:
			m = (key, dic[key])
	return m[0]

def get_distance_nD(a, b):
	 """ return the distance between two points in a three dimensional plane """
	 acc = 0
	 for i in range(len(a)):
	 	acc += (a[i] - b[i])**2
	 return sqrt(acc)

def mean(cluster):
	""" return the average of many points """
	points = []
	for d in range(len(cluster[0])):
		acc = 0
		for p in cluster:
			acc += p[d]
		points.append(int(acc/len(cluster)))
	return tuple(points)


