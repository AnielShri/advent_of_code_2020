#!/usr/bin/env python3

#-------------------------------------------------------------------+
#
# Advent of Code - Day 1 - Part 2
#
#-------------------------------------------------------------------+

#-------------------------------------------------------------------+
#	dependencier
#-------------------------------------------------------------------+

import os
from typing import List

#-------------------------------------------------------------------+
#	main algorithm
#-------------------------------------------------------------------+

class Algorithm:
	def __init__(self):
		pass

	# loads data from input file
	def _load_data(self, file:str) -> List[int]:
		try:
			entries = [int(data.rstrip()) for data in open(file)]
		except Exception as e:
			print("Exception: {}".format(e))
			return [-1]
		else:
			return entries

	# finds a matching pair 
	def _find_match(self, entries:List[int]) -> List[int]:
		pos_x = -1
		pos_y = -1

		found = False
		max_entry = len(entries)

		for rx in range(max_entry):
			for ry in range(max_entry):
				for rz in range(max_entry):
					sum_entries = entries[rx] + entries[ry] + entries[rz]

					if sum_entries != 2020:	# no match? go to next entry combo
						continue

					# else do calculations
					found = True
					pos_x = rx
					pos_y = ry
					pos_z = rz
					break
			#endfor

			if found == True:
				break
		#endfor

		return [pos_x, pos_y, pos_z]

	# call this "public" function for execute algorithm
	def execute(self, file: str) -> int:	

		entries = self._load_data(file)

		[found_x, found_y, found_z] = self._find_match(entries)

		x = entries[found_x]
		y = entries[found_y]
		z = entries[found_z]

		prod_lines = x * y * z

		print("{} + {} + {} = 2020".format(x, y, z))

		return prod_lines

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