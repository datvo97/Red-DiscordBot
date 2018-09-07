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
heroID = 70
tempUrl = "https://m.mobilelegends.com/en/hero/"
with open("itemNames2.csv", "w") as file:
	file.write("name,rank,rate,hero\n")
with open('heroes.txt') as my_file:
    heroes_array = my_file.readlines()
for heroName in heroes_array:
	if heroName.endswith('\n'):
		heroName = heroName[:-1]
	print(heroID)
	finalUrl = tempUrl + str(heroID)
	browser.get(finalUrl + "/gear")
	soupObject = BeautifulSoup(browser.page_source,'html.parser')
	authorsCSS = soupObject.findAll(class_='detail')
	for specAuthor in authorsCSS[0:5]:
		authorInfo = specAuthor.find(class_='attr clearfix').find(class_='value name').getText()
		authorRank = specAuthor.find(class_='attr clearfix').findAll(class_='value')
		print(authorInfo + "," + authorRank[1].getText() + "," + authorRank[2].getText() + "," + heroName + "\n")
		with open("itemNames2.csv", "a") as file:
			file.write(authorInfo + "," + authorRank[1].getText() + "," + authorRank[2].getText() + "," + heroName + "\n")
	heroID += 1

browser.quit()