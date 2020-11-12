import csv
from pathlib import Path

root = "data/"

def parseFile(filename):
	"""Returns content of file as a list or dictionary
	:param filename: filename (including file extension)
	:return: a list containing the contents of each line if filename ends in .txt, otherwise a dict corresponding to the content if filename ends in .cvs 
	"""
	filepath = root + filename
	try:
		if filename.endswith('.txt'):
			file = open(filepath)
			return file.read().splitlines()
		elif filename.endswith('.csv'):
			reader = csv.reader(open(filepath))
			result = {}
			for row in reader:
			    key = row[0]
			    result[key] = row[1]
			return result
	except FileNotFoundError:
		open(filepath,"w+").close()

def searchFile(filename, term):
	"""searches content of a .txt file for a term 
	:param filename: filename (including file extension)
	:param term: term to search for
	:return: true is term is found in file, otherwise false 
	"""
	try:
		filepath = root + filename
		file = open(filepath)
		return term in file.read().splitlines()
		file.close()
	except FileNotFoundError:
		open(filepath,"w+").close()

def appendStringToFile(filename, string):
	"""appends a string to the end of the .txt file on a new line 
	:param filename: full filename including extension
	:param term: string to append 
	"""
	filepath = root + filename
	file = open(filepath, 'a+')
	file.write(string + "\n")
	file.close()

def appendDictToFile(filename, dict):
	filepath = root + filename
	if Path(filepath).is_file():
		file = open(filepath, 'a') 
		fieldnames =  list(dict.keys())
		dict_writer = csv.DictWriter(file, fieldnames = fieldnames)
		dict_writer.writerow(dict)
	else:
		with open(filepath, 'w', newline='') as file:
			fieldnames = list(dict.keys())
			writer = csv.DictWriter(file, delimiter=',', lineterminator='\n',fieldnames=fieldnames)
			writer.writeheader();