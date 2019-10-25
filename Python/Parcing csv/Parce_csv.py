
from os import listdir
from os.path import isfile, join
import csv
import json
from pprint import pprint

def get_data(filename, dataset):  # функция для получения данных типа "dataset" из файла "filename"
	with open('Data/' + filename) as f:  # открытие файла
		for line in f:                # пробегаем все строки
			if line.startswith(dataset[0]):    # по ключевым словам определяем тип и записываем в соотв. категорию
				prod = line.replace(dataset[0],'')
			elif line.startswith(dataset[1]):
				name = line.replace(dataset[1],'')
			elif line.startswith(dataset[2]):
				code = line.replace(dataset[2],'')
			elif line.startswith(dataset[3]):
				tpe = line.replace(dataset[3],'')
	return prod, name, code, tpe


def write_to_csv(filename, dataset, headers):  # запись в формате csv
	with open (filename, 'w') as file:
		writer = csv.DictWriter(file, fieldnames = headers)
		writer.writeheader()
		for row in dataset:
			writer.writerow(row)


def read_from_csv(filename):                    # чтение из формата CSV
	with open (filename) as file:
		reader= csv.DictReader(file)
		csv_data = []
		for row in reader:
			csv_data.append(row)
	return csv_data


def write_to_json(filename, dataset):            # запись в формате json
	with open(filename, 'w') as file:
		json.dump(dataset, file)


def read_from_json(filename):                  # чтение из формата CSV
	with open (filename) as file:
		json_data = json.load(file)
	return json_data


CATEGORIES = ['Изготовитель системы: ', "Название ОС:", "Код продукта:", "Тип системы:"]     # интересующие категории

textfiles = [f for f in listdir("Data") if isfile(join("Data", f)) and f.endswith('.txt')]   # поиск .txt файлов в папке

data_sorted = []

for file in textfiles :    # для каждого файла осуществляется разбиение данных по категориям
	data = get_data(file, CATEGORIES)
	data_dict = dict(zip(CATEGORIES, data))
	data_sorted.append(data_dict)

csv_file = write_to_csv('sorted.csv', data_sorted, CATEGORIES)  # конвертация в csv
csv_data = read_from_csv('sorted.csv')

json_file = write_to_json('sorted.json', csv_data)               # конвертация в json
json_data = read_from_json('sorted.json')
pprint(json_data)
