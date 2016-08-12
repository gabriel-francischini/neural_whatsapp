#!/usr/bin/python
# -*- coding: utf-8
import selenium
import socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as condition
from selenium.common.exceptions import WebDriverException 
from selenium.common.exceptions import TimeoutException 
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
import os
import wget
from tqdm import tqdm
import time
import progressbar
import threading
from queue import Queue 
import sys
import urllib.request
import neural
from random import *

from color import *


# Queues for to-do organization
# One for links to download,
# other for strings to search
# and other for getting keywords from descriptions
download_queue = Queue()
search_queue = Queue()
keywords_queue = Queue()
print_queue = Queue()

download_lock = threading.Lock()
search_lock = threading.Lock()
keywords_lock = threading.Lock()

threads = []

keywords_occurence = {}
already_used_searchs = []



def qprint(string):

	print_queue.put((threading.current_thread().name,
					 time.asctime(),
					 string))

def printThread():

	(threadname, print_time_request, print_string) = print_queue.get()

	print("[" + print_time_request + " " + threadname + "]:\t"
		  + print_string)


def qolorize(string, *colors):
	
	return colorize(string, *colors, do_printing = False)




# This function can be used to sometimes get a element
# (when it needs to be loaded) or to do sane-checking
# before trying other ways to get the element
def waitElement(driver, by_clause, value, timing = 30, reload = False, loop = False):

	element = None

	# Try to wait to get the element, but a timeout
	# exception can occur
	try:
		element = WebDriverWait(driver, timing).until(
						 condition.presence_of_element_located(
						  (by_clause, value) ))
	except TimeoutException:

		# If a exception do rise, we try again
		try: 
			element = WebDriverWait(driver, timing).until(
				condition.presence_of_element_located(
			    (by_clause, value) ))

		# At the third time we see if we can reload
		except TimeoutException as timeout:
			if reload and not loop:
				driver.get(driver.current_url)

				try:
					element = WebDriverWait(driver, timing).until(
				condition.presence_of_element_located(
			    (by_clause, value) ))

				except TimeoutException as timeout:
					raise timeout


			else:
				raise timeout

	if loop:
		while not element:
			try:
				element = waitElement(driver, by_clause, value,
				 reload = reload, loop = False)
			except TimeoutException as timeout:
				pass



	# If there's no error, we should be with a element	
	return element


# This function do a google image search using
# the string indicated by text
def googleImageSearch(driver, text):

	qprint("Starting a new search with \"" + qolorize(text, Fore.CYAN) 
		+ "\"")

	# Navigates to google image
	driver.get("https://images.google.com.br")

	# Sometimes searchbar already has focus when
	# we access the google images, so we click
	# the searchbutton to guarantee it doesn't have
	# focus and we can find it

	qprint("Waiting for the search button...")

	searchbutton = waitElement(driver, By.CLASS_NAME, "lsb", 
		reload = True, loop = True)
	
	qprint("Clicking the search button")

	#searchbutton = driver.find_element_by_class_name("lsb")
	searchbutton.click()

	# Try to get the searchbar element
	# This could rise a exception, but we're no ready
	# for them yet

	qprint("Waiting for the search bar...")

	searchbar = waitElement(driver, By.CLASS_NAME, "gsfi", 
		reload = True, loop = True)
	
	qprint("Sending \"" + qolorize(text, Fore.CYAN) + "\" to"
	" the search bar" )

	# And input the search in the searchbar and GOOGLE IT!
	searchbar.send_keys(text)
	searchbar.send_keys(Keys.RETURN)
	
	# And we're done
	return None


# This function googles images related to a string
# The it write out a list with links to the images
# and the respective brief descriptions
# Those list with (link, description) will'be use
# to download them and improve keyword-search
def findImages(driver, searchtext):

	qprint("Starting the search for new images for \'" +
		qolorize(searchtext, Fore.CYAN) + "\"")

	# We first google the text
	googleImageSearch(driver, searchtext)

	# We need to know if the page has results to not bug
	hasResults = False

	qprint("Returning to the findImages()")

	try:
		driver.find_element_by_class_name("mnr-c")
	except selenium.common.exceptions.NoSuchElementException:
		hasResults = True

	if (not hasResults):
		return []


	# We make sure the page has loaded and it's
	# suitable for clicking and interacting
	qprint("Waiting for the list of images to crawl by...")

	images = waitElement(driver, By.CLASS_NAME, "rg_i", reload = True)
	images = WebDriverWait(driver, 60).until(
	condition.element_to_be_clickable((By.CLASS_NAME, "rg_ic")))

	# Now we get the google's thumbnails	
	qprint("Getting the first wave of images in search...")

	images = driver.find_elements_by_xpath("//img[@class='rg_i rg_ic']")
	
	# Make sure we can see the images
	images[0].location_once_scrolled_into_view

	# This variable prepares the environment for the next loop
	old_len_images = 0

	qprint("Entering the loop to crawl images")

	# We'll keep scrolling down while the
	# number of images keep increasing as we do it
	# (it means we have not reached the bottom end yet)
	# Sometimes we'll need to click on the "View More Results" button
	while len(images) > old_len_images:

		# Annotates the current size
		old_len_images = len(images)

		# Keep scrolling down through the
		# last 25 images on the list
		for element in images[-25:]:
			element.location_once_scrolled_into_view
		
		# Wait a little for no bugs, since
		# more images are loading to page
		time.sleep(3)

		# See the new images that could have been loaded
		# while we were scrolling down
		images = driver.find_elements_by_xpath("//img[@class='rg_i rg_ic']")

		# See if we can see the "View More Results" button
		# (it blocks new image's loading)
		more_results = driver.find_element_by_id("smb")
		
		# If we can see one...
		if (more_results is not None):
		
			# And it can be clicked...
			if more_results.is_displayed():

				# CLICK IT!
				more_results.click()

	qprint("Processing images crawled to a link-text format...")

	# So far we should have a list with images
	# inside the image variable.
	# It's time to turn them in links and text! ;)
	link_list = []

	# While we have images to process,
	while images:
		# Get the last image on the list and open it
		image = images.pop()
		for i in range(100):
			image.location_once_scrolled_into_view
		try:
			image.click()
		except:
			continue

		# Wait the brief-view of google to pop up with thumbnails
		# and other info like source link, description, etc.
		texts = waitElement(driver, By.XPATH, "//span[@class='irc_su']")
		
		# Get the description above the buttons "View Page" and "View Image"
		# Unfortunately often other two None strings are found with this
		# method, but we can get rid of them (they're just empty strings after all)
		texts = driver.find_elements_by_xpath("//span[@class='irc_su']")

		# Take the strings that aren't empty (generally one)
		# and use it as description
		description = ""
		for value in texts:
			if value:
				description += value.text + " "

		# Guarantees we can see the button of "View Image"
		# And get it for manipulating 
		buttons = waitElement(driver, By.XPATH, "//a[@class='irc_fsl irc_but i3596']")
		buttons = driver.find_elements_by_xpath("//a[@class='irc_fsl irc_but i3596']")
		
		# As text, the link also has a problem of raising usually empty
		# strings with it, so we take the cautious to only choose the button
		# which has the link to the image
		image_link = None
		for button in buttons:

			# "Visualizar imagem" is the text that appears on my
			# "View Image" button. Replace it with whatever
			# appears at your "View Image" button
			if button.text == "Visualizar imagem":
				# The link to the image is in the
				# "href" attribute inside the "a" tag that holds the button
				image_link = button.get_attribute("href")
		if image_link:
			namefile = image_link.rsplit('/').pop()
			namefile = namefile.rsplit('?')[0]	
			namefile = namefile.rsplit('%')[0]	
			namefile = namefile.rsplit('&')[0]
			qprint("New image for download: \'" + qolorize(
				namefile, Fore.GREEN) + "\' from search "
				+ " \'" + qolorize(searchtext, Fore.MAGENTA) + "\'")

			# Put the links to download
			download_queue.put((image_link, description, searchtext))

			# Returns a reasonable list of (link,description) :)
			link_list += [(image_link, description)]

	return link_list
		

def downloadImage(url, description, folder = ""):
	# wget was running into problems while trying to 
	# connect to some sites, so I change it with this
	# urllib with these headers thing
	# I don't know it deeply but...

	qprint("Get download for \"" + qolorize(url, Fore.YELLOW)
		+ "\"")

	qprint("Opening header for download...")
	# Opens the header
	opener=urllib.request.build_opener()
	opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
	urllib.request.install_opener(opener)

	# Find a suitable filename to the archive
	
	# First we get the filename
	filename = url.rsplit('/').pop()

	# Separate it from its extension
	extension = filename.rsplit('.').pop()
	extension = extension.rsplit('?')[0]
	extension = extension.rsplit('&')[0]
	extension = extension.rsplit('%')[0]

	# And format the filename to a better name
	filename = filename.rsplit('.')[0]
	filename = removeIlegalCharacters(filename)

	if len(filename) > 50:
		filename = filename[:49]
	
	file = "./" + folder + '/' + filename + "." + extension 
	
	qprint("Downloading " + qolorize(filename + "." +
		   extension, Fore.CYAN) + " at " + qolorize(
		   folder, Fore.MAGENTA))

	# And try to download it
	try:
		if filename:
			urllib.request.urlretrieve(url, file)

	# If it fails, try again
	except urllib.error.HTTPError:
		try:
			file = "./" + folder + "2" + url.rsplit('/').pop()
			urllib.request.urlretrieve(url, file)

		# If fails, try a easy way
		except urllib.error.HTTPError:
			try:
				opener=urllib.request.build_opener()
				opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
				urllib.request.install_opener(opener)
				file = "./" + url.rsplit('/').pop()
				urllib.request.urlretrieve(url, file)

			# If fails again, give the shit up
			except urllib.error.HTTPError:
				pass
				return None


	# Put the keywords to be analyzed
	keywords_queue.put((description))
	return None


def removeIlegalCharacters(old_string):
	string = ""

	#qprint("Removing illegal characters from \""
	#	+ qolorize(old_string, Fore.BLUE) + "\"")

	# First we remove some odd characters
	for character in old_string:
		if character in (",!?.:;^~\'\"\n\r\t\v\f\x1c\x1d\x1e\x85\u2028\u2029"
			"\{\}[]()/\\ +=_-@#$%¨&*£¢¬§ªº°|"):
			character = " "
		string += character

	# After we try to remove all white spaces
	# And turn all in lower case and split
	# the string word-by-word
	string = string.expandtabs()
	string = string.lower()
	
	for i in range(8):
		string = string.replace("  ", " ")

	string = string.strip()

	return string



# This functions analyzes keywords and generates new
# searches based upon them
def analyze(original_description):

	qprint("Getting keywords from \"" +
		qolorize(original_description, Fore.YELLOW, Back.BLUE)
		+ qolorize("\"", Back.BLACK))

	global keywords_occurence

	description = removeIlegalCharacters(original_description)
	description = description.split(" ")

	for word in description:
		word = word.strip()


	# Now we add the words to the keywords dict:
	for word in description:
		keywords_occurence[word] = keywords_occurence.setdefault(word, 0) + 1

	
	return None

def newSearch():

	global already_used_searchs

	# We sort the most used keywords:
	neural.setTupleSorting(1)

	# First we transform the dict in a list of tuples
	keywords = keywords_occurence.items()


	# And then we sort the tuples
	keywords = sorted(keywords, key = neural.byTuple, reverse = True)


	only_keywords = []
	for word,value in keywords:
		for i in range(value):
			only_keywords += [word]

	keywords = only_keywords

	words = set()
	for i in range(randint(0, 7)):
		words.add(choice(keywords))

	for seth in already_used_searchs:
		if words == seth:
			return None

	already_used_searchs += [words]

	words = list(words)
	searchstring = ""

	for word in words:
		searchstring += word + " "

	qprint("Creating new search: " +
		qolorize(searchstring, Fore.GREEN))

	search_queue.put(searchstring)



def searchThread():
	qprint(qolorize("Thread created: " + threading.current_thread().name,
	      Fore.YELLOW))

	display = Display(visible=0, size=(1024, 768))
	time.sleep(5)

	display.start()
	time.sleep(10)

	driver = webdriver.Chrome()
	time.sleep(15)

	while True:

		searchstring = search_queue.get()

		
		try:
			searchresult = findImages(driver, searchstring)
		except TimeoutException as timeout:
			print((colorize("{} : {} {}", Fore.RED) + 
				" has occurred while searching, retrying").format(
				type(timeout), timeout.args, timeout))

		search_queue.task_done()


def downloadThread():
	qprint(qolorize("Thread created: " + threading.current_thread().name,
	      Fore.YELLOW))

	while True:

		(url, description, searchtext) = download_queue.get()
		if not (url and searchtext):
			download_queue.task_done()
			continue
		folder = ""
		folder += searchtext#.replace(" ","-")

		if not os.path.exists(folder):
			os.makedirs(folder)

		try:
			downloadImage(url, description, folder)
		except socket.gaierror:
			pass
		except urllib.error.URLError:
			pass

		download_queue.task_done()

def analyzeThread():
	qprint(qolorize("Thread created: " + threading.current_thread().name,
	      Fore.YELLOW))

	i = 0

	while True:
		keywords = keywords_queue.get()

		analyze(keywords)
		
		keywords_queue.task_done()

		newSearch()
		
		i += 1
		if (i%20) == 0:
			i = 0
			newSearch()



def createThreads():

	global threads

	for i in range(5):
		thread = threading.Thread(target = searchThread)
		thread.start()
		threads += [thread]
		time.sleep(10)

	for i in range(5):
		thread = threading.Thread(target = downloadThread)
		thread.start()
		threads += [thread]
		time.sleep(10)

	for i in range(5):
		thread = threading.Thread(target = analyzeThread)
		thread.start()
		threads += [thread]
		time.sleep(10)

	while True:
		
		printThread()