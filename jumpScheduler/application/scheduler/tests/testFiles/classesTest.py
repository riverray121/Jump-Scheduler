# classesTest.py

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
from readInClassesFile import *



# MAIN EXECUTION 
def main():

    # Clean classes.txt file 
    cleanClassesTXT()
    
    # Read in classes and sort class sections
    classesDic = readInClasses()
    AMSMasterSchedule = masterSchedule(classesDic)

    # Print all classes of desired team or of whole school (if no team specified)
    #masterSchedule.getOrPrintTeamClasses(AMSMasterSchedule)
    #masterSchedule.getOrPrintTeamClasses(AMSMasterSchedule, 'M', True)
    
    # Get the classes for manzanita
    manzanitaClasses = masterSchedule.getOrPrintTeamClasses(AMSMasterSchedule, 'M')

    # Print the classes for manzanita by period
    manzClassesByPeriod = masterSchedule.getOrPrintClassesByPeriod(manzanitaClasses, True)

    


# RUN MAIN 
if __name__ == '__main__':

    main()


