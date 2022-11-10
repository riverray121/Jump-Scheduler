# teacherInputFuncs.py

import sys
import os
import csv
import functions
import xlsxwriter

# Get import path information
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import classes.classes as classes

# Function read in the predetermined teacher input -- in the future this will need to queery the user
def readInTeacherInput(filename='MAZ-CSV/INC-PCAT-CSV.csv'):

    # Read in MAZ-CSV/INC-PCAT-CSV.csv
    teacherAssignedINCandPCATs = {}
    
    # Open classes csv 
    with open(filename, newline = '', encoding='utf-8-sig') as file:

        classReader = csv.reader(file, delimiter = ',')
        
        for row in classReader:

            if row[0] not in teacherAssignedINCandPCATs:
                # Add to dictionary 
                teacherAssignedINCandPCATs[row[0]] = [row[6].upper()]
                # print(row[6].upper())
            else:
                teacherAssignedINCandPCATs[row[0]].append(row[6].upper())
                # print(row[6].upper())

            # print(f'STUDENT ID: {row[0]} INC/PCAT: {row[6]}')

    return teacherAssignedINCandPCATs

# Function to add read in teacher input of classes to the students requested classes 
def populateStudentsWithTeacherInput(allStudentsDic, teacherInput, manzanitaClasses):

    # Add the class to the student's schedule
    for cl in teacherInput:

        if cl in allStudentsDic:
            for i in range(len(teacherInput[cl])):
                allStudentsDic[cl].addClassToSchedule(teacherInput[cl][i], manzanitaClasses)
        else:
            print(f'STUDENT {cl} (placed into {teacherInput[cl]}) was read in from teach input, but not in class list')


# Print the schedules of all students
def printAllStudentsSched(allStudentsDic):
    row = 0
    workbook2 = xlsxwriter.Workbook("application/excell/generated/Book2.xlsx")
    worksheet2 = workbook2.add_worksheet("secSheet")
    cell_format = workbook2.add_format()
    cell_format.set_text_wrap()

    for i in range(2,10):
        worksheet2.write(row, i, f'period {i-1}(B)', cell_format)
    for i in range(10,18):
        worksheet2.write(row, i, f'period {i-9}(G)', cell_format)
    row += 2

    for stu in allStudentsDic:

        allStudentsDic[stu].printStudentSched()
        allStudentsDic[stu].printStudentSchedToExcel(row, worksheet2, cell_format)
        row += 2

    workbook2.close()



