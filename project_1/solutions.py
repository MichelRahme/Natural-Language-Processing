"""
Write your reusable code here.
Main method stubs corresponding to each block is initialized here. Do not modify the signature of the functions already
created for you. But if necessary you can implement any number of additional functions that you might think useful to you
within this script.

Delete "Delete this block first" code stub after writing solutions to each function.

Write you code within the "WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv" code stub. Variable created within this stub are just
for example to show what is expected to be returned. You CAN modify them according to your preference.
"""

import os
import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

def block_reader(path):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    # Look for all .SGM files
    for file in os.listdir(path):
        if file.endswith(".sgm"):
            filename = os.path.join(path, file)  # join the file with the full path
            f = open(filename, 'r', encoding='utf-8', errors='ignore')
            reuters_file_content = f.read()  # read the file into a string
            yield reuters_file_content
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_document_segmenter(INPUT_STRUCTURE):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    for reutersSGM in INPUT_STRUCTURE:
        s = BeautifulSoup(reutersSGM, "lxml")  # parse the .SGM string
        file_content = s.find_all('reuters')  # find all occurrences of the <reuters> tag unique to each document
        # segment each document in .SGM string into a standalone String
        for document in file_content:
            document = str(document)
            document = document.replace("reuters", "REUTERS")
            yield document
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_extractor(INPUT_STRUCTURE):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    content_dict = {}
    documentID = 0
    for dirtyDocument in INPUT_STRUCTURE:
        documentID = documentID + 1
        s = BeautifulSoup(dirtyDocument, "lxml")
        document = s.find('text')
        document = document.text
        # Remove everything except alphabetical characters then lowercase
        document = re.sub(r'[^a-zA-Z\s]', '', document).lower()
        # Remove all occurrences of the word reuter
        document = document.replace("reuter", "")
        # Remove all break lines
        document = document.replace('\n', " ")
        # Store each document text in a dictionary along with the docID
        content_dict.update({'ID': documentID, 'TEXT': document})
        yield content_dict
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_tokenizer(INPUT_STRUCTURE):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    for dictionary in INPUT_STRUCTURE:
        # tokenize the text
        tokens = dictionary["TEXT"].split()
        # store each token in a tuple along with docID
        for token in tokens:
            token_tuple = (dictionary["ID"], token)
            yield token_tuple
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_stemmer(INPUT_STRUCTURE):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    ps = PorterStemmer()
    for entry in INPUT_STRUCTURE:
        stemmed = ps.stem(entry[1])  # stem token using NLTK's porter stemmer
        token_tuple = (entry[0], stemmed)
        yield token_tuple
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_stopwords_removal(INPUT_STRUCTURE, stopwords):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    stopWords_file = open("stopwords.txt", 'r')
    stopWords = []
    for word in stopWords_file:
        stopWords.append(word.replace('\n', ''))
    for entry in INPUT_STRUCTURE:
        if entry[1] not in stopWords:  # filter out stop words
            token_tuple = (entry[0], entry[1])
            yield token_tuple
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^
