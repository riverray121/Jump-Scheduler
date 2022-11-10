# classes.py
from copy import deepcopy
import csv
import random
import sys
import os
import xlsxwriter

# Get import path information
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
 
# Import from parent directory
import settings as settings



##### CLASS SECTION CLASSES

# Class for storing distribution information cleanly within a class
class classVitals:

    def __init__(self):

        self.grade = {
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

# Class for storing a class section
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
    def __init__(self, classPeriod=''):

        # Initiate in case of an empty classSection
        self.schoolID = ''
        self.sectionNumber = ''
        self.courseNumber = ''
        self.termID = ''
        self.courseName = ''
        self.teacher = ''
        self.teacherNumber = ''
        self.period = ''
        self.roomNumber = ''

        self.classSize = 0
        #self.numberOfPeriods = 0
        self.classRoster = []

        # CLASS VITALS - DISTRIBUTION NUMBERS FOR CHECKING CLASS 
        self.classVitals = classVitals()
        
        # classSection is being created from input
        if classPeriod:

            self.schoolID = classPeriod[0]
            self.sectionNumber = classPeriod[1]
            self.courseNumber = classPeriod[2]
            self.termID = classPeriod[3] 
            self.courseName = classPeriod[4]
            self.teacher = classPeriod[5]
            self.teacherNumber = classPeriod[6]
            self.period = classPeriod[7]
            self.roomNumber = classPeriod[8] 
    
    # Add student to the class roster
    def addStudent(self, student):
        self.classRoster.append(student)
        self.classSize = self.classSize + 1

# Class for creating and storing a master schedule
class masterSchedule:

    # Function to print out all the read in classes information
    def printClasses(allClasses, classCategory, short=False, toPrint=False):

        # Write to classes.txt file 
        with open("application/scheduler/printOuts/classes.txt", "a") as newFile:

            newFile.write(f'\n \n {classCategory} \n \n')

            for classSec in allClasses:

                # Print classes and relevent info
                if toPrint: print(f'CLASS: {classSec} | COURESE NUM: {allClasses[classSec].courseNumber} | COURSE NAME: {allClasses[classSec].courseName}')

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

    # Sort core classes into buckets by class type
    def sortCoresBySubject(classes):

        # Dictionary to store classes by subject
        subjectSortedCores = {}

        # Add classes to dictionary under buckets of the class subject
        for cl in classes:

            if classes[cl].courseName not in subjectSortedCores:

                subjectSortedCores[classes[cl].courseName] = [classes[cl]]
            else: 

                subjectSortedCores[classes[cl].courseName].append(classes[cl])
    
        return subjectSortedCores

    # Sort core classes into buckets by class type
    def sortCoresByCourseNum(classes):

        # Dictionary to store classes by subject
        subjectSortedCourseNum = {}

        # Add classes to dictionary under buckets of the class subject
        for cl in classes:

            if classes[cl].courseNumber not in subjectSortedCourseNum:

                subjectSortedCourseNum[classes[cl].courseNumber] = [classes[cl]]
            else: 

                subjectSortedCourseNum[classes[cl].courseNumber].append(classes[cl])
    
        return subjectSortedCourseNum

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
        """
        FORMAT:

        [
        [dic of classes of category, string containing name of that category]
        .
        .
        .
        ]

        """

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
            for cl in self.wholeSchool['U']:
                toPrint.append([self.wholeSchool['U'][cl], cl])

        if print:
            masterSchedule.printSortedClasses(self, toPrint)

        return toPrint
    
    # Function to convert all teams classes to dictionary with classID as key 
    def teamClassesAsDic(teamClasses):

        teamClassesDic = {}

        for arr in teamClasses:
            for cl in arr[0]:
                teamClassesDic[cl] = arr[0][cl]

        return teamClassesDic

        

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



##### STUDENT CLASSES

# Class for storing a student and student info
class student: 

    # STUDENTS CAN HAVE THE FOLLOWING ATTRIBUTES:
    """
    LAST NAME: String
    FIRST NAME: String

    STUDENT ID: String

    GRADE: 6 / 7 / 8
    GENDER: M / F / X

    SIXTH GRADE HOMEROOM: Teacher last name
    SIXT GRADE TEAM: Cascades / Siskiyous

    STUDENT DOB: M/D/Y

    CASE MANAGER: FIRST NAME LAST NAME 

    SPED FLAG: Yes / blank
        IEP READING: Current / blank
        IEP WRITING: Current / blank
        IEP MATH: Current / blank
        IEP SPEECH: Current / blank
        IEP BEHAVIOR/SOCIAL: Current / blank
    
    504: Current / blank
        504 REASON: Custom string / blank

    TAG: Yes / blank 
    ELL: Yes / blank 

    ACIDEMIC RATING: 1-3
    BEHAVIOR RATING: 1-3

    MATH PLACEMENT: 7th / ALG / pre alg / sped

    READING LEVEL: Above / Grade / Below
    WRITING LEVEL:  Above / Grade / Below
    i-READY ELA WINTER: Level
    i-READY MATH WINTER: Level 

    SIXTH GRADE INC: INC Subject
    INC RECCOMENDATIONS: Inc Subject Reccomendations 

    CORE READING SUPPORT: Current / blank

    STRUGGELS WITH ORGANIZATION: Yes / blank
    STRUGGLES WITH WORK COMPLETION: Yes / blank
    STRUGGLES WITH ATTENDANCE: Yes / blank

    ASC RECCOMENDED: Reccommended / blank
    NATIVE SPANISH SPEAKER: Yes / blank

    POSATIVE PEERS: Names of posative peers 
    NEGATIVE PEERS: Names of negative peers

    BAND: Yes / blank 
    ORCHESTRA: Yes / blank

    """

    # Parse the posative peers of a student into an array TODO
    def parseStudentPeers(peers):
        
        parsedPeers = [peers]

        return parsedPeers


    # Initiate a student instance
    def __init__(self, studentArray=[]):

        self.requestedClasses = []
        self.fullyScheduled = False

        # Fill the students schedule with empty classSection objects
        self.studentSchedule = []
        for i in range(0, 16): self.studentSchedule.append(classSection())

        # TEMP ALT VERSION OF CLASSES STORAGE:
        self.studentSched = {
            '_1B': {},
            '_2B': {}, 
            '_3B': {}, 
            '_4B': {}, 
            '_5B': {}, 
            '_6B': {}, 
            '_7B': {}, 
            '_8B': {}, 

            '_1G': {}, 
            '_2G': {}, 
            '_3G': {}, 
            '_4G': {}, 
            '_5G': {}, 
            '_6G': {}, 
            '_7G': {}, 
            '_8G': {}, 
        }


        # Set empty values for an instance of an empty student
        self.lastName = ''
        self.firstName = ''
        self.studentID = ''

        self.grade = 0
        self.gender = ''

        self.sixthHR = ''
        self.sixthTeam = ''

        self.DOB = ''

        self.caseManager = ''

        self.SPED = False
        self.IEPReading = False
        self.IEPWriting = False
        self.IEPMath = False
        self.IEPSpeech = False
        self.IEPBehaviorSocial = False

        self._504 = False
        self._504Reason = ''

        self.TAG = False

        self.ELL = False

        self.academicRating = 0
        self.behaviorRating = 0

        self.mathPlacement = ''
        self.spanishPlacement = ''

        self.readingLevel = 0
        self.writingLevel = 0
        self.iReadyELAWinter = ''
        self.iReadyMathWinter = ''

        self.sixthINC = ''
        self.INCRecomendations = ''

        self.coreReadingSupport = False
        self.strugglesWithOrganization = False
        self.strugglesWithWorkCompletion = False
        self.strugglesWithAttendance = False

        self.ASCReccomended = False
        self.nativeSpanishSpeaker = False

        self.posativePeers = []
        self.negativePeers = []

        self.band = False
        self.orchestra = False

        self.lunchPeriod = ''

        # If information for the student was passes then create the student otherwise create empty
        if studentArray:

            # Student ID info
            self.lastName = studentArray[0]
            self.firstName = studentArray[1]
            self.studentID = studentArray[2]

            # Student grade and gender
            if studentArray[3]: self.grade = int(studentArray[3]) + 1
            self.gender = studentArray[4]

            # Student history
            self.sixthHR = studentArray[5]
            self.sixthTeam = studentArray[6]

            self.DOB = studentArray[7]

            self.caseManager = studentArray[8]

            # Student SPED info
            self.SPED = studentArray[9] == 'Yes'
            self.IEPReading = studentArray[10] == 'Current'
            self.IEPWriting = studentArray[11] == 'Current'
            self.IEPMath = studentArray[12] == 'Current'
            self.IEPSpeech = studentArray[13] == 'Current'
            self.IEPBehaviorSocial = studentArray[14] == 'Current'

            self._504 = studentArray[15] == 'Current'
            self._504Reason = studentArray[16]

            self.TAG = studentArray[17] == 'Yes'

            self.ELL = studentArray[18] == 'Yes'

            # Student distribution traits 
            if studentArray[19]: self.academicRating = int(studentArray[19])
            if studentArray[20]: self.behaviorRating = int(studentArray[20])

            # Correct math placement        NOTE: Does not account for HS geo placement 
            if settings.mathSchedByGrade:
                if self.grade == 7: self.mathPlacement = 'M_INT_MATH7'
                else: self.mathPlacement = 'M_INT_MATH8'
            else:
                if studentArray[21] == '7th' or studentArray[21] == "pre alg": self.mathPlacement = 'M_INT_MATH7'    # WILL NEED TO BE MODIFIED TO WORK WITH 6TH GRADERS
                elif studentArray[21] == 'sped': self.mathPlacement = 'SPED_MATH'
                else: self.mathPlacement = 'M_INT_MATH8'


            # More student traits 
            self.readingLevel = studentArray[22]
            self.writingLevel = studentArray[23]
            self.iReadyELAWinter = studentArray[24]
            self.iReadyMathWinter = studentArray[25]

            if self.readingLevel == "Below": self.readingLevel = 1
            elif self.readingLevel == "Grade": self.readingLevel = 2
            elif self.readingLevel == "Above": self.readingLevel = 3
            else: self.readingLevel = random.randint(1, 3)
                
            if self.writingLevel == "Below": self.writingLevel = 1
            elif self.writingLevel == "Grade": self.writingLevel = 2
            elif self.writingLevel == "Above": self.writingLevel = 3
            else: self.writingLevel = random.randint(1, 3)

            # More student history
            self.sixthINC = studentArray[26]
            self.INCRecomendations = studentArray[27]

            # Student qualatative support info
            self.coreReadingSupport = studentArray[28] == 'Current'
            self.strugglesWithOrganization = studentArray[29] == 'Yes'
            self.strugglesWithWorkCompletion = studentArray[30] == 'Yes'
            self.strugglesWithAttendance = studentArray[31] == 'Yes'

            # More student traits  
            self.ASCReccomended = studentArray[32] != ''
            self.nativeSpanishSpeaker = studentArray[33] == 'Yes'

            # Student peers info 
            self.posativePeers = student.parseStudentPeers(studentArray[34])
            self.negativePeers = student.parseStudentPeers(studentArray[35])

            # Student music envolvement
            self.band = studentArray[36] == 'Yes'
            self.orchestra = studentArray[37] == 'Yes'


            #### Update the requested classes for the student ####
            if self.mathPlacement: self.requestedClasses.append(self.mathPlacement) # Math Placement

            if self.grade > 6: self.lunchPeriod = 'M_L1' # Lunch Class grade 7/8
            else: self.lunchPeriod = 'M_L2'  # Lunch class grade 6
            self.requestedClasses.append(self.lunchPeriod) 

            self.requestedClasses.append('M_HR') # Add homeroom

            if self.grade > 6:  # Add core classes
                self.requestedClasses.append('M_LA') 
                self.requestedClasses.append('M_SCI')
                # self.requestedClasses.append('M_SPN')
                self.requestedClasses.append('M_SS_7_8')     


    # Print the students schedule by period
    def printStudentSched(self, print=False):

        # Write to studentSchedules.txt file 
        with open("src/printOuts/studentSchedules.txt", "a") as newFile:

            newFile.write(f'ID: {self.studentID} LAST: {self.lastName} \n')
            if print: print(f'ID: {self.studentID} LAST: {self.lastName} \n')

            for period in self.studentSched:

                if self.studentSched[period]:

                    if print: print(f'{period} : {self.studentSched[period].courseNumber}, {self.studentSched[period].courseName}, {self.studentSched[period].period}\n')
                    newFile.write(f'{period} : {self.studentSched[period].courseNumber}, {self.studentSched[period].courseName}, {self.studentSched[period].period}\n')
                
                else:

                    if print: print(f'{period} : EMPTY\n')
                    newFile.write(f'{period} : EMPTY\n')

            newFile.write('\n')

    def printStudentSchedToExcel(self, row, worksheet2, cell_format):

        worksheet2.write(row, 0, f'ID: {self.studentID}', cell_format)
        worksheet2.write(row, 1, f'LAST: {self.lastName}', cell_format)

        for i, period in enumerate(self.studentSched):

            if self.studentSched[period]:

                worksheet2.write(row, i+2, f'{period} : {self.studentSched[period].courseNumber}, {self.studentSched[period].courseName}, {self.studentSched[period].period}', cell_format)
            
            else:

                worksheet2.write(row, i+2, f'{period} : EMPTY', cell_format)

        row += 1


    # Update fully scheduled - NEED TO REPLACE WITH SOME BETTER
    def updateFullyScheduled(self):
        self.fullyScheduled == True
        for cl in self.studentSchedule:
            if cl.courseNumber == "":
                self.fullyScheduled = False
                break

    # Function to add a class to the students schdule based on the classID
    def addClassToSchedule(self, classID, teamClassesDic, print_b=False):


        def errorPrinter(stuID, classIDone, classIDtwo, period):
            print(f'ERROR: Student {stuID} scheduled into {classIDone} but already in {classIDtwo} both at period {period} -> discrepency: class period assigned and school class schedue')


        # Get the class period's classSection object 
        if classID in teamClassesDic:
            classSec = teamClassesDic[classID]
        
            # Add class id to the requested classes 
            if classSec.courseNumber not in  self.requestedClasses:
                self.requestedClasses.append(classSec.courseNumber)        

            # Add the class section to the appropriate period in the students schedule
            for i in range(1,9):
                if str(i) in classSec.period:
                    if 'B-G' in classSec.period:
                        if self.studentSched[f'_{i}B']: errorPrinter(self.studentID, classID, self.studentSched[f'_{i}B'].sectionNumber, classSec.period)
                        if self.studentSched[f'_{i}G']: errorPrinter(self.studentID, classID, self.studentSched[f'_{i}G'].sectionNumber, classSec.period)
                        self.studentSched[f'_{i}B'] = classSec
                        self.studentSched[f'_{i}G'] = classSec
                    elif 'B' in classSec.period:
                        if self.studentSched[f'_{i}B']: errorPrinter(self.studentID, classID, self.studentSched[f'_{i}B'].sectionNumber, classSec.period)
                        self.studentSched[f'_{i}B'] = classSec
                    elif 'G' in classSec.period:
                        if self.studentSched[f'_{i}G']: errorPrinter(self.studentID, classID, self.studentSched[f'_{i}G'].sectionNumber, classSec.period)
                        self.studentSched[f'_{i}G'] = classSec
                    else: raise Exception("Class period does not exist")

        elif classID == 'NOT FOUND':
            if print_b: print(f'Student {self.studentID} has NOT FOUND')
        elif classID == 'FALSE':
            if print_b: print(f'Student {self.studentID} has FALSE')
            
        else: 
            #raise Exception(f'{classID}') 
            print(f'ERROR: Student {self.studentID} is placed into {classID} which cannot be found in manz classes')


    # Funtion to add lunch to the schedule
    def addLunchToSchedule(self, teamClassesDic):
        
        classID  = ''

        # Get the students lunch period 
        if '1' in self.lunchPeriod:
            classID = 'LUNCH1'
        elif '2' in self.lunchPeriod:
            classID = 'LUNCH2'
        else: raise Exception("No such lunch exists")

        # Add lunch to their schedule
        self.addClassToSchedule(classID, teamClassesDic)

    # ????
    def findRosterIndexOfClassPeriod(self, classSec):
        indexes = []
        if "B" in classSec.period:
            indexes.append(int(classSec.period[0]))
        if "G" in classSec.period:
            indexes.append(int(classSec.period[0]) + 8)
        return indexes

    # Add class to the student schedule 
    def addClassSection(self, classSection):
        indexes = student.findRosterIndexOfClassPeriod(classSection)
        if len(indexes) == 1:
            if self.studentSchedule[indexes[0]] != "":
                self.studentSchedule[indexes[0]].append(classSection)
            else:
                print("Could not add " + classSection.courseName + " to student's roster at index: " + indexes[0])
        if len(indexes) == 2:
            if self.studentSchedule[indexes[0]] != "":
                self.studentSchedule[indexes[0]].append(classSection)
            else:
                print("Could not add " + classSection.courseName + " to student's roster at index: " + indexes[0])
            if self.studentSchedule[indexes[1]] != "":
                self.studentSchedule[indexes[1]].append(classSection)
            else:
                print("Could not add " + classSection.courseName + " to student's roster at index: " + indexes[1])
        self.classSize = self.classSize + 1


    # Correct students read in  
    def correctedStudentsReadIn(filenameOne='MAZ-CSV/COR-STU-CSV.csv', filenameTwo='MAZ-CSV/STUDENTS-CSV.csv'):

        allStuOneDic = {}

        allStuTwoDic = {}

        allStuFinalDIc = {}

        # # Open the CSV 
        # with open(filename, newline = '', encoding='utf-8-sig') as studentsCorFile:
    
        #     studentReader = csv.reader(studentsCorFile, delimiter = ',')

        #     for row in studentReader:


        #         # Check if student already exists 
        #         if row[2] in studentsDic:

        #             allCorStudentsDic[row[2]] = studentsDic[row[2]]

        #             print("UNCORRECTED: \n")
        #             studentsDic[row[2]]

        with open(filenameOne, newline = '', encoding='utf-8-sig') as stuOneFile:


            # print("Student ONE")
            

            stuOneReader = csv.reader(stuOneFile, delimiter = ',')

            for row in stuOneReader:

                row[:] = [x if x != '\xa0' else '' for x in row]

                allStuOneDic[row[2]] = row

                # print(row)
                # print("\n")


        

        with open(filenameTwo, newline = '', encoding='utf-8-sig') as stuTwoFile:


            # print("Student TWO")
            

            stuTwoReader = csv.reader(stuTwoFile, delimiter = ',')

            for row in stuTwoReader:

                row[:] = [x if x != '\xa0' else '' for x in row]

                allStuTwoDic[row[2]] = row

                # print(row)
                # print("\n")

        
        #emptyStuArr = ['Magana', 'Asher', '39054', '6', 'M', 'Pryor', 'Cascades', '8/17/09', '', '', '', '', '', '', '', '', '', '', '', '2', '2', '7th', 'Grade', 'Grade', 'Level 5', 'Level 3', '', 'ASC', '', '', '', '', 'Recommend', '', 'Vincent Jarvis, Dominic Flucas ', 'Devin Box', '', '']
        emptyStuArr = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
 


        for stuOne in allStuOneDic:

            if stuOne in allStuTwoDic:

                allStuFinalDIc[stuOne] = student(allStuTwoDic[stuOne])

            else:

                newStu = deepcopy(emptyStuArr)

                newStu[0] = allStuOneDic[stuOne][0]
                newStu[1] = allStuOneDic[stuOne][1]
                newStu[2] = allStuOneDic[stuOne][2]
                newStu[3] = str(int(allStuOneDic[stuOne][4]) - 1)
                newStu[4] = allStuOneDic[stuOne][3]

                if allStuOneDic[stuOne][5] != '': newStu[9] = 'Yes' # IEP
                if allStuOneDic[stuOne][6] != '': newStu[17] = 'Yes' # TAG

                if allStuOneDic[stuOne][7] != '':
                    if 'IEP' in allStuOneDic[stuOne][7]:
                        if 'M' in allStuOneDic[stuOne][7]:
                            newStu[12] = 'Current'
                        if 'R' in allStuOneDic[stuOne][7]:
                            newStu[10] = 'Current'
                        if 'W' in allStuOneDic[stuOne][7]:
                            newStu[11] = 'Current'
                    if 'Speech' in allStuOneDic[stuOne][7]:
                        newStu[13] = 'Current'

                newStu[19] = allStuOneDic[stuOne][8] # Acidem rate
                newStu[20] = allStuOneDic[stuOne][9] # Behave rate

                newStu[21] = allStuOneDic[stuOne][10] # Math plcment
                
                newStu[22] = allStuOneDic[stuOne][15] # Reading 
                newStu[23] = allStuOneDic[stuOne][16] # Writing 

                newStu[24] = allStuOneDic[stuOne][11] # ireadela 
                newStu[25] = allStuOneDic[stuOne][12] #  ireadymath



                allStuFinalDIc[stuOne] = student(newStu)

                    



        return allStuFinalDIc



