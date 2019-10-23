# Написать программу сложения и умножения двух шестнадцатеричных чисел. 
# При этом каждое число представляется как массив, элементы которого это цифры числа. 
# Например, пользователь ввёл A2 и C4F. Сохранить их как [‘A’, ‘2’] и [‘C’, ‘4’, ‘F’] 
# соответственно. Сумма чисел из примера: [‘C’, ‘F’, ‘1’], 
# произведение - [‘7’, ‘C’, ‘9’, ‘F’, ‘E’

from collections import deque
import collections
import string



def dec_to_hex(number):
	for i in range (0, len(number)):
		if number[i] in HEX:
			number[i] = HEX.get(number[i])
	return number

def get_letters(number):
	for i in range (0, len(number)):
		if number[i] > 9:
			number[i] = DEC.get(number[i])
	return number

def summ_hex(first, second):
	first = dec_to_hex(first)
	second = dec_to_hex(second)
	first = collections.deque(first) 
	second = collections.deque(second)
	first.reverse()
	second.reverse()

	summ_hex = deque()

	for i in range (0, len(second)):
		summ = int(first[i]) + int(second[i])
		summ_hex.appendleft(summ)

	for i in range (len(second), len(first)):
		summ_hex.appendleft(int(first[i]))

	for i in range (len(summ_hex) - 1, -1, -1):
		if summ_hex[i] >= 16:
			if (i - 1) > -1:
				summ_hex[i-1] = int(summ_hex[i-1]) + 1
				summ_hex[i] = summ_hex[i] - 16
			else:
				summ_hex[i] = summ_hex[i] - 16
				summ_hex.appendleft(1)

	return list(summ_hex)


def mult_hex(first, second):
	first = dec_to_hex(first)
	second = dec_to_hex(second)
	first = collections.deque(first) 
	second = collections.deque(second)
	first.reverse()
	second.reverse()

	mult_hex = []

	for j in range (0, len(second)):
		temp_mult = deque()
		for i in range (0, len(first)):
			mult = int(first[i])*(int(second[j])*16**j)
			temp_mult.appendleft(mult)

		for i in range (len(temp_mult) - 1 , -1, -1):
			if temp_mult[i] > 15:
				if i > 0:
					temp_mult[i-1] = temp_mult[i-1] + temp_mult[i]//16
					temp_mult[i] = temp_mult[i] % 16
				else:
					while temp_mult[i] > 15:
						temp_mult.appendleft(temp_mult[i]//16)
						temp_mult[i+1] = temp_mult[i+1] % 16

		temp_mult = list(temp_mult)
		mult_hex = summ_hex(temp_mult, mult_hex)

	return list(mult_hex)


first = list(input('Введите первое шестнадцатиричное число: ').upper())
second = list(input('Введите второе шестнадцатиричное число: ').upper())


LETTERS = ['A','B','C','D','E','F']
VALUES = [i for i in range (10, 16)]

HEX = dict(zip(LETTERS, VALUES))
DEC = dict(zip(VALUES, LETTERS))

if len(first) >= len(second):
	summ = summ_hex(first, second)
	mult = mult_hex(first, second)
else:
	summ = summ_hex(second, first)
	mult = mult_hex(second, first)

summ = get_letters(summ)
mult = get_letters(mult)

print('Сумма чисел равна: ', summ)
print('произведение', mult)