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
tempUrl = "https://m.mobilelegends.com/en/hero/"
for heroID in range(1, 64):
	finalUrl = tempUrl + str(heroID)
	browser.get(finalUrl + "/gear")
	soupObject = BeautifulSoup(browser.page_source,'html.parser')
	heroName = soupObject.find(class_='picwrapper').find('div',attrs={'class':'name'}).get_text()
	with open("heroes.txt", "a") as file:
		file.write(str(heroName + '\n'))
browser.quit()