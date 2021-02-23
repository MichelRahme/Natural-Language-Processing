#!/usr/bin/env python
""" BLOCK 3
Objective: Text corpus contains a lot of noise and meta data. It is important to identify the important information and
            extract them. The objective of this block is to identify which parts in the news document will be useful to
            construct an inverted index.

Fill in your code within the 'WRITE YOUR CODE HERE' stub in function "block_extractor" in solutions.py file. Do not
attempt to modify any code in this file as they might affect your grading.

Input: Individual news documents (Output from Block-2-document-segmenter.py)
Output: A Python dictionary data structure containing an ID (corresponding to document ID) and TEXT (corresponding to
        the text extracted from each news documents).  Number of iteration in the loop created for you should be equal
        to the number of documents inside the corpus.

Sample output structure: {ID: 1, TEXT: "This is text from first document. The boy is playing outside"}

Marking criteria:
     - The content of the output variable: structure, type and size
"""

import argparse
import json
import asserts
import solutions

parser = argparse.ArgumentParser(description='Process input path parameter')
args = asserts.init_params()

# Calling your solution. Execute your solution in the following method in solutions.py file
for content_item in solutions.block_extractor((json.loads(line) for line in args.input_file)):
    # Validating output format
    asserts.block_3_extractor_validate(content_item)
    # Write results to stdout or file
    asserts.output(content_item)



