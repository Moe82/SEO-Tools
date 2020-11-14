import csv
from pathlib import Path

root = "data/"

def parse_file(filename):
    """Returns content of file as a list or dictionary
    :param filename: filename (including file extension)
    :return: a list containing the contents of each line if filename ends in .txt, otherwise a dictionary corresponding to the content if filename ends in .cvs 
    """
    filepath = root + filename
    try:
        if filename.endswith('.txt'):
            with open(filepath) as file:
                return file.read().splitlines()
        elif filename.endswith('.csv'):
            reader = csv.reader(open(filepath))
            result = {}
            for row in reader:
                key = row[0]
                result[key] = row[1]
            return result
    except FileNotFoundError:
        with open(filepath,"w+") as file:
            append_string_to_textfile(filename, "Placeholder")
            print("here")
            return (parse_file(filename))

def search_file(filename, term):
    """searches content of a .txt file for a term 
    :param filename: filename (including file extension)
    :param term: term to search for
    :return: true is term is found in file, otherwise false 
    """
    try:
        filepath = root + filename
        with open(filepath) as file:
            return term in file.read().splitlines()
    except FileNotFoundError:
        with open(filepath,"w+") as file:
            return (search_file(filename, term))

def append_string_to_textfile(filename, string):
    """appends a string to the end of the .txt file on a new line 
    :param filename: full filename including extension
    :param term: string to append 
    """
    filepath = root + filename
    with open(filepath, 'a+') as file:
        file.write(string + "\n")

def append_dict_to_csv_file(filename, dictionary):
    filepath = root + filename
    if Path(filepath).is_file():
        with open(filepath, 'a') as file:
            fieldnames =  list(dictionary.keys())
            dict_writer = csv.DictWriter(file, fieldnames = fieldnames)
            dict_writer.writerow(dictionary)
    else:
        with open(filepath, 'w', newline='') as file:
            fieldnames = list(dictionary.keys())
            writer = csv.DictWriter(file, delimiter=',', lineterminator='\n',fieldnames=fieldnames)
            writer.writeheader();
            return (append_dict_to_csv_file(filename, dictionary))
