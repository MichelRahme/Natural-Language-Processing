import ast
import json


def query_processor(index, path, query):
    dictionary = {}
    # parse the dictionary from the file
    for i in index:
        dictionary = ast.literal_eval(i)
    # look for query in the dictionary and retrieve all docID's
    q = {}
    for entry in dictionary:
        for word in query:
            if entry == word:
                q[entry] = dictionary[entry]

    json.dump(q, open(path, "w", encoding="utf−8"), indent=3)
    return q

