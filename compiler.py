import re
from variable import Variable


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

marks: dict[str, int] = {}

variables: list[Variable] = []

def set_marks(lines: list[str], start_pos: int):
	out_lines = []
	i = 0
	for line in lines:
		match = re.search(r'\S+(?=:\s?)', line)
		if match:
			marks[match[0]] = i + start_pos
			continue
		out_lines.append(line)
		i += 2
	return out_lines

def int_2_hex(num: int) -> str:
	return hex(num)[2:].upper()

def op_2_code(operator: str) -> str:
	return hex(operators.index(operator)+5)[2:]

def addr_value(word: str) -> str:
	match = re.search(r'(?<=\[)[0-9a-fA-F]{2}(?=\])', word)
	if not match:
		return None
	return match[0]


def get_arg_type(word: str) -> ARG_TYPE:
	if addr_value(word):
		return ARG_TYPE.ADDRESS
	if len(word) == 1:
		return ARG_TYPE.REGISTER
	return ARG_TYPE.LITERAL

def move(words: list[str]) -> str:
	src_type, dst_type = [get_arg_type(word) for word in words[1:]]
	if src_type == ARG_TYPE.ADDRESS and dst_type == ARG_TYPE.REGISTER:
		return f'1{words[2]}{addr_value(words[1])}'
	if src_type == ARG_TYPE.LITERAL and dst_type == ARG_TYPE.REGISTER:
		return f'2{words[2]}{words[1]}'
	if src_type == ARG_TYPE.REGISTER and dst_type == ARG_TYPE.ADDRESS:
		return f'3{words[1]}{addr_value(words[2])}'
	if src_type == ARG_TYPE.REGISTER and dst_type == ARG_TYPE.REGISTER:
		return f'40{words[1]}{words[2]}'
	raise ValueError('Address not read correctly')

def operator(words: list[str]) -> str:
	operator, a, b, dest = words
	return f'{op_2_code(operator)}{dest}{a}{b}'

def rotate(words: list[str]) -> str:
	return f'A{words[1]}0{words[2]}'

def jump(words: list[str]) -> str:
	is_conditional = words[0].upper() == 'CJUMP'

	dest_mark = words[2 if is_conditional else 1]

	dest_str = int_2_hex(marks[dest_mark])

	return f'B{words[1] if is_conditional else 0}{dest_str}'

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
	'CJUMP': jump,
	'HALT': lambda _: 'C000',
	'HCF': halt_and_catch_fire,
	'HACF': halt_and_catch_fire
}

def convert_line(l: str):
	l = l.split('//')[0] #Ignore comments
	l.replace(',', '')   #Remove commas
	words = l.strip().split(' ')
	return instructions[words[0]](words)

def compile_vole(src: str, start_pos: int):
	src_lines = src.splitlines()
	src_lines = set_marks(src_lines, start_pos)
	start_str = int_2_hex(start_pos)
	out_lines = [f'[PC]{start_str}', f'[{start_str}]']
	out_lines.extend([convert_line(line) for line in src_lines])
	return '\n'.join(out_lines).upper()
