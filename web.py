#!/usr/bin/python
# -*- coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as condition
from selenium.common.exceptions import WebDriverException 
from selenium.common.exceptions import TimeoutException 
from selenium.common.exceptions import ElementNotVisibleException
import os
import wget
from color import *

def waitElement(driver, by_clause, value, time = 180):
	try:
		element = WebDriverWait(driver, time).until(
						 condition.presence_of_element_located(
						  (by_clause, value)								 ))
	except TimeoutException:
		pcolor(Fore.RED, "Houve uma exceção de timeout, retentando por mais " + str(time*2) + " segundos. ")
		waitElement(driver, by_clause, value, time*2) 
	finally:
		return element

def googleSearch(driver, text):
	driver.get("https://images.google.com.br")
	try:
		searchbar = waitElement(driver, By.CLASS_NAME, "gsfi")
	finally:
		pass
	searchbar.send_keys(text)
	searchbar.send_keys(Keys.RETURN)
	
	return None

def findImages(driver):
	images = waitElement(driver, By.CLASS_NAME, "rg_i")
	images = WebDriverWait(driver, 30).until(
	condition.element_to_be_clickable((By.CLASS_NAME, "rg_i")))
	images = driver.find_elements_by_xpath("//img[@class='rg_i']")
	if images is None:
		images = driver.find_elements_by_class_name("rg_i")
	selected = []
	for image in images:
		jsaction = image.get_attribute("jsaction")
		#print(jsaction)
		if jsaction is None:
			continue
		else:
			selected.append(image)
	images = selected
	return images

def downloadImage(driver,index):
	images = findImages(driver)	
	try:	
		images[index].click()
	except WebDriverException:
		return (None, None)
	except ElementNotVisibleException:
		return None, None
	texts = waitElement(driver, By.XPATH, "//span[@class='irc_su']")
	texts = driver.find_elements_by_xpath("//span[@class='irc_su']")
	description = ""
	for value in texts:
		description += " " + value.text
	buttons = waitElement(driver, By.XPATH, "//a[@class='irc_fsl irc_but i3596']")
	buttons = driver.find_elements_by_xpath("//a[@class='irc_fsl irc_but i3596']")
	pcolor(Fore.MAGENTA, "\n\nDesc : " + description)
	links = []
	for button in buttons:
		if button is None:
			continue
		image_link = button.get_attribute("href")
		if image_link is None:
			continue
		links.append(image_link)
		#pcolor(Fore.BLUE, "image_link : " + image_link)
	#desc_links = ""
	#for link in links:
	#	desc_links += " " + link
	#pcolor(Fore.CYAN, "Links : " + desc_links)
	if links is None:
		pcolor(Fore.RED, "\n Ocorreu um erro ao receber os links das imagens, retornando nulo")
		return (None, None)
	
	filenames = []
	links = [links.pop()]
	for link in links:
		driver.get(link)
		link = driver.current_url
		#pcolor(Fore.BLUE, link)
		filename = link.rsplit('/').pop()
		if not os.path.isfile(filename):
			try:
				try:
					try:
						filename = wget.download(link)
					except:
						filename = wget.download(link)
				except:
					filename = wget.download(link)
			except:
				return None, None
			filenames.append(filename)
	for link in links:
		driver.back()
	close_button = waitElement(driver, By.XPATH, "//a[@id='irc_cb']")
	try:
		close_button = WebDriverWait(driver, 90).until(
							condition.element_to_be_clickable((By.XPATH, "//a[@id='irc_cb']")))
	except TimeoutException:
		pcolor(Fore.RED, "\n A conexão está prejudicando o acesso a https://www.google.com.br/")
		driver.get(driver.current_url)
		try:
			close_button = WebDriverWait(driver, 360).until(
							condition.element_to_be_clickable((By.XPATH, "//a[@id='irc_cb']")))
		except TimeoutException:
			pcolor(Fore.RED, "\n A conexão foi perdida")
			exit(1)
	try:
		close_button.click()
	except WebDriverException:
		return (None, None)
	except ElementNotVisibleException:
		return None, None
	return (filenames, description)
		
#driver = webdriver.Chrome()
def tente(driver, text, n):
	googleSearch(driver, text)
	for i in range(n):
		a, b = downloadImage(driver, i)
		if a is None:
			googleSearch(driver, text)