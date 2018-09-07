#! /usr/bin/python3
import urllib.request
import os
import asyncio
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
display = Display(visible=0, size=(240, 240))
display.start()
tempUrl = "https://m.mobilelegends.com/en/hero/"

for heroID in range(1, 66):
	print(heroID)
	finalUrl = tempUrl + str(heroID)
	browser = webdriver.Firefox()
	browser.get(finalUrl + "/gear")
	time.sleep(2)
	count = 1001
	soupObject = BeautifulSoup(browser.page_source,'html.parser')
	buildsCSS = soupObject.findAll(class_='detail')
	for specItem in buildsCSS[0:5]:
		buildimages = specItem.find(class_='elist clearfix').findAll('img')
		for specImage in buildimages:
			fullfilename = os.path.join(os.getcwd(), "hero"+str(heroID), "File"+str(count)+".png")
			print(specImage['src'])
			if(urllib.request.urlretrieve(specImage['src'], fullfilename)):
				count = count + 1
	browser.quit()