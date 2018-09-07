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
url = "https://m.mobilelegends.com/en/hero/1/gear"
browser.get(url)
soupObject = BeautifulSoup(browser.page_source,'html.parser')

loop = asyncio.get_event_loop()
with open("output1.txt", "w") as file:
    file.write(str(soupObject))
loop.close()

browser.quit()