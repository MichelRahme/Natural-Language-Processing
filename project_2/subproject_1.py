import os
import string

from bs4 import BeautifulSoup
import re
from nltk.tokenize import word_tokenize
import ast


def process_files(path):
    listF = []
    for file in os.listdir(path):
        if file.endswith(".sgm"):
            filename = os.path.join(path, file)  # join the file with the full path
            f = open(filename, 'r', encoding='utf-8', errors='ignore')
            reuters_file_content = f.read()  # read the file into a string
            s = BeautifulSoup(reuters_file_content, "lxml")  # parse the .SGM string
            file_content = s.find_all('reuters')  # find all occurrences of the <reuters> tag unique to each document

            for document in file_content:
                docID = document['newid']
                text = document.find('text').text
                # tokenize the text
                tokens = word_tokenize(text)

                for token in tokens:
                    if not re.fullmatch('[' + string.punctuation + ']+', token):
                        if not re.search("\^[a-z]?", token, flags=re.IGNORECASE) and not re.match("'[a-zA-Z]", token):
                            if not re.match('(reuter?[a-zA-Z])', token, flags=re.IGNORECASE):
                                listF.append((token, docID))
    return listF


def sort_list(listF):
    for i in listF:
        # transform string to List; slow but accurate
        input_list = ast.literal_eval(i)
        # Remove duplicates using Set()
        sorted_list = list(set(input_list))
        # Sort the list based on token (alphanumerically)
        sorted_list.sort(key=lambda x: x[0])
        return sorted_list


def postings_list(sorted_list):
    inverted_index = {}
    sorted_tuples = []
    for input_list in sorted_list:
        # Turn string input into list
        sorted_tuples = ast.literal_eval(input_list)
    for entry in sorted_tuples:
        # Set initial word frequency
        frequency = 1
        # Check if token is not already in inverted_index
        # if it's not then add it, along with frequency 1, and DocID
        if entry[0] not in inverted_index:
            inverted_index[entry[0]] = [frequency, [entry[1]]]
        # if tuple is in inverted index
        else:
            # get the list of docID's for that tuple 
            list_of_docs = inverted_index.get(entry[0])
            # make sure docID is not already recorded, if not then add docID into list
            if entry[1] not in list_of_docs[1]:
                list_of_docs[0] = list_of_docs[0] + 1
                list_of_docs[1].append(entry[1])
                inverted_index[entry[0]] = list_of_docs
    # print(inverted_index, file=open("data/index.txt", 'w'))
    return inverted_index
