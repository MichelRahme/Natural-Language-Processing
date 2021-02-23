import os
import re
import string

from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import time


class Collection:

    def __init__(self, path, numberOfFiles):
        t0 = time.time()
        print("\nTask 1: Reading and extracting Reuters21578 docs...")
        self.path = path
        self.numberOfFiles = numberOfFiles
        # Load the files
        self.files = self.get_files(numberOfFiles)
        # Parse the documents and store in Dict
        self.documents = self.get_document_tokens()
        t1 = time.time()
        print("Done! Total Time: {}".format(t1 - t0))

    def get_files(self, numberOfFiles):
        files = [file for file in os.listdir(self.path)]
        return sorted(files)[:numberOfFiles]

    def get_document_tokens(self):
        processedDocuments = {}
        for file in self.files:
            soup = BeautifulSoup(open(os.path.join(self.path, file), 'r', encoding='utf-8', errors='ignore'), "lxml")
            documents = soup.find_all('reuters')

            for document in documents:
                docID = document['newid']
                text = document.find('text').text
                tokens = word_tokenize(text)
                tokens_no_punct = []
                """
                Clean punctuation as per the new Amended Project
                """
                for token in tokens:
                    if not re.fullmatch('[' + string.punctuation + ']+', token):
                        tokens_no_punct.append(token)
                """
                Store the processed docs in a dict: { "docID" : [tokens]}
                """
                processedDocuments[docID] = tokens_no_punct
        return {k: processedDocuments[k] for k in list(processedDocuments)}
