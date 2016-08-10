#!/usr/bin/python
# -*- coding: utf-8

# Import necessary modules and packages
from random import *
# from graphics import *
from decimal import Decimal, localcontext
from math import *
from time import *
from color import *
from filter import *
from colorama import *

# Start a seed for the randoms functions
seed()

# p is a sigmoid variable. It's a measure of the sigmoid' smoothness result.
# The formula of a sigmoid used is 1/(1+ e^(-input/p)
# Higher p indicates a homogeneous function
# (the function gets more linear with higher p)
p = 1.0

# How precise a neuron's output is. Default value is 80, so if
# input is greater than 80p the output will be approximated to 1 
# (output value for a 80p-input would be 1/1+e^-80 = 1/0.999999999... )
# If it's less than -80p output will be approximated to 0.
# (output for -80p would be 1/1+e^80 approx.  1/(5.54 * 10^34) = 0.000000000... )
sig_prec = 80

# Calculate min and max relative-to-p 
# values upon which an output will be
# approximated based on sig_prec, p
# and a arbitrary constant
# (i.e. if input/p < min_sig_value it'll 
# be rounded to 0)
# (min needs to a be negative value because
# even if output is between 0 and 1, input
# can be negative values [due to weights 
# applied to them])
min_sig_value = -1 * sig_prec
max_sig_value = 1 * sig_prec


# Should we do warnings and rise exceptions?
do_warnings = True

# Self-explanatory
crossover_rate = 0.7
mutation_rate = 0.0001


# A scaling factor for DNA values
dna_factor = 10

# Defines min and max single DNA values
dna_max = 1 * dna_factor
dna_min = -1 * dna_factor

# Default values for neurons by layer
default_1st_layer = 50
default_hidden_layers = 10
default_neurons_by_hidden_layer = 10
default_last_layer = 4

# Here's a variable to limit DNA length:
# TODO: rewrite it
max_genes = 1000

# Defines max and min number of genes
# for a new genome
min_starting_genes = 0.2 * max_genes
max_starting_genes = 0.8 * max_genes

# Defines variables for mutation's processes
min_mutation_length = 1
max_mutation_length = 3
min_mutation_interactions = 1
max_mutation_interactions = 3

# Value of which parameter to use in a tuple, for sorting
sorting_tuple_position = 1

# Set up the tuple's list sorting function
def setTupleSorting(position):
	sorting_tuple_position = position
	return None

# Used with sorted(), it will be called
# to get a value upon which sorts the tuple's list
# example:
# setTupleSorting(1)
# my_unsorted_list = [(1,2),(2,3),(5,1)]
# result = sorted(my_unsorted_list, key= byTuple)
# print(result)
# [(5,1),(1,2),(2,3)]
# It has been sorted by the second (1) element
# (computers count starting at zero)
def byTuple(item):
	return item[sorting_tuple_position]


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
			In this case, it'll smooth neuron's output.
			The sigmoid formula is 1/(1 + e^(-input/p))
		"""

		# p is a indicative of sigmoid' smoothness
		# it's also the value of comparison for
		# approximations (it's useless to represent 
		# almost-1 numbers or almost-0 numbers, because
		# it can raise errors in number representation)
		relative_output = self.output/p

		# calculation of a sigmoid involves division
		# and as it's not allowed to divide by 0 or None
		# so the divider needs to be initialized
		divider = 1

		# If input is reasonable, use it
		if(min_sig_value < relative_output < max_sig_value):
			divider = 1.0 + pow(e, -relative_output)
			self.output = 1/divider

		# otherwise, approximate the output
		elif(relative_output > max_sig_value):
			self.output = 0.0

		elif(relative_output < min_sig_value):
			self.output = 1.0

		return None


	def doOutput(self):
		""" Calculate a neuron's output and return it """

		# We start with a zeroed output
		self.output = 0.0

		# Each input, already multiplied by its weight
		# Is summed up to the output
		for input in self.inputs:
			self.output = self.output + input

		# The value is compared to the bias
		self.output = self.output - self.bias

		# And smoothed
		self.doSigmoid()

		# Clean the inputs for reuse
		self.inputs = []

		# Clean the index for reuse
		self.index = 0
		
		return self.output


	def addInput(self, input, warning = do_warnings):
		""" Add an input to the neuron (circular) """

		try:
			# We multiply the input by a respective weight
			input = input * self.weights[self.index]

		# Sometimes there's more inputs than weights
		except IndexError:

			# We can raise a exception OR silently do it
			if(warning):
				raise TooMuchInputs("Attempt to add more inputs" 
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
		self.neurons = []
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

		# Now we reset self.index for new 
		# use with new inputs
		self.index = 0

		return self.outputs

	def addInput(self, value, neuron_number = None):
		""" Add a input to a neuron """

		# If neuron_number is not provided, use self.index instead
		# (for finding a correct neuron to add input)
		if (neuron_number != 0) and (neuron_number is None):
			# We want a neuron we didn't use yet (this time,
			# because we can use neurons in a circular way)
			self.index = self.index + 1
			neuron_number = self.index

		# Verifies if neuron_number is a valid neuron
		if neuron_number < len(self.neurons):
			pass

		# If it isn't, try to rise a exception
		elif do_warnings:
			raise TooMuchInputs(" Attempted to add a input to a non-existing neuron inside a layer. Maybe you should reset layer.index to neuron 0? (layer.index = 0)")
		
		# But don't rise it if we should silently ignore it
		else:
			neuron_number = neuron_number % len(self.neurons)

		self.neurons[self.index].addInput(value)

		# Our job here is done
		return None

	def addInputList(self, inputs):
		""" Add a inputs for the neurons """

		# Check if inputs is a viable list of values for ALL neurons

		# If it is possible to complete assigns inputs to all neurons 
		# without any input left, then it maybe a no-problems input
		# (If it's possible to evenly assign inputs to all neurons, then 
		# the number of inputs must be a multiple of the number of the 
		# neurons i.e. there's a integer k that satisfies the relationship 
		# n_inputs = k * n_neurons )
		# ( Therefore, if n_inputs = k * n_neurons then n_inputs/n_neurons = k, 
		# and if k is a integer there follows that n_inputs/n_neurons should be 
		# integer too, so there's no leftover of the division between n_inputs and
		# n_neurons. The % return the leftover of a division)

		if (len(inputs) % len(self.neurons)) == 0:
			pass

		# Otherwise, it's probably a bad input and we should rise a exception
		elif do_warnings:
			raise TooMuchInputs("Attempted to add a non-compatible list of inputs to a layer. Number of inputs and number of neurons differs.")

		# We can ignore if it's configured to, but some neurons will got more inputs than others
		else:
			pass

		# For each input inside the inputs list:
		for input in range(len(inputs)):
			# We find a suitable neuron for that input
			correspondent_neuron = input%len(self.neurons)

			self.neurons[correspondent_neuron].addInput(inputs[input])

		
		return None


	def addInputDistributed(self, list):
		""" Add a list with inputs for all neurons. 
		Useful in deeply connected networks """

		# For each neuron in layer's neuron...
		for neuron in self.neurons:
			# We add the inputs given
			for value in list:
				neuron.addInput(value)

		# That's all
		return None
		

class genome:
	""" Implements a genome (DNA) """

	# A variable that controls genome numbering,
	# so every instance of genome has a unique id.
	# It changes every time a new genome is created
	genome_id = 0

	def __init__(self):
		""" Randomly generates a new DNA """

		# We refresh the random function
		# (it's not necessary, but can be useful)
		seed()

		# Initializes genome's DNA
		self.dna = []

		# Index for providing next DNA's value
		self.index = 0

		# Randomize a suitable number of genes
		number_of_genes = randint(min_starting_genes, max_starting_genes)

		# Attach each gene to the DNA
		for genes in range(number_of_genes):
			self.dna.append(self.newGene())


		# Find a suitable name for the new genome
		genome.genome_id = genome.genome_id + 1

		# And assigns it to the new-born genome
		self.id = genome.genome_id

		# Formats the id to a friendly-name to future print() calls
		self.name = "{:0>8X}".format(genome.genome_id)

		# We're done here
		return None

	def newGene(self = None):
		""" Creates (and returns) a random gene """

		gene = uniform(dna_min,dna_max)
		return gene

	def getGene(self):
		""" Returns the next gene (in a float number form) in the DNA """
		
		# If everything fails, we have a value to return
		gene = 0

		# We try to access the next gene
		try:
			gene = self.dna[self.index]

		# If we can't, we raise a error
		except IndexError:

			# ... but only if we should
			if do_warnings:
				raise GeneInexistent("Attempted to access a inexistent gene (self.index >= len(self.dna))")

			# Otherwise, we restart from the very beginning of DNA
			else:
				self.index = 0
				try:
					gene = self.dna[self.index]
				
				# We can have a error if there's no first item on the DNA
				except IndexError:
					colorize("Fatal error while getting dna from {}:"
						     " there's no self.dna[0]. Adding "
						     "random.".format(self.name).upper(), 
						     Fore.RED)

					# So we generate a random gene for it
					gene = genome.newGene()
					self.dna.append(gene)

		# The index needs to point to the next gene
		self.index = self.index + 1

		# Return our work
		return gene

	def crossover(genome_a, genome_b):
		""" Do a genetic crossover between two genome """

		# If a random number between 0 and 1 is
		# bigger than the crossover_rate then
		# we're on the not-crossovered side
		# so there's nothing to do
		if random() > crossover_rate:
			return None

		# See the dna's length of each genome
		# We'll need this to find the smaller
		# genome and find a valid point to do
		# the crossover (any place inside the
		# smaller genome should be a valid point)
		size_dna_a = len(genome_a.dna)
		size_dna_b = len(genome_b.dna)

		# Discover which dna is bigger
		# If size of dna a is bigger than b
		# then it must be the bigger genome
		if size_dna_a > size_dna_b:
			bigger_dna = genome_a.dna
			smaller_dna = genome_b.dna
		
		# Otherwise, if dna a is shorter than b
		# then it must be the smaller genome
		else:
			bigger_dna = genome_b.dna
			smaller_dna = genome_a.dna

		# We take the size of the smaller genome...
		size_smaller_dna = len(smaller_dna)

		# Find a point between 0 and (size of smaller genome - 1)
		# where the crossover will occur
		crossover_point = randrange(0, size_smaller_dna)

		# The first half of each genome is untouched
		# (:crossover_point starts on the list's beginning)
		new_bigger_dna = bigger_dna[:crossover_point]
		new_smaller_dna = smaller_dna[:crossover_point]

		# We append the second half, but swapped
		# (crossover_point: ends on the list's end)
		new_bigger_dna += smaller_dna[crossover_point:]
		new_smaller_dna += bigger_dna[crossover_point:]

		# Now the originals genomes is rewrote
		bigger_dna = new_bigger_dna
		smaller_dna = new_smaller_dna

		# Now we make sure each genome don't break
		# the rules about DNA length
		genome_a.cutExcess()
		genome_b.cutExcess()

		return None

	def mutate(self):
		""" Do mutations in a genome """

		# For each gene inside the dna, we test
		# (computers counts starting at 0)
		for index in range(len(self.dna)-1):

			# If the gene was lucky enough to get mutated
			# (we should be on the mutated side of the random)
			if random() < mutation_rate:
				# Choses a random mutation
				mutation_type = choice([genome.substitutingMutation,
										genome.insertingMutation,
										genome.deletingMutation,
										genome.copyMutation])

				# Sometimes a IndexError can happen
				try:
					# Do the mutation selected
					mutation_type(self, index)
				# We give it a treatment like any other error
				except IndexError:
					if do_warnings:
						raise GeneInexistent("A error occurred while doing a muta"
										 "tion at position {} in a DNA with " 
										 "{} genes in mutation type {}".format(index, 
										 	len(self.dna), mutation_type))
					else:
						pass

		# Guarantees we don't overpass the limits
		self.cutExcess()

		# We are done
		return None


	def substitutingMutation(self, index):
		""" Implements a simple substitute mutation """
		# Substitutes the given gene by a new one
		if index < len(self.dna):
			self.dna[index] = genome.newGene()
		elif do_warnings:
			raise GeneInexistent("Attempted to access gene {}"
				" from a len(self.dna) equals to {}".format(index, len(self.dna)))
		return None

	def insertingMutation(self, index):
		""" Inserts a random gene at self.dna[index] """
		self.dna.insert(index, genome.newGene())
		return None

	def deletingMutation(self, index):
		""" Delete gene at self.dna[index] """
		self.dna.pop(index)
		return None

	def copyMutation(self, index):
		""" Replicate a block of genes at dna[index] """

		# Give a proper name to the variable
		dna = self.dna

		# Get a valid random value for the length of the mutation 
		length = randint(min_mutation_length - 1, max_mutation_length)

		# Get a number of times to repeat the paste process
		interactions = randint(min_mutation_interactions - 1, max_mutation_interactions)

		# Calculate where would be the end of dna snippet
		# to copy
		final_index = index + length

		# If final_index is inside the range 0-len(dna)
		# then it should be a valid index and we could
		# use it to get a dna snippet
		if final_index < len(dna):
			dna_snippet = dna[index:final_index]
		# Otherwise, we should use index - length instead,
		# because we're near the end of dna's list
		else:
			start_index = index - length
			dna_snippet = dna[start_index:index]

		# We inset the dna_snippet where index is 
		# a couple of times
		for value in range(interactions):
			dna[index:index] = dna_snippet

		# And we're done
		return None

	def clone(self):
		""" Returns a copy of this genome """
	
		# First we generate a random genome
		new_genome = self.__class__()

		# Then we it's dna
		new_genome.dna.clear()

		# Substitute it by ours dna
		new_genome.dna += self.dna

		# And returns it
		return new_genome

	def cutExcess(self):
		""" Limits the dna's size """

		number_of_genes = len(self.dna)

		# If the number of genes is greater
		# than the allowed...
		if number_of_genes > max_genes:

			# Cut it off
			del self.dna[max_genes:]

		return None

	def clear(self):
		""" Resets the index to reuse the genome """

		self.index = 0
		return None

	def reset(self):
		self.clear()

	def showInfo(self):
		""" Print/return DNA's statistics """

		# A dictionary to hold (gene, number of occurrences) values
		genes_info = {}

		# For each gene we count how many times it happens
		for gene in self.dna:
			genes_info[gene] = genes_info.setdefault(gene, 0) + 1

		# Transforms the genes_info dict in a 
		# list of (key,value)
		genes_info = genes_info.items()

		# Set a key to use with sorted()
		# specific to sort tuples by second (1) value
		setTupleSorting(1)

		# Now genes_info will contains all the pairs 
		# (key,value) but sorted by value and starting by
		# the greatest value (of value)
		genes_info = sorted(genes_info, key = byTuple, reverse = True)

		# Now we prepare the information for printing
		# First print out a heading with name of sample
		heading = colorize("\n\n\t   Genes in the sample ", Fore.WHITE, do_printing = False)
		heading = heading + colorize(self.name, Fore.YELLOW, Back.BLUE, do_printing = False)

		# Then print it out
		colorize(heading, "")

		# And print a separating line
		colorize( "\t" + "-"*32, Fore.WHITE, Back.WHITE)
		print("\n")

		# Calculate how many different genes we have
		gene_variety = len(genes_info)

		# Print it
		colorize( "\t Number of different gene types: " +
				   str(gene_variety), Fore.WHITE)

		# Name the colors
		red = colorize("RED", Fore.RED, do_printing = False)
		cyan = colorize("CYAN", Fore.CYAN, do_printing = False)
		green = colorize("GREEN", Fore.GREEN, do_printing = False)

		# Print a ""information box""/caption/subtitle
		colorize("\t *"+ red + " percentages are genes with a occurrence above 20%")
		colorize("\t *"+ cyan + " percentages are genes with a occurrence > 5%")
		colorize("\t *"+ green + " percentages are almost-no-repetitive genes")

		# Print a blank line
		print()

		# Defines a blank line
		blank_line = colorize("\t |" + "-"*15  + "|" + "-"*10 + "|" + "-"*10 + "|", Fore.WHITE, do_printing = False)

		# Print a blank (column) line
		colorize(blank_line, "")

		# The column's names
		gene_text = "GENE"
		perc_text = "PERC.%"
		amount_text = "OCCUR."

		# Each column's way of formating
		format_gene_col = " {:^ 12.10f} "
		format_perc_col = " {:>8.4%} "
		format_occur_col = " {:.>8} "

		# Print out column names
		colorize("\t | {: ^13} | {: ^8} | {: ^8} |"
				 .format(gene_text, perc_text, amount_text), Fore.WHITE)
		
		# Print a blank line
		colorize(blank_line, "")

		# DNA's length will be useful for statistics
		total_genes = len(self.dna)

		# For each gene, print a entry
		for info in genes_info:
			gene, occurrences = info
			percentage = occurrences/total_genes

			# Starts the string to be printed as a entry
			entry = colorize("\t |",Fore.WHITE, do_printing = False)

			# Defines a column separator (as above)
			separator = colorize("|", Fore.WHITE, do_printing = False)

			# Put colors at the first column
			# And add it to be printed
			entry += colorize(format_gene_col.format(gene),
							   Fore.MAGENTA, do_printing = False) + separator

			# Chooses a suitable color for the percentage
			if percentage > 20:
				percentage_color = Fore.RED
			elif percentage > 5:
				percentage_color = Fore.CYAN
			else:
				percentage_color= Fore.GREEN

			# Colorize the percentage
			entry += colorize(format_perc_col.format(percentage),
					  percentage_color, do_printing = False) + separator
			
			# Write the number of occurrences
			entry += colorize(format_occur_col.format(occurrences),
							  Fore.YELLOW, do_printing = False) + separator

			# Print the string as an entry
			colorize(entry)

		# Print a couple of blank lines
		colorize(blank_line, "")
		print("\n\n")

		return total_genes, genes_info

class network:
	""" Implements a neural network """

	def __init__(self, first_layer_neurons = default_1st_layer,
				 hidden_layers = default_hidden_layers,
				 hidden_layer_neurons = default_neurons_by_hidden_layer,
				 last_layer = default_last_layer):

		# Number of total layers to be created
		number_of_layers = 1 + hidden_layers + 1

		# Since this values can change between networks
		# and are relevant to the software's logic, it's
		# saved
		self.first_layer_neurons = first_layer_neurons
		self.hidden_layers = hidden_layers
		self.hidden_layer_neurons = hidden_layer_neurons
		self.last_layer = last_layer

		# For adding inputs, there's a index
		self.index = 0

		# And a output
		self.output = 0

		# Layers' list
		self.layers = []

		# Creates the layers
		for i in range(number_of_layers):
			self.layers += [layer()]

		# Adds neurons to the first layer
		for i in range(self.first_layer_neurons):
			self.layers[0].addNeuron(neuron())

		# Adds neurons to the hidden layers
		for hidden_layer in self.layers[1:hidden_layers+1]:
			for i in range(hidden_layer_neurons):
				hidden_layer.addNeuron(neuron())

		# Adds neurons to the last layer
		for i in range(self.last_layer):
			self.layers[-1].addNeuron(neuron())


	def readGenome(self, Genome):
		# This method is close-related to the
		# doOutput() function, because the two
		# need to use the same standard for
		# how to connect a neuron input with other
		# neuron output (which is completely arbitrate)

		# We can run out of genes anytime, so
		# it's wrapped inside a try block
		try:
			# In the first layer is a neuron for each input
			# In the system, so there's only one weight
			for Neuron in self.layers[0].neurons:
				Neuron.bias = Genome.getGene()
				Neuron.addWeight(Genome.getGene())

			# The first hidden layer's neurons receive
			# the output from the first layer, so there
			# is a weight for each output (or neuron) 
			# of the first layer
			for Neuron in self.layers[1].neurons:
				Neuron.bias = Genome.getGene()
				for i in range(len(self.layers[0].neurons)):
					Neuron.addWeight(Genome.getGene())

			# The other layers receive input from the previous
			# layer, and since the previous layers is a hidden layer
			# that have neurons_by_hidden outputs (one for each neuron)
			# we'll have that amount of input
			for hiddenLayer in self.layers[2:]:
				for Neuron in hiddenLayer.neurons:
					Neuron.bias = Genome.getGene()
					for i in range(self.hidden_layer_neurons):
						Neuron.addWeight(Genome.getGene())



		except GeneInexistent:
			raise InsufficientGenes("There aren't enough genes to fulfill the network")

	def doOutput(self):

		# We first clear the output
		self.output = None

		# Do the output of the first layer
		self.output = self.layers[0].doOutput()

		# And pass it to the next in the chain
		for Layer in self.layers[1:]:
			Layer.addInputList(self.output)
			self.output = Layer.doOutput()

		# After the last one did it output, we're done
		return self.output

	def addInput(self,input):

		try:
			self.layers[0].neurons[self.index].addInput(input)
		except IndexError:
			raise TooMuchInputs("Attempted to add a input to a network,"
				" but it's inputs are already full")
		except TooMuchInputs:
			raise NetworkNotInitialized("Attempted to add inputs to a network "
				"without weights. Use network.readGenome(self, genome) first.")

		self.index += 1

		return None

	def clear(self):
		self.reset()

	def reset(self):
		self.index = 0

		return None










class NetworkNotInitialized(Exception):
	pass

class InsufficientGenes(Exception):
	pass

class GeneInexistent(Exception):
	pass	

class TooMuchInputs(Exception):
	pass

