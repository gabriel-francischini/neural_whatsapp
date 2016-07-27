#!/usr/bin/python
# -*- coding: utf-8
from random import *
from graphics import *
from decimal import Decimal, localcontext
from math import *
from time import *
from color import *
from filter import *
from colorama import *
init()

seed()

gen_number = 0

# p é um valor de ajuste na sigmóide, representa a "régua" que usamos para 
# medir o valor de saída para saber se ele está muito alto ou baixo, influenci-
# ando no quão grande é faixa e a suavidade que a sigmóide abrange
p = 1.0

# O quão grande/pequeno a saída de um neurônio precisa ser em relação a p
# para que passemos a aproximar a saída
sig_prec = 80

crossover_rate = 0.7
mutation_rate = 0.0001

# Contêm a magnitude máxima dos valores no DNA
mult_all = 10

fix_first_layer = 50
fix_hidden_layers = 10
fix_neurons_by_hidden = 10
fix_last_layer = 4

# Impede que um gene tenha tamanho infinito
max_genes = int(((fix_first_layer + fix_neurons_by_hidden*fix_first_layer + (fix_hidden_layers - 1 + fix_last_layer)*(fix_neurons_by_hidden) + fix_first_layer + fix_hidden_layers*fix_neurons_by_hidden + fix_last_layer) + palette_size*filter_size + recipe_size*round(log(recipe_size,10)))*1.05 +1)

class neuron:
	"""Essa classe implementa um neurônio
	
	Atributos:
		entradas -- lista com as entradas
		pesos -- lista com os pesoas respectivos a cada entrada
		saida -- resultado da saída
		bias -- valor de ativação do neurônio
	"""
	
	def __init__(self,nbias = 0.0):
		""" Inicia os atributos do neurônio"""
		
		self.entradas = []
		self.pesos = []
		self.indice = 0
	
		# A saída deve sempre ter um resultado válido
		self.saida = 0.0
		
		# Bias é o valor mínimo para um sinal positivo
		self.bias = nbias 	
	
	def sigmoid(self):
		""" Calcula e retorna a sigmóide usando a self.saida 
		Torna a curva de ativação mais suave.
		"""
		
		# Não é possível dividir por zero
		lower_part = 1
	
			
		# p representa o quão grande é a faixa de valores de saída possíveis
		# por examplo, quando self.saida = 4p a diferença entre a sigmóide
		# e 1 (ou -1) é de apx. 0.2
		if(-sig_prec < (self.saida/p) < sig_prec ):
			lower_part = 1.0 + pow(e,(-self.saida/p))
		
		# Arredonda para evitar problemas de memória
		elif((self.saida/p) > sig_prec):
			return 0.0
		elif((self.saida/p) < -sig_prec):
			return 1.0
		
		# Termina a sigmóide e a ajusta para assimilar-se a um
		# gene qualquer
		result = 1.0 / lower_part
		self.saida = result * mult_all
		
		return self.saida
	
	
	def resultado(self):
		""" Calcula a saída de um nerônio e a retorna"""
	
		self.saida = 0.0
		
		for input in self.entradas:
			self.saida = self.saida + input
		
		# Para que o neurônio exprima uma saída alta,
		#	o valor dos pesos*entradas devem ser maiores que o bias
		self.saida = self.saida - self.bias
	
		return self.sigmoid()
		
		
	def addInput(self, input):
		""" Adiciona uma entrada ao neurônio"""
		
		novaEntrada = 0
		
		# Adiciona a entrada como uma saída parcial,
		# usando os pesos de forma circular
		try:
			novaEntrada = input*(self.pesos[self.indice])
		except IndexError:
			try:
				self.indice = 0
				novaEntrada = input*(self.pesos[self.indice])
			except IndexError:
				novaEntrada = input*1
				
		self.entradas.append(novaEntrada)
		return self
		
	def clear(self):
		""" Limpa as entradas para reutilização. Afeta as estatísticas"""
		
		self.entradas.clear()
		self.saida = 0.0
		return self
		
	def addPeso(self,peso):
		""" Adiciona um peso que será usado no neurônio"""
		
		self.pesos.append(peso)
		return self
	
class layer:
	""" Uma camada de neurônios
	Atributos:
		neuronios -- lista de neurônios
		saidas -- lista com as saídas de cada neurônio
	"""
	
	def __init__(self):
		""" Inicia os atributos"""
		
		self.neuronios = []
		self.saidas = []
	
	def addNeuron(self, neuronio):
		""" Inclui o neurônio à lista neuronios"""
	
		self.neuronios.append(neuronio)
		return self
		
	def doOutput(self):
		""" Calcula a saída da camada"""
		
		temp_output = []
		
		for neuronio in self.neuronios:
			temp_output.append(neuronio.resultado())
		
		self.saidas = temp_output
		return self.saidas
		
	def takeInput(self, list):
		"""Adiciona uma entrada geral para os neurônios da camada"""
		
		for neuronio in self.neuronios:
			for value in list:
				neuronio.addInput(value)
		return self
		
	def clear(self):
		""" Retorna cada neurônio da camada ao seu estado original"""
	
		for neuronio in self.neuronios:
			neuronio.clear()
		self.saidas.clear()
		return self
				
class genome:
	""" Implementa um conjunto genômico (DNA) """

	def __init__(self):
		""" Cria aleatóriamente um DNA"""
		
		seed()
		
		global gen_number
		
		self.dna = []
		self.indice = 0
		for i in range(randint(9,100)):
			self.dna.append(genome.newGene())
		self.name = gen_number
		gen_number = gen_number + 1
		
	def getGene(self):
		""" Retorna o próximo gene (float) presente no DNA"""
		
		gene = 0
		try:
			gene = self.dna[self.indice]
		except IndexError:
			try:
				self.indice = 0
				gene = self.dna[self.indice]
			except IndexError:
				print(Fore.RED + "\n Erro no genoma {:0>8X}".format(self.name), 
				": Não há primeiro gene em genome.dna[0], adicionando aleatório" + Fore.RESET)
				gene = genome.newGene()
				self.dna.append(gene)
				
		self.indice = self.indice + 1
		return gene
	
	def newGene(self = None):
		""" Cria um gene aleatório"""
	
		return uniform(-1*mult_all,1*mult_all)
	
	def crossover(genome_a, genome_b):
		""" Realiza a troca gênica entre duas moléculas de DNA (indivíduos)"""

		if(random() > crossover_rate):
			return self
					
		maior = 0
		menor = 0
		
		if(len(genome_a.dna) > len(genome_b.dna)):
			maior = genome_a
			menor = genome_b
		else:
			maior = genome_b
			menor = genome_a
			
		pos = randrange(0, len(menor.dna))
		mmaior = maior.dna[:pos]
		mmenor = menor.dna[:pos]
		
		mmaior.extend(menor.dna[pos:])
		mmenor.extend(maior.dna[pos:])
		
		maior.dna = mmaior
		menor.dna = mmenor
		
		genome_a.sumarize()
		genome_b.sumarize()
		return self
		
		
	def mutation(self):			
		""" Produz probabilisticamente uma mutação em cada gene"""
		
		for i in range(len(self.dna)):
			if(random() < mutation_rate):
				tipo = randint(1,5)
				#print("Mutando na posicão {} de {}, tipo {}".format(i,len(self.dna), tipo))
				#print("Mutação tipo ", tipo, ".")
				try:
					if(tipo == 1):
						self.dna[i] = self.newGene()
					if(tipo == 2):
						self.dna.insert(i, self.newGene())
					if(tipo == 3):
						inutil_sem_uso = self.dna.pop(i)
					if(tipo == 4):
						j = randrange((i-3), (i+3))
						if(j < i):
							self.dna[i:i] = self.dna[j:i]
						else:
							self.dna[i:i] = self.dna[i:j]
					if(tipo == 5):
						tamanho = randint(0,3)
						lista = 0
						if((i+tamanho) >= (len(self.dna))):
							lista = self.dna[i:]
						else:
							lista = self.dna[i:(i+tamanho)]
						b = []	
						for j in range(randint(0,3)):
							b.extend(lista)
						lista.extend(b)
						self.dna[i:i] = lista
				except IndexError:
						print(Fore.RED + 
						"\n\t\tOcorreu um erro de índice ao tentar acessar"
						" o elemento {} de uma dna de tamanho {}"
						.format(i,len(self.dna)) + Fore.RESET)
						
		self.sumarize()
		return self
	
	def clone(self):
		""" Retorna uma cópia desse DNA"""
	
		new_genome = self.__class__()
		new_genome.dna.clear()
		new_genome.dna.extend(self.dna)
		return new_genome
	
	def  sumarize(self):
		""" Corrige se houver mais genes do que o permitido"""
		
		if(len(self.dna) > max_genes):
			del self.dna[max_genes:]
			
		return self
			
			
	def showInfo(self):
		""" Mostra estatísticas dos genes neste DNA"""
		
		dna_len = len(self.dna)
		value = []
		count = []
		
		for gene in self.dna:
			exist = False
			
			for entry in value:
				if(entry == gene):
					count[value.index(entry)] = (count[value.index(entry)] + 1)
					exist = True
			
			if(exist == False):
				value.append(gene)
				count.append(1)
		
		total = len(self.dna)
		print( Fore.WHITE
		          + "\n\n\t   Genes presentes na amostra " 
		          + Fore.RESET
				  + Fore.YELLOW + Back.BLUE 
				  + "{:0>8X}".format(self.name)
				  + Fore.RESET + Back.RESET )
				  
		print( "\t" +Fore.WHITE + Back.WHITE 
		          + "-"*48
				  + Fore.RESET + Back.RESET
				  + "\n" )
		
		sum_percent = 0.0
		while(value != []):
			max = 0
			max_index = 0
			index = 0
			
			for number in count:
				if(number > max):
					max = number
					max_index = index
				index += 1			
			
			max = count.pop(max_index)
			number = value.pop(max_index)
			frac = 100.0*(max/total)
			
			if(frac > 20):
				signal = Fore.RED
			elif(frac > 5):
				signal = Fore.CYAN
			else:
				signal = Fore.GREEN
				
			sum_percent += frac
			
			if(sum_percent <= 80):
				per = Fore.CYAN
			else:
				per = Fore.RED
			
			print("\t " 
					  + Back.RESET + Fore.MAGENTA 
					  + "{:^ 12.10f} ".format(number)
					  + Fore.RESET + Back.RESET,
                      Fore.WHITE + ":"  + Fore.RESET,			
			          signal + "{:>5.2f}".format(frac)
					  + Fore.RESET 
					  + Fore.WHITE 
					  + "%" + Fore.RESET,
					  Fore.WHITE + "("  + Fore.RESET
					  + Fore.YELLOW 
					  + "{:.>3}".format(max)
					  + Fore.RESET +
					  Fore.WHITE + ") "  + Fore.RESET)
		
		print("\n\n")
		return self
							
	def clear(self):
		""" Recomeça a ler o DNA a partir do início"""
		
		self.indice = 0
		return self
		
	
class network:
	""" Implementa uma rede neural e suas funcionalidades"""

	def __init__(self, first = fix_first_layer, hidden = fix_hidden_layers, neurons_by_hidden = fix_neurons_by_hidden, last = fix_last_layer):
		self.nfirst = first
		self.nhidden = hidden
		self.nneurons_by_hidden = neurons_by_hidden
		self.nlast = last
	
		self.firstLayer = layer()
		for i in range(first):
			self.firstLayer.neuronios.append(neuron())
		
		self.firstHidden = layer()
		for i in range(neurons_by_hidden):
			self.firstHidden.neuronios.append(neuron())
		
		self.hiddenLayers = []
		for i in range(hidden-1):
			self.hiddenLayers.append(layer())
			for j in range(neurons_by_hidden):
				self.hiddenLayers[i].neuronios.append(neuron())
				
		self.lastLayer = layer()
		for i in range(last):
			self.lastLayer.neuronios.append(neuron())
			
	def calculate(self):
		output = self.firstLayer.doOutput()
		self.firstHidden.takeInput(output)
		output = self.firstHidden.doOutput()
		
		for i in self.hiddenLayers:
			i.takeInput(output)
			output = i.doOutput()
			
		self.lastLayer.takeInput(output)
		return self.lastLayer.doOutput()
			
	def clear(self):
		self.firstLayer.clear()
		self.firstHidden.clear()
		for i in self.hiddenLayers:
			i.clear()
		self.lastLayer.clear()
		
		return self
		
	def readGenome(self, genoma):
		for neuronio in self.firstLayer.neuronios:
			neuronio.bias = genoma.getGene()
			neuronio.addPeso(genoma.getGene())
			
		for neuronio in self.firstHidden.neuronios:
			neuronio.bias = genoma.getGene()
			for i in range(len(self.firstLayer.neuronios)):
				neuronio.addPeso(genoma.getGene())
		
		for camada in self.hiddenLayers:
			for neuronio in camada.neuronios:
				neuronio.bias = genoma.getGene()
				for i in range(len(camada.neuronios)):
					neuronio.addPeso(genoma.getGene())
					
		for neuronio in self.lastLayer.neuronios:
			neuronio.bias = genoma.getGene()
			for i in range(self.nneurons_by_hidden):
				neuronio.addPeso(genoma.getGene())
				
		return None
				
	def showInfo(self):

		i = 0
		print("\n\n\tCamada visível: ", end='')
		for neuronio in self.firstLayer.neuronios:
			print("\n\t\tNeuronio {:0>3}".format(i), end='')
			print(" bias: " 
					+ color("{:^ 12.10f}".format(neuronio.bias),
								colorChoice(neuronio.bias>0))
					, end='')
			
			print("    pesos: ", end='')
			for peso in neuronio.pesos:
				print(color("   {:^ 12.10f}".format(peso),
						  colorChoice(peso > 0)), end='')
			i = i + 1
		
		i = 0
		j = 1
		print("\n\n\tCamada oculta 01: ", end='')
		for neuronio in self.firstHidden.neuronios:
			print("\n\t\tNeuronio {:0>3}".format(i), end='')
			print(" bias: " 
					 + color("{:^ 12.10f}".format(neuronio.bias),
								colorChoice(neuronio.bias >0)), 
					 end='')
					 
			print("    pesos: ", end='')
			for peso in neuronio.pesos:
				print(color("   {:^ 12.10f}".format(peso),
						  colorChoice(peso>0)), end='')
			i = i + 1
		
		for camada in self.hiddenLayers:
			j = j + 1
			i = 0
			print("\n\n\tCamada oculta {:0>2}".format(j),": ", end='')
			for neuronio in camada.neuronios:
				print("\n\t\tNeuronio {:0>3}".format(i), end='')
				print(" bias: " 
						 + color("{:^ 12.10f}".format(neuronio.bias),
									 colorChoice(neuronio.bias > 0)), 
						 end='')
				
				print("    pesos: ", end='')
				for peso in neuronio.pesos:
					print(color("   {:^ 12.10f}".format(peso),
									  colorChoice(peso>0)), 
							  end='')
				i = i + 1
		
		i = 0
		print("\n\n\tCamada final: ", end='')		
		for neuronio in self.lastLayer.neuronios:
			print("\n\t\tNeuronio {:0>3}".format(i), end='')
			print(" bias:" 
					 + color("{:^ 12.10f}".format(neuronio.bias),
								 colorChoice(neuronio.bias>0)),
					 end='')
			
			print("    pesos: ", end='')
			for peso in neuronio.pesos:
				print(color("   {:^ 12.10f}".format(peso),
								  colorChoice(peso>0)), 
						  end='')
			i = i + 1
			
		print("\n")
		
		return None
		
	def showStats(self):
	
		i = 0
		print("\n\n\tCamada visível: ", end='')
		for neuronio in self.firstLayer.neuronios:
			print("\n\t\tNeuronio {:0>3}".format(i), end='')
			print(" saída: " 
					 +  colorGen("{:> 17.10f}".format(neuronio.saida)
										,neuronio.saida), 
					end='')
			
			print("    entradas: ", end='')
			for entrada in neuronio.entradas:
				print(colorGen("   {:> 15.10f}".format(entrada),entrada), 
						 end='')
			i = i + 1
		
		i = 0
		j = 1
		print("\n\n\tCamada oculta 01: ", end='')
		for neuronio in self.firstHidden.neuronios:
			print("\n\t\tNeuronio {:0>3}".format(i), end='')
			print(" saída: " 
					 + colorGen("{:> 17.10f}".format(neuronio.saida)
									   , neuronio.saida), 
					 end='')
			
			print("    entradas: ", end='')
			for entrada in neuronio.entradas:
				print(colorGen("   {:> 15.10f}".format(entrada),entrada)
						  , end='')
			i = i + 1
		
		for camada in self.hiddenLayers:
			j = j + 1
			i = 0
			print("\n\n\tCamada oculta {:0>2}".format(j),": ", end='')
			for neuronio in camada.neuronios:
				print("\n\t\tNeuronio {:0>3}".format(i), end='')
				print(" saída: " + colorGen("{:> 17.10f}".format(neuronio.saida)
														   , neuronio.saida)
						  , end='')
				print("    entradas: ", end='')
				for entrada in neuronio.entradas:
					print(colorGen("   {:> 15.10f}".format(entrada),entrada)
							  , end='')
				i = i + 1
		
		i = 0
		print("\n\n\tCamada final: ", end='')		
		for neuronio in self.lastLayer.neuronios:
			print("\n\t\tNeuronio {:0>3}".format(i), end='')
			print(" saída: " 
					 + colorGen("{:> 17.10f}".format(neuronio.saida),
										neuronio.saida)
					, end='')
			print("    entradas: ", end='')
			for entrada in neuronio.entradas:
				print(colorGen("   {:> 15.10f}".format(entrada),entrada)
						  , end='')
			i = i + 1
			
		print("\n")
		
		return None		

def  testRadioactivity():		
	__counter = 0
	__dna = genome()
	__len = len(__dna.dna)
	print("\t Tamanho do gene antes do teste: {:^ 5}".format(len(__dna.dna)))
	while len(__dna.dna)<(max_genes-1) :
	    __counter +=1
	    __dna.mutation()
	    #print("\t\tTentativa número {} de {} de tamanho".format(__counter, len(__dna.dna)))
	__len2 = len(__dna.dna)
	print("\t Levaram-se {} mutações para alcançar o tamanho genômico de {}  com uma taxa de {:.2f} mutações por tentativa ou {:.2f} tentativas por mutação.".format(__counter, __len2, (__len2-__len)/__counter, __counter/(__len2-__len)))
	__dna.showInfo()

# a = filter()
# print(a.calculate([1,2,3,4,5,6,7,8,9]))
