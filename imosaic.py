
from PIL import Image
from pathlib import Path
import palettes


def dir_to_list(dr):
	""" returns files from dir in list form, using pathlib """
	l = list()
	for file in dr.iterdir():
		if file.is_file() and not file.name.split('.')[1] == 'DS_Store':
			l.append(file)
	return l


def crop_center_square(im):
	""" return image cropped as square in center """
	if im.width > im.height:
		return im.crop(((im.width - im.height)/2, 0, ((im.width - im.height)/2) + im.height, im.height))
	else:
		return im.crop((0, (im.height-im.width)/2, im.width, ((im.height-im.width)/2) + im.width))


def create(or_img, r, lot, alpha=None):
	""" create a mosaic of images that makes one larger image 
	input: the main picture, the number of rows, all the little pictures
	in a list, the alpha of the images to be blended if blended  """

	# set up sizing
	or_height = or_img.height
	or_width = or_img.width
	c = int((r/or_height) * or_width) # determines the number of columns
	img = or_img.resize((c, r), Image.BICUBIC).convert('RGB') # resize image

	# edit lot images
	for i in range(len(lot)):
		lot[i] = crop_center_square(lot[i]).resize((int(or_width/c), int(or_height/r)), Image.BICUBIC).convert('RGB')

	# get palettes
	pals = {}
	for i in lot:
		pals[palettes.iPalette(i, 2, 'RGB').dom_color()] = i

	# make empty mosaic array
	mosaic = []
	for rows in range(r):
		mosaic.append([])
		for columns in range(c):
			mosaic[rows].append(None)

	# get right images
	for row in range(img.height):
		for column in range(img.width):
			p = img.getpixel((column, row))

			distances = list(map( lambda c: (abs(p[0]-c[0]) + abs(p[1]-c[1]) + abs(p[2]-c[2])) , list(pals.keys()) ))
			mosaic[row][column] = lot[distances.index(min(distances))]

	# make mosaic
	canvas = Image.new('RGB', (or_width, or_height))
	for row in range(r):
		y = int(row * or_height/r)
		for column in range(c):
			x = int(column * or_width/c)

			canvas.paste(mosaic[row][column], (x, y))

	if alpha != None:
		canvas = Image.blend(canvas, or_img, alpha)

	return canvas

