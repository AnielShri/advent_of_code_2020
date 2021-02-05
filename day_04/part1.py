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
from os.path import split
import re
from typing import List, Optional, Tuple

#-------------------------------------------------------------------+
#	main algorithm
#-------------------------------------------------------------------+

class Algorithm:
	def __init__(self):
		pass

	# use example input
	def _test_input(self) -> List[str]:
		adv_data = "\r\n".join([
			"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
			"byr:1937 iyr:2017 cid:147 hgt:183cm",
			"",
			"iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
			"hcl:#cfa07d byr:1929",
			"",
			"hcl:#ae17e1 iyr:2013",
			"eyr:2024",
			"ecl:brn pid:760753108 byr:1931",
			"hgt:179cm",
			"",
			"hcl:#cfa07d eyr:2025 pid:166559648",
			"iyr:2011 ecl:brn hgt:59in"
		])

		return adv_data.split("\r\n\r\n")

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

	# core algorithm
	# sloppy checking -> we assume that the entries are in key:value format
	# splitting a passport entry using the `:` seperator allows to count the number of pairs 
	# we also assume that the keys will either be present or not, we do not check for invalid keys
	#
	# input -> filename => if none is given, loads test data
	# output -> valid_passport (bool), from_northpole (bool), num_pairs (int, for debugging)
	def _valid_entry(self, passport: str) -> Tuple[bool, bool, int]:
		# num_pairs = len(passport.split(":")) - 1 # split adds +1 -> max 8 entries becomes max 9
		num_pairs = len(passport.replace("\n", " ").split(" "))
		valid_passport = True 
		from_northpole = False

		if num_pairs <= 6: # anything less than 7 is an invalid entry
			valid_passport = False
		elif num_pairs == 7: # is only valid when `cid` is missing
			if passport.find("cid:") == -1:
				from_northpole = True
			else:
				valid_passport = False
		elif num_pairs > 9: # this should not happen
			valid_passport = False
		# endif

		return (valid_passport, from_northpole, num_pairs)


	# public function 
	def execute(self, filename:str) -> int:
		# entries = self._load_data()
		entries = self._load_data(filename)

		num_valid = 0
		num_northpole = 0
		max_loop = len(entries)

		for n in range(max_loop):
			ret = self._valid_entry(entries[n])
			if ret[0] == True:
				num_valid += 1
			print("{:3d}: {:3d}, {}, {}, {}".format(n, num_valid, ret[0], ret[1], ret[2]))

		# print(len(entries))


		return num_valid
		

#-------------------------------------------------------------------+
#	startup
#-------------------------------------------------------------------+
if __name__ == "__main__":
	separator = "\r\n+----------------------------+\r\n"
	filename = "{}/input.txt".format(os.path.dirname(__file__))

	print(separator)

	alg = Algorithm()
	data = alg.execute(filename)
	print("\nTotal valid: {}".format(data))

	print(separator)