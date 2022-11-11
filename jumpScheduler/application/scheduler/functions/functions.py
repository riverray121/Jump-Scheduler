# src/functions/functions.py
"""
All functions
"""

import sys
import os
import csv
import random
import xlsxwriter



# Get import path information
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
 
# Import from parent directory
import settings as settings
from classes import classes as classes
 



#####CLASSESS FUNCTIONS

def readInClasses(filename='MAZ-CSV/CLASSES-CSV.csv'):
    """ 

    Function to read in all the classes from CSV file into a dictionary

    Args:

    Returns: 

    """

    allClassesDic = {}

    # Open classes csv 
    with open(filename, newline = '', encoding='utf-8-sig') as file:

        classReader = csv.reader(file, delimiter = ',')
        
        for row in classReader:
            
            # Add classes to dictionary with section numbers as their Keys
            allClassesDic[row[1]] = classes.classSection(row)

    return allClassesDic

# fill number of periods of each class that is offered
def fillNumberOfPeriods(allClassesDic):
    uniqueClasses = []
    for i in allClassesDic:
        if i not in uniqueClasses: # caused when we try to access a 0 key in a dictionary that doesn't contain the key
            # for x in allClassesDic: print(x)
            uniqueClasses.append(i)
    for i in uniqueClasses:
        numPeriods = len(allClassesDic[i])
        for j in range(len(allClassesDic[i])):
            allClassesDic[i][j].numberOfPeriods = numPeriods

# fill classes that only have one period
def fillClassesWithOnePeriodOffered(studentsArray):
    for i in range(len(studentsArray)):
        for j in range(len(studentsArray[i].requestedClasses)):
            if studentsArray[i].requestedClasses[j].numberOfPeriods == 1:
                studentsArray[i].addClassSection(studentsArray[i].requestedClasses[j])
                studentsArray[i].requestedClasses[j].addStudent(studentsArray[i])

# Function to print out the smallest period of each class 
def findMin(classesArray): #return a class section that the student will add to his classes array, and add that student to that class's student array

    # For each class in the dictionary 

    minimum = 1000
    minClass = []

    for cl in classesArray:

        tempMin = minimum
        minimum = min(minimum, cl.classSize)
        if tempMin != minimum:
            minClass.append(cl)
    return minClass[-1]

# Function to...
def findRosterIndexOfClassPeriod(classSec):
    indexes = []
    if "B" in classSec.period:
        indexes.append(int(classSec.period[0]))
    if "G" in classSec.period:
        indexes.append(int(classSec.period[0]) + 8)
    return indexes




#####STUDENTS FUNCTIONS 

# Function to read in all students and their attributes from CSV file
def readInStudents(filename='MAZ-CSV/STUDENTS-CSV.csv'):

    allStudentsDic = {}

    # Open the CSV 
    with open(filename, newline = '', encoding='utf-8-sig') as studentsfile:
   
        studentReader = csv.reader(studentsfile, delimiter = ',')

        for row in studentReader:
            
            # Add the students to a dictoinary with student ID's as the primary keys
            allStudentsDic[row[2]] = classes.student(row)

    return allStudentsDic

# Function to print out all the read in student information
def printStudents(studentsDic, toPrint=False):

    # Write to students.txt file 
    with open("application/scheduler/printOuts/students.txt", "w") as newFile:

        for stu in studentsDic:

            # Print student IDs and Last Names (Skipping over the student last name keys)
            if toPrint: print(f'STUDENT ID: {stu} | LAST NAME: {studentsDic[stu].lastName}')

            newFile.write(f'STUDENT ID: {stu} | LAST NAME: {studentsDic[stu].lastName} | FIRST NAME: {studentsDic[stu].firstName} GRADE: {studentsDic[stu].grade} GENDER: {studentsDic[stu].gender} STUDENT DOB: {studentsDic[stu].DOB} CASE MANAGER: {studentsDic[stu].caseManager} SPED FLAG: {studentsDic[stu].SPED} IEP READING: {studentsDic[stu].IEPReading} IEP WRITING: {studentsDic[stu].IEPWriting} IEP MATH: {studentsDic[stu].IEPMath} IEP SPEECH: {studentsDic[stu].IEPSpeech} IEP BEHAVIOR/SOCIAL: {studentsDic[stu].IEPBehaviorSocial} 504: {studentsDic[stu]._504} TAG: {studentsDic[stu].TAG} ELL: {studentsDic[stu].ELL} ACIDEMIC RATING: {studentsDic[stu].academicRating} BEHAVIOR RATING: {studentsDic[stu].behaviorRating} MATH PLACEMENT: {studentsDic[stu].mathPlacement} INC REC: {studentsDic[stu].INCRecomendations} ')

            newFile.write('\n')
      
# Function to print out the students along with their requested classes 
def printStudentRecClasses(studentsDic, toPrint=False):

    # Write to students.txt file 
    with open("application/scheduler/printOuts/students.txt", "w") as newFile:

        for stu in studentsDic:

            # Print student IDs and Last Names (Skipping over the student last name keys)
            if toPrint: print(f'STUDENT ID: {stu} | LAST NAME: {studentsDic[stu].lastName} \n')
            if toPrint: print(f'REQUESTED CLASSES: {studentsDic[stu].requestedClasses} \n')

            newFile.write(f'STUDENT ID: {stu} | LAST NAME: {studentsDic[stu].lastName} \n')
            newFile.write(f'REQUESTED CLASSES: {studentsDic[stu].requestedClasses} \n')

            newFile.write('\n')

# Functions to ...
def getRatingsAverages(allStudentsDic):
    ratingsAverageArray = []

    behaviorRatingsTotal = 0
    for i, stu in enumerate(allStudentsDic):
        behaviorRatingsTotal += allStudentsDic[stu].behaviorRating
        #numStudents = i
    behaviorRatingsAverage = behaviorRatingsTotal/i

    academicRatingsTotal = 0
    for stu in allStudentsDic:
        academicRatingsTotal += allStudentsDic[stu].academicRating
    academicRatingsAverage = academicRatingsTotal/i

    readingRatingsTotal = 0
    for stu in allStudentsDic:
        readingRatingsTotal += allStudentsDic[stu].readingLevel
    readingRatingsAverage = readingRatingsTotal/i

    writingRatingsTotal = 0
    for stu in allStudentsDic:
        writingRatingsTotal += allStudentsDic[stu].writingLevel
    writingRatingsAverage = writingRatingsTotal/i

    ratingsAverageArray.append(behaviorRatingsAverage)
    ratingsAverageArray.append(academicRatingsAverage)
    ratingsAverageArray.append(readingRatingsAverage)
    ratingsAverageArray.append(writingRatingsAverage)

    return ratingsAverageArray



##### SCHEDULING FUNCTIONS 

def getPrincipalsIdealWeights():
    """ Function to query for ideal weights
    """

    principalWeights = []
    print("On a scale of 1->10, how much do you value the gender ratio in your classes?")
    genderW = int(input())
    principalWeights.append(genderW)
    
    print("On a scale of 1->10, how much do you value the seventh/eighth grade ratio in your classes?")
    gradeW = int(input())
    principalWeights.append(gradeW)

    print("On a scale of 1->10, how much do you value the equal distribution of students' behavior in your classes?")
    behaviorW = int(input())
    principalWeights.append(behaviorW)

    print("On a scale of 1->10, how much do you value the equal distribution of students' academic abilities in your classes?")
    academicW = int(input())
    principalWeights.append(academicW)

    print("On a scale of 1->10, how much do you value the equal distribution of students' reading abilities in your classes?")
    readingW = int(input())
    principalWeights.append(readingW)

    print("On a scale of 1->10, how much do you value the equal distribution of students' writing abilities in your classes?")
    writingW = int(input())
    principalWeights.append(writingW)

    return principalWeights
        
def sortStudentsIntoCoreClasses(classSection, ratingsAverageArray, allStudentsDic, principalWeights, teamClassesAsDic):
    """ Function to sort students into core classes 
    """
    #create IALs (Ideal Average Lines) for each of the class's ideal characteristics which are increased as the class size increases
    behaviorIAL = ratingsAverageArray[0] + (ratingsAverageArray[0] * len(classSection.classRoster))
    academicIAL = ratingsAverageArray[1] + (ratingsAverageArray[1] * len(classSection.classRoster))
    readingIAL = ratingsAverageArray[2] + (ratingsAverageArray[2] * len(classSection.classRoster))
    writingIAL = ratingsAverageArray[3] + (ratingsAverageArray[3] * len(classSection.classRoster))

    classPer = findRosterIndexOfClassPeriod(classSection)

    #add infinitely bad student to winning student array, and each time a student beats out that student (tempStudent) they are added to the back of the winning student array and then tempStudent is set to that student which has just been added. After iterating through all students, the best student to add will be at the back of the winning student's array
    winningStudent = []
    tempStudent = classes.student()
    tempStudent.firstName = "Mistake"
    tempStudent.lastName = "Mistake"
    tempStudent.gender = "M"
    tempStudent.behaviorRating = 100000
    tempStudent.academicRating = 100000
    tempStudent.writingRating = 100000
    tempStudent.readingRating = 100000
    winningStudent.append(tempStudent)



    #give each a weight
    Bweight = settings.BR - behaviorIAL
    Aweight = settings.AR - academicIAL
    Rweight = settings.RR - readingIAL
    Wweight = settings.WR - writingIAL

    #find gender ratio
    M = 0
    F = 0
    womanWeight = 0
    manWeight = 0
    for i in classSection.classRoster:
        if i.gender == "M":
            M += 1
        elif i.gender == "F":
            F += 1
        else:
            randomNumber = random.randint(0,1)
            if randomNumber == 1:
                M += 1
            else:
                F += 1
    if M > F:
        womanWeight = (M - F)
    else:
        manWeight = (F - M)
    
    #find seventh/eighth grade ratio
    numSeventhGraders = 0
    numEighthGraders = 0
    seventhWeight = 0
    eighthWeight = 0
    for i in classSection.classRoster:
        if i.grade == 7:
            numSeventhGraders += 1
        else:
            numEighthGraders += 1
    if numSeventhGraders > numEighthGraders:
        seventhWeight = numEighthGraders - numSeventhGraders
    else:
        eighthWeight = numSeventhGraders - numEighthGraders

    for i, stu in enumerate(allStudentsDic):
        canAdd = True
        isInRequestedClasses = False
        for j in allStudentsDic[stu].studentSchedule:
            if j.courseName == classSection.courseName:
                canAdd = False
            for req in allStudentsDic[stu].requestedClasses:
                if req == classSection.courseNumber:
                    isInRequestedClasses = True
                    break
            
        if canAdd and isInRequestedClasses:
            
            maleCode = 0
            femaleCode = 0
            seventhGradeCode = 0
            eighthGradeCode = 0
            if allStudentsDic[stu].gender == "F":
                femaleCode = 50 * principalWeights[0]
            else: 
                maleCode = 50 * principalWeights[0]
            if allStudentsDic[stu].grade == 7:
                seventhGradeCode = 50 * principalWeights[0]
            else:
                eighthGradeCode = 50 * principalWeights[0]
            
            tempMaleCode = 0
            tempFemaleCode = 0
            tempSeventhGradeCode = 0
            tempEighthGradeCode = 0
            if tempStudent.gender == "F":
                tempFemaleCode = 50 * principalWeights[1]
            else: 
                tempMaleCode = 50 * principalWeights[1]
            if tempStudent.grade == 7:
                tempSeventhGradeCode = 50 * principalWeights[1]
            else:
                tempEighthGradeCode = 50 * principalWeights[1]
            
            
            num1a = (((((allStudentsDic[stu].behaviorRating + settings.BR - behaviorIAL) * (allStudentsDic[stu].behaviorRating + settings.BR - behaviorIAL)) * Bweight * principalWeights[2]) + (((allStudentsDic[stu].academicRating + settings.AR - academicIAL) * (allStudentsDic[stu].academicRating + settings.AR - academicIAL)) * Aweight * principalWeights[3]) + (((allStudentsDic[stu].readingLevel + settings.RR - readingIAL) * (allStudentsDic[stu].readingLevel + settings.RR - readingIAL)) * Rweight * principalWeights[4]) + (((allStudentsDic[stu].writingLevel + settings.WR - writingIAL) * (allStudentsDic[stu].writingLevel + settings.WR- writingIAL))) * Wweight * principalWeights[5]))
            
            num1b = ((maleCode * manWeight) + (femaleCode * womanWeight)) + ((seventhGradeCode * seventhWeight) + (eighthGradeCode * eighthWeight))

            num2a = ((((tempStudent.behaviorRating + settings.BR - behaviorIAL) * (tempStudent.behaviorRating + settings.BR - behaviorIAL)) * Bweight * principalWeights[2]) + (((tempStudent.academicRating + settings.AR - academicIAL) * (tempStudent.academicRating + settings.AR - academicIAL)) * Aweight * principalWeights[3]) + (((tempStudent.readingLevel + settings.RR - readingIAL) * (tempStudent.readingLevel + settings.RR - readingIAL)) * Rweight * principalWeights[4]) + (((tempStudent.writingLevel + settings.WR - writingIAL) * (tempStudent.writingLevel + settings.WR - writingIAL)) * Wweight * principalWeights[5]))
            
            num2b = ((tempMaleCode * manWeight) + (tempFemaleCode * womanWeight)) + ((tempSeventhGradeCode * seventhWeight) + (tempEighthGradeCode * eighthWeight))


            if abs(num1a) - num1b < abs(num2a) - num2b and (allStudentsDic[stu].studentSchedule[classPer[0]].courseName == "" and allStudentsDic[stu].studentSchedule[classPer[-1]].courseName == ""):
                winningStudent.append(allStudentsDic[stu])
                tempStudent = allStudentsDic[stu]

    settings.BR += winningStudent[-1].behaviorRating
    settings.AR += winningStudent[-1].academicRating
    settings.RR += winningStudent[-1].readingLevel
    settings.WR += winningStudent[-1].writingLevel
    
    winningStudent[-1].studentSchedule[classPer[0]] = classSection
    winningStudent[-1].studentSchedule[classPer[-1]] = classSection

    winningStudent[-1].addClassToSchedule(classSection.sectionNumber, teamClassesAsDic)

    classSection.addStudent(winningStudent[-1])
    winningStudent.clear()

def scheduleLunches(allStudentsDic, teamClassesDic):
    """ Funtion to schedule the lunch of all students
    """
    for stu in allStudentsDic:

        allStudentsDic[stu].addLunchToSchedule(teamClassesDic)

def tempScheduleStudentsFunction(allStudentsDic, teamCoresByCourseNum, ratingsAverageArray, principalWeights, courseNum, row, column, column2, column3, teamClassesAsDic, workbook, worksheet, worksheet2, worksheet3):
    #with open("theoStudentScheduleOutput.txt", "a") as myfile:
        # myfile.write("appended text")
    # Schedule the students
    
    tempRow = row
    
    for i in allStudentsDic:

        classToBeUpdated = findMin(teamCoresByCourseNum[courseNum])
        sortStudentsIntoCoreClasses(classToBeUpdated, ratingsAverageArray, allStudentsDic, principalWeights, teamClassesAsDic)
       
        # if classToBeUpdated[-1].firstName == "Mistake":
        #     for j in allStudentsDic: #find the first student j that is missing from that subject
        #         hasClass = False
        #         for k in j.studentSchedule:
        #             if k.courseNum == classToBeUpdated.courseNum:
        #                 hasClass = True
        #                 break
        #         if hasClass == False: #needs to be added to a classSection of this subject
        #             arr = []
        #             while arr.length < allClassesDic.length and not done:

        #                 while(arr[-1].courseNum == arr[-2].courseNum and not done):
        #                     fakeArray = manzCoresByCourseNum['M_LA'] #needs to be added to M_LA
        #                     bestOption = findMin(fakeArray)
        #                     if j.studentSchedule[findRosterIndexOfClassPeriod(bestOption)[0]].courseNum and j.studentSchedule[findRosterIndexOfClassPeriod(bestOption)[-1]].courseNum in manzCoresByCourseNum:
        #                         #switch to a different period
        #                         for l in manzCoresByCourseNum[j.studentSchedule[findRosterIndexOfClassPeriod(bestOption)[0]].courseNum]: #iterate through all M_LA
        #                             if not (j.studentSchedule[findRosterIndexOfClassPeriod(l)[0]] and j.studentSchedule[findRosterIndexOfClassPeriod(l)[-1]]):
        #                                 j.studentSchedule[findRosterIndexOfClassPeriod(l)[0]] = l
        #                                 j.studentSchedule[findRosterIndexOfClassPeriod(l)[-1]] = l
        #                                 l.classRoster.append(j)
        #                                 j.studentSchedule[findRosterIndexOfClassPeriod(bestOption)[0]] = bestOption
        #                                 j.studentSchedule[findRosterIndexOfClassPeriod(bestOption)[-1]] = bestOption
        #                                 done = True
        #                                 break
        #                             arr.append(l)
                        
                            

        # get first student from allStudentsDic who has not been scheduled into a classSection yet
        # find smallest class in 

    # PRINT OUT SCHEDULED INFO
    behPrintArray = []
    acaPrintArray = []
    reaPrintArray = []
    wriPrintArray = []
    for i, clas in enumerate(teamCoresByCourseNum[courseNum]):
        worksheet.write(row, column, f'{courseNum} period {str(i+1)} Roster:')
        worksheet3.write(0, column3, f'{courseNum} period {str(i+1)} Roster:')
        row += 2
        M = 0
        F = 0
        nonBinary = 0
        sev = 0
        eig = 0
        beh = 0
        aca = 0
        rea = 0
        wri = 0

        behRatArray = {'1': 0, '2': 0, '3': 0}
        acaRatArray = {'1': 0, '2': 0, '3': 0}
        reaRatArray = {'1': 0, '2': 0, '3': 0}
        wriRatArray = {'1': 0, '2': 0, '3': 0}

        for index, j in enumerate(clas.classRoster):
            worksheet.write(row, column, j.firstName)
            worksheet.write(row, column+1, j.lastName)
            worksheet.write(row, column+2, str(j.behaviorRating))
            worksheet.write(row, column+3, str(j.academicRating))
            worksheet.write(row, column+4, str(j.readingLevel))
            worksheet.write(row, column+5, str(j.writingLevel))

            worksheet3.write(index+1, column3, f'{j.firstName} {j.lastName}')
            row += 1
            if j.gender == "M":
                M += 1
            elif j.gender == "F":
                F += 1
            else:
                nonBinary += 1
            if j.grade == 7:
                sev += 1
            else: 
                eig += 1
            beh += j.behaviorRating
            aca += j.academicRating
            rea += j.readingLevel
            wri += j.writingLevel

            if str(j.behaviorRating) in behRatArray: behRatArray[str(j.behaviorRating)] += 1
            else: behRatArray[str(j.behaviorRating)] = 1
            if str(j.academicRating) in acaRatArray: acaRatArray[str(j.academicRating)] += 1
            else: acaRatArray[str(j.academicRating)] = 1
            if str(j.readingLevel) in reaRatArray: reaRatArray[str(j.readingLevel)] += 1
            else: reaRatArray[str(j.readingLevel)] = 1
            if str(j.writingLevel) in wriRatArray: wriRatArray[str(j.writingLevel)] += 1
            else: wriRatArray[str(j.writingLevel)] = 1
        
        maleToFem = "infinity"
        if F != 0: maleToFem = M/F

        sevToEig = "infinity"
        if eig != 0: sevToEig = sev/eig

        column3 += 1
        row +=1
        worksheet.write(row, column, 'General Statistics:')
        row += 2
        worksheet.write(row, column, f'Gender ratio of Boys to Girls =  {str(maleToFem)} or M:F of {M}:{F} with {nonBinary} non-binary students')
        row +=1
        worksheet.write(row, column, f'7th to 8th grade ratio = {str(sevToEig)} or 7th:8th of {sev}:{eig}')
        row += 2
        behPrint = f'Total Behavior ratings in {courseNum} period {str(i)} are {beh}:     {behRatArray[str(1)]} students who have BRs of 1, {behRatArray[str(2)]} with BRs of 2, and {behRatArray[str(3)]} with BRs of 3'
        worksheet.write(row, column, behPrint)
        row += 1
        behPrintArray.append(behPrint)
        acaPrint = f'Total Academic ratings in {courseNum} period {str(i)} are {aca}:     {acaRatArray[str(1)]} students who have ARs of 1, {acaRatArray[str(2)]} with ARs of 2, and {acaRatArray[str(3)]} with ARs of 3'
        worksheet.write(row, column, acaPrint)
        row += 1
        acaPrintArray.append(acaPrint)
        reaPrint = f'Total reading ratings in {courseNum} period {str(i)} are {rea}:     {reaRatArray[str(1)]} students who have RRs of 1, {reaRatArray[str(2)]} with RRs of 2, and {reaRatArray[str(3)]} with RRs of 3'
        worksheet.write(row, column, reaPrint)
        row += 1
        reaPrintArray.append(reaPrint)
        wriPrint = f'Total writing ratings in {courseNum} period {str(i)} are {wri}:     {wriRatArray[str(1)]} students who have WRs of 1, {wriRatArray[str(2)]} with WRs of 2, and {wriRatArray[str(3)]} with WRs of 3'
        worksheet.write(row, column, wriPrint)
        row += 2
        wriPrintArray.append(wriPrint)
    

    seventh = 0
    eighth = 0 
    num = 0
    for i in allStudentsDic:
        if allStudentsDic[i].grade == 7:
            seventh += 1
        else: 
            eighth += 1
        num += 1
   
    row = tempRow
    worksheet2.write(row, column2, 'School-Wide Statistics:\n\n' + "seventh to eighth ratio is " + str(seventh/eighth))
    row += 1
    worksheet2.write(row, column2, "total number of students " + str(num))
    row += 3

    for i in behPrintArray:
        worksheet2.write(row, column2, i)
        row += 1
    row += 2
    for i in acaPrintArray:
        worksheet2.write(row, column2, i)
        row += 1
    row += 2
    for i in reaPrintArray:
        worksheet2.write(row, column2, i)
        row += 1
    row += 2
    for i in wriPrintArray:
        worksheet2.write(row, column2, i)
        row += 1
    row += 2

    fillNumberOfPeriods(teamCoresByCourseNum)

def excellTemp(teamClassesByCourseNum, course, colmOne, colmTwo):
    """ temp excell function 
    """

    #temp = 0
    for i, clas in enumerate(teamClassesByCourseNum[course]):
        temp = i
    settings.column3 += temp+2
    settings.column = colmOne
    settings.column2 = colmTwo
    # print('column = ' + str(column) + '\n')

    settings.xlConstOne = settings.xlConstOne * 2
    settings.xlConstTwo = settings.xlConstOne + 2

def scheduleStudents(teamStudentsDic, teamCoresByCourseNum, ratingsAverageArray, principalWeights, teamClassesAsDic, teamHRByCourseNum, toSchedInputs):
    """ Function to schedule everything 
    """

    # WHILE STUDENTS-ALL-SCHEDULED == FLASE

        # STEP 1: Sort students into classes that only have one period

        # STEP 2: Schedule all remaining SPED classes
            # - Distrubuter function
                # Input: All sped classes, and all students with Sped attribute 
                # Output: Students scheduled into all classes, distrubuted equally by
                    # Class size, Grade, gender, acidemics, behavior, sped, 504, migrant ed, home language (prioritized in that order)

        # STEP 3: Schedule all remaining MAth Placement classes
            # Distrubuter function

        # STEP 4: Schedule all remaining Spanish Placement classes
            # Distrubuter function

        # STEP 5: Schedule all remaining ELL classes
            # Distrubuter function

        # STEP 6: Schedule all remaining ASC classes
            # Distrubuter function

        # STEP 7: Schedule all remaining INC Classes classes
            # Distrubuter function

            # STEP 7.5: - Wind Ensamble and Orchestra

        # STEP 8: Schedule all remaining CORE classes
            # Distrubuter function
            

        # ALSO - IEP, CORE, and OTHER???

        # NEGATIVE PEERS, POSATIVE PEERS 

# Distrubuter function
# Input: All sped classes, and all students with Sped attribute 
    # Output: Students scheduled into all classes, distrubuted equally by
            # Grade, gender, acidemics, behavior, sped, 504, migrant ed, home language (prioritized in that order)

    # courseArr = []
    # toScheArr = []
    toScheArr = toSchedInputs

    # print(f'Please choose which classes you would like to schedule: ')
    # for i, course in enumerate(teamCoresByCourseNum):
    #     courseArr.append(course)
    #     print(f'({i}) {course}')

    # print(f'Type each class you would like (0 - {int(len(courseArr)) - 1}) followed by ENTER \nWhen finished press "d" followed by ENTER')

    # userInput = ''

    # while userInput != "d":
    #     userInput = input()
    #     if userInput == "d": break
    #     toScheArr.append(courseArr[int(userInput)])

    # print(toScheArr)

    print("Begining Scheduling")

    # Order in which to schedule classes 
    scheduleOrder = ['M_INT_MATH8', 'M_INT_MATH7', 'M_SPN_ADV', 'M_SPN', 'M_SS_7_8', 'M_SCI', 'M_LA']

    # Schedule the selected classes 
    for cl in scheduleOrder:

        if cl in toScheArr:

            tempScheduleStudentsFunction(teamStudentsDic, teamCoresByCourseNum, ratingsAverageArray, principalWeights, cl, 0, settings.column, settings.column2, settings.column3, teamClassesAsDic, settings.workbook, settings.worksheet, settings.worksheet2, settings.worksheet3)
            excellTemp(teamCoresByCourseNum, cl, settings.xlConstOne, settings.xlConstTwo)

    tempScheduleStudentsFunction(teamStudentsDic, teamHRByCourseNum, ratingsAverageArray, principalWeights, 'M_HR', 0, settings.column, settings.column2, settings.column3, teamClassesAsDic, settings.workbook, settings.worksheet, settings.worksheet2, settings.worksheet3)
    excellTemp(teamHRByCourseNum, 'M_HR', settings.xlConstOne, settings.xlConstTwo)


    return 0
