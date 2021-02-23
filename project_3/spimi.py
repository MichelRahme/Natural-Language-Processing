import os
import shutil
import json
import collections
import time
from sortedcontainers import SortedSet


def create_directory():
    """
    Creates the Blocks folder
    :return: Null
    """
    try:
        print("\nTask 2: Creating new Blocks Folder...")
        os.mkdir("Blocks")
    except FileExistsError:
        print("Old Blocks folder overwritten.")
        shutil.rmtree("Blocks")
        os.mkdir("Blocks")
    print("Done!")


def add_to_dict(dictionary, term):
    """
    Adds a term to dictionary
    :param dictionary:
    :param term:
    :return: dictionary[term]
    """
    dictionary[term] = []
    return dictionary[term]


def set_default(obj):
    """
    Helper function to write SortedSets in Json Files
    :return: Null
    """
    if isinstance(obj, SortedSet):
        return list(obj)
    raise TypeError


def disk_block_merging_fast(blocks):
    """
    The function takes the list of Block names. (The blocks in the Block Folder)
    These blocks are then opened and loaded in memory.

    We use the collections.DefaultDict along with SortedSet to achieve merging of all block in 6seconds!
    The resulting index is then saved in finalIndex.json and returned
    :param blocks:
    :return: Sorted_Super_Dict
    """
    opened_blocks = [open(block, 'r') for block in blocks]
    dicts = [json.load(block) for block in opened_blocks]
    super_dict = collections.defaultdict(SortedSet)
    for d in dicts:
        for k, v in d.items():
            for posting in v:
                super_dict[k].add(int(posting))
    t0 = time.time()
    print("Sorting Dict...")
    sorted_super_dict = dict(sorted(super_dict.items()))
    t1 = time.time()
    print("Time taken to sort is {}".format(t1 - t0))
    result = json.dumps(sorted_super_dict, default=set_default, indent=4)
    f = open('finalIndex.json', 'w')
    f.write(result)
    return sorted_super_dict


def disk_block_merging_book(blocks):
    """

    The function takes the list of Block names. (The blocks in the Block Folder)
    These blocks are then opened and loaded in memory.

    Here, we follow the merging mentioned in the book. Please note that you can replace which method of merging to use
    down in line 133

    This merging method is indeed slower, taking 49 seconds to merge all blocks.

    The logic behind the method is explained in the report.
    :param blocks:
    :return: Sorted_Super_Dict
    """
    opened_blocks = [open(block, 'r') for block in blocks]
    dicts = [json.load(block) for block in opened_blocks]
    list_of_keys = [list(loaded_dict.keys()) for loaded_dict in dicts]
    temp = {}
    sorted_super_dict = {}
    while True:
        temp.clear()
        for y in range(0, len(dicts)):
            if len(list_of_keys[y]) != 0:
                temp[y] = list_of_keys[y][0]
        if len(temp) != 0:
            entry = min(temp, key=temp.get)
            list_of_keys[entry].pop(0)
        else:
            break
        dictionary = dicts[entry]
        if temp[entry] not in sorted_super_dict:
            sorted_super_dict[temp[entry]] = dictionary[temp[entry]]
            del dictionary[temp[entry]]
        elif temp[entry] in sorted_super_dict:
            sorted_super_dict[temp[entry]].extend(dictionary[temp[entry]])
            del dictionary[temp[entry]]

    # Return the Index and store it in JSON file
    result = json.dumps(sorted_super_dict, indent=4)
    f = open('finalIndex.json', 'w')
    f.write(result)
    return sorted_super_dict


class Spimi:

    def __init__(self, documents):
        create_directory()
        print("\nTask 3: Processing and Storing the Blocks...")
        t0 = time.time()
        self.documents = documents
        self.blockNumber = 0
        self.blocks = []
        self.construct_blocks(self.documents)
        t1 = time.time()
        print("Done! Total Time: {}".format(t1 - t0))
        print("\nTask 4: Merging blocks...")
        t2 = time.time()
        # Change merging function here
        self.finalIndex = disk_block_merging_fast(self.blocks)
        t3 = time.time()
        print("Done! Total time: {}".format(t3 - t2))

    def construct_blocks(self, documents):
        """
        This methods takes the documents generated from collection.py

        We iterate over each token in each document, with a counter of K tokens, and creating X mini indexes called
        Blocks.

        These blocks are then stored in the Blocks folder.
        :param documents:
        :return: Null
        """
        dictionary = {}
        token_counter = 0
        for entry in documents:
            for token in documents[entry]:
                """
                Just like to add that the prof mentioned that for every k TOKENS we switch 
                blocks, but another TA said that for every k TERMS we switch block. 
                
             
                In the book they say for every TOKEN as well, but in the project handout you say term...
                Not sure who to trust here so I  just followed the book and the prof. 
                
                Thanks
                """
                # Change K value here
                if token_counter < 500:
                    token_counter += 1
                    if token not in dictionary:
                        postings = add_to_dict(dictionary, token)
                    else:
                        postings = dictionary[token]
                    if entry not in postings:
                        postings.append(entry)
                else:
                    self.add_to_block(dictionary)
                    dictionary.clear()
                    token_counter = 0
        # Make sure the last elements in the dictionary are also added.
        if token_counter != 0:
            self.add_to_block(dictionary)
            dictionary.clear()

    def add_to_block(self, dictionary):
        """
        Helper function to add to a block.
        A block is opened and the mini-dict is dumped into the block.

        Here we also append the block name to our Blocks list used in the merge functions
        :param dictionary:
        :return: Null
        """
        blockFile = "Blocks/block_{}.json".format(self.blockNumber)
        f = open(blockFile, 'w')
        f.write(json.dumps(dictionary, sort_keys=True, indent=4))
        self.blockNumber += 1
        self.blocks.append(blockFile)
