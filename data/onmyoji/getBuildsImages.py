#! /usr/bin/python3
import urllib.request
import os
import asyncio
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
display = Display(visible=0, size=(240, 240))
display.start()
tempUrl = "https://www.onmyojiarena.us/ssl/page.html?id="
	
with open('heroes.txt') as my_file:
    heroes_array = my_file.readlines()
for heroID in range(1001, 1051):
	print(heroID)
	finalUrl = tempUrl + str(heroID)
	browser = webdriver.Firefox()
	browser.get(finalUrl)
	count = 1
	soupObject = BeautifulSoup(browser.page_source,'html.parser')
	buildsCSS = soupObject.find(class_='cz clearfix').findAll('img')
	for specItem in buildsCSS:
		fullfilename = os.path.join(os.getcwd(), "hero"+str(heroID), "File"+str(count)+".png")
		if(urllib.request.urlretrieve(specItem['src'], fullfilename)):
			count = count + 1
		print(specItem['src'])
	browser.quit()
	browser = webdriver.Firefox()
	browser.get(finalUrl)
	browser.find_element_by_class_name('tzcz02').click()
	soupObject = BeautifulSoup(browser.page_source,'html.parser')
	buildsCSS = soupObject.find(class_='cz clearfix').findAll('img')
	for specItem in buildsCSS:
		fullfilename = os.path.join(os.getcwd(), "hero"+str(heroID), "File"+str(count)+".png")
		if(urllib.request.urlretrieve(specItem['src'], fullfilename)):
			count = count + 1
		print(specItem['src'])
	browser.quit()
	browser = webdriver.Firefox()
	browser.get(finalUrl)
	browser.find_element_by_class_name('tzcz03').click()
	soupObject = BeautifulSoup(browser.page_source,'html.parser')
	buildsCSS = soupObject.find(class_='cz clearfix').findAll('img')
	for specItem in buildsCSS:
		fullfilename = os.path.join(os.getcwd(), "hero"+str(heroID), "File"+str(count)+".png")
		if(urllib.request.urlretrieve(specItem['src'], fullfilename)):
			count = count + 1
		print(specItem['src'])
	browser.quit()
	os.system("killall firefox")