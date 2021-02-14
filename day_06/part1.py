#!/usr/bin/env python3

#-------------------------------------------------------------------+
#
# Advent of Code - Day 4 - Part 1
#
#-------------------------------------------------------------------+

#-------------------------------------------------------------------+
#	dependencies
#-------------------------------------------------------------------+

import os
# from os.path import split
from typing import List, Optional, Tuple

#-------------------------------------------------------------------+
#	main algorithm
#-------------------------------------------------------------------+

class Algorithm:
	def __init__(self):
		pass

	# use example input
	def _test_input(self) -> List[str]:
		adv_data = "\n".join([
			"abc",
			"",
			"a",
			"b",
			"c",
			"",
			"ab",
			"ac",
			"",
			"a",
			"a",
			"a",
			"a",
			"",
			"b",
		])

		return adv_data.split("\n\n")

	def _unique_answers(self, item:str) -> int:
		ord_a = ord("a")
		all_answers = [0] * (ord("z") - ord_a + 1)
		# print(len(all_answers))
		for letter in item.replace("\n", ""):	
			all_answers[ord(letter) - ord_a] = 1
		print(all_answers)
		return sum(all_answers)

	# load input
	def _load_data(self, filename: Optional[str] = None) -> List[str]:
		if filename == None: # load Advent of Code example data
			return self._test_input()

		# if a filename is given, try to load it
		try:
			# entries = [data.rstrip() for data in open(filename)]
			with open(filename) as f:
				entries = f.read().split("\n\n")
		except Exception as e:
			print("Exception: {}".format(e))
			return [""]
		else:
			return entries


	# public function 
	def execute(self, filename: Optional[str] = None) -> int:
		# entries = self._load_data()
		entries = self._load_data(filename)
		yes_count = 0

		for item in entries:
		# for n in range(1):
			# item = entries[n]
			yes_count += self._unique_answers(item)

		return yes_count
		

#-------------------------------------------------------------------+
#	startup
#-------------------------------------------------------------------+
if __name__ == "__main__":
	separator = "\r\n+----------------------------+\r\n"
	filename = "{}/input.txt".format(os.path.dirname(__file__))

	print(separator)

	alg = Algorithm()

	# test data
	data = alg.execute()
	print("\nTotal unique yes: {}".format(data))

	# own data
	data = alg.execute(filename)
	print("\nTotal unique ye: {}".format(data))

	print(separator)