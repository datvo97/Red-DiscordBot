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
tempUrl = "https://www.onmyojiarena.us/ssl/page.html?id="
for heroID in range(1001, 1050):
	finalUrl = tempUrl + str(heroID)
	browser.get(finalUrl)
	soupObject = BeautifulSoup(browser.page_source,'html.parser')
	heroName = soupObject.find(class_='abstract-cont show').find('p',attrs={'class':'tit'}).get_text()
	with open("heroes.txt", "a") as file:
		file.write(str(heroName + '\n'))
browser.quit()