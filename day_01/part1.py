#!/usr/bin/env python3

#-------------------------------------------------------------------+
#
# Advent of Code - Day 1 - Part 1
#
#-------------------------------------------------------------------+

#-------------------------------------------------------------------+
#	dependencier
#-------------------------------------------------------------------+

import os

#-------------------------------------------------------------------+
#	main algorithm
#-------------------------------------------------------------------+

class Algorithm:
	def __init__(self):
		pass

	def execute(self, file: str) -> int:
		try:
			entries = [int(data.rstrip()) for data in open(file)]

			found = False
			prod_lines = 0
			for x in entries:
				for y in entries:
					sum_lines = x + y
					if sum_lines == 2020:
						prod_lines = x * y
						found = True
						print("{} + {} = 2020".format(x, y))
						break
					#endif
				#endfor
				
				if found == True:
					break
				#endif
			#endfor

		except Exception as e:
			print("Exception: {}".format(e))
			return -1
		else:
			return prod_lines

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