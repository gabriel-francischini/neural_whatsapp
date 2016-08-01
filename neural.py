#!/usr/bin/python
# -*- coding: utf-8

# Import necessary modules and packages
from random import *
from graphics import *
from decimal import Decimal, localcontext
from math import *
from time import *
from color import *
from filter import *
from colorama import *

# Start a seed for the randoms functions
seed()

# p is a sigmoid variable. It's a measure of the sigmoid' smoothness result.
# Higher p indicates a homogeneous function
p = 1.0

# How precise a neuron's output is. Default value is 80, so if
# output is greater than 80p it will be approximated to 1.
# If it's less than -80p it'll be approximated to -1.
sig_prec = 80


# Should we do warnings and rise exceptions?
do_warnings = True


crossover_rate = 0.7
mutation_rate = 0.0001


# A scaling factor for DNA values
dna_factor = 10


# Default values for neurons
default_1st_layer = 50
default_hidden_layers = 10
default_neurons_by_hidden_layer = 10
default_last_layer = 4

# Here's a variable to limit DNA length:
# TODO: rewrite it
max_genes = 10000


class neuron:
	"""This class implements a neuron.

	Attributes:
		inputs -- list with inputs (already multiplied by the weights)
		weights -- list with each weight (associated with each input)
		output -- output's value
		bias -- neuron's threshold value
		index -- wight corresponding to the next input
	"""

	def __init__(self, bias = 0.0):
		""" Initialize neuron's attributes """

		self.inputs = []
		self.weights = []
		self.index = 0

		self.output = 0.0

		self.bias = bias

	def doSigmoid(self):
		""" Sigmoid is a function to smooth a value.
			In this case, it'll smooth neuron's output
		"""

		# p is a indicative of sigmoid' smoothness
		# it's also the value of comparison for
		# approximations (it's useless to represent 
		# almost-1 numbers or almost-0 numbers, since
		# it can raise errors in number representation)
		relative_output = self.output/p

		# calculation of a sigmoid involves division
		# and as it's not allowed to divide by 0 or None
		# so the divider needs to be initialized
		divider = 1

		# If output is reasonable, use it
		if(-sig_prec < relative_output < sig_prec):
			divider = 1.0 + pow(e, -relative_output)
			self.output = 1/divider

		# otherwise, approximate it
		elif(relative_output > sig_prec):
			self.output = 0.0

		elif(relative_output < -sig_prec):
			self.output = 1.0

		return None


	def doOutput(self):
		""" Calculate a neuron's output and return it """

		# We start with a zeroed output
		self.output = 0.0

		# Each input, already multiplied by its weight
		# Is summed up to the output
		for input in self.inputs:
			self.output = self.output + bias

		# The value is compared to the bias
		self.output = self.output - self.bias

		# And smoothed
		self.doSigmoid()

		# Clean the inputs for reuse
		self.inputs = []

		# Clean the index for reuse
		self.index = 0
		
		return None


	def addInput(self, input, warning = do_warnings):
		""" Add an input to the neuron (circular) """

		try:
			# We multiply the input by a respective weight
			input = input * self.weights[self.index]

		# Sometimes there's more inputs than weights
		except IndexError:

			# We can raise a exception OR silently do it
			if(warning):
				raise neuron.TooMuchInputs("Attempt to add more input" 
					" than there are weights on neuron")
			else:
				# Find a valid weight similar to the input, using 
				# a circular approach 
				input = input * self.weights[index % len(weights)]


		# And changes the index
		self.index = self.index + 1

		# Add the partial-input to the list
		self.inputs.append(input)

		return None

	def addWeight(self, weight):
		""" Adds a weight in the neuron """

		# Simply append the new weight
		self.weights.append(weight)
		return None

	class TooMuchInputs(Exception):
		pass


class layer:
	""" A layer of neurons 

	Attributes:
		neurons -- list containing neurons
		outputs -- list with each neuron's output
		index -- next neuron to receive a input
	"""

	def __init__(self):
		""" Initialize attributes """

		self.index = 0
		self.neuronios = []
		self.outputs = []

	def addNeuron(self, neuron):
		""" Annexes the neuron to the neuron's list """

		self.neurons.append(neuron)
		return None

	def doOutput(self):
		""" Do the output of all neurons and store it in self.outputs """

		# Begin with an empty list
		self.outputs = []

		# For each neuron, do its output and
		# put it in the list
		for neuron in self.neurons:
			neuron.doOutput()
			self.outputs.append(neuron.output)

		return None

	def addInput(self, value, neuron_number = index):
		""" Add a input to a neuron """

		# Verifis if neuron_number is a valid neuron
		if neuron_number > len(self.neurons):
			pass

		# If it isn't, try to rise a exception
		elif do_warnings:
			raise layer.TooMuchInputs(" Attempted to add a input to a non-existing neuron inside a layer. Maybe you should reset layer.index to neuron 0? (layer.index = 0)")
		
		# But don't rise it if we should silently ignore it
		else:
			neuron_number = neuron_number % len(self.neurons)

		self.neurons[self.index].addInput(value)

		# Our job here is done
		return None

	def addInputList(self, inputs):
		""" Add a inputs for the neurons """

		# Check if inputs is a viable list of values for ALL neurons

		# If it is possible to complete assigns inputs to all neurons without any input left, then it maybe a no-problems input
		# (If it's possible to evenly assign inputs to all neurons, the the number of inputs must be a multiple of the number of the neurons i.e. there's a integer k that satisfies the relationship n_inputs = k * n_neurons )
		# ( Therefore, if n_inputs = k * n_neurons then n_inputs/n_neurons = k, and if k is a integer there follows that n_inputs/n_neurons should be integer too, otherwise k should not be an integer and it would not be possible to distribute the inputs to the neurons in an even way)
		if isinstance( ( len(inputs) / len(self.neurons) ), int):
			pass

		# Otherwise, it's probably a bad input and we should rise a exception
		elif do_warnings:
			raise layer.TooMuchInputs("Attempted to add a non-compatible list of inputs to a layer. Number of inputs and number of neurons differs.")

		# We can ignore if it's configured to but some neurons will got more inputs than others
		else:
			pass

		# For each input inside the inputs list:
		for input in range(len(inputs)):
			# We find a suitable neuron for that input
			correspondent_neuron = input%len(self.neurons)

			self.neurons[correspondent_neuron].addInput(inputs[input])

		
		return None
		
	class TooMuchInputs(Exception):
		pass