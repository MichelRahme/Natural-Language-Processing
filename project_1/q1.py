import os
import re
from nltk.tokenize import word_tokenize


docID = 0
f1 = open("tuples.txt", 'w')
tuple_list = []
inverted_index = {}

for file in sorted(os.listdir("question1")):
    docID = docID + 1
    if file.endswith(".txt"):
        filename = os.path.join("question1", file)  # join the file with the full path
        f = open(filename, 'r')
        fileContent = f.read()  # read the file into a string
        print(word_tokenize(fileContent))
        tokens = fileContent.split()
        for token in tokens:
            token = re.sub(r'[^a-zA-Z\s]', '', token)
            if token.endswith("ore"):
                token = re.sub('ore$', 'or', token)
            if token.endswith("oris"):
                token = re.sub('oris$', 'or', token)
            if token.endswith("orum"):
                token = re.sub('orum$', 'or', token)
            tuple_entry = (token.lower(), docID)
            tuple_list.append(tuple_entry)

tuple_list.sort(key=lambda x: x[0].lower())

test = list(set(tuple_list))

test.sort(key=lambda x: x[0].lower())

print(test)

for word, doc in tuple_list:
    frequency = 1
    if word not in inverted_index:
        inverted_index[word] = [frequency, [doc]]
    else:
        list_of_docs = inverted_index.get(word)
        if doc not in list_of_docs[1]:
            list_of_docs[0] = list_of_docs[0] + 1
            list_of_docs[1].append(doc)
            inverted_index[word] = list_of_docs

f1.write("{\n")
for entry in inverted_index.items():
    f1.write(str(entry) + "\n")
f1.write("}\n")

