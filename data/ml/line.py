#! /usr/bin/python3

import sys
import os
with open('allHeroes.txt') as my_file:
    heroes_array = my_file.readlines()
heroDetail = 0
scriptDir = os.getcwd()
for heroes in heroes_array:
	if heroes.endswith('\n'):
		heroes = heroes[:-1]
	if not os.path.exists(os.path.join(scriptDir, heroes)):
		os.makedirs(os.path.join(scriptDir, heroes))

	os.chdir(os.path.join(scriptDir, heroes))
	print(os.getcwd())