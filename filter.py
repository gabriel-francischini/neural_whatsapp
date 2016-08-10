#!/usr/bin/python
# -*- coding: utf-8
from PIL import Image
from PIL import ImageFilter
from color import *

# Default filter (it do nothing to images)
default_filter = [1,1,1,    1,1,1,    1,1,1]

# Max number of different filters a A.I. can have
max_palette_size = 50

# Max number of length a A.I. can combine the filters
# To create a "recipe"
max_recipe_size = 80


# This function applies a filter to a image
def applyFilter(image, filter = default_filter):
	
	# Transforms filter in a real kernel
	kernel = ImageFilter.Kernel( (3,3), filter )

	# Apply the filter 
	image.filter(kernel)

	# Get the image's size
	x_size, y_size = image.size

	# If the image is already one pixel
	# we don't need to crop nothing
	if (x_size < 2) and (y_size < 2):
		return image

	# Otherwise, we need to made it smaller
	else:
		
		# If the image has a width of one pixel,
		# we'll only smaller it's height
		if(x_size <= 2):
			# Don't crop the single pixel
			x_crop_beginning = 0
			# And don't exclude it
			x_lenght = 1
		
		# Otherwise, we should crop it's width too
		else:
			# We crop the first pixel (pixel 0)
			x_crop_beginning = 1
			# And the last one
			x_lenght = x_size - 1


		# If the image has a height of one single pixel,
		# we'll only smaller it's width
		if y_size <=2:
			# We don't crop the first pixel
			y_crop_beginning = 0
			# And don't exclude it
			y_length = 1
		
		# Otherwise, we crop it's height too
		else:
			# We crop the first and last pixel
			y_crop_beginning = 1
			y_length = y_size - 1

		image = image.crop((x_crop_beginning, y_crop_beginning, 
							x_lenght, y_length))

		return image