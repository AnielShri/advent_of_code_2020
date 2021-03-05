#!/usr/bin/env python3

#-------------------------------------------------------------------+
#
# Advent of Code - Day 7 - data parsing
#
#-------------------------------------------------------------------+

#-------------------------------------------------------------------+
#	dependencies
#-------------------------------------------------------------------+

import os
import re
import sqlite3
from typing import List

#-------------------------------------------------------------------+
#	main algorithm
#-------------------------------------------------------------------+

class Algorithm:
	def __init__(self):
		self._sql = None
		self._total = 0
		

	def _recursive_parse(self, walk_arr:List, curr_index:int, id:int):

		print("Recursive: {}  -> {} @ {} of {} for {}".format(
			walk_arr, walk_arr[curr_index],curr_index, len(walk_arr), id)
			)

		curr_lookup = [walk_arr[curr_index]] * 4 # max 4 type of bags per parent bag

		query = """
			SELECT root_color
			FROM input_data 
			WHERE 
				color_1 = ? OR
				color_2 = ? OR
				color_3 = ? OR
				color_4 = ?
			"""
		
		result = self._sql.execute(query, curr_lookup)

		query_result = result.fetchall()
		next_array = [r[0] for r in query_result]
		num_branches = len(next_array)

		if num_branches > 0:
			self._total += num_branches
			next_id = id + 1

			query = "INSERT OR IGNORE INTO bag_holder(bag) VALUES(?)"
			print(query_result)
			self._sql.executemany(query, query_result)
			self._sql.commit()

			self._recursive_parse(next_array, 0, next_id)

		else:
			next_index = curr_index + 1
			if next_index < len(walk_arr):
				self._recursive_parse(walk_arr, next_index, id)
			else:
				print("---")

	# end def
			

		
	def execute(self, database:str) -> int:
		try:

			self._sql = sqlite3.connect(database)

			query = """
				SELECT root_color
				FROM input_data 
				WHERE 
					color_1 = "shiny gold" OR
					color_2 = "shiny gold" OR
					color_3 = "shiny gold" OR
					color_4 = "shiny gold"
				ORDER BY id
				"""

			result = self._sql.execute(query)
			query_result = result.fetchall()
			walk_array = [r[0] for r in query_result]

			print(walk_array)

			query = "INSERT OR IGNORE INTO bag_holder(bag) VALUES(?)"
			print(query_result)
			self._sql.executemany(query, query_result)
			self._sql.commit()

			for n in range(len(walk_array)):
				self._recursive_parse(walk_array, n, 0)

			query = "SELECT COUNT(*) FROM bag_holder"
			result = self._sql.execute(query)

			print("total found: {} | sqlite count: {}".format(self._total, result.fetchone()[0]))

		except sqlite3.Error as e:
			print("sqlite error: {}".format(e))

		finally:
			self._sql.close()

		return 0

#-------------------------------------------------------------------+
#	startup
#-------------------------------------------------------------------+
if __name__ == "__main__":
	separator = "\r\n+----------------------------+\r\n"

	filebase = "own_data"

	filename = "{}/{}.txt".format(os.path.dirname(__file__), filebase)
	database = "{}/{}.db3".format(os.path.dirname(__file__), filebase)

	print(separator)

	alg = Algorithm()
	data = alg.execute(database)
	print("\nTotal rules: {}".format(data))

	print(separator)			