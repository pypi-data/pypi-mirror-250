import argparse

from .parser import Parser
from .interpreter import interpret

def repl(prompt=":) "):
	while True:
		try:
			_in = input(prompt)
		except:
			break
		p = Parser(string=_in)
		print(interpret(p.root()))

def interpret_file(fname):
	f = open(fname)
	p = Parser(input_file=f)
	while not p.empty():
		print(interpret(p.next()))
	f.close()

def cli():
	ap = argparse.ArgumentParser(description="Educational Polish Notation Evaluation Language interpreter with REPL")
	ap.add_argument("input", nargs="?", help="path to your input file")
	args = ap.parse_args()
	if args.input:
		interpret_file(args.input)
	else:
		repl()

if __name__ == "__main__":
	repl()
