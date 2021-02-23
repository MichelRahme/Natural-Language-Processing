from collection import Collection
from spimi import Spimi
from query import Query

"""
This is the main class. 
For this project, you only need to run 'python main.py' (make sure path to reuters file is correct, line 43)

We first start with the Collection class where we parse the Reuters21578 library and divide it into a dictionary of the 
form { "docID" : [tokens] }

The reason I chose to store the index that way is because we're going to use the document length, documents average 
length later on. Also, this makes is very easy to go over 500 tokens and divide them into blocks.

We then move to the SPIMI class, where we are dividing the collection into separate blocks and then merging these blocks

Query and BM25 classes are then used to process queries and rank the resulting documents.
"""

def ask_for_query():
    """
    Helper static function that handles user input for submitting queries.
    """
    while True:
        queryType = input('\n\nPlease select query type: [1] SINGLE [2] AND [3] OR [4] BM25: ')
        if queryType not in {'1', '2', '3', '4'}:
            print('We expect you to enter a valid integer')
        else:
            num = int(queryType)
            query = input("Please enter query: ")
            return [num, query]


if __name__ == '__main__':

    """
    Divide the collection into a dictionary of the form:
    {"docID" : [tokens]}
    
    Takes input to Reuters21578 folder and also the desired number files to process. 
    """
    collection = Collection(
        path="../reuters21578",    # Change the path to reuters documents
        numberOfFiles=22)

    """
    Take the collection of documents and run SPIMI
    """
    module1 = Spimi(
        documents=collection.documents
    )

    """
    Ask for user query
    """
    while True:
        user_input = ask_for_query()
        module2 = Query(user_input[1], int(user_input[0]), module1.finalIndex, collection.documents)
        entry = input("\nWould you like to run another query? [T/F] : ")
        if entry.lower() == "t":
            continue
        if entry.lower() == "f":
            print("Thanks, Goodbye!")
            break
