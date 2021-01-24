#!/usr/bin/env python3

#-------------------------------------------------------------------+
#
# Advent of Code - Day 2 - Part 2
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
	def _valid_entries(self, entries:List[str]) -> int:
		# regular expression works on string format as found in input text
		regex = re.compile("(?P<yes>\d+)-(?P<no>\d+) (?P<letter>\w): (?P<pwd>\w+)")

		num_valid = 0

		for item in entries:
			parts = regex.match(item)

			index_yes = int(parts.group("yes")) - 1
			index_no = int(parts.group("no")) - 1
			pwd = parts.group("pwd")

			has_yes = False
			has_no = False

			if pwd[index_yes] == parts.group("letter"):
				has_yes = True
			
			if pwd[index_no] == parts.group("letter"):
				has_no = True

			if has_yes == True and has_no == False:
				num_valid = num_valid + 1

			if has_yes == False and has_no == True:
				num_valid = num_valid + 1
		#end for
		
		return num_valid		

	# public function 
	def execute(self, filename:str) -> int:
		entries = self._load_data(filename)

		valid_entries = self._valid_entries(entries)

		return valid_entries
		

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