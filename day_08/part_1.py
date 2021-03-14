#!/usr/bin/env python3


# imports
from typing import List

# globals
instruction_index = 0
accumulated_value = 0

# input data => 
#	[
#		[operator(value), prev_executed]
#		[operator(value), prev_executed]
#		...
#		[operator(value), prev_executed]
#	]
def load_data(input_file) -> List:
    input_data = [
        [
            "{})".format(instruction.rstrip().replace(" ", "(")),
            False
        ]
        for instruction in open(input_file)
        ]
    return input_data


def acc(value):
    global accumulated_value
    global instruction_index
    accumulated_value += value
    instruction_index += 1
    print("Accumulate: {}".format(value))


def jmp(value):
    global instruction_index
    instruction_index += value
    print("Jump: {}".format(value))


def nop(value):
    global instruction_index
    instruction_index += 1
    print("NOP: {}".format(value))


# script entry
if __name__ == "__main__":
    input_file = "day_08/input.txt"

    data  = load_data(input_file)

    while True:
        item = data[instruction_index]

        # have we done this before?
        if item[1] is True:
            break

        # if not, execute
        eval(item[0])
        item[1] = True
    
    # result
    print("Accumulated: {}".format(accumulated_value))