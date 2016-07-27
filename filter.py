#!/usr/bin/python
# -*- coding: utf-8
from PIL import Image
from PIL import ImageFilter
from color import *

filter_default_list = [1,1,1,   1,1,1,   1,1,1]
filter_size = len(filter_default_list)
palette_size = 50
recipe_size = 80


class filter:
	
	def __init__(self, args = filter_default_list):
		self.weights = []
		for arg in args:
			self.weights.append(arg)
		return None
		
	def calculate(self, list):
		result = 0
		index = 0
		try:
			for input in list:
				result+= self.weights[index]*input
				index += 1
		except IndexError:
			print("Valores demais foram passados ao filtro. Ignorando o excesso.")
		return result

		
def applyFilter(image, filterlist):
	kernel = []
	for value in range(9):
		try:
			kernel.append(filterlist[value])
		except IndexError:
			color("Houve um erro numa tentativa de acesso a um filtro/kernel.",
					 Fore.RED)
	kernel = ImageFilter.Kernel( (3,3), kernel)
	sizex, sizey = image.size
	if (sizex < 2 and sizey < 2):
		return image
	else:
		image.filter(kernel)
		if(sizex <= 2):
			posx = 0
			lenghtx = 1
		else:
			posx = 1
			lenghtx = sizex - 1
		if(sizey <= 2):
			posy = 0
			lenghty = 1
		else:
			posy = 1
			lenghty = sizey - 1
		image = image.crop((posx, posy, lenghtx, lenghty))
		return image
	