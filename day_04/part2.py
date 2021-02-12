#!/usr/bin/env python3

#-------------------------------------------------------------------+
#
# Advent of Code - Day 4 - Part 2
#
# I tried to complete this one without using regular expressions
# Note: I should look up has maps, might be easier 
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
		adv_data = "\n".join([
			"eyr:1972 cid:100",
			"hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926",
			"",
			"iyr:2019",
			"hcl:#602927 eyr:1967 hgt:170cm",
			"ecl:grn pid:012533040 byr:1946",
			"",
			"hcl:dab227 iyr:2012",
			"ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277",
			"",
			"hgt:59cm ecl:zzz",
			"eyr:2038 hcl:74454a iyr:2023",
			"pid:3556412378 byr:2007",
			"",
			"pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980",
			"hcl:#623a2f",
			"",
			"eyr:2029 ecl:blu cid:129 byr:1989",
			"iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm",
			"",
			"hcl:#888785",
			"hgt:164cm byr:2001 iyr:2015 cid:88",
			"pid:545766238 ecl:hzl",
			"eyr:2022",
			"",
			"iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719",
		])

		return adv_data.split("\n\n")

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

	# encapsulates the built-in `int` function and checks if the value is valid
	def _valid_int(self, strint: str, base: Optional[int] = 10) -> int:
		try:
			retval = int(strint, base)
			return retval
		except ValueError:
			return -1

	# splits an item into key -> entry and checks if the value is valid
	def _valid_item(self, item: str) -> bool:
		[key, val] = item.split(":")

		if key == "byr":
			birth_year = self._valid_int(val)
			if birth_year < 1920 or birth_year > 2002:
				return False

		elif key == "iyr":
			issue_year = self._valid_int(val)
			if issue_year < 2010 or issue_year > 2020:
				return False

		elif key == "eyr":
			experation_year = self._valid_int(val)
			if experation_year < 2020 or experation_year > 2030:
				return False

		elif key == "hgt":
			unit = val[-2:] # start, end, step -> blank end -> end of string
			height = self._valid_int(val[0:-2]) # start, end -> start of str to -2 of len(str)
			if unit == "cm":
				if height < 150 or height > 193:
					return False
			elif unit == "in":
				if height < 59 or height > 76:
					return False
			else: # invalid unit
				return False	

		elif key == "hcl":
			if len(val) != 7:
				return False
			if self._valid_int(val[1:], 16) == -1:
				return False	

		elif key == "ecl": 
			if val == "amb" or val == "blu" or val == "brn" or val == "gry" or val == "grn" or val == "hzl" or val == "oth":
				pass # we only return False on error, so do nothing here
			else:
				return False

		elif key == "pid":
			if len(val) != 9:
				return False
			if self._valid_int(val) == -1:
				return False

		# we don't check for country
		# endif
		
		# we looped over each item without registering a fake? -> valid
		return True

	# core algorithm using mapping keys -> values method
	def _valid_entry(self, passport: str) -> Tuple[bool, str]:
		items = passport.replace("\n", " ").split(" ") # clean up the formatting
		num_pairs = len(items)
		valid_passport = True 
		failed_test = "Pass"

		if num_pairs <= 6: # anything less than 7 is an invalid entry
			valid_passport = False
			failed_test = "num_pairs"
		elif num_pairs == 7: # if `cid` is part of items -> missing non-optional item -> invalid
			if passport.find("cid:") != -1:
				valid_passport = False
				failed_test = "cid"
		elif num_pairs > 9: # this should not happen
			valid_passport = False
			failed_test = "num_pairs > 9"
		# endif

		if valid_passport == False:
			return (valid_passport, failed_test)

		# contains the right ammount of entries? are they valid?
		for item in items:
			valid_passport = self._valid_item(item)
			if valid_passport == False:
				failed_test = item
				break

		return (valid_passport, failed_test)


	# public function 
	def execute(self, filename: Optional[str] = None) -> int:
		# entries = self._load_data()
		entries = self._load_data(filename)

		num_valid = 0
		max_loop = len(entries)

		for n in range(max_loop):
			ret = self._valid_entry(entries[n])
			if ret[0] == True:
				num_valid += 1
			print("{:3d}: {:3d}, {} @ {}".format(n, num_valid, ret[0], ret[1]))

		return num_valid
		

#-------------------------------------------------------------------+
#	startup
#-------------------------------------------------------------------+
if __name__ == "__main__":
	separator = "\r\n+----------------------------+\r\n"
	filename = "{}/input.txt".format(os.path.dirname(__file__))

	print(separator)

	alg = Algorithm()
	data = alg.execute()
	print("Test data -> valid: {}".format(data))

	data = alg.execute(filename)
	print("Own data -> valid: {}".format(data))

	print(separator)