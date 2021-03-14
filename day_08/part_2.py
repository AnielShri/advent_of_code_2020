#!/usr/bin/env python3


# imports
from os import terminal_size
import re
from typing import List

# globals
instruction_index = 0
accumulated_value = 0

# input data => 
#	[
#		[operator, value, prev_executed]
#		[operator, value, prev_executed]
#		...
#		[operator, value, prev_executed]
#	]
def load_data(input_file) -> List:
    regex = re.compile("(?P<operator>\w+) (?P<value>[+|\-\d]+)")
    data_input = []

    for line in open(input_file):
        parts = regex.match(line)
        data_input.append([
            parts.group("operator"),
            parts.group("value"),
            False
        ])
    return data_input


def acc(value):
    global accumulated_value
    global instruction_index
    accumulated_value += value
    instruction_index += 1
    # print("Accumulate: {}".format(value))


def jmp(value):
    global instruction_index
    instruction_index += value
    # print("Jump: {}".format(value))


def nop(value):
    global instruction_index
    instruction_index += 1
    # print("NOP: {}".format(value))


# script entry
if __name__ == "__main__":
    input_file = "day_08/input.txt"

    data = load_data(input_file)
    max_index = len(data)

    for n_fix in range(max_index):
        # reset for new program loop
        instruction_index = 0
        accumulated_value = 0
        data = [[instr, val, False] for instr, val, _ in data]

        while True:
            str_eval = ""

            # last instruction?
            if instruction_index == max_index:
                break 
            
            # get data @ current instruction_index
            item = data[instruction_index]

            # have we done this before?
            if item[2] is True:
                break

            # try to fix the bug
            if instruction_index == n_fix:
                if item[0] == "nop":
                    str_eval = "jmp({})".format(item[1])
                elif item[0] == "jmp":
                    str_eval = "nop({})".format(item[1])

            # if not done yet, generate the instruction set
            if str_eval == "":
                str_eval = "{}({})".format(item[0], item[1])
            eval(str_eval)
            item[2] = True
            # print("Instruction: {} @ {}".format(str_eval, instruction_index))
        # end while
        
        # check where we exited the program loop
        if instruction_index == max_index:
            fixed_instr = "jmp" if data[n_fix][0] == "nop" else "nop"
            print("Bug Fixed @ {} => {} to {} -> accumulated: {}".format(
                n_fix, data[n_fix][0], fixed_instr, accumulated_value
            ))
            break
        else:
            print("Bug persists @ {}, loop_index: {} => accumulated: {}".format(
                n_fix, instruction_index, accumulated_value))
    # end for
