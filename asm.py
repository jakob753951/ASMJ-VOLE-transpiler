import argparse
from os.path import exists
from compiler import compile_vole

parser = argparse.ArgumentParser(description='Transpile ASMJ to a VOLE program.')
parser.add_argument('source', type=str)
parser.add_argument('destination', type=str)
parser.add_argument('-s', '--starting_position', type=str, default='C0')
args = parser.parse_args()

with open(args.source, 'r') as in_file:
	src_txt = in_file.read()

starting_position = int(args.starting_position, 16)
vole_code = compile_vole(src=src_txt, start_pos=starting_position)

with open(args.destination, 'w' if exists(args.destination) else 'x') as out_file:
	out_file.write(vole_code)