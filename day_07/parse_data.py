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

#-------------------------------------------------------------------+
#	main algorithm
#-------------------------------------------------------------------+

class Algorithm:
	def __init__(self):
		self._sql = None


	def _load_data(self, filename:str) -> int:
		regex = re.compile("(?P<nbr>\d+) (?P<color>\w+ \w+) bag[s]*")
		num_entries = 0

		for line in open(filename):
			data = []
			total = 0
			num_entries += 1

			line = line.replace(".\n", "")
			[root, contents] = line.split(" bags contain ")
			data.append(root)
			
			all_bags = contents.split(", ")
			for bag_descr in all_bags:
				b = regex.match(bag_descr)
				if b is not None:
					data.append(b.group("nbr"))
					data.append(b.group("color"))
					total += int(b.group("nbr"))

			for _ in range(len(data), 9):
				data.append(None)
			data.append(total)

			print("{}".format(data))

			query = """
				INSERT INTO input_data 
				(
					root_color, nbr_1, color_1, nbr_2, color_2, 
					nbr_3, color_3, nbr_4, color_4, nbr_bags
				) 
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
			"""
			self._sql.execute(query, data)
		# end for

		return num_entries
	# end def

	def _recreate_db(self) -> bool:
		ret = True

		# data table
		query = "DROP TABLE input_data"

		try:
			self._sql.execute(query)
		except sqlite3.OperationalError as e:			
			print("Error while delating table: {}".format(e))

		query = """
			CREATE TABLE "input_data" (
				"id"	INTEGER,
				"root_color"	TEXT NOT NULL UNIQUE,
				"nbr_1"	INTEGER DEFAULT 0,
				"color_1"	TEXT,
				"nbr_2"	INTEGER DEFAULT 0,
				"color_2"	TEXT,
				"nbr_3"	INTEGER DEFAULT 0,
				"color_3"	TEXT,
				"nbr_4"	INTEGER DEFAULT 0,
				"color_4"	TEXT,
				"nbr_bags"	INTEGER DEFAULT 0,
				PRIMARY KEY("id" AUTOINCREMENT)
			)
			"""

		try:
			self._sql.execute(query)
		except sqlite3.OperationalError as e:			
			print("Error while creating table: {}".format(e))
			ret = False

		# bag_holder table
		query = "DROP TABLE recursive_bags"

		try:
			self._sql.execute(query)
		except sqlite3.OperationalError as e:			
			print("Error while delating table: {}".format(e))			

		query = """
				CREATE TABLE "recursive_bags" (
					"id"				INTEGER,
					"container_color"	TEXT UNIQUE,
					"child_color"		TEXT,
					PRIMARY KEY("id" AUTOINCREMENT)
				)
			"""

		try:
			self._sql.execute(query)
		except sqlite3.OperationalError as e:			
			print("Error while delating table: {}".format(e))	


		self._sql.commit()

		return ret
	# end def

	def parse(self, filename:str, database:str) -> int:
		self._sql = sqlite3.connect(database)

		ret = self._recreate_db()

		if not ret:
			return -1

		self._load_data(filename)

		self._sql.commit()

		self._sql.close()

		return 0

#-------------------------------------------------------------------+
#	startup
#-------------------------------------------------------------------+
if __name__ == "__main__":
	separator = "\r\n+----------------------------+\r\n"

	filebase = "input"

	filename = "{}/{}.txt".format(os.path.dirname(__file__), filebase)
	database = "{}/{}.db3".format(os.path.dirname(__file__), filebase)

	print(separator)

	alg = Algorithm()
	data = alg.parse(filename, database)
	print("\nTotal rules: {}".format(data))

	print(separator)	