
from pathlib import Path
from PIL import Image
import palettes

""" sort images by color """

def sort(apath, intervals, specificity=3, first_sort=0, second_sort=2):
	""" sort the images in a directory by their color by giving them
	numbers as names 
	apath: the pathlib Path object for the directory
	specificity: the number of colors to choose from to see which
	are dominant in each image
	first_sort: either hue, saturation, or value, the base order of the
	sort
	second_sort: either hue, saturation, or value, the order of each
	section of the colors
	intervals: how many colors each section of the second_sorting is """

	path = apath
	colors = {}

	for file in path.iterdir():
		if file.suffix in ['.jpeg', '.jpg', '.png']:
			img = Image.open(file)
			pal = palettes.iPalette(img, specificity, 'RGB')
			colors[pal.dom_color()] = file

	palette = palettes.Palette(list(colors.keys()), 'RGB')
	palette.deep_sort(first_sort, second_sort, intervals, False)
	palette.display().show()

	ordered_list = []
	for color in palette.palette:
		ordered_list.append(colors[color])

	for i in range(len(ordered_list)):
		file_name = '0'*(3-len(str(i))) + str(i) + ordered_list[i].suffix
		p = path / file_name
		if p.exists() and p in ordered_list:
			print('renamed')
			p.rename(path / (file_name + ' copy' + p.suffix))
		ordered_list[i].rename(p)


dr = Path.home() / 'Documents' / 'Desktop_Pics' / 'Sort2022Desktop'
sort(dr, 5)

