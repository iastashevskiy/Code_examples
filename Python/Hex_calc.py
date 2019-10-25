# Написать программу сложения и умножения двух шестнадцатеричных чисел без использования встроенных преобразователей Python. 
# При этом каждое число представляется как массив, элементы которого это цифры числа. 
# Например, пользователь ввёл A2 и C4F. Сохранить их как [‘A’, ‘2’] и [‘C’, ‘4’, ‘F’] 
# соответственно. Сумма чисел из примера: [‘C’, ‘F’, ‘1’], 
# произведение - [‘7’, ‘C’, ‘9’, ‘F’, ‘E’]

from collections import deque
import collections
import string



def dec_to_hex(number):                               #функция для перевода числа из десятичной системы в шестнадцатиричную
	for i in range (0, len(number)):
		if number[i] in HEX:
			number[i] = HEX.get(number[i])
	return number

def get_letters(number):                             # функция для преобразования значений 10-15 в шестнадцатиричные A-F
	for i in range (0, len(number)):
		if number[i] > 9:
			number[i] = DEC.get(number[i])
	return number

def summ_hex(first, second):                      # функция, суммирующая шестнадцатиричные числа
	first = dec_to_hex(first)                 # перевод десятичных чисел в шестнадцатиричные (так как по условиям нельзя пользоваться
	second = dec_to_hex(second)		  # функцией сложения шестнадцатиричных чисел)
	first = collections.deque(first)          # запись в виде списка
	second = collections.deque(second)
	first.reverse()
	second.reverse()

	summ_hex = deque()

	for i in range (0, len(second)):     # получаем сумму в виде списка, где каждый элемент - сумма соответвующих элементов слагаемых
		summ = int(first[i]) + int(second[i])
		summ_hex.appendleft(summ)

	for i in range (len(second), len(first)): #добавляем к нему элементы первого слагаемого с разрядностью больше чем разрядность второго
		summ_hex.appendleft(int(first[i]))

	for i in range (len(summ_hex) - 1, -1, -1):           # пробегаем список суммы в обратном порядке
		if summ_hex[i] >= 16:                       # если значение элемента больше 16, то переносим единицу на разряд выше
			if (i - 1) > -1:
				summ_hex[i-1] = int(summ_hex[i-1]) + 1
				summ_hex[i] = summ_hex[i] - 16
			else:                           # если это элемент с высшей разрядности, приписываем единицу слева
				summ_hex[i] = summ_hex[i] - 16
				summ_hex.appendleft(1)

	return list(summ_hex)


def mult_hex(first, second):   		# Функция для умножения шестнадцатиричных чисел
	first = dec_to_hex(first)       # перевод десятичных чисел в шестнадцатиричные (так как по условиям нельзя пользоваться
	second = dec_to_hex(second)     # функцией сложения шестнадцатиричных чисел)
	first = collections.deque(first) # запись в виде списка
	second = collections.deque(second)
	first.reverse()
	second.reverse()

	mult_hex = []

	for j in range (0, len(second)):       # произведение в виде словаря, элементами которого являются произведение соотв. элементов множителей
		temp_mult = deque()
		for i in range (0, len(first)):
			mult = int(first[i])*(int(second[j])*16**j)
			temp_mult.appendleft(mult)

		for i in range (len(temp_mult) - 1 , -1, -1):           # пробегаем результат справа налево
			if temp_mult[i] > 15:                           # если элемент больше 15 и не может быть записан как один разряд в шестнадцатиричном
				if i > 0:                               # делим его на 16 и переносим соотв. значение на разряд выше
					temp_mult[i-1] = temp_mult[i-1] + temp_mult[i]//16
					temp_mult[i] = temp_mult[i] % 16
				else:                                   # для элемента с наибольшей разрядностю (левого)
					while temp_mult[i] > 15:        # до тех пор, пока не станет меньше 16
						temp_mult.appendleft(temp_mult[i]//16)           # приписываем слева еще один регистр
						temp_mult[i+1] = temp_mult[i+1] % 16 # делим второй (был первым до приписывания) элемент на 16

		temp_mult = list(temp_mult)
		mult_hex = summ_hex(temp_mult, mult_hex)

	return list(mult_hex)


first = list(input('Введите первое шестнадцатиричное число: ').upper())   # запрос чисел у пользователя и перевод их в верхний регистр
second = list(input('Введите второе шестнадцатиричное число: ').upper())


LETTERS = ['A','B','C','D','E','F']                     # формирование словарей соответствия для значений от 10 до 15
VALUES = [i for i in range (10, 16)]

HEX = dict(zip(LETTERS, VALUES))
DEC = dict(zip(VALUES, LETTERS))

if len(first) >= len(second):          # функции суммы и умножения в первую принимают число с большей разрядностью. Определяем его и
				       # подаем соответствующее первым
	summ = summ_hex(first, second)
	mult = mult_hex(first, second)
else:
	summ = summ_hex(second, first)
	mult = mult_hex(second, first)

summ = get_letters(summ)
mult = get_letters(mult)

print('Сумма чисел равна: ', summ)      # вывод результатов
print('произведение', mult)
