from sys import *
from color import *
from neural import *
from filter import *
from web import *

from random import *

def random_string(length = 50):
	""" Creates random strings"""

	# Starts with a random string
	string = ""

	# Give "lenght" random characters 
	for i in range(length):
		string += str(randint(0,9))

	# And that's it
	return string

def random_fore():
	""" Returns a random fore color """

	return   choice([Fore.BLACK, Fore.RED, Fore.GREEN,
					 Fore.YELLOW, Fore.BLUE, Fore.MAGENTA,
					 Fore.CYAN, Fore.WHITE])

def random_back():
	""" Returns a random back color """

	return choice([Back.BLACK, Back.RED, Back.GREEN,
			   	   Back.YELLOW, Back.BLUE, Back.MAGENTA,
				   Back.CYAN, Back.WHITE])

def random_style():
	""" Returns a random style for text """
	
	return choice([Style.DIM, Style.NORMAL, Style.BRIGHT])

def random_color():
	""" Generates a random formating for text """

	return random_back() + random_fore() + random_style()

def test_color(testing_times = 300, size = 50):
	print("\n\t Testing colorize method:\n\n")

	# String which will be big
	big_string = ""

	# Test for strings
	for i in range(testing_times):
		print("\n\t\t Testing {}:".format(i))

		# Starts a empty string
		string = "\t\t"

		# Randomize a string
		string += random_string(size)

		print("\n\t String: {}\n".format(string))

		# And use it
		colorize(string, random_color())

		# And add the string to the big string
		big_string += colorize(string, random_color(), do_printing = False)

	print("\n\t Big string: {}\n".format(big_string))

	# Test for the BIG string
	colorize(big_string)


	print("\n\t Testing colorChoice method:\n\n")

	for i in range(testing_times):
		print("\n\t\t Testing {}:".format(i))

		# Generates a random string with size lenght
		string = "\n\t\t" + random_string(size)

		# Get two randoms colors to use
		random_color_a = random_color()
		random_color_b = random_color()

		# Two randoms numbers
		random_a = random()
		random_b = random()

		print("\n\t String: {}\n\t Color A: {}"
			  "\n\t Color B: {}\n\t A: {}\n\t B: {}\n\n".format(
			  	string, random_color_a, random_color_b, random_a, random_b))

		# And use colorChoice on them
		colorChoice(string, random_a < random_b, random_color_a, random_color_b)

	return None


def test_neural(testing_times = 50, size = 50):

	#### Tests the neurons
	print("\n\t Testing neurons: ")

	for test in range(testing_times):
	
		print("\n\t\t Testing {}:".format(test))

		# Get a random neuron
		test_neuron = neuron()

		# Give it some inputs & weights
		inputs = randint(0,size)
		for input in range(0,inputs):

			#Generate random input and weight
			weight = random()
			neuron_input = random()

			print("\n\t\t\t Weight: {}\n\t\t\t Input: {}".format(
				weight, neuron_input))

			# And assign it with the neuron
			test_neuron.addWeight(weight)
			test_neuron.addInput(neuron_input)

		# Do the neuron's output and print it to the user
		print("\n\t\t\t Output: {}".format( test_neuron.doOutput()) )

	#### Tests the layers	
	print("\n\t Testing layers: ")

	for test in range(testing_times):

		print("\n\t\t Testing {}:".format(test))

		# Generate a random layer
		test_layer = layer()

		number_of_neurons = randint(0, size)
		
		# And give it some neurons
		
		for i in range(number_of_neurons):
			# Assign  a random neuron to the layer
			test_layer.addNeuron(neuron())

		# This is for the output don't be filled up
		# with "Testing n: \n Testing n+1", so now
		# we have a "Done." between testings :)
		print("\n\t\t\t Done.")
		

	#### Test the methods

	# As above, creates a random layer
	test_layer = layer()

	# With a random number of neurons
	number_of_neurons = randint(0,size)
	for i in range(number_of_neurons):

		# Create a random neuron
		randomNeuron = neuron()

		# And assign "size" randoms inputs to it
		for j in range(size):
			randomNeuron.addWeight(random())
		test_layer.addNeuron(randomNeuron)

	# (It's to be used in other tests)


	#### Test addInput()
	print("\n\t Testing layer.addInput() :")

	for i in range(testing_times):
		print("\n\t\t Testing {}:".format(i))

		# This second for loop is need
		# Since we can accidentaly try do add a input
		# for a inexisting neuron
		for test_neuron in range(number_of_neurons):

			print("\n\t\t\t Adding input to neuron {}:".format(
				  test_neuron))

			# Add inputs to a neuron
			test_layer.addInput(random(), test_neuron)

		# Do the output to reuse the neurons/layer
		print("\n\t\t Output: ".format(test_layer.doOutput()))


	#### Test addInputList()
	print("\n\t Testing layer.addInputList() :")

	for i in range(testing_times):
		print("\n\t\t Testing {}:".format(i))
		

		# Generate a random list at a perfectly size for
		# the neuron's layer
		input_list = []

		# By perfectly size we mean a size where there's no
		# neuron with less inputs than other
		list_size = randint(0,size) * number_of_neurons
		for j in range(list_size):
			input_list += [random()]

		# And print out to the user the input_list
		# And other info
		print("\n\t\t Input_list: {}".format(input_list))
		print("\n\t\t list_size: {}\n\t\t number of neurons :{}".format(
			  list_size, number_of_neurons))
		print("\n\t\t Ratio: ".format(list_size/number_of_neurons))
		test_layer.addInputList(input_list)

		print("\n\t\t output: {}".format(test_layer.doOutput()))



	#### Test addInputDistributed()
	print("\n\t Testing layer.addInputDistributed() :")

	for i in range(testing_times):
		print("\n\t\t Testing {}:".format(i))

		# We generate a random list
		input_list = []

		for j in range(randint(0,number_of_neurons)):
			input_list += [random()]

		# And add it
		test_layer.addInputDistributed(input_list)
		test_layer.doOutput()
	

	print("\n\t Single testing layer.doOutput:")
	
	for i in range(testing_times):
		print("\n\t\t layer.doOutput(): {}".format(test_layer.doOutput()))

	# genome's test

	#### Testing getGene()
	print("\n\t Testing getGene(): ")

	for test in range(testing_times):
		print("\n\t\t Testing {}:".format(test))
		
		# Get a random genome to test
		test_genome = genome()

		for i in range(int(random()+1) * max_genes):
			
			# It's not guaranteed we're inside the gene length
			# so we need to be alert to the exceptions
			try:
				gene = test_genome.getGene()
			except GeneInexistent:
				test_genome.index = 0
				gene = test_genome.getGene()

			print("\n\t\t Gene {}: {}".format(i, gene))



	#### Testing crossover()

	print( "\n\t Testing crossover():" )

	testing = 0

	while testing <= testing_times:
		print("\n\t\t Testing {}:".format(test))

		# Random genomes
		genome_a = genome()
		genome_b = genome()

		# Create a copy to compare so we'll
		# know if it has changed
		before_a = genome_a.clone()

		# String with info about them before
		# The parenthesis is to not raise a unexpected indent
		before = ("\n\t\t\t Before: \n\t\t\t\t {}: {}"
			"\n\t\t\t\t {}: {}".format(genome_a.name, genome_a.dna,
			  genome_b.name, genome_b.dna))

		# Crossover the two
		genome_a.crossover(genome_b)

		# String with info about them after
		after = ("\n\t\t\t After: \n\t\t\t\t {}: {}"
			"\n\t\t\t\t {}: {}".format(genome_a.name, genome_a.dna,
			  genome_b.name, genome_b.dna))

		# If the dna has changed, show it
		if before_a.dna != genome_a.dna:
			print(before)
			print(after)

		testing += 1



	#### Testing mutate()
	print("\n\t Testing mutate():")

	testing = 0

	while testing <= testing_times:
		print("\n\t\t Testing {}:".format(testing))

		test_genome = genome()
		before_genome = test_genome.clone()

		before_string = "\n\t\t\t Before: \n\t\t\t\t {}".format(test_genome.dna)

		test_genome.mutate()

		after_string = "\n\t\t\t After: \n\t\t\t\t {}".format(test_genome.dna)

		if before_genome.dna != test_genome.dna:
			print(before_string)
			print(after_string)
			testing += 1


	##### Tests networks creation

	print("\n\t Testing network():")
	for i in range(testing_times):
		print("\n\t\t Testing nº {}".format(i))
		new_network = network()

	#### Tests readGenome()
	print("\n\t Testing readGenome():")

	for i in range(testing_times):
		print("\n\t\t Testing nº {}".format(i))
		test_network = network()
		try:
			test_network.readGenome(genome())
		except InsufficientGenes:
			print("\n\t\t\t InsufficientGenes rose")

	#### Tests addInput and doOutput
	print("\n\t Testing addInput() and doOutput():")
	for i in range(testing_times):
		
		print("\n\t\t Testing nº. {}".format(i))
		
		inputs = randint(1,size)

		test_network = network(inputs)

		try:
			test_network.readGenome(genome())
		
		except InsufficientGenes:
			print("\n\t\t\t InsufficientGenes rose")

			new_genome = genome()
			for i in range(size):
				new_genome.dna += genome().dna
			new_genome.dna += [3]*1000
			test_network.readGenome(new_genome)

		for i in range(inputs + randint(0,2)):
			try:
				test_network.addInput(uniform(-10,10))
			except TooMuchInputs:
				print("\n\t\t\t TooMuchInputs rose")

def test_filter(number_of_tests = 50):
	print("\n\t Testing filter.py:")
	
	# Opens a image for altering
	image = Image.open("test.jpeg")

	for i in range(number_of_tests):
		print("\n\t\t Testing nº {}".format(i))
		
		filter = [random(), random(), random(),
			  random(), random(), random(),
			  random(), random(), random()]


		# Resize the filter
		for value in filter:
			value = value * 5

		x_size,y_size = image.size
		
		print("\n\t\t\t Size: {}".format(image.size))

		# If we're done with the image, restarts
		if (x_size < 2) and (y_size < 2):
			image = Image.open("test.jpeg")

		# Otherwise, apply the filter
		else:
			image = applyFilter(image, filter)
		
			

			




def print_usage():
	print("\n\t Usage: {} times_to_test_color.py "
		"[times_to_test_neural.py] [times_to_test_web.py]\n".format(argv[0]))


### Main flow of testing

# Get the first number test
try:
	color_testing_times = int(argv[1])

# This exceptions is rose when there's no
# second argument
except IndexError:
	
	# Prints the correct usage for the user
	print_usage()

	# Rerise exception to stop the program
	raise Exception("Incorrect usage")

# Get the second number test
try:
	neural_testing_times = int(argv[2])

# If it's not given, then use the same as
# number of testing used to test colors
except IndexError:
	neural_testing_times = color_testing_times

# Get the third number test
try:
	filter_testing_times = int(argv[3])
# If there's none, use the previous
except IndexError:
	filter_testing_times = neural_testing_times


test_color(color_testing_times)
test_neural(neural_testing_times)
test_filter(filter_testing_times)