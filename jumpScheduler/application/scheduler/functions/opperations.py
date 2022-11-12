# src/functions/operations.py

"""
Functions for the general operations of the program and system 
"""

# Imports 
import sys
import os
from os.path import exists

# Get import path information
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
 
# Import from parent directory
import settings as settings
from classes import classes as classes
import functions.functions as functions
import functions.teacherInputFuncs as teachInp
import functions.masterExcel as xl


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def cleanTXTFiles():
    """ Function to clean previous classes.txt
    """

    # Clean classes.txt file
    with open("application/scheduler/printOuts/classes.txt", "w") as newFile:

            newFile.write(f'\n')
    
    # Clean StudentSchedules.txt file     
    with open("application/scheduler/printOuts/studentSchedules.txt", "w") as newFile:

            newFile.write(f'\n')

    # Clean excell file 
    if exists('application/excell/generated/Book2.xlsx'): 
        try:
            os.remove('application/excell/generated/Book2.xlsx')
        except OSError as e: # name the Exception `e`
            print (f"Failed with:", e.strerror )# look what it says
            print (f"Error code:", e.code )
    

    if exists('application/excell/generated/Book1.xlsx'): os.remove('application/excell/generated/Book1.xlsx')

    if exists('application/excell/import/.DS_Store'): os.remove('application/excell/import/.DS_Store')

def removeOldFiles():

    if exists('application/excell/import/output.xlsx'): os.remove('application/excell/import/output.xlsx')
    if exists('application/excell/export/output.xlsx'): os.remove('application/excell/export/output.xlsx')

def startUpPrompts():
    """ Get information from the user nessisary to run the program 
    """

    # Prompt the user to upload the excell file 
        # Prompt 
        # Comfirm 
    input("\nPlease upload your master schedule excell sheet to the INPUTS folder. \n\nPress ENTER to confirm\n")

    # Query the user for a team 
        # Select an option 1 - 4 
            # 1 Aspen 
            # 2 Manzinita 
            # 3 Sequoia 
            # 4 Enter team name 
    teams = ['A', 'M', 'S']
    team = input("Please select the team (1-4) you would like to schedule for: \n (1) Aspen \n (2) Manzanita \n (3) Sequoia \n (4) Other \n")
    if team == '4':
        team = input("Please enter the name of yout team: ")
    else:
        team = teams[int(team) - 1]

    # Determine type of math scheduling to be done 
    settings.mathSchedByGrade = (input("Would you like to schedule math students by grade (0) or by math placement (1) ?\n") == "0")

    return team

def readInFilesClasses(readInType):

    if readInType == '1':

        # Read in the classes
        allClassesDic = functions.readInClasses('MAZ-CSV/CLASSES-CSV.csv')

    elif readInType == '2':

        # Get the master excell file 
        file_name = os.listdir('application/excell/import/')

        # Read in classes from excell 
        allClassesDic = xl.readInClassesFromExcell(f'application/excell/import/{file_name[0]}')

    else: 
        raise Exception("ERROR: Invalid read in type")

    # Build master schedule from classes 
    AMSMasterSchedule = classes.masterSchedule(allClassesDic)

    return AMSMasterSchedule

def readInFilesStudents(readInType):

    if readInType == '1':

        # Read in Manzanita students
        manzStudentsDic = functions.readInStudents('MAZ-CSV/STUDENTS-CSV.csv')

        mazStudentsCorrectedDic = classes.student.correctedStudentsReadIn()

        manzStudentsDic = mazStudentsCorrectedDic

        teamStudentsDic = manzStudentsDic

    elif readInType == '2':

        # Get the master excell file 
        file_name = os.listdir('application/excell/import/')

        # Read in students from excell 
        teamStudentsDic = xl.readInStudentsFromExcell(f'application/excell/import/{file_name[0]}')

    else: 
        raise Exception("ERROR: Invalid read in type")

    return teamStudentsDic

def readInFiles(team):
    """
    """

    # readInType = input("Please select the type of file read in you would like (1 or 2): \n (1) Multi-file \n (2) Single-File \n")
    readInType = '2'

    AMSMasterSchedule = readInFilesClasses(readInType)

    teamStudentsDic = readInFilesStudents(readInType)


    # Print all classes of desired team or of whole school (if no team specified)
    #classes.masterSchedule.getOrPrintTeamClasses(AMSMasterSchedule)
    classes.masterSchedule.getOrPrintTeamClasses(AMSMasterSchedule, team, True)

    # Get the classes for specified team
    teamClasses = classes.masterSchedule.getOrPrintTeamClasses(AMSMasterSchedule, team)
    teamClassesAsDic = classes.masterSchedule.teamClassesAsDic(teamClasses)

    # Print the classes for team by period
    teamClassesByPeriod = classes.masterSchedule.getOrPrintClassesByPeriod(teamClasses, True)

    # Print the read in students
    functions.printStudents(teamStudentsDic)

    # Schedule studnts lunch periods
    functions.scheduleLunches(teamStudentsDic, teamClassesAsDic)


    if readInType == '1':

        # Read in teacher input on students placent in classes
        teacherInput = teachInp.readInTeacherInput() # NOTE: IS MISSING SPECIFIC CORE ASSIGNMENTS FROM TEACHERS

        # Populate the students requested classes and shedules with the inout from teachers 
        teachInp.populateStudentsWithTeacherInput(teamStudentsDic, teacherInput, teamClassesAsDic)

        # # Print and write file for all the students current schedules 
        # teachInp.printAllStudentsSched(manzStudentsDic)

    elif readInType != '2': raise Exception("ERROR: Invalid read in type")

    # Print the students and their requested classes 
    functions.printStudentRecClasses(teamStudentsDic)


    return [readInType, teamStudentsDic, teamClassesAsDic, AMSMasterSchedule]

def sortClasses(team, AMSMasterSchedule):

    # Get the team core classes 
    teamHRClasses = AMSMasterSchedule.wholeSchool[team]['HOMEROOMS']
    teamCoreClasses = AMSMasterSchedule.wholeSchool[team]['CORES']

    # Sort the core classes into buckets by class name 
    teamCoresBySubject = classes.masterSchedule.sortCoresBySubject(teamCoreClasses)

    # Sort the core classes into buskets by course num
    teamCoresByCourseNum = classes.masterSchedule.sortCoresByCourseNum(teamCoreClasses)
    teamHRByCourseNum = classes.masterSchedule.sortCoresByCourseNum(teamHRClasses)

    return teamCoreClasses, teamHRClasses, teamCoresBySubject, teamCoresByCourseNum, teamHRByCourseNum
