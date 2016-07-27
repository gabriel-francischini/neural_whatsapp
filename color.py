#!/usr/bin/python
# -*- coding: utf-8
from colorama import *


def color(string, color):
	init()
	return (color + string + Fore.RESET + Back.RESET + Style.RESET_ALL)

def pcolor(scolor,string):
	try:
		try:
			try:
				try:
					print(color(string,scolor))
				except UnicodeError:
					print(color(string.encode("latin-1", "ignore"), scolor))
			except UnicodeError:
				print(color(string.encode("ascii", "ignore"),scolor))
		except UnicodeError:
			print("\nError while printing a string".encode("ascii", "ignore"))
	except:
		pass
	#try:
	#	print(color(string,scolor))
	#except UnicodeError:
	#	try:
	#		print(color(string.encode("latin-1", "ignore"), scolor))
	#	except UnicodeError:
	#		try:
	#			print(color(string.encode("ascii", "ignore"),scolor))
	#		except UnicodeError:
	#			try:
	#				print("\nError while printing a string".encode("ascii", "ignore"))
	#			except UnicodeError:
	#				pass
	finally:
		return None


def colorChoice(evaluation, colorFalse = Fore.RED, colorTrue = Fore.GREEN):
	if evaluation:
		return colorTrue
	else:
		return colorFalse


def colorGen(string, value):
	return color(string, colorChoice(value > 0))