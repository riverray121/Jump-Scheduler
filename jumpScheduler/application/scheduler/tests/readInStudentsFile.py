# readInStudentsFile.py

import csv


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

    # Initiate a new student instance
    def __init__(self, studentArray):

        self.requestedClasses = []

        self.lastName = studentArray[0]
        self.firstName = studentArray[1]
        self.studentID = studentArray[2]

        self.grade = int(studentArray[3]) + 1
        self.gender = studentArray[4]

        self.sixthHR = studentArray[5]
        self.sixthTeam = studentArray[6]

        self.DOB = studentArray[7]

        self.caseManager = studentArray[8]

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

        self.academicRating = int(studentArray[19])
        self.behaviorRating = int(studentArray[20])

        # Correct math placement        NOTE: Does not account for HS geo placement 
        self.mathPlacement = ''
        if studentArray[21] == '7th': self.mathPlacement = 'M_INT_MATH7'    # WILL NEED TO BE MODIFIED TO WORK WITH 6TH GRADERS
        elif studentArray[21] == 'sped': self.mathPlacement = 'SPED_MATH'
        else: self.mathPlacement == 'M_INT_MATH8'

        self.readingLevel = studentArray[22]
        self.writingLevel = studentArray[23]
        self.iReadyELAWinter = studentArray[24]
        self.iReadyMathWinter = studentArray[25]

        if self.readingLevel == "Below": self.readingLevel = 1
        elif self.readingLevel == "Grade": self.readingLevel = 2
        else: self.readingLevel = 3
            
        if self.writingLevel == "Below": self.writingLevel = 1
        elif self.writingLevel == "Grade": self.writingLevel = 2
        else: self.writingLevel = 3

        self.sixthINC = studentArray[26]
        self.INCRecomendations = studentArray[27]

        self.coreReadingSupport = studentArray[28] == 'Current'
        self.strugglesWithOrganization = studentArray[29] == 'Yes'
        self.strugglesWithWorkCompletion = studentArray[30] == 'Yes'
        self.strugglesWithAttendance = studentArray[31] == 'Yes'

        self.ASCReccomended = studentArray[32] != ''
        self.nativeSpanishSpeaker = studentArray[33] == 'Yes'

        self.posativePeers = studentArray[34]
        self.negativePeers = studentArray[35]

        self.band = studentArray[36] == 'Yes'
        self.orchestra = studentArray[37] == 'Yes'


        self.studentSchedule = []
        for i in range(0, 16): self.studentSchedule.append("")

        self.fullyScheduled = False


        #### Update the requested classes for the student ####
        if self.mathPlacement: self.requestedClasses.append(self.mathPlacement) # Math Placement

        if self.grade > 6: self.requestedClasses.append('M_L1') # Lunch Class grade 7/8
        else: self.requestedClasses.append('M_L2')  # Lunch class grade 6

        self.requestedClasses.append('M_HR') # Add homeroom


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

    

    # Update fully scheduled - NEED TO REPLACE WITH SOME BETTER
    def updateFullyScheduled(self):
        if "" not in self.studentSchedule: self.fullyScheduled = True

    # 
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


# Function to read in all students and their attributes from CSV file
def readInStudents(filename='MAZ-CSV/STUDENTS-CSV.csv'):

    allStudentsDic = {}

    # Open the CSV 
    with open(filename, newline = '', encoding='utf-8-sig') as studentsfile:
   
        studentReader = csv.reader(studentsfile, delimiter = ',')

        for row in studentReader:
            
            # Add the students to a dictoinary with student ID's as the primary keys
            allStudentsDic[row[2]] = student(row)

    return allStudentsDic


# Function to print out all the read in student information
def printStudents(allStudents):

    # Write to students.txt file 
    with open("src/printOuts/students.txt", "w") as newFile:

        for student in allStudents:

            # Print student IDs and Last Names (Skipping over the student last name keys)
            print(f'STUDENT ID: {student} | LAST NAME: {allStudents[student].lastName}')

            newFile.write(f'STUDENT ID: {student} | LAST NAME: {allStudents[student].lastName} | FIRST NAME: {allStudents[student].firstName} GRADE: {allStudents[student].grade} GENDER: {allStudents[student].gender} STUDENT DOB: {allStudents[student].DOB} CASE MANAGER: {allStudents[student].caseManager} SPED FLAG: {allStudents[student].SPED} IEP READING: {allStudents[student].IEPReading} IEP WRITING: {allStudents[student].IEPWriting} IEP MATH: {allStudents[student].IEPMath} IEP SPEECH: {allStudents[student].IEPSpeech} IEP BEHAVIOR/SOCIAL: {allStudents[student].IEPBehaviorSocial} 504: {allStudents[student]._504} TAG: {allStudents[student].TAG} ELL: {allStudents[student].ELL} ACIDEMIC RATING: {allStudents[student].academicRating} BEHAVIOR RATING: {allStudents[student].behaviorRating} MATH PLACEMENT: {allStudents[student].mathPlacement} INC REC: {allStudents[student].INCRecomendations} ')

            newFile.write('\n')
      

# Function to print out the students along with their requested classes 
def printStudentRecClasses(allStudents):


    # Write to students.txt file 
    with open("src/printOuts/students.txt", "w") as newFile:

        for student in allStudents:

            # Print student IDs and Last Names (Skipping over the student last name keys)
            print(f'STUDENT ID: {student} | LAST NAME: {allStudents[student].lastName} \n')
            print(f'REQUESTED CLASSES: {allStudents[student].requestedClasses} \n')

            newFile.write(f'STUDENT ID: {student} | LAST NAME: {allStudents[student].lastName} \n')
            newFile.write(f'REQUESTED CLASSES: {allStudents[student].requestedClasses} \n')

            newFile.write('\n')
    

# Function read in the predetermined teacher input -- in the future this will need to queery the user
def readInTeacherInput():
    return 0




# # MAIN EXECUTION 
# def main():
    
#     # Read in Students 
#     manzStudentsDic = readInStudents()

#     # Print all Students 
#     printStudents(manzStudentsDic)


#     # Print students and their requested classes
#     printStudentRecClasses(manzStudentsDic)

#     # Read in the input from the teachers 

#     # Print students and their requested classes




# # RUN MAIN 
# if __name__ == '__main__':

#     main()

