from PIL import Image, ImageDraw, ImageOps
from random import choice, randint
from useful import *
from pathlib import Path
import colorsys as cs


class Palette:

	def __init__(self, colors, mode):
		""" input the colors in a list of rgb tuples
		mode is either 'RGB' or 'HSV' """

		self.palette = colors
		self.num = len(self.palette)
		self.mode = mode

		if self.mode == 'RGB':
			self.rtoh = {}
			for c in self.palette:
				self.rtoh[c] = rgb_to_hsv(c)
			self.htor = dict((v,k) for k,v in self.rtoh.items())
		elif self.mode == 'HSV':
			self.htor = {}
			for c in self.palette:
				self.htor[c] = hsv_to_rgb(c)
			self.rtoh = dict((v,k) for k,v in self.htor.items())


	def __str__(self):
		""" print palette """
		return str(self.palette)

	def __getitem__(self, item):
		""" use palette as a list """
		return self.palette[item]

	def __add__(self, other):
		""" return a palette with colors from both palettes """
		if other.mode == self.mode:
			return Palette(list(set(self.palette).union(set(other.palette))), self.mode)

	def __sub__(self, other):
		""" return a palette with a color removed """
		palette = self.palette
		palette.remove(other)
		return Palette(palette, self.mode)

	def add(self, color):
		""" return palette with added color """
		if color not in self.palette:
			palette = self.palette
			palette.append(color)
			return Palette(palette, self.mode)
		else:
			return Palette(self.palette, self.mode)

	def take(self, color):
		""" return a palette with removed color """
		if color in self.palette:
			palette = self.palette
			palette.remove(color)
			return Palette(palette, self.mode)
		else:
			return Palette(self.palette, self.mode)

	def invert(self):
		""" return a palette with inverted colors """
		if self.mode == 'RGB':
			new = list(map(lambda color: invertC(color, self.mode), self.palette))
			return Palette(new, 'RGB')
		elif self.mode == 'HSV':
			new = list(map(lambda t: (invert(t[0]), t[1], t[2]), self.palette))
			return Palette(new, 'HSV')

	def change_hue(self, amount):
		if self.mode == 'RGB':
			self.set_mode('HSV')
			p = Palette(list(map(lambda t: (change(t[0], amount), t[1], t[2]), self.palette)), 'HSV')
			p.set_mode('RGB')
			self.set_mode('RGB')
			return p
		elif self.mode == 'HSV':
			p = Palette(list(map(lambda t: (change(t[0], amount), t[1], t[2]), self.palette)), 'HSV')
			return p

	def change_sat(self, amount):
		if self.mode == 'RGB':
			self.set_mode('HSV')
			p = Palette(list(map(lambda t: (t[0], change(t[1], amount), t[2]), self.palette)), 'HSV')
			p.set_mode('RGB')
			self.set_mode('RGB')
			return p
		elif self.mode == 'HSV':
			p = Palette(list(map(lambda t: (t[0], change(t[1], amount), t[2]), self.palette)), 'HSV')
			return p

	def change_val(self, amount):
		if self.mode == 'RGB':
			self.set_mode('HSV')
			p = Palette(list(map(lambda t: (t[0], t[1], change(t[2], amount)), self.palette)), 'HSV')
			p.set_mode('RGB')
			self.set_mode('RGB')
			return p
		elif self.mode == 'HSV':
			p = Palette(list(map(lambda t: (t[0], t[1], change(t[2], amount)), self.palette)), 'HSV')
			return p


	def set_mode(self, mode):
		""" set the mode """
		if mode == 'RGB' and self.mode == 'HSV':
			self.palette = list(map(lambda c: self.htor[c], self.palette))
			self.mode = mode
		elif mode == 'HSV' and self.mode == 'RGB':
			self.mode = mode
			self.palette = list(map(lambda c: self.rtoh[c], self.palette))


	def reverse(self):
		""" reverse order of palette """
		self.palette.reverse()


	def sort_by_hsv(self, n):
		""" sort the palette by 0: hue, 1: saturation, 2: value """
		if self.mode == 'RGB':
			self.set_mode('HSV')
			self.palette.sort(key = lambda item: item[n])
			self.set_mode('RGB')
		else:
			self.palette.sort(key = lambda item: item[n])

		if n == 0:
			distances = [abs(self.palette[0][n] - self.palette[self.num-1][n])]
			for i in range(self.num-1):
				distances.append(abs(self.palette[i][n] - self.palette[i+1][n]))
			indx = distances.index(max(distances))
			self.palette = self.palette[indx:] + self.palette[:indx]

	def deep_sort(self, b, v, n, bw=False):
		""" best for large amounts of color (100)
		sort by hue, saturation, or value, specified by b,
		then split into groups of n and sort those groups by v """

		if self.mode == 'RGB':
			mode = 'RGB'
			self.set_mode('HSV')
		elif self.mode == 'HSV':
			mode = 'HSV'

		p = Palette(self.palette.copy(), 'HSV')
		gry = Palette([], 'HSV')

		if bw:
			for color in p.palette:
				if color[1] < 25 or color[2] < 50:
					gry = gry.add(color)
					p = p.take(color)
			gry.sort_by_hsv(2)
		
		p.sort_by_hsv(b)
		secs = chunk_palette(p, n)
		for s in range(len(secs)):
			if s % 2 == 0:
				secs[s].sort_by_hsv(v)
			else:
				secs[s].sort_by_hsv(v)
				secs[s].reverse()
		if s % 2 == 0:
			gry.reverse()

		self.palette = []
		for s in secs:
			self.palette = self.palette + s.palette
		self.palette = self.palette + gry.palette

		if mode == 'RGB':
			self.set_mode('RGB')


	def display(self, size=(800, 200)):
		""" show palette """

		im = Image.new(self.mode, size, color=(255, 255, 255))
		ob = ImageDraw.Draw(im, mode=self.mode)

		cx = size[0]/(self.num)

		for i in range(self.num):
			coords = [i*cx, 0, (i+1)*cx, size[1]]
			ob.rectangle(coords, fill=self.palette[i])

		return im


class iPalette(Palette):


	def __init__(self, image, num, mode):
		""" take the name/path of the image, the number of colors,
		and the mode of the colors either 'RGB' or 'HSV' """
		
		self.mode = mode
		self.num = num

		self.original = image
		if image.mode != self.mode:
			image = image.convert(self.mode)
		self.image = image.resize((100, int((image.height*100)/image.width)))

		self.frequencies = self.image.getcolors(16777216)
		self.colors = list(dict.fromkeys(list(map(second, self.frequencies))))

		self.clusters = []
		self.palette = self.k_means()

		if self.mode == 'RGB':
			self.rtoh = {}
			for c in self.palette:
				self.rtoh[c] = rgb_to_hsv(c)
			self.htor = dict((v,k) for k,v in self.rtoh.items())
		elif self.mode == 'HSV':
			self.htor = {}
			for c in self.palette:
				self.htor[c] = hsv_to_rgb(c)
			self.rtoh = dict((v,k) for k,v in self.htor.items())


	def k_means(self):
		""" return palette using k_means algorithm """

		clusters = []
		old_clusters = None

		# pick random centroids
		choices = self.colors
		centroids = []
		for k in range(self.num):
			centroids.append(choices.pop(choices.index(choice(self.colors))))

		while old_clusters != clusters:
		
			# make empty clusters
			old_clusters = clusters
			clusters = []
			for k in range(self.num):
				clusters.append([])

			# group clusters
			for c in self.colors:
				distances = list(map(lambda centroids: get_distance_nD(centroids, c), centroids))
				clusters[distances.index(min(distances))].append(c)

			# makes new centroids
			old_centroids = centroids
			centroids = []
			for c in range(len(clusters)):
				if len(clusters[c]) != 0:
					centroids.append(mean(clusters[c]))
				else:
					centroids.append(old_centroids[c])

		self.clusters = clusters
		return centroids

	def get_count(self):
		""" get the actual count of the colors in the clusters for
		each palette color """

		count = dict.fromkeys(self.palette, 0)

		for c in range(self.num):
			for color in self.clusters[c]:
				if color in self.colors:
					count[self.palette[c]] += self.frequencies[self.colors.index(color)][0]

		return count

	def pure_dom_color(self):
		""" return the most frequent color """
		return max(self.frequencies)[1]


	def dom_color(self):
		""" return the dominant color """
		return dicmax(self.get_count())


	def sort_by_freq(self):
		""" sort the colors by their frequency """

		count = self.get_count()

		sorted_palette = []
		sorted_clusters = []
		for i in range(self.num):
			color = dicmax(count)
			sorted_palette.append(color)
			sorted_clusters.append(self.clusters[self.palette.index(color)])
			del count[color]
		self.palette = sorted_palette
		self.clusters = sorted_clusters


	def invert(self):
		""" return a palette with inverted colors """
		return iPalette(ImageOps.invert(self.original), self.num, self.mode)


	def display_wimage(self, height=0.2):
		""" show palette under image """

		im = self.original.copy()
		pal = self.display((im.width, int(im.height*height)))

		new = Image.new('RGB', (im.width, im.height + pal.height), color=(255, 255, 255))
		new.paste(im, (0, 0))
		new.paste(pal, (0, im.height))

		return new

# functions to make palettes

def randomC():
	""" return a random color """
	return (randint(0, 255), randint(0, 255), randint(0, 255))

def invertC(color, mode):
	""" return an inverted color """
	if mode == 'RGB':
		return ((255-color[0]), (255-color[1]), (255-color[2]))

def invert(o):
	""" invert hue """
	return change(o, 128)

def change(o, c):
	""" change value """
	value = o + c
	if value > 255:
		value -= 255
	return value


def randomP(num, mode='RGB'):
	""" return a palette with random colors """

	p = []
	for i in range(num):
		p.append(randomC())

	return Palette(p, mode)

def adicP(color, n):
	""" input a color in HSV and the number of colors in the palette
	and return a color palette with evenly spaced colors """
	p = []
	hue = color[0]
	for i in range(n):
		p.append((hue, color[1], color[2]))
		hue = abs(int(hue + 255/n))
		if hue > 255:
			hue -= 255
	return Palette(p, 'HSV')

def monochromaticP(hue, saturation, num):
	""" input a hue, saturation and the number of colors in the palette
	and return a monochromatic color palette """

	p = []
	c = int(200/num)

	for n in range(num):
		p.append((hue, saturation, 60+(c*n)))

	return Palette(p, 'HSV')

def analogousP(color, n, step=50):
	""" input color and number of neighbors/2, return a color palette """
	p = []
	for i in range(-n, n+1):
		p.append((color[0] + step*i, color[1], color[2]))
	return Palette(p, 'HSV')

def random_monochromaticP(num):
	""" input the number of colors
	and output a random monochromatic color scheme """
	hue = randint(0, 255)
	pl = []
	for c in range(num):
		pl.append((hue, randint(0, 255), randint(20, 255)))
	return Palette(pl, 'HSV')

def random_analogousP(num):
	""" input the number of colors and return analogous color scheme """
	if num >= 3:
		pl = []
		hue = randint(0, 255)
		for c in range(num):
			if c % round(num/3) == 0:
				hue = change(hue, 35)
			pl.append((hue, randint(0, 255), randint(0, 255)))
		print(pl)
		return Palette(pl, 'HSV')

def random_complementaryP(num):
	""" input the number of colors, return complementary color scheme """
	pl = []
	hue = randint(0, 255)
	for c in range(num):
		if c == round(num/2):
			hue = invert(hue)
		pl.append((hue, randint(0, 255), randint(0, 255)))
	return Palette(pl, 'HSV')


# other

def chunk_palette(p, n):
	""" return a list of n-sized palettes of the list """
	r = []
	for i in range(0, len(p.palette), n):
		r.append(Palette(p.palette[i:i+n], p.mode))
	return r


# converting

def rgb_to_hsv(color):
	""" input RGB color and return HSV color """
	percentages = tuple(map(lambda c: c/255, color))
	return tuple(map(lambda c: round(c*255), cs.rgb_to_hsv(*percentages)))


def hsv_to_rgb(color):
	""" input HSV color and return RGB color """
	percentages = tuple(map(lambda c: c/255, color))
	return tuple(map(lambda c: round(c*255), cs.hsv_to_rgb(*percentages)))

if __name__ == '__main__':

	file = Path.home() / 'path here'
	img = Image.open(file)
	pal = iPalette(img, 5, 'RGB')
	pal.sort_by_freq()
	pal.display_wimage().show()

	# dr = Path.cwd() / 'Apps'

	# for file in path.iterdir():
	# 	if file.suffix in ['.jpeg', '.jpg', '.png']:
	# 		img = Image.open(file)
	# 		pal = iPalette(img, 3, 'RGB')
	# 		pal.display_wimage();


