# Day 6

##  Part 1

Algorihm is fairly straight forward. 

For each group:
* The algorithm creates a 26-length, zero-initialized array. 
* It then merges all the answers from the group into one string by replacing the newline character
* Starting at the fist letter of the string, the value of the array at the corresponding letter index is set to 1. Example:
	* `all_answers[0] = 1` for `letter = 'a'`
	* `all_answers[1] = 1` for `letter = 'b'`
	* ...
	* `all_answers[25] = 1` for `letter = 'z'`
* This has the following consequence:
	* If the previous value was 0 -> new value = 1
	* if the previous value was 1 -> new value is still equal to 1
	* In other words: the index value can only be 0 or 1, effectively counting only unique answers
* The answer array for the group bellow is: `[0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0]` 
```
dcqgyiflm
gqcfn
fcqgwnh
qpgfkhbc
```
* Letter value at array index is done for every character in the merged string
* At the end of the loop the sum of the answer array is calculated to determine the total number of unique answers

### Code implementation

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

---

## Part 2

Part 2 is solved using binary operations

For each group:

* An initial group answer is selected where all 26 options are chosen => `0x03FFFFF` or `0b0011 1111 1111 1111 1111 1111 1111`
* For each person's answer:
	* The bit corresponding to the letter value is set equal to `1`
		* `a` -> `answer = 0b1`
		* `b` -> `answer = 0b10`
		* ...
		* `z` -> `answer = 0b0010 0000 0000 0000 0000 0000 0000`
	* This is repeated for each letter in the answer
	* For example, the individual answer `fcqgwnh` is represented by the binary value of `0b0000 0100 0001 0010 0000 1110 0100`
* Once the binary value of a person's answer is determined, this value is combined with the group total using an `AND` operation. This will ensure that only the bits ( -> yes) that are set in all to `1` for every person in the group will end up in the final value of the group total
* Since the end result requires counting the bits that are equal to `1`, we use some additional bit manipulation
	* Starting at the `0th`, all other bits are set to equal to `0`, except the `0th` bit. 
	* The value of this bit is then added to the `sum_total` of the group
	* Next, the `1st` bit is shifted to `position bit 0`, after all other bits have been set to `0`. The value is also added to the `sum_total` of the group
	* This is repeated for all 26 bits 
* The final value of unique `yes` answers equals to the value calculated in the previous step.


```python
	def _unique_answers(self, item:str) -> int:
		ord_a = ord("a")
		all_answers = item.split("\n") # splits the string in answer/person
		group_total = 0x03FFFFFF # initial assumption: all answers are `yes`

		# loop over each person's answers
		for inidividual_answer in all_answers:
			# edge case for emty array item (last group) -> causes group_total = 0
			if len(inidividual_answer) == 0: 
				continue
			
			answers = 0 # start with empty value to push results into

			# loop over each letter
			for letter in inidividual_answer:
				# sets the bit value at position of letter to 1
				answers = answers | (1 << (ord(letter) - ord_a))

			# finally the answers for the current person is added to total
			group_total = group_total & answers

		total_unique = 0
		# to count each bit value, all bits but the current index is set equal to 0
		# this bit is then shifted to the 0th position and added to the total
		for bit in range(26):
			total_unique += (group_total & (1 << bit)) >> bit)
		
		return total_unique


	# public function, same as for part 1
	def execute(self, filename: Optional[str] = None) -> int:
		entries = self._load_data(filename)
		yes_count = 0

		for item in entries:
			yes_count += self._unique_answers(item)

		return yes_count
```
