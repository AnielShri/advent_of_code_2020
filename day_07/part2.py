#!/usr/bin/env python3

#-------------------------------------------------------------------+
#
# Advent of Code - Day 7 - part 2
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
			SELECT 
				input_data.root_color, 
				input_data.color_1,  
				input_data.color_2, 
				input_data.color_3, 
				input_data.color_4,
				input_data.nbr_1,
				input_data.nbr_2,
				input_data.nbr_3,
				input_data.nbr_4,
				(
					input_data.nbr_1 + input_data.nbr_2 + 
					input_data.nbr_3 + input_data.nbr_4
				) as nbr_total
			FROM input_data
			WHERE root_color = "shiny gold"
			LIMIT 1
		"""

		result = self._sql.execute(query)

		data = result.fetchone()
		root_color = data[0]
		colors = data[1:5]
		mult_factors = data[5:9]
		total = data[9]
		print("root: {}, colors: {}, mult_factors: {}, total: {}".format(
			root_color, colors, mult_factors, total)
			)		

		# shiny gold
		query = """
			INSERT INTO 
				part2_bags (root_color, num_children, tot_bags)
			VALUES (?, ?, ?)
		"""
		self._sql.execute(query, [root_color, total, total])

		# first children
		query = """
			INSERT INTO 
				part2_bags (root_color, mult_factor)
			VALUES (?, ?)
		"""

		for c, m in zip(colors, mult_factors):
			if c == '':
				break
			self._sql.execute(query, [c, m])

		# self._sql.commit()
	# end def

	def _get_next_id(self, curr_id:int) -> int:
		query = 'SELECT id FROM "part2_bags" WHERE "id" > ? LIMIT 1'
		result = self._sql.execute(query, [curr_id])

		next_id = result.fetchone()

		if next_id is not None:
			return next_id[0]
		else:
			return -1
	# end def

	def _find_children(self, select_id:int):
		query = """
			SELECT 
				input_data.root_color, 
				input_data.color_1,  
				input_data.color_2, 
				input_data.color_3, 
				input_data.color_4,
				input_data.nbr_1,
				input_data.nbr_2,
				input_data.nbr_3,
				input_data.nbr_4,
				(
					input_data.nbr_1 + input_data.nbr_2 + 
					input_data.nbr_3 + input_data.nbr_4
				) as nbr_total
			FROM input_data
			WHERE root_color = (
				SELECT root_color FROM part2_bags WHERE id = ? LIMIT 1
				)
			LIMIT 1
		"""

		result = self._sql.execute(query, [select_id])
		data = result.fetchone()
		root_color = data[0]
		colors = data[1:5]
		mult_factors = data[5:9]
		total = data[9]
		print("root: {}, colors: {}, mult_factors: {}, total: {}".format(
			root_color, colors, mult_factors, total)
			)	

		# update root
		query = """
			UPDATE part2_bags 
			SET 
				num_children = ?, 
				tot_bags = ? * (
					SELECT mult_factor FROM part2_bags WHERE id = ? LIMIT 1
				) 
			WHERE id = ?
		"""
		self._sql.execute(query, [total, total, select_id, select_id])

		# insert children
		query = """
			INSERT INTO 
				part2_bags (root_color, mult_factor)
			VALUES (?, ?)
		"""

		for c, m in zip(colors, mult_factors):
			if c == '':
				break
			self._sql.execute(query, [c, m])
	# end def

	def _count_containers(self) -> int:
		query = 'SELECT SUM(tot_bags) FROM part2_bags'

		result = self._sql.execute(query, [])

		count = result.fetchone()

		return count[0]
	# end def
		

	def execute(self, db:str) -> int:
		try:
			self._sql = sqlite3.connect(db)

			self._add_initial()

			prev_id = self._get_next_id(0) # shiny gold

			while True:
				next_id = self._get_next_id(prev_id)

				if next_id == -1:
					break

				# print("Next id: {:3d}".format(next_id))

				self._find_children(next_id)
				prev_id = next_id
			# end loop

			# update table
			self._sql.commit()

			num_containers = self._count_containers()

		except sqlite3.Error as e:
			print("A sqlite3 error occured: {}".format(e))

		finally:
			self._sql.close()

		return num_containers
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