import argparse
from os.path import exists
import re

parser = argparse.ArgumentParser(description='Transpile JASM to a VOLE program.')
parser.add_argument('source', type=str)
parser.add_argument('destination', type=str)
args = parser.parse_args()

class ARG_TYPE:
	ADDRESS  = 0
	LITERAL  = 1
	REGISTER = 2

operators = [
	'IADD',
	'FADD',
	'OR',
	'AND',
	'XOR'
]

def op_2_code(operator: str) -> str:
	return hex(operators.index(operator)+5)[2:]

def addr_value(word: str) -> str:
	match = re.search(r'(?<=\[)[0-9a-fA-F]{2}(?=\])', word)
	if not match:
		return None
	return match[0]


def get_arg_type(word):
	if addr_value(word):
		return ARG_TYPE.ADDRESS
	if len(word) == 1:
		return ARG_TYPE.REGISTER
	return ARG_TYPE.LITERAL

def move(words):
	src_type, dst_type = [get_arg_type(word) for word in words[1:]]
	if src_type == ARG_TYPE.ADDRESS and dst_type == ARG_TYPE.REGISTER:
		return f'1{words[2]}{addr_value(words[1])}'
	if src_type == ARG_TYPE.LITERAL and dst_type == ARG_TYPE.REGISTER:
		return f'2{words[2]}{words[1]}'
	if src_type == ARG_TYPE.REGISTER and dst_type == ARG_TYPE.ADDRESS:
		return f'3{words[1]}{addr_value(words[2])}'
	if src_type == ARG_TYPE.REGISTER and dst_type == ARG_TYPE.REGISTER:
		return f'40{words[1]}{words[2]}'

def operator(words: list[str]):
	operator, a, b, dest = words
	return f'{op_2_code(operator)}{dest}{a}{b}'

def rotate(words):
	return f'A{words[1]}0{words[2]}'

def jump(words): # JUMP R [XY] = BRXY
	dest = addr_value(words[2])
	if not dest:
		raise Exception('Address not read correctly')
	return f'B{words[1]}{dest}'

def halt_and_catch_fire(_):
	pass

instructions = {
	'MOVE': move,
	'IADD': operator,
	'FADD': operator,
	'OR': operator,
	'AND': operator,
	'XOR': operator,
	'ROTATE': rotate,
	'JUMP': jump,
	'HALT': lambda _: 'C000',
	'HCF': halt_and_catch_fire
}
def r_pad(s: str, length: int):
	while len(s) < length:
		s += '0'
	return s

def convert_line(l: str):
	l = l.split('//')[0] #Ignore comments
	l.replace(',', '')   #Remove commas
	words = l.split(' ')
	return instructions[words[0]](words)

with open(args.source, 'r') as in_file:
	src_lines = in_file.read().splitlines()

out_strings = ['[PC]C0', '[C0]']
out_strings += [convert_line(line) for line in src_lines]

with open(args.destination, 'w' if exists(args.destination) else 'x') as out_file:
	out_file.write('\n'.join(out_strings))