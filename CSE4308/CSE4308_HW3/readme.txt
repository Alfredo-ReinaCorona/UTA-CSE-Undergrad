Alfredo Reina Corona
1001935392

Language and Version: Python 3.10.12 

Structure:

    - The code has 8 functions and 1 class
    - Open dataset extracts all the information into a 2D numpy array which is then processed to extract the needed information
    - the information gain is divided into 2 sections. The information_gain function and the entropy function
    - a probability density function is used in order to get the best attribute for the nexit iteration of the tree generation
    - DTL is a recursive function, so DTL_Top level is there to provide it with the needed starting values
    - the Tree class defines a tree , its attributes, left and right branches as well as it's data gain

    - The driver of the code is the DTL_TopLevel, DTL functions along with the Tree class. These pieces of the code allow the tree to learn from the dataset



HOW TO RUN:

    - python3 dtree.py pendigits_training.txt pendigits_test.txt randomized 
    - python3 [python file] [training_dataset] [testing_dataset] [optimized | randomized | forest3 | forest15]
    - Please makes sure that the datasets are in the SAME directory as the python file, not nested within a folder or someplace else

WARNINGS:
    - randomized takes ~5 seconds to run on my machine, but forest3,forest15, and optimized can take anywhere from 30seconds to a minute. Please be patient with the code. It WILL run.


CITATIONS
    - I had a VERY similar assignment in CSE4309(Machine Learning). ~80%+ of my code is directly COPIED from that assignment.

    

