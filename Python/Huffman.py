
from collections import Counter
from collections import OrderedDict

class Node:     #класс узелЖ имеет два листа - правый и левый
	def __init__(self, value, left = None, right = None):
		self.value = value
		self.left = left
		self.right = right

class Letter:
	def __init__(self, letter, code):
		self.letter = letter
		self.code = code		


def get_huffman_dict(statement):          # формирования словаря, включающего в себя символы исходного выражения и их количество 
	statement = Counter(statement)
	statement = OrderedDict(sorted(statement.items(), key = lambda t: t[1]))

	return statement


def get_huffman_nodes(statement):     # функция,задающая значения узла 
	order = list(statement.values())
	value = list(statement.keys())
	nodes = []
	m = 1
	L = len(order)
	while len(order) > 1:   # перебираем значения, пока они не закончатся    
		
		val = int(order[0]) + int(order[1])
		lft = value[0]   # заносим значения, встречающиеся реже в правый и левый лист бинарного дерева 
		rght = value[1]
		new_node = Node(val+m, lft, rght)   # создание нового элемента класса узел
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


def get_node_by_branch_value(value, nodes): # функция,для получения кода для правого и левого листа узла
	new_value = ''
	code = ''
	for i in range (len(nodes) -1, -1, -1): # пробегаем все узлы в обратном порядке
		if value == nodes[i].right:   # если это правый лист, то значение 1
			new_value = nodes[i].value
			code = '1'
		if value == nodes[i].left:      # если левый лист, то значение 0
			new_value = nodes[i].value
			code = '0'

	return new_value, code



def get_huffman_code(letter, nodes): # функция для получения кода для элемента исходного выражения
	Letter_code = ''
	Root = nodes[0]
	step = get_node_by_branch_value(letter, nodes)  # пошагово обход дерева с получением значения 0 или 1 в зависимости от листа
	Letter_code = Letter_code + step[1]

	while step[0] != Root.value:    # совершаем обход пока не окажемся в корне
		step = get_node_by_branch_value(step[0], nodes)
		Letter_code = Letter_code + step[1]

	Letter_code = Letter_code[::-1]   # код был в обратном порядке, разворот кода
	
	letter = Letter(letter, Letter_code) # объект класса letter

	return letter
		

statement = input('Введите слова: ') # запрос выражения у пользователя
raw = get_huffman_dict(statement)  # формирование словаря символов и частоты их употребления
used_letters = list(raw.keys())
nodes = get_huffman_nodes(raw)

for i in used_letters:  # обход всех элементов выражения
	symbol = get_huffman_code(i, nodes)


Encoded = ''
for i in statement:
	symbol = get_huffman_code(i, nodes)
	Encoded = Encoded + symbol.code + ' '

print('Закодированное выражение: ', Encoded)




