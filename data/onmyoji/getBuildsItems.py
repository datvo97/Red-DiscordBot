#! /usr/bin/python3
import urllib.request
import os
import asyncio
from selenium import webdriver
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
display = Display(visible=0, size=(240, 240))
display.start()
browser = webdriver.Firefox()
heroID = 1001
tempUrl = "https://www.onmyojiarena.us/ssl/page.html?id="
with open('heroes.txt') as my_file:
    heroes_array = my_file.readlines()
for heroName in heroes_array:
	if heroName.endswith('\n'):
		heroName = heroName[:-1]
	print(heroID)
	finalUrl = tempUrl + str(heroID)
	browser.get(finalUrl)
	soupObject = BeautifulSoup(browser.page_source,'html.parser')
	skillsCSS = soupObject.find(class_='cz clearfix').findAll('a',attrs={'href':'javascript:;'})
	with open("itemNames1.csv", "a") as file:
		for specSkill in skillsCSS:
			file.write(specSkill['title'] + "," + heroName + "\n")
	browser.find_element_by_class_name('tzcz02').click()
	soupObject = BeautifulSoup(browser.page_source,'html.parser')
	skillsCSS = soupObject.find(class_='cz clearfix').findAll('a',attrs={'href':'javascript:;'})
	with open("itemNames1.csv", "a") as file:
		for specSkill in skillsCSS:
			file.write(specSkill['title'] + "," + heroName + "\n")
	browser.find_element_by_class_name('tzcz03').click()
	soupObject = BeautifulSoup(browser.page_source,'html.parser')
	skillsCSS = soupObject.find(class_='cz clearfix').findAll('a',attrs={'href':'javascript:;'})
	with open("itemNames1.csv", "a") as file:
		for specSkill in skillsCSS:
			file.write(specSkill['title'] + "," + heroName + "\n")
	heroID += 1


browser.quit()