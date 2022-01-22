import pymysql
from flask import Blueprint, session, request, g,redirect,render_template,url_for,flash
from datetime import datetime

appointment = Blueprint('appointment', __name__,template_folder='templates')
from pymysql.constants import CLIENT

@appointment.before_request
def db_connect():
    try:
        if 'db' not in g:
            g.db = pymysql.connect(host='localhost',
                                   user='root',
                                   password='Ayush17!@#&%',
                                   database='hospital_management',
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor,
            )
            cursor = g.db.cursor()
            print('connection established')
    except Exception as e:
        print('error in establishing connection')


@appointment.teardown_request
def db_disconnect(exception):
    try:
        if exception:
            raise(exception)
        elif 'db' not in g:
            print('connection not opened at all')
    except Exception as e:
        print(e)
    finally:
        g.cursor.close()
        g.db.close()
        print('connection closed')

import re
     
@appointment.route('/')
def allAppointments():
    g.cursor.execute('select * from appointments')
    res = g.cursor.fetchall()
    print(res)
    return render_template('hello.htm', name = 'department')

@appointment.route('/<username>')
def user_appointment():
    user = session['user']
    username = session['username']
    
    if user == 'patient':
        g.cursor.execute('select D.Fname,D.Lname,A.Appointment_DT from doctor D,Appointment A \
                        where A.PatId = %s and A.DocId = D.DocId',(username,))
        res = g.cursor.fetchall()
        return [x for x in res]
        
    else:
        g.cursor.execute('select P.Fname,P.Lname,A.Appointment_DT from patient P,Appointment A \
                        where A.DocId = %s and A.PatId = P.PatId',(username,)) 
        res = g.cursor.fetchall()
        return [x for x in res]
        
@appointment.route('/add',methods = ["GET", "POST"])
def addAppointment():
    username = session['username']
    g.cursor.execute('select PatId from Patient where PatId = %s',(username,))
    flag = g.cursor.fetchone()
    if request.method == 'POST' and 'DocId' in request.form and flag != None:
        
        DocId = request.form['DocId']
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        
        g.cursor.execute('insert into Appointment values\
                            (%s,%s,%s)',(username,DocId,formatted_date))
        return redirect(url_for('hello'))
    elif request.method == 'POST':
        msg = 'no doctors selected'
        return render_template('hello.htm',name = msg)
    return render_template('hello.htm', name = "addAppointment")
        