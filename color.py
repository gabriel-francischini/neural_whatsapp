#!/usr/bin/python
# -*- coding: utf-8
from os import isatty
from colorama import *

# Initialize colorama, important for windows
init()

# This is a function for easly coloring output
def colorize(string, *colors):
	
	# If script is running on a console,
	# color information should be added
	if isatty():

		# colored_string is a self-contained colored string
		colored_string = ""

		# User's options about color and style are added to string...
		for color in colors:
			colored_string += color


		# And the we prevent other non-related strings 
		# to be formatted as above
		colored_string += Fore.RESET + Back.RESET + Style.RESET_ALL
	
	else:
		# Otherwise, string show be a raw string
		colored_string = string

	# Frequently UnicodeEncodeError or UnicodeDecodeError
	# rises while attempting to print out the string
	try:
		print(colored_string)
	
	# If it do rise, the we should try other encoding
	except UnicodeError:
		try:
			print(colored_string.encode("latin-1", "ignore"))
		
		except UnicodeError:
			try:
				print(colored_string.encode("ascii", "ignore"))
			
			# At last, when no solution worked, we output a raw string
			except UnicodeError:
				try:
					print(string)

				# May God prevent us from needing to ignore the
				# original string and print out something else
				except UnicodeError:
					print("\n\tFatal error while printing string".upper())


	return None


# A coloring function based in some evaluation
def colorChoice(string, evaluation, colorTrue = Fore.GREEN, colorFalse = Fore.RED):
	if evaluation:
		colorize(string, colorTrue)
	
	else:
		colorize(string, colorFalse)

	return
