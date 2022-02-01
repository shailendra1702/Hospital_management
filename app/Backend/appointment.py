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
            g.cursor = g.db.cursor()
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
    user = session['user']
    username = session['username']
    print(user)
    if user =='patient':
        g.cursor.execute('select D.Fname,A.Appointment_DT from appointment A,doctor D where D.DocId = A.DocId and A.PatId = %s',(username,))
    elif user == 'doctor':
        g.cursor.execute('select P.Fname,A.Appointment_DT from appointment A,patient P where P.PatId = A.PatId and A.DocId = %s',(username,))
    else:
        g.cursor.execute('select * from appointment')
        
    res = g.cursor.fetchall()
    # print(res)
    return render_template("appointment/all_appointments.htm",user = user, res = res)
        
@appointment.route('/add',methods = ["GET", "POST"])
def addAppointment():
    username = session['username']
    # g.cursor.execute('select PatId from Patient where PatId = %s',(username,))
    # flag = g.cursor.fetchone()

    g.cursor.execute('select DocId,Fname,Speciality from doctor')
    res = g.cursor.fetchall()
    if request.method == 'POST' and 'docid' in request.form:
        
        DocId = request.form['docid']
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        
        g.cursor.execute('insert into Appointment values\
                            (%s,%s,%s)',(username,DocId,formatted_date))
        g.db.commit()
        return render_template("appointment/add_appointment.htm", res = res)
    elif request.method == 'POST':
        msg = 'no doctors selected'
        return msg
   
    return render_template("appointment/add_appointment.htm", res = res)
        