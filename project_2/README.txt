hello,


The code is divided into 5 modules.

Module 1,2,3 belong to SubProject 1
Module 4 belongs to SubProject 2
Module 5 belongs to SubProject 3

Please make sure all libraries specified in the report are installed.


######To run SubProject 1 and generate the Index#######

python3 module1.py -p reuters21578 | python3 module2.py | python2 module3.py -o index.txt

-p path to the reuters docs


######To run SubProject 2#######

python3 module4.py -i index.txt -p testQueries.json -q Apple Banana Tomato

-i is the input file (the index we will be searching)
-p is the path to the .json file where the results will be stored
-q the query terms


######To run Subproject 3#######

python3 module5.py -o data/table.txt

-o is the output where the resulting table will be stored


Thanks,
Michel
