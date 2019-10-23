
from collections import Counter
from collections import OrderedDict

class Node:
	def __init__(self, value, left = None, right = None):
		self.value = value
		self.left = left
		self.right = right

class Letter:
	def __init__(self, letter, code):
		self.letter = letter
		self.code = code		


def get_huffman_dict(statement):
	statement = Counter(statement)
	statement = OrderedDict(sorted(statement.items(), key = lambda t: t[1]))

	return statement


def get_huffman_nodes(statement):
	order = list(statement.values())
	value = list(statement.keys())
	# print(order)
	# print(value)
	nodes = []
	m = 1
	L = len(order)
	while len(order) > 1:
		
		val = int(order[0]) + int(order[1])
		lft = value[0]
		rght = value[1]
		new_node = Node(val+m, lft, rght)
		nodes.append(new_node)
		order.pop(1)
		order.pop(0)
		order.append(val+m)
		order.sort()
		value.pop(1)
		value.pop(0)
		value.insert(order.index(val+m), val+m)

		L = int(L/2)
		m = m + L


	nodes.reverse()
	return nodes


def get_node_by_branch_value(value, nodes):
	new_value = ''
	code = ''
	for i in range (len(nodes) -1, -1, -1):
		if value == nodes[i].right:
			new_value = nodes[i].value
			code = '1'
		if value == nodes[i].left:
			new_value = nodes[i].value
			code = '0'

	return new_value, code



def get_huffman_code(letter, nodes):
	Letter_code = ''
	Root = nodes[0]
	step = get_node_by_branch_value(letter, nodes)
	Letter_code = Letter_code + step[1]

	while step[0] != Root.value:
		step = get_node_by_branch_value(step[0], nodes)
		Letter_code = Letter_code + step[1]

	Letter_code = Letter_code[::-1]
	
	letter = Letter(letter, Letter_code)

	return letter
		

statement = input('Введите слова: ')
raw = get_huffman_dict(statement)
used_letters = list(raw.keys())
nodes = get_huffman_nodes(raw)

for i in used_letters:
	symbol = get_huffman_code(i, nodes)
	print(symbol.letter, symbol.code)

Encoded = ''
for i in statement:
	symbol = get_huffman_code(i, nodes)
	Encoded = Encoded + symbol.code + ' '

print('Закоированное выражение: ', Encoded)




