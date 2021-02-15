#!/usr/bin/env python3

#-------------------------------------------------------------------+
#
# Advent of Code - Day 6 - Part 2
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
			"",
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


	def _unique_answers(self, item:str) -> int:
		ord_a = ord("a")
		all_answers = item.split("\n")
		# print("all_answers: {}".format(all_answers))
		group_total = 0x03FFFFFF # initial assumption: all answers are `yes`
		# unique_yes = 0xFFFFFFFF # initial assumption: all answers are `yes`
		for persons_answer in all_answers:
			if len(persons_answer) == 0: # edge case for last entry -> contains emty array
				continue					 # causes last total_unique = 0
			answers = 0
			for letter in persons_answer:
				answers = answers | (1 << (ord(letter) - ord_a))
			group_total = group_total & answers
			# print("{} -> {} @ {}".format(persons_answer, group_total, answers))
			print("Unique yes: {:026b} for {:026b} in @ {}".format(group_total, answers, persons_answer))

		total_unique = 0
		for bit in range(26):
			total_unique += (group_total & (1 << bit)) >> bit
		print("Final: {:026b} -> total: {}".format(group_total, total_unique))
		return total_unique


	def _unique_answers_or(self, item:str) -> int:
		ord_a = ord("a")
		all_answers = item.split("\n")
		group_total = 0 # initial assumption: all answers are `no`
		for inidividual_answer in all_answers:
			answers = 0
			for letter in inidividual_answer:
				answers = answers | (1 << (ord(letter) - ord_a))
			group_total = group_total | answers
			# print("{} -> {} @ {}".format(inidividual_answer, unique_yes, answers))

		total_unique = 0
		for bit in range(32):
			total_unique += ((group_total & (1 << bit)) >> bit)
		print("Final: {} -> total: {}".format(group_total, total_unique))
		return total_unique


	# public function 
	def execute(self, filename: Optional[str] = None) -> int:
		# entries = self._load_data()
		entries = self._load_data(filename)
		yes_count = 0

		for item in entries:
		# for n in range(6):
			# item = entries[n]
			# yes_count += self._unique_answers(item)
			yes_count += self._unique_answers(item)
			# print("yes_count = {}".format(yes_count))

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