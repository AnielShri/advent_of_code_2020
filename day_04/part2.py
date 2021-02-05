#!/usr/bin/env python3

#-------------------------------------------------------------------+
#
# Advent of Code - Day 4 - Part 2
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
		self._use_json = True

	# use example input
	def _test_input(self) -> List[str]:
		adv_data = "\n".join([
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

	def _valid_item_mapping(self, items: str) -> bool:
		for item in items:
			[key, val] = item.split(":")

			if key == "byr":
				birth_year = int(val)
				if birth_year < 1920 or birth_year > 2002:
					return False

			elif key == "iyr":
				issue_year = int(val)
				if issue_year < 2010 or issue_year > 2020:
					return False

			elif key == "eyr":
				experation_year = int(val)
				if experation_year < 2020 or experation_year > 2030:
					return False

			elif key == "hgt":
				unit = val[-2:] # start, end, step -> blank end -> end of string
				height = int(val[0:-2]) # start, end -> start of str to -2 of len(str)
				if unit == "cm":
					if height < 150 or height > 193:
						return False
				elif unit == "in":
					if height < 59 or height > 76:
						return False
				else: # invalid unit
					return False	

			elif key == "hcl":
				# we could use int(val, 16), but it throws an exception, and I don't want to handle it
				matches = re.search("#[0-9a-f]{6}", val)
				if matches == 0:
					return False
			
			elif key == "ecl": # need to clean up the if statements
				if val == "amb":
					pass
				elif val == "blu":
					pass
				elif val == "brn":
					pass
				elif val == "gry":
					pass
				elif val == "grn":
					pass
				elif val == "hzl":
					pass
				elif val == "oth":
					pass
				else:
					return False

			elif key == "pid":
				# passport_id = int(val) # I probably need a int -> catch exception function
				if len(val) != 9:
					return False
			# we don't check for country
			# endif
		
		# we looped over each item without registering a fake? -> valid
		return True
		
		return True

	# core algorithm using mapping keys -> values method
	def _valid_entry_mapping(self, passport: str) -> bool:
		items = passport.replace("\n", " ").split(" ") # clean up the formatting
		num_pairs = len(items)
		valid_passport = True 

		if num_pairs <= 6: # anything less than 7 is an invalid entry
			valid_passport = False
		elif num_pairs == 7: # if `cid` is part of items -> missing non-optional item -> invalid
			if passport.find("cid:") != -1:
				valid_passport = False
		elif num_pairs > 9: # this should not happen
			valid_passport = False
		# endif

		if valid_passport == False:
			return valid_passport

		# contains the right ammount of entries? are they valid?
		valid_passport = self._valid_item_mapping(items)
		return valid_passport


	# public function 
	def execute(self, filename: Optional[str] = None) -> int:
		# entries = self._load_data()
		entries = self._load_data(filename)

		num_valid = 0
		max_loop = len(entries)

		for n in range(max_loop):
			ret = self._valid_entry_mapping(entries[n])
			if ret == True:
				num_valid += 1
			# print("{:3d}: {:3d}, {}".format(n, num_valid, ret))

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

	# data = alg.execute(filename)
	# print("Own data -> valid: {}".format(data))

	print(separator)