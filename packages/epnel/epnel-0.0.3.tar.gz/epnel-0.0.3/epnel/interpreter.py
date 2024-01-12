from .parser import AST_Node

symbol_table = dict()

def operator(node):
	if node.value == "+":
		return interpret(node.children[0]) + interpret(node.children[1])
	elif node.value == "-":
		return interpret(node.children[0]) - interpret(node.children[1])
	elif node.value == "*":
		return interpret(node.children[0]) * interpret(node.children[1])
	elif node.value == "/":
		return interpret(node.children[0]) // interpret(node.children[1])
	elif node.value == "<":
		return interpret(node.children[0]) < interpret(node.children[1])
	elif node.value == ">":
		return interpret(node.children[0]) > interpret(node.children[1])
	elif node.value == "|":
		return interpret(node.children[0]) | interpret(node.children[1])
	elif node.value == "^":
		return interpret(node.children[0]) ^ interpret(node.children[1])
	elif node.value == "&":
		return interpret(node.children[0]) & interpret(node.children[1])
	elif node.value == "=":
		return interpret(node.children[0]) == interpret(node.children[1])
	else:
		raise Exception("invalid operator", node)

def conditional(node):
	if interpret(node.children[0]):
		return interpret(node.children[1])
	else:
		return interpret(node.children[2])

def assignment(node):
	key = node.children[0]
	if key.type == "number":
		key = key.value
	else:
		key = str(interpret(key))
	if node.value == ".":
		symbol_table[key] = interpret(node.children[1])
		return symbol_table[key]
	elif node.value == ",":
		symbol_table[key] = node.children[1]
		return interpret(node.children[2])
	elif node.value == ":":
		key = str(number(AST_Node(key, "number")))
		return number(AST_Node(key, "number"))
	else:
		raise Exception("invalid assignment", node)

def boolean(node):
	return False

def number(node):
	if node.value in symbol_table:
		if isinstance(symbol_table[node.value], AST_Node):
			return interpret(symbol_table[node.value])
		else:
			return symbol_table[node.value]
	if node.value.isnumeric():
		return int(node.value)
	return 0

# tree-walking interpreter
def interpret(node):
	if node.type == "operator":
		return operator(node)
	elif node.type == "conditional":
		return conditional(node)
	elif node.type == "assignment":
		return assignment(node)
	elif node.type == "boolean":
		return boolean(node)
	elif node.type == "number":
		return number(node)
	else:
		raise Exception("invalid type", node)
