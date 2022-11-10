# jumpScheduler/application/scheduler/runScheduler.py

""" Main functions for running the scheduling software 
"""

# Imports
from .functions import functions as functions
from .functions import websiteProcess as wP
import functions.opperations as operations
import functions.teacherInputFuncs as teachInp
import functions.masterExcel as masterXL
import settings as settings
import classes.classes as classes


def scheduleForAMS(teacherInputs):
    """ Schedule using an AMS spreadsheet as the inport
    
    """

    # Initiate all global variables 
    settings.initVariables()

    # Clean .txt files
    operations.cleanTXTFiles()

    # # Querry user with startup prompts 
    # team = operations.startUpPrompts()

    # Process the input from the user from the website 
    team = wP.processUserInput(teacherInputs)

    schoolInfo = operations.readInFiles(team)

    readInType, teamStudentsDic, teamClassesAsDic, AMSMasterSchedule = schoolInfo

    # Get ratings average array 
    ratingsAverageArray = functions.getRatingsAverages(teamStudentsDic)

    # Sort the teams classes 
    teamCoreClasses, teamHRClasses, teamCoresBySubject, teamCoresByCourseNum, teamHRByCourseNum = operations.sortClasses(team, AMSMasterSchedule)

    # # Query the scheduler for weights for attributes 
    # principalWeights = functions.getPrincipalsIdealWeights()
    principalWeights = wP.processWebPrincipalWeights(teacherInputs[0])

    # Schedule the students into the core class and print results 
    functions.scheduleStudents(teamStudentsDic, teamCoresByCourseNum, ratingsAverageArray, principalWeights, teamClassesAsDic, teamHRByCourseNum, teacherInputs[2])
    
    settings.workbook.close()
    
    #functions.writeToExcelTest()
    teachInp.printAllStudentsSched(teamStudentsDic)

    masterXL.writeToMasterExcell(teamStudentsDic)
