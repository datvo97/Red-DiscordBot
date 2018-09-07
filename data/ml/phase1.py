#! /usr/bin/python3
import urllib.request
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
browser = webdriver.PhantomJS()
with open('allHeroes.txt') as my_file:
    heroes_array = my_file.readlines()
heroDetail = 0
for heroes in heroes_array:
	if heroes.endswith('\n'):
		heroes = heroes[:-1]
	heroDetail += 1
	print(heroDetail)
	print(heroes)

	url = "https://www.mobilelegends.com/hero/detail-" + str(heroDetail)
	browser.get(url)
	wait = WebDriverWait(browser, 10)
	wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.archive_loading_bar')))
	soupObject = BeautifulSoup(browser.page_source,'html.parser')
	trs = soupObject.findAll(class_='left eqwrapper clearfix')

	with open("output1.csv", "a") as file:
		for tr in trs:
			tds = tr.findAll("span") # you get list
			
			count = 1			
			for p in tds:
				if (p.get_text() == 'A' or p.get_text() == 'B' or p.get_text() == 'C'):
					continue;
				else:
					if (count == 4):
						file.write(p.get_text() + "," + heroes + "\n")
						count = 1
					else:
						file.write(p.get_text() + ",")
						count += 1
						
		for trss in trs:
			elements = trss.findAll('img', attrs={'class':'lazyload'})
			count = 1
			for element in elements:
				fullfilename = os.path.join(os.getcwd(), heroes, "File"+str(count)+".png")
				if(urllib.request.urlretrieve(element['data-src'], fullfilename)):
					count = count + 1
				print(element['data-src'])
					




#authorInfoOne = soupObject.find(class_='left eqwrapper clearfix').find(class_='item').find(class_='header clearfix').find(class_='right')
#authorInfoTwo = authorInfoOne.findNextSibling()
#authorInfoThree = authorInfoTwo.findNextSibling()
#print (authorInfoOne.get_text())
#print (authorInfoTwo)
#print (authorInfoThree.get_text())
#print (authorInfo.findNext())
#with open("output1.txt", "w") as file:
#    file.write(str(authorInfo))

