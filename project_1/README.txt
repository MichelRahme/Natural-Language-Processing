Welcome to Project 1.
---------------------------------------------

The objective of this project is to make you familiarize with nltk functionalities and understand the basic building
blocks of constructing an Inverted Index.

The pipeline for this project consists of several Python files.
Some of which you will need to read and understand in order to complete the assignment. Each file mentioned below has it's
own objectives to satisfy along with specific input and output structures. Read thoroughly the documentation part on top
of each of the following scripts to know what to code. But DO NOT ATTEMPT TO MODIFY ANY CODE IN THESE FILES.
    - block-1-reader.py
    - block-2-document-segmenter.py
    - block-3-extractor.py
    - block-4-tokenizer.py
    - block-5-stemmer.py
    - block-6-stopwords-removal.py

Implementation of each python script mentioned above should be completed within the python function stubs created for you
in the following file. You can create additional functions than the one created for you to write any reusable code.
    - solutions.py 

Since each block-*.py file expects specific output structure of the values passed out of each script there are some
pre-built simple testcases in assert.py file to help you understand your mistake. Read through the assert messages
thoroughly to understand where you are making a mistake in terms of the input and output values. Again DO NOT ATTEMPT TO
MODIFY ANY CODE IN THIS FILE.

Commands to execute each block(python scripts) can be found below. Each python script mentioned above has a default set
of parameters that you can pass in when calling each Python script. For some scripts some parameters are mandatory while
for others these parameters are optional. Parameters you can pass in and description are as below:

  -h, --help                                    will show description of all parameters and exit
  -i INPUT_FILE, --input_file INPUT_FILE        Input from file, default stdin
  -o OUTPUT_FILE, --output_file OUTPUT_FILE     Output to file, default stdout
  -p PATH, --path PATH                          Reuters collection directory
  -s STOPWORDS, --stopwords STOPWORDS           path to Stopword list from file


##### Commands ###################
Sample commands to show different options of running the scripts. 

Running python scripts with default functionality
--------------------------------------------------------------------
python ./block-1-reader.py --path <Reuters folder path>
python ./block-1-reader.py --path <Reuters folder path> | python ./block-2-document-segmenter.py
python ./block-1-reader.py --path <Reuters folder path> | python ./block-2-document-segmenter.py | python ./block-3-extractor.py
python ./block-1-reader.py --path <Reuters folder path> | python ./block-2-document-segmenter.py | python ./block-3-extractor.py | python ./block-4-tokenizer.py
python ./block-1-reader.py --path <Reuters folder path> | python ./block-2-document-segmenter.py | python ./block-3-extractor.py | python ./block-4-tokenizer.py | python ./block-5-stemmer.py
python ./block-1-reader.py --path <Reuters folder path> | python ./block-2-document-segmenter.py | python ./block-3-extractor.py | python ./block-4-tokenizer.py | python ./block-5-stemmer.py | python ./block-6-stopwords-removal.py


Running python scripts to save intermediary results as text files:
---------------------------------------------------------------------
python ./block-1-reader.py --path <Reuters folder path> -o block1.json
python ./block-1-reader.py --path <Reuters folder path> | python .block-2-document-segmenter.py -o block2.json
OR 
python ./block-1-reader.py --path ./Reuters --output_file block1.json
python ./block-1-reader.py --path <Reuters folder path> | python .block-2-document-segmenter.py --output_file block2.json


Using intermediary results output from the previous block as an input into the current block.
----------------------------------------------------------------------------------------------------------
python ./block-2-document-segmenter.py -i block1.json -o block2.json
python ./block-3-extractor.py -i block2.json -o block3.json
OR
python ./block-2-document-segmenter.py -input_file block1.json --output_file block2.json
python ./block-3-extractor.py -input_file block2.json --output_file block3.json


Optional for block 6. If you wish to pass a stopwords list from an external file, use the following:
-----------------------------------------------------------------------------------------------------------
python ./block-6-stopwords-removal.py -s <Stopwords file path>
OR
python ./block-6-stopwords-removal.py --stopwords <Stopwords file path>
