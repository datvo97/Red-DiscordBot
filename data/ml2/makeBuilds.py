#! /usr/bin/python3
import sys
from PIL import Image
import sys
import os
import time

with open('heroes.txt') as my_file:
    heroes_array = my_file.readlines()
scriptDir = os.getcwd()
for heroID in range(1,66):
	builds = [[],[],[],[],[]]
	os.chdir(os.path.join(scriptDir, "hero" + str(heroID)))
	print(os.getcwd())
	indexFile = 1001
	for i in range(5):
		for x in range(6):
			builds[i].append("File"+str(indexFile)+".png")
			indexFile = indexFile + 1

	for xs in builds:
		print(" ".join(map(str, xs)))
			
	for i in range(5):
		images = map(Image.open, builds[i])

		total_width = 630
		max_height = 105

		new_im = Image.new('RGB', (total_width, max_height), (0, 0, 0, 0))

		x_offset = 5
		for im in images:
			new_im.paste(im, (x_offset,0))
			x_offset += 105

			new_im.save('build'+str(i)+'.png')