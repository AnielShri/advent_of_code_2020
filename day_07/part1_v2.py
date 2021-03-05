#!/usr/bin/env python3

#-------------------------------------------------------------------+
#
# Advent of Code - Day 7 - part 1
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
	# end def

	def _add_initial(self):
		# the one that starts it all
		query = """
			WITH search_bag AS (SELECT "shiny gold" AS color)
			INSERT OR IGNORE INTO part1_bags (container_color, child_color)
			SELECT input_data.root_color, search_bag.color
			FROM input_data, search_bag
			WHERE 
				input_data.color_1 = search_bag.color OR
				input_data.color_2 = search_bag.color OR
				input_data.color_3 = search_bag.color OR
				input_data.color_4 = search_bag.color
		"""

		self._sql.execute(query)
		self._sql.commit()
	# end def

	def _get_next_id(self, curr_id:int) -> int:
		query = 'SELECT id FROM "part1_bags" WHERE "id" > ? LIMIT 1'
		result = self._sql.execute(query, [curr_id])

		next_id = result.fetchone()

		if next_id is not None:
			return next_id[0]
		else:
			return -1
	# end def

	def _find_containers(self, select_id:int):
		query = """
			WITH search_bag AS 
				(
				SELECT container_color as color FROM part1_bags WHERE id = ? LIMIT 1
				)
			INSERT OR IGNORE INTO part1_bags (container_color, child_color)
			SELECT input_data.root_color, search_bag.color
			FROM input_data, search_bag
			WHERE 
				input_data.color_1 = search_bag.color OR
				input_data.color_2 = search_bag.color OR
				input_data.color_3 = search_bag.color OR
				input_data.color_4 = search_bag.color
		"""

		result = self._sql.execute(query, [select_id])
	# end def

	def _count_containers(self) -> int:
		query = 'SELECT COUNT(id) FROM part1_bags'

		result = self._sql.execute(query, [])

		count = result.fetchone()

		return count[0]
	# end def
		

	def execute(self, db:str) -> int:
		try:
			self._sql = sqlite3.connect(db)

			self._add_initial()

			prev_id = 0

			while True:
				next_id = self._get_next_id(prev_id)

				if next_id == -1:
					break

				print("Next id: {:3d}".format(next_id))

				self._find_containers(next_id)
				prev_id = next_id
			# end loop

			# update table
			self._sql.commit()

			max_containers = self._count_containers()

		except sqlite3.Error as e:
			print("A sqlite3 error occured: {}".format(e))

		finally:
			self._sql.close()

		return max_containers
	# end dif


#-------------------------------------------------------------------+
#	startup
#-------------------------------------------------------------------+
if __name__ == "__main__":
	separator = "\r\n+----------------------------+\r\n"

	filebase = "test_data2"

	filename = "{}/{}.txt".format(os.path.dirname(__file__), filebase)
	database = "{}/{}.db3".format(os.path.dirname(__file__), filebase)

	print(separator)

	alg = Algorithm()
	data = alg.execute(database)
	print("\nTotal: {}".format(data))

	print(separator)	