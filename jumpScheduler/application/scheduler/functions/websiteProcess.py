# jumpScheduler/application/scheduler/functions/websiteProcess.py

""" 
"""

# Imports 
import sys
import os
from os.path import exists

# Get import path information
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import settings as settings

def processUserInput(webInput):


    # Query the user for a team 
        # Select an option 1 - 4 
            # 1 Aspen 
            # 2 Manzinita 
            # 3 Sequoia 
            # 4 Enter team name 
    teams = ['A', 'M', 'S']
    team = webInput[1]
    team = teams[int(team) - 1]
    print(f'Scheduling for {team}')

    # Determine type of math scheduling to be done 
    settings.mathSchedByGrade = True
    #settings.mathSchedByGrade = (input("Would you like to schedule math students by grade (0) or by math placement (1) ?\n") == "0")

    return team


def processWebPrincipalWeights(webWeights):

    principalWeights = []

    genderW = int(webWeights[0])
    principalWeights.append(genderW)
    
    gradeW = int(webWeights[1])
    principalWeights.append(gradeW)

    behaviorW = int(webWeights[2])
    principalWeights.append(behaviorW)

    academicW = int(webWeights[3])
    principalWeights.append(academicW)

    readingW = int(webWeights[4])
    principalWeights.append(readingW)

    writingW = int(webWeights[5])
    principalWeights.append(writingW)

    print(f'Principle weights are {principalWeights}')

    return principalWeights
