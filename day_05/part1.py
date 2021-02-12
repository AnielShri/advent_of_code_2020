#!/usr/bin/env python3

#-------------------------------------------------------------------+
#
# Advent of Code - Day 5 - part 1
#
#-------------------------------------------------------------------+

#-------------------------------------------------------------------+
#	dependencies
#-------------------------------------------------------------------+

import os
from typing import Any, List, Optional, Tuple
import math

#-------------------------------------------------------------------+
#	main algorithm
#-------------------------------------------------------------------+

class Algorithm:
	def __init__(self):
		pass

	# use example input
	def _test_input(self) -> List[str]:
		adv_data = "\n".join([
			"FBFBBFFRLR",
			"BFFFBBFRRR",
			"FFFBBBFRRR",
			"BBFFBBFRLL"
		])

		return adv_data.split("\n")

	# load input
	def _load_data(self, filename: Optional[str] = None) -> List[str]:
		if filename == None: # load Advent of Code example data
			return self._test_input()

		# if a filename is given, try to load it
		try:
			entries = [data.rstrip() for data in open(filename)]			
			return entries 

		except Exception as e:
			print("Exception: {}".format(e))
			return [""]
	# end load_data
	
	# calculates a values based on `binary space partitioning`
	def _bin_space(self, sequence: str, max_range:Any, min_range: Optional[Any] = 0) -> int:
		for sq in sequence: # loop through each letter
			if sq == "F" or sq == "L": # lower half
				max_range = (max_range - min_range - 1) / 2 + min_range
			elif sq == "B" or sq == "R": # upper half
				min_range = (max_range - min_range + 1) / 2 + min_range
			else:
				raise ValueError("Invalid sequence letter! -> {} @ {}".format(sequence, sq))

		if max_range != min_range:
			raise ValueError("Max != Min => incomplete binary space partitioning")
		
		return max_range
	# end bin_space		

	# calculates the row, column and seat ID based on a given sequence
	def _seat_id(self, sequence: str) -> Tuple[int, int, int]:
		# init variables
		max_row = 127
		max_col = 7

		row = 0
		col = 0

		# calculate column
		row = self._bin_space(sequence[0:7], max_row)
		col = self._bin_space(sequence[-3:], max_col)

		sid = (row * 8) + col

		return (row, col, int(sid)) # sid to int, to make bin search easier
	# end seat_id

	# binary search
	def _bin_search(self, id_list: List[int]):
		bin_min = id_list[0]
		bin_max = id_list[-1]
		bin_mid = math.ceil(len(id_list) / 2)

		for n in range(3):
			val_list = id_list[bin_mid] 
			val_calc = math.ceil((bin_max - bin_min) / 2 + bin_min)
			print("[{}, {}] -> List: {}, Calc: {}".format(bin_min, bin_max, val_list, val_calc))

			if val_calc == val_list: # lower half does not contain a missing number
				bin_min = val_calc
			else:					 # discontinuity in counting in lower half
				bin_max = val_calc

			bin_mid = math.ceil((bin_max - bin_min) / 2 + bin_min)

	def _bin_search2(self, id_list: List[])


	# brute force approach
	def _brute_search(self, id_list: List[int]) -> int:
		prev_id = id_list[0]
		for n in range(1, len(id_list)):
			id = id_list[n]
			if prev_id + 1 != id:
				print("Found!: {}".format(prev_id + 1))
				break
			else:
				prev_id = id
		# end for
		return prev_id + 1
	# end brute_seatch
			



	# public function 
	def execute(self, filename: Optional[str] = None) -> int:
		entries = self._load_data(filename)

		missing_sid = 0
		min_sid = 127 * 8 + 8

		sid_list = []

		# loop through all entries and append to sid_list
		for item in entries:
			data = self._seat_id(item)
			sid_list.append(data[2])			
			# print("{} - {}, {} -> {}".format(item, data[0], data[1], data[2]))

		# now sort the list to find the max/min
		# sort is also used for the next stage
		sid_list.sort()
		max_sid = sid_list[-1]

		print("min_sid: {}, max_sid: {} in total of {}".format(sid_list[0], sid_list[-1], len(entries)))

		missing_sid = self._brute_search(sid_list)
		self._bin_search(sid_list)

		# print(sid_list)v 

		return missing_sid

	# end execute

		

#-------------------------------------------------------------------+
#	startup
#-------------------------------------------------------------------+
if __name__ == "__main__":
	separator = "\r\n+----------------------------+\r\n"
	filename = "{}/input.txt".format(os.path.dirname(__file__))

	print(separator)

	alg = Algorithm()
	# data = alg.execute()
	# print("Test data -> valid: {}".format(data))
	

	data = alg.execute(filename)
	print("Own data -> valid: {}".format(data))

	print(separator)