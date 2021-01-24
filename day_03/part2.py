#!/usr/bin/env python3

#-------------------------------------------------------------------+
#
# Advent of Code - Day 3 - Part 2
#
#-------------------------------------------------------------------+

#-------------------------------------------------------------------+
#	dependencies
#-------------------------------------------------------------------+

import os
import re
import math
from typing import List

#-------------------------------------------------------------------+
#	main algorithm
#-------------------------------------------------------------------+

class Algorithm:
	def __init__(self):
		pass

	# load input
	def _load_data(self, filename:str) -> List[str]:
		try:
			entries = [data.rstrip() for data in open(filename)]
		except Exception as e:
			print("Exception: {}".format(e))
			return [""]
		else:
			return entries

	# core of algorithm
	def _count_trees(self, entries:List[str], right:int, down:int) -> int:
		num_trees = 0
		col = 0
		row = 0
		max_col = len(entries[0])
		max_row = len(entries)

		# we're not stepping through each entry, so use an infinite loop, and break at end of list
		while True:
			item = entries[row]
			if item[col] == "#":
				num_trees = num_trees + 1
			#end if 

			# calculate next col, account for overflow -> repeating biome pattern
			col = (col + right) %  max_col
			
			# move down until end last entry
			row = row + down
			if row >= max_row:
				break
		#end loop

		return num_trees		

	# public function 
	def execute(self, filename:str) -> int:
		entries = self._load_data(filename)

		slopes = [
			[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]
		]

		num_trees = [0] * len(slopes)
		
		for n in range(len(slopes)):
			num_trees[n] += self._count_trees(entries, slopes[n][0], slopes[n][1])
		#end for

		prod_trees = math.prod(num_trees)

		return prod_trees
		

#-------------------------------------------------------------------+
#	startup
#-------------------------------------------------------------------+
if __name__ == "__main__":
	separator = "\r\n+----------------------------+\r\n"
	filename = "{}/input.txt".format(os.path.dirname(__file__))

	print(separator)

	alg = Algorithm()
	data = alg.execute(filename)
	print("\nProduct total: {}".format(data))

	print(separator)