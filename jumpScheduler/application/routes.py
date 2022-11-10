# jumpScheduler/application/routes.py 

"""
"""
from flask import Flask, request, render_template, send_file
# import pandas as pd
from jinja2  import TemplateNotFound

from application import application
from .scheduler import runScheduler

# App main route + generic routing
@application.route('/')
def index():
    return render_template( '/index.html' )

# @app.route('/login')
# def login():
#     return "<h1>Welcome</h1>"

@application.route('/excell-upload', methods=['GET','POST'])
def excellUpload():
    return render_template('excellImport.html')
    
@application.route('/teacher-input', methods=['GET', 'POST'])
def teacherInput():
    if request.method == 'POST':
        file = request.files['file'] 
        file.save(f'application/excell/import/output.xlsx')
        #data = pd.read_excel(f'jumpScheduler/application/excell/import/output.xlsx')
        
        #return render_template('ratings.html', data=data.to_dict())
        return render_template('teacherInput.html')

@application.route('/schedule', methods=['POST'])
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

    teacherInput = [ratingsArray, teamID]

    # Run the scheuduler using the uploaded excell file and the teacher input / preferences 
    runScheduler.scheduleForAMS(teacherInput)

    return render_template('excelDownload.html')

@application.route('/excell-download')
def download_file():
    p = "excell/export/output.xlsx"
    return send_file(p, as_attachment=True)


