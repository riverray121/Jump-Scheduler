# studentsTest.py

import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)
 
# now we can import the module in the parent
# directory.
from readInStudentsFile import *



#/Users/elijahretzlaff/Documents/DEVELOPMENT/Skewl-Project/src/functionspkg/readInStudentsFile.py

# MAIN EXECUTION 
def main():
    
    # Read in Students 
    manzStudentsDic = readInStudents()

    # Print all Students 
    printStudents(manzStudentsDic)


    # Print students and their requested classes
    printStudentRecClasses(manzStudentsDic)

    # Read in the input from the teachers 

    # Print students and their requested classes




# RUN MAIN 
if __name__ == '__main__':

    main()

