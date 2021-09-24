import argparse
from os.path import exists
from compiler import compile_vole

parser = argparse.ArgumentParser(description='Transpile ASMJ to a VOLE program.')
parser.add_argument('source', type=str)
parser.add_argument('destination', type=str)
parser.add_argument('-s', '--program-starting-position', type=str, default='00')
parser.add_argument('-v', '--variables-starting-position', type=str, default='C0')
args = parser.parse_args()

with open(args.source, 'r') as in_file:
	src_txt = in_file.read()

vole_code = compile_vole(src_txt, int(args.starting_position, 16))

with open(args.destination, 'w' if exists(args.destination) else 'x') as out_file:
	out_file.write(vole_code)