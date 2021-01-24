#!/usr/bin/env python3

#-------------------------------------------------------------------+
#
# Advent of Code - Day 3 - Part 1
#
#-------------------------------------------------------------------+

#-------------------------------------------------------------------+
#	dependencies
#-------------------------------------------------------------------+

import os
import re
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
	def _count_trees(self, entries:List[str]) -> int:
		num_trees = 0
		col = 0
		max_col = len(entries[0])

		for row in entries:
			if row[col] == "#":
				num_trees = num_trees + 1
			# end if 

			# calculate next index, account for overflow -> repeating biome pattern
			col = col + 3
			if col >= max_col:
				col = col - max_col
		# end for
		
		return num_trees		

	# public function 
	def execute(self, filename:str) -> int:
		entries = self._load_data(filename)

		num_trees = self._count_trees(entries)

		return num_trees
		

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