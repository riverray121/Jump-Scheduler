# readInClassesFile.py

import csv
#import pandas as pd

# Class for storing distribution information cleanly within a class
class classVitals:

    def __init__(self):

        self.grade = {
            "6": 0,
            "7": 0,
            "8": 0
        }

        self.gender = { # male, female, other 
            "M": 0,
            "F": 0,
            "O": 0
        }

        self.acidemics = { 
            "1": 0,
            "2": 0,
            "3": 0
        }

        self.behvior = { 
            "1": 0,
            "2": 0,
            "3": 0
        }

        self.spedFlag = False
        self.TAG = False
        self.fiveOfour = False

        self.migrantED = False
        self.homeLanguage = ""


class classSection:

    """
    SCHOOL ID: 

    SECTION NUMBER:
    COURSE NUMBER:

    TERM ID: 

    COURSE NAME: 

    TEACHER: 
    TEACHER NUMBER: 

    PERIOD: 
    ROOM NUMBER:

    """
    
    # Initiate the class section given all the infromation of that section / period
    def __init__(self, classPeriod):

        self.schoolID = classPeriod[0]
        self.sectionNumber = classPeriod[1]
        self.courseNumber = classPeriod[2]
        self.termID = classPeriod[3] 
        self.courseName = classPeriod[4]
        self.teacher = classPeriod[5]
        self.teacherNumber = classPeriod[6]
        self.period = classPeriod[7]
        self.roomNumber = classPeriod[8]

        self.classSize = 0
        
        self.classRoster = []

        # CLASS VITALS - DISTRIBUTION NUMBERS FOR CHECKING CLASS 
        self.classVitals = classVitals()
    

    # Add student to the class roster
    def addStudent(self, student):
        self.classRoster.append(student)
        self.classSize = self.classSize + 1


class masterSchedule:

    # Function to print out all the read in classes information
    def printClasses(allClasses, classCategory, short=False):

        # Write to classes.txt file 
        with open("src/printOuts/classes.txt", "a") as newFile:

            newFile.write(f'\n \n {classCategory} \n \n')

            for classSec in allClasses:

                # Print classes and relevent info
                print(f'CLASS: {classSec} | COURESE NUM: {allClasses[classSec].courseNumber} | COURSE NAME: {allClasses[classSec].courseName}')

                if short:
                    newFile.write(f'CLASS: {classSec} | COURSE NAME: {allClasses[classSec].courseName} | PERIOD: {allClasses[classSec].period}')
                else: 
                    newFile.write(f'CLASS: {classSec} | SECTION NUM: {allClasses[classSec].sectionNumber} | COURESE NUM: {allClasses[classSec].courseNumber} | TERM ID: {allClasses[classSec].termID} COURSE NAME: {allClasses[classSec].courseName} TEACHER: {allClasses[classSec].teacher} PERIOD: {allClasses[classSec].period} CLASS SIZE: {allClasses[classSec].classSize} ')

                newFile.write('\n')

    # Sort class sections by type
    def sortClassSectionsByType(allClasses):

        # Dictionaries for sorted class types
        coreClasses = {}
        homeRooms = {}
        yearClasses = {}
        trimesterClasses = {}

        # Sort the class sections
        for classSec in allClasses:

                if allClasses[classSec].sectionNumber[-2] == 'C':   # FIND CORE CLASSES

                    coreClasses[classSec] = allClasses[classSec]

                elif 'HR' in allClasses[classSec].courseNumber:    # FIND HOMEROOMS

                    homeRooms[classSec] = allClasses[classSec]

                elif allClasses[classSec].termID == '3200':

                    yearClasses[classSec] = allClasses[classSec]

                else: 

                    trimesterClasses[classSec] = allClasses[classSec]

        return [coreClasses, homeRooms, yearClasses, trimesterClasses]
    
    # Sort class sections by team
    def sortClassSectionsByTeam(classesByType):

        # Dictionaries for team classes
        manzanita = {}
        sequoia = {}
        aspen = {}
        siskiyous = {}
        cascades = {}
        unknown = {}

        for classSec in classesByType:

            if classesByType[classSec].sectionNumber[:2] == 'SY':

                siskiyous[classSec] = classesByType[classSec]
            
            elif classesByType[classSec].sectionNumber[0] == 'S':

                sequoia[classSec] = classesByType[classSec]

            elif classesByType[classSec].sectionNumber[0] == 'M':

                manzanita[classSec] = classesByType[classSec]

            elif classesByType[classSec].sectionNumber[0] == 'A':

                aspen[classSec] = classesByType[classSec]

            elif classesByType[classSec].sectionNumber[0] == 'C':

                cascades[classSec] = classesByType[classSec]

            else:

                unknown[classSec] = classesByType[classSec]

        sortedByTeam = {
            "M" : manzanita, 
            "S" : sequoia, 
            "A" : aspen, 
            "SY" : siskiyous, 
            "C" : cascades, 
            "U" : unknown
            }

        return sortedByTeam

    # Sort class sections by INC
    def sortClassSectionsByINC(classes):

        # Dictionaries to store INC 
        INCClasses = {}
        nonINCClasses = {}

        for classSec in classes:

            if ('INC' in  classes[classSec].courseNumber) or ('INC' in classes[classSec].sectionNumber):

                INCClasses[classSec] = classes[classSec]
            
            else:

                nonINCClasses[classSec] = classes[classSec]

        return [INCClasses, nonINCClasses]

    # Sort class sections by trimester 
    def sortClassesByTrimester(classes):

        # Define Dictionaries to store by trimester 
        trimesterOne = {}
        trimesterTwo = {}
        trimesterThree = {}

        for classSec in classes:

            if 'T1' in  classes[classSec].sectionNumber:

                trimesterOne[classSec] = classes[classSec]

            if 'T2' in  classes[classSec].sectionNumber:

                trimesterTwo[classSec] = classes[classSec]

            if 'T3' in  classes[classSec].sectionNumber:

                trimesterThree[classSec] = classes[classSec]

        return [trimesterOne, trimesterTwo, trimesterThree]

    # Sort classes by periods
    def sortClassesByPeriod(classes):

        # Dictionanaries for each period
        _1B, _2B, _3B, _4B, _5B, _6B, _7B, _8B = {}, {}, {}, {}, {}, {}, {}, {}
        _1G, _2G, _3G, _4G, _5G, _6G, _7G, _8G = {}, {}, {}, {}, {}, {}, {}, {}

        blueDay = [_1B, _2B, _3B, _4B, _5B, _6B, _7B, _8B]
        goldDay = [_1G, _2G, _3G, _4G, _5G, _6G, _7G, _8G]

        for classSec in classes:

            if 'B-G' in  classes[classSec].period:

                blueDay[int(classes[classSec].period[0]) - 1][classSec] = classes[classSec]
                goldDay[int(classes[classSec].period[0]) - 1][classSec] = classes[classSec]

            elif 'B' in  classes[classSec].period:

                blueDay[int(classes[classSec].period[0]) - 1][classSec] = classes[classSec]

            elif 'G' in  classes[classSec].period:

                goldDay[int(classes[classSec].period[0]) - 1][classSec] = classes[classSec]


        return {'B': blueDay, 'G': goldDay}


    # Initiate a new masterSchedule instance
    def __init__(self, allClasses):

        # Sort class sections 
        sortedClassesByType = masterSchedule.sortClassSectionsByType(allClasses)

        # Sort core classes by team
        coreClasses = masterSchedule.sortClassSectionsByTeam(sortedClassesByType[0])

        # Sort homeroom classes by team 
        homeroomClasses = masterSchedule.sortClassSectionsByTeam(sortedClassesByType[1])

        # Sort out the INC classes from year and trimester classes
        yearINCSortedClasses = masterSchedule.sortClassSectionsByINC(sortedClassesByType[2])
        trimesterINCSortedClasses = masterSchedule.sortClassSectionsByINC(sortedClassesByType[3])

        # Sort the trimester based classes by trimester
        trimesterINCClasses = masterSchedule.sortClassesByTrimester(trimesterINCSortedClasses[0])
        trimesterNonINCClasses = masterSchedule.sortClassesByTrimester(trimesterINCSortedClasses[1])

        # Sort the trimester based INC classes by team 
        trimesterOneINCClasses = masterSchedule.sortClassSectionsByTeam(trimesterINCClasses[0])
        trimesterTwoINCClasses = masterSchedule.sortClassSectionsByTeam(trimesterINCClasses[1])
        trimesterThreeINCClasses = masterSchedule.sortClassSectionsByTeam(trimesterINCClasses[2])



        ### CORE CLASSES ###
        # Core classes 7 / 8 grade teams 
        self.manzanitaCores = coreClasses['M']
        self.sequoiaCores = coreClasses['S']
        self.aspenCores = coreClasses['A']
        # Core classes 6 grade teams 
        self.siskiyousCores = coreClasses['SY']
        self.cascadesCores = coreClasses['C']
        # Core classes unknown
        self.unknownCores = coreClasses['U']  ### NOTE NEED TO DEAL WITH 

        ### HOMEROOM CLASSES ###
        # Homeroom classes 7 / 8 grade teams 
        self.manzanitaHomerooms = homeroomClasses['M']
        self.sequoiaHomerooms = homeroomClasses['S']
        self.aspenHomerooms = homeroomClasses['A']
        # Homeroom classes 6 grade teams 
        self.siskiyousHomerooms = homeroomClasses['SY']
        self.cascadesHomerooms = homeroomClasses['C']
        # Homeroom classes unknown
        self.unknownHomerooms = homeroomClasses['U']  ### NOTE NEED TO DEAL WITH 

        ### YEAR LONG CLASSES ###
        # Year long Non-INC classes - NOTE: full schoool
        self.yearNonINCClasses = yearINCSortedClasses[1]
        # Year long INC classes - NOTE: full schoool
        self.yearINCClasses = yearINCSortedClasses[0]


        ### TRIMESTER LONG CLASSES ###
        # Trimester Non-INC classes - NOTE: full schoool
        self.trimesterOneNonINCClasses = trimesterNonINCClasses[0]
        self.trimesterTwoNonINCClasses = trimesterNonINCClasses[1]
        self.trimesterThreeNonINCClasses = trimesterNonINCClasses[2]

        # Trimester One INC classes 7 / 8 grade teams
        self.manzanitaTrimesterOneINC = trimesterOneINCClasses['M']
        self.sequoiaTrimesterOneINC = trimesterOneINCClasses['S']
        self.aspenTrimesterOneINC = trimesterOneINCClasses['A']

        # Trimester Two INC classes 7 / 8 grade teams
        self.manzanitaTrimesterTwoINC = trimesterTwoINCClasses['M']
        self.sequoiaTrimesterTwoINC = trimesterTwoINCClasses['S']
        self.aspenTrimesterTwoINC = trimesterTwoINCClasses['A']

        # Trimester Three INC classes 7 / 8 grade teams 
        self.manzanitaTrimesterThreeINC = trimesterThreeINCClasses['M']
        self.sequoiaTrimesterThreeINC = trimesterThreeINCClasses['S']
        self.aspenTrimesterThreeINC = trimesterThreeINCClasses['A']

        # Trimester One INC classes 6 grade teams
        self.siskiyousTrimesterOneINC = trimesterOneINCClasses['SY']
        self.cascadesTrimesterOneINC = trimesterOneINCClasses['C']

        # Trimester Two INC classes 6 grade teams
        self.siskiyousTrimesterTwoINC = trimesterTwoINCClasses['SY']
        self.cascadesTrimesterTwoINC = trimesterTwoINCClasses['C']

        # Trimester Three INC classes 6 grade teams 
        self.siskiyousTrimesterThreeINC = trimesterThreeINCClasses['SY']
        self.cascadesTrimesterThreeINC = trimesterThreeINCClasses['C']

        # Trimester Unknown Team INC Classes
        self.unknownTriOneINC = trimesterOneINCClasses['U']  ### NOTE NEED TO DEAL WITH
        self.unknownTriTwoINC = trimesterTwoINCClasses['U']  ### NOTE NEED TO DEAL WITH 
        self.unknownTriThreeINC = trimesterThreeINCClasses['U']  ### NOTE NEED TO DEAL WITH 


        #### REDUNDANT BUT HELPS FOR ORGANIZING FOR NOW
        self.teamManzanita = {
            "CORES": self.manzanitaCores,
            "HOMEROOMS": self.manzanitaHomerooms,
            "T1 INC": self.manzanitaTrimesterOneINC,
            "T2 INC": self.manzanitaTrimesterTwoINC,
            "T3 INC": self.manzanitaTrimesterThreeINC

        }

        self.teamSequoia = {
            "CORES": self.sequoiaCores,
            "HOMEROOMS": self.sequoiaHomerooms,
            "T1 INC": self.sequoiaTrimesterOneINC,
            "T2 INC": self.sequoiaTrimesterTwoINC,
            "T3 INC": self.sequoiaTrimesterThreeINC
        }

        self.teamAspen = {
            "CORES": self.aspenCores,
            "HOMEROOMS": self.aspenHomerooms,
            "T1 INC": self.aspenTrimesterOneINC,
            "T2 INC": self.aspenTrimesterTwoINC,
            "T3 INC": self.aspenTrimesterThreeINC

        }

        self.teamSiskiyous = {
            "CORES": self.siskiyousCores,
            "HOMEROOMS": self.siskiyousHomerooms,
            "T1 INC": self.siskiyousTrimesterOneINC,
            "T2 INC": self.siskiyousTrimesterTwoINC,
            "T3 INC": self.siskiyousTrimesterThreeINC
        }

        self.teamCascades = {
            "CORES": self.cascadesCores,
            "HOMEROOMS": self.cascadesHomerooms,
            "T1 INC": self.cascadesTrimesterOneINC,
            "T2 INC": self.cascadesTrimesterTwoINC,
            "T3 INC": self.cascadesTrimesterThreeINC

        }

        self.teamUnknown = { ### NOTE NEED TO DEAL WITH 
            "CORES": self.unknownCores,
            "HOMEROOMS": self.unknownHomerooms,
            "T1 INC": self.unknownTriOneINC,
            "T2 INC": self.unknownTriTwoINC,
            "T3 INC": self.unknownTriThreeINC
        }

        self.teamWholeSchool = {
            "YEAR NON INC": self.yearNonINCClasses,
            "YEAR INC": self.yearINCClasses,

            "T1 NON INC": self.trimesterOneNonINCClasses,
            "T2 NON INC": self.trimesterTwoNonINCClasses,
            "T3 NON INC": self.trimesterThreeNonINCClasses

        }


        # Dictionary of all team dictionaries 
        self.wholeSchool = {
            "A": self.teamAspen,
            "M": self.teamManzanita,
            "S": self.teamSequoia,
            "SY": self.teamSiskiyous,
            "C": self.teamCascades,
            "U": self.teamUnknown,
            "W": self.teamWholeSchool

        }

    # Function to print out all sorted class sections 
    def printSortedClasses(self, toPrint):

        for p in toPrint:
            masterSchedule.printClasses(p[0], p[1])

    # Get or print classes of a specific team 
    def getOrPrintTeamClasses(self, team='', print=False):

        toPrint = []

        if team == '':
            toPrint = [
            [self.manzanitaCores, 'manzanitaCores'], 
            [self.sequoiaCores, 'sequoiaCores'], 
            [self.aspenCores, 'aspenCores'], 
            [self.siskiyousCores, 'siskiyousCores'], 
            [self.cascadesCores, 'cascadesCores'], 
            [self.unknownCores, 'unknownCores'],
            [self.manzanitaHomerooms, 'manzanitaHomerooms'],
            [self.sequoiaHomerooms, 'sequoiaHomerooms'],
            [self.aspenHomerooms, 'aspenHomerooms'],
            [self.siskiyousHomerooms, 'siskiyousHomerooms'],
            [self.cascadesHomerooms, 'cascadesHomerooms'],
            [self.unknownHomerooms, 'unknownHomerooms'],
            [self.yearINCClasses, 'yearINCClasses'],
            [self.yearNonINCClasses, 'yearNonINCClasses'],

            [self.trimesterOneNonINCClasses, 'trimesterOneNonINCClasses'],
            [self.trimesterTwoNonINCClasses, 'trimesterTwoNonINCClasses'],
            [self.trimesterThreeNonINCClasses, 'trimesterThreeNonINCClasses'],

            [self.manzanitaTrimesterOneINC, 'manzanitaTrimesterOneINC'],
            [self.sequoiaTrimesterOneINC, 'sequoiaTrimesterOneINC'],
            [self.aspenTrimesterOneINC, 'aspenTrimesterOneINC'],

            [self.manzanitaTrimesterTwoINC, 'manzanitaTrimesterTwoINC'],
            [self.sequoiaTrimesterTwoINC, 'sequoiaTrimesterTwoINC'],
            [self.aspenTrimesterTwoINC, 'aspenTrimesterTwoINC'],

            [self.manzanitaTrimesterThreeINC, 'manzanitaTrimesterThreeINC'],
            [self.sequoiaTrimesterThreeINC, 'sequoiaTrimesterThreeINC'],
            [self.aspenTrimesterThreeINC, 'aspenTrimesterThreeINC'],

            [self.siskiyousTrimesterOneINC, 'siskiyousTrimesterOneINC'],
            [self.cascadesTrimesterOneINC, 'cascadesTrimesterOneINC'],
        
            [self.siskiyousTrimesterTwoINC, 'siskiyousTrimesterTwoINC'],
            [self.cascadesTrimesterTwoINC, 'cascadesTrimesterTwoINC'],

            [self.siskiyousTrimesterThreeINC, 'siskiyousTrimesterThreeINC'],
            [self.cascadesTrimesterThreeINC, 'cascadesTrimesterThreeINC'],

            [self.unknownTriOneINC, 'unknownTriOneINC'],
            [self.unknownTriTwoINC, 'unknownTriTwoINC'],
            [self.unknownTriThreeINC, 'unknownTriThreeINC'],
            ]
        else:
            for cl in self.wholeSchool[team]:
                toPrint.append([self.wholeSchool[team][cl], cl])
            for cl in self.wholeSchool['W']:
                toPrint.append([self.wholeSchool['W'][cl], cl])
            # for cl in self.wholeSchool['U']:
            #     toPrint.append([self.wholeSchool['U'][cl], cl])

        if print:
            masterSchedule.printSortedClasses(self,toPrint)

        return toPrint
    
    # Function to get or print out classes by period
    def getOrPrintClassesByPeriod(allClasses, print=False):

        # Dictionanaries for each period
        _1B, _2B, _3B, _4B, _5B, _6B, _7B, _8B = {}, {}, {}, {}, {}, {}, {}, {}
        _1G, _2G, _3G, _4G, _5G, _6G, _7G, _8G = {}, {}, {}, {}, {}, {}, {}, {}
        # List to store periods
        blueDay = [_1B, _2B, _3B, _4B, _5B, _6B, _7B, _8B]
        goldDay = [_1G, _2G, _3G, _4G, _5G, _6G, _7G, _8G]

        # sort by periods 
        for p in allClasses:
            blueAndGold = masterSchedule.sortClassesByPeriod(p[0])
            # blueDay += blueAndGold['B']
            # goldDay += blueAndGold['G']
            for i, b in enumerate(blueAndGold['B']):
                for cl in b:
                    blueDay[i][cl] = b[cl]
            for i, g in enumerate(blueAndGold['G']):
                for cl in g:
                    goldDay[i][cl] = g[cl]

        # Print all the classes sorted
        if print: 
            for i, period in enumerate(blueDay):
                masterSchedule.printClasses(period, f'{i + 1}B', True)
            for i, period in enumerate(goldDay):
                masterSchedule.printClasses(period, f'{i + 1}B', True)

        return {'B': blueDay, 'G': goldDay}


# def readInClassSupplementals():

#     masterBellSchedule = pd.read_excel('AMS Spreadsheets/Master Bell.xlsx')


# Function to read in all the classes from CSV file into an array
def readInClasses(filename='MAZ-CSV/CLASSES-CSV.csv'):

    allClassesDic = {}

    # Open classes csv 
    with open(filename, newline = '', encoding='utf-8-sig') as file:

        classReader = csv.reader(file, delimiter = ',')
        
        for row in classReader:
            
            # Add classes to dictionary with section numbers as their Keys
            allClassesDic[row[1]] = classSection(row)


    return allClassesDic


# Function to clean previous classes.txt
def cleanClassesTXT():

    # Clean classes.txt file
    with open("src/printOuts/classes.txt", "w") as newFile:

            newFile.write(f'\n')


# # MAIN EXECUTION 
# def main():

#     # Clean classes.txt file 
#     cleanClassesTXT()
    
#     # Read in classes and sort class sections
#     classesDic = readInClasses()
#     AMSMasterSchedule = masterSchedule(classesDic)

#     # Print all classes of desired team or of whole school (if no team specified)
#     #masterSchedule.getOrPrintTeamClasses(AMSMasterSchedule)
#     masterSchedule.getOrPrintTeamClasses(AMSMasterSchedule, 'M', True)
    
#     # Get the classes for manzanita
#     manzanitaClasses = masterSchedule.getOrPrintTeamClasses(AMSMasterSchedule, 'M')

#     # Print the classes for manzanita by period
#     #manzClassesByPeriod = masterSchedule.getOrPrintClassesByPeriod(manzanitaClasses, True)

    


# # RUN MAIN 
# if __name__ == '__main__':

#     main()