#! /usr/bin/python3
import sys
from PIL import Image
import sys
import os
import time

with open('allHeroes.txt') as my_file:
    heroes_array = my_file.readlines()
heroDetail = 59
scriptDir = os.getcwd()
for heroes in heroes_array:
	builds = [[],[],[],[],[],[],[],[],[],[],[],[]]
	authors = [[],[],[],[]]
	if heroes.endswith('\n'):
		heroes = heroes[:-1]
	os.chdir(os.path.join(scriptDir, heroes))
	print(os.getcwd())
	indexFile = 3
	for i in range(12):
		for x in range(6):
			if (indexFile == 21 or indexFile == 41 or indexFile == 61):
				indexFile = indexFile + 2
					
			builds[i].append("File"+str(indexFile)+".png")
			indexFile = indexFile + 1

	for xs in builds:
		print(" ".join(map(str, xs)))
			
	for i in range(12):
		images = map(Image.open, builds[i])

		total_width = 305
		max_height = 45

		new_im = Image.new('RGB', (total_width, max_height), (0, 0, 0, 0))

		x_offset = 5
		for im in images:
			new_im.paste(im, (x_offset,0))
			x_offset += 50

			new_im.save('build'+str(i)+'.png')
	authorIndex = 0
	for i in range(4):
		for x in range(3):
			authors[i].append("build"+str(authorIndex)+".png")
			authorIndex = authorIndex + 1
	for xs in authors:
		print(" ".join(map(str, xs)))		
	for i in range(4):
		images = map(Image.open, authors[i])
		ironman = Image.open("/root/Red-DiscordBot/data/ml/Divider.png", 'r')
		total_width = 305
		max_height = 236

		new_im = Image.new('RGB', (total_width, max_height), (0, 0, 0, 0))

		y_offset = 5
		for im in images:
			new_im.paste(im, (0,y_offset))
			y_offset += 35
			new_im.paste(ironman, (0,y_offset), mask=ironman)
			y_offset += 55
			new_im.save('author'+str(i)+'.png')