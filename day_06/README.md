# Day 6 - Part 1

Algorihm is fairly straight forward. 

* The algorithm first creates a 26-length, zero-initialized array. 
* It then goes through the answers of each person, and sets the value of the corresponding letter index to 1. Example:
	* `all_answers[0] = 1` for `letter = 'a'`
	* `all_answers[1] = 1` for `letter = 'b'`
	* ...
	* `all_answers[25] = 1` for `letter = 'z'`
* This has the following consequence:
	* If the previous value was 0 -> new value = 1
	* if the previous value was 1 -> new value is still equal to 1
	* In other words: the index value can only be 0 or 1, effectively counting only unique answers
* At the end of the loop the sum of the answer array is calculated to determine the total number of unique answers

```python

	# group analysis
	def _unique_answers(self, item:str) -> int:
		# needed a few times, so calculate once and store in memory		
		ord_a = ord("a") 

		# 26 length zero-initialized array		
		all_answers = [0] * (ord("z") - ord_a + 1) 

		# loop
		for letter in item.replace("\n", ""):	
			# set the index value corresponding to letter equal to 1
			# if the previous value was 0 -> new value = 1
			# if the previous value was 1 -> new value = 1
			all_answers[ord(letter) - ord_a] = 1 

		# in the end we need the sum of all unique answers
		return sum(all_answers)

	# public function
	def execute(self, filename: Optional[str] = None) -> int:
		entries = self._load_data(filename) # loads data
		yes_count = 0 

		# loop through every group of answers and calculate sum of uniques
		for item in entries:
			yes_count += self._unique_answers(item)

		return yes_count

```