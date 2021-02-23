import os
import shutil
import json
import collections
from sortedcontainers import SortedSet


def create_directory():
    """
    Creates the Blocks folder
    :return: Null
    """
    try:
        os.mkdir("Blocks")
    except FileExistsError:
        shutil.rmtree("Blocks")
        os.mkdir("Blocks")


def add_to_dict(dictionary, term):
    """
    Adds a term to dictionary
    :param dictionary:
    :param term:
    :return: dictionary[term]
    """
    dictionary[term] = [0, {}]
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

    We use the collections.DefaultDict and we achieve merging of all block in less than 10 seconds!
    The resulting index is then saved in finalIndex.json and returned
    :param blocks:
    :return: Sorted_Super_Dict
    """
    opened_blocks = [open(block, 'r') for block in blocks]
    dicts = [json.load(block) for block in opened_blocks]
    super_dict = collections.defaultdict(list)
    for d in dicts:
        for k, v in d.items():
            if k not in super_dict:
                super_dict[k] = v
            else:
                for entry in v[1]:
                    if entry not in super_dict[k][1]:
                        super_dict[k][0] += 1
                        super_dict[k][1][entry] = v[1][entry]
                super_dict[k][1] = {k: v for k, v in
                                    sorted(super_dict[k][1].items(), key=lambda item: item[1], reverse=True)}
    sorted_super_dict = dict(sorted(super_dict.items()))
    result = json.dumps(sorted_super_dict, default=set_default, indent=4)
    f = open('finalIndex.json', 'w')
    f.write(result)
    return sorted_super_dict


class Spimi:

    def __init__(self):
        create_directory()
        self.blockNumber = 0
        self.blocks = []
        self.scraped_data = json.load(open('result.json'))
        self.construct_blocks(self.scraped_data)
        self.finalIndex = disk_block_merging_fast(self.blocks)

    def construct_blocks(self, data):
        """
        This methods takes the documents generated from collection.py

        We iterate over each token in each document, with a counter of K tokens, and creating X mini indexes called
        Blocks.

        These blocks are then stored in the Blocks folder.
        :param data:
        :param documents:
        :return: Null
        """
        print("Scrapy Done! Building Index using SPIMI.....")
        dictionary = {}
        token_counter = 0
        doc_counter = 0
        for html_dict in data:
            doc_counter += 1
            for token in html_dict['content']:
                token_occurrence = html_dict['content'].count(token)
                if token_counter < 500:
                    token_counter += 1
                    if token not in dictionary:
                        postings = add_to_dict(dictionary, token)
                    else:
                        postings = dictionary[token]
                    if doc_counter not in postings[1]:
                        postings[0] += 1
                        postings[1][doc_counter] = token_occurrence
                else:
                    self.add_to_block(dictionary)
                    dictionary.clear()
                    token_counter = 0
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
