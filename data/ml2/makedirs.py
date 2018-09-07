#! /usr/bin/python3

import sys
import os
with open('heroes.txt') as my_file:
    heroes_array = my_file.readlines()
heroID = 1
scriptDir = os.getcwd()
for heroes in heroes_array:
	if not os.path.exists(os.path.join(scriptDir, "hero"+str(heroID))):
		os.makedirs(os.path.join(scriptDir, "hero"+str(heroID)))

	os.chdir(os.path.join(scriptDir, "hero"+str(heroID)))
	heroID += 1
	print(os.getcwd())