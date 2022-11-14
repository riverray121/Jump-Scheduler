# jumpScheduler/application/routes.py 

"""
"""
from flask import Flask, request, render_template, send_file, session
# import pandas as pd
from jinja2  import TemplateNotFound
import os
import datetime

from application import application
from .scheduler import runScheduler
from .scheduler import settings
from .scheduler.functions import opperations

# App main route + generic routing
@application.route('/')
def index():
    return render_template('/index.html')

#background process happening without any refreshing
@application.route('/background_process_test')
def background_process_test():

    teacherInput = session.get('teacherInput', None)

    print("RUNNING SCHEDULER")

    # Run the scheuduler using the uploaded excell file and the teacher input / preferences 
    runScheduler.scheduleForAMS(teacherInput)

    print("SHEDULER COMPLETE")

    # return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return "SHEDULER COMPLETE"

@application.route('/progress')
def schedule_progress():
    # print(opperations.getScheduleProgress())
    # print("\n")
    return str(opperations.getScheduleProgress())

@application.route('/excell-download')
def download_file():
    p = "excell/export/output.xlsx"
    return send_file(p, as_attachment=True)

@application.route('/download-file-ams-manz')
def download_file_ams_manz():
    f = "excell/AMS-MANZ/2022.23 Manzanita Master Schedule example 2.xlsx"
    return send_file(f, as_attachment=True)

@application.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@application.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard/dashboard-dashboard.html')

@application.route('/dashboard-analytics', methods=['GET'])
def dashboardAnalytics():
    return render_template('dashboard/dashboard-analytics.html')

@application.route('/dashboard-payment', methods=['GET'])
def dashboardPayment():
    return render_template('dashboard/dashboard-payment.html')


# Scheduler Routes
@application.route('/scheduler-excell-import', methods=['GET', 'POST'])
def excelImport():
    return render_template('dashboard/scheduler/excel-import.html')

@application.route('/scheduler-teacher-input', methods=['GET', 'POST'])
def teacherInput():
    if request.method == 'POST':
        file = request.files['file'] 
        if not os.path.exists(f'{application.config.root_path}/excell/import'): os.mkdir(f'{application.config.root_path}/excell/import')
        if not os.path.exists(f'{application.config.root_path}/excell/export'): os.mkdir(f'{application.config.root_path}/excell/export')
        if not os.path.exists(f'{application.config.root_path}/excell/generated'): os.mkdir(f'{application.config.root_path}/excell/generated')
        if not os.path.exists(f'{application.config.root_path}/static/generated'): os.mkdir(f'{application.config.root_path}/static/generated')

        opperations.removeOldFiles()

        file.save(f'{application.config.root_path}/excell/import/output.xlsx')
        print(f'APP ROOT PATH: {application.config.root_path}')
        #data = pd.read_excel(f'jumpScheduler/application/excell/import/output.xlsx')
        
        #return render_template('ratings.html', data=data.to_dict())
        return render_template('dashboard/scheduler/teacher-input.html')

@application.route('/scheduler-schedule', methods=['POST'])
def schedule():

    ratingsArray = []
    firsttext = request.form['gender ratio']
    ratingsArray.append(firsttext)
    sectext = request.form['grade ratio']
    ratingsArray.append(sectext)
    thirdtext = request.form['behavior ratings']
    ratingsArray.append(thirdtext)
    fourthtext = request.form['academic ratings']
    ratingsArray.append(fourthtext)
    fifthtext = request.form['reading ratings']
    ratingsArray.append(fifthtext)
    sixthtext = request.form['writing ratings']
    ratingsArray.append(sixthtext)

    teamID = request.form["team ID"]

    math8 = request.form.get('math8')
    math7 = request.form.get('math7')
    advspn = request.form.get('advspn')
    spn = request.form.get('spn')
    socialstud = request.form.get('socialstud')
    sci = request.form.get('sci')
    langart = request.form.get('langart')

    classesToSchedule = [math8, math7, advspn, spn, socialstud, sci, langart]

    teacherInput = [ratingsArray, teamID, classesToSchedule]

    session['teacherInput'] = teacherInput

    return render_template('dashboard/scheduler/schedule.html')

@application.route('/scheduler-completed', methods=['POST'])
def scheduleCompleted():
    return render_template('dashboard/scheduler/download-output.html')