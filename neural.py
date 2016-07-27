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

# Initialize colorama, important for windows
init()

# Start a seed for the randoms functions
seed()

# p is a sigmoid variable. It's a measure of the sigmoid' smoothness result.
# Higher p indicates a homogeneous function
p = 1.0

# How precise a neuron's output is. Default value is 80, so if
# output is greater than 80p it will be approximated to 1.
# If it's less than -80p it'll be approximated to -1.
sig_prec = 80


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



