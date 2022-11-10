# settings.py
import xlsxwriter

def initVariables():

    global mathSchedByGrade
    mathSchedByGrade = False

    global BR
    BR = 0
    global AR
    AR = 0
    global RR 
    RR = 0
    global WR
    WR = 0

    global column
    column = 0
    global column2
    column2 = 0
    global column3
    column3 = 0

    global xlConstOne
    xlConstOne = 7
    global xlConstTwo
    xlConstTwo = 2

    global workbook 
    workbook = xlsxwriter.Workbook("Book1.xlsx")
    global worksheet
    worksheet = workbook.add_worksheet("Bulk Roster w Stats")
    global worksheet2
    worksheet2 = workbook.add_worksheet("Side By Side Comparisons")
    global worksheet3
    worksheet3 = workbook.add_worksheet("Simple Class Rosters")