import argparse
from os.path import exists

parser = argparse.ArgumentParser(description='Transpile JASM to a VOLE program.')
parser.add_argument('source', type=str)
parser.add_argument('destination', type=str)
args = parser.parse_args()

instructions = [
	'LOAD',
	'LOADLITERAL',
	'STORE',
	'MOVE',
	'ADDINT',
	'ADDFLOAT',
	'OR',
	'AND',
	'XOR',
	'ROTATE',
	'JUMP',
	'HALT'
]
def get_instr(word: str) -> str:
	return hex(instructions.index(word.upper())+1)[2:]

def r_pad(s: str, length: int):
	while len(s) < length:
		s += '0'
	return s

def convert_line(l: str):
	words = l.split(' ')
	instr = get_instr(words[0])
	out = [instr, *words[1:]]
	code = ''.join(out)
	final = r_pad(code, 4)
	return final

with open(args.source, 'r') as in_file:
	src_lines = in_file.read().splitlines()

out_strings = ['[PC]C0', '[C0]']
out_strings += [convert_line(line) for line in src_lines]

with open(args.destination, 'w' if exists(args.destination) else 'x') as out_file:
	out_file.write('\n'.join(out_strings))