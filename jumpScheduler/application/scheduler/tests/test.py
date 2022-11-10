import csv


# Function to read in all the classes from CSV file into a dictionary
def readInClassesM(filename='MAZ-CSV/INC-PCAT-CSV.csv'):

    INCPCAT = {}

    # Open classes csv 
    with open(filename, newline = '', encoding='utf-8-sig') as file:

        classReader = csv.reader(file, delimiter = ',')
        
        for row in classReader:
            
            # Add classes to dictionary with section numbers as their Keys
            INCPCAT[row[0]] = True
            print(row[0])

    return INCPCAT


# Function to read in all the classes from CSV file into a dictionary
def readInClassesT(filename='MAZ-CSV/TEMP.csv'):

    temp = {}

    # Open classes csv 
    with open(filename, newline = '', encoding='utf-8-sig') as file:

        classReader = csv.reader(file, delimiter = ',')
        
        for row in classReader:
            
            # Add classes to dictionary with section numbers as their Keys
            temp[row[2]] = True
            print(row[2])

    return temp


def findDifferent(m, t):

    for student in m:

        if student not in t:

            print(f'Could not find {student} from INC PCATS in the main manz file\n')



def main():

    m = readInClassesM()
    t = readInClassesT()

    findDifferent(m, t)


if __name__ == '__main__':
    
    main()