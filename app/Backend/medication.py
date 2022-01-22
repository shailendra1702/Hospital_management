import pymysql
from flask import Blueprint, session, request, g,redirect,render_template,url_for,flash

med = Blueprint('med', __name__,template_folder='templates')
from pymysql.constants import CLIENT

@med.before_request
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


@med.teardown_request
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
     
@med.route('/')
def medication():
    g.cursor.execute('select * from medication')
    res = g.cursor.fetchall()
    print(res)
    return res

@med.route('/add',methods = ["GET", "POST"])
def addMedication():
    username = session["username"]
    g.cursor.execute('select AdminId from admin where AdminId = %s',(username,))
    flag = g.cursor.fetchone()
    if request.method == 'POST' and 'medcode' in request.form and 'mname' in request.form and 'mbrand' in request.form and 'desc' in request.form and flag != None:
        
        medcode = request.form['medcode']
        mname = request.form['mname']
        mbrand = request.form['mbrand']
        desc = request.form['desc']
        
        if not re.match(r'[a-zA-Z]{2}[0-9]{3}+',medcode):
            msg = 'medcode should match pattern like AB123'
        elif not re.match(r'[a-zA-Z]+',mname):
            msg = 'med name should contain only alphabaet characters'
        elif not re.match(r'[a-zA-Z]+',mbrand):
            msg = 'brand name should contain only alphabaet characters'
        else:
            g.cursor.execute('insert into department values(%s,%s,%s,%s)',(medcode,mname,mbrand,desc))
            msg = 'medcode {medcode} successfully added'
            print(msg)
        
        return render_template('addMedication.htm')

@med.route('/proc')
def procedure():
    g.cursor.execute('select * from procedure')
    res = g.cursor.fetchall()
    print(res)
    return res

@med.route('/add',methods = ["GET", "POST"])
def addProcedure():
    username = session["username"]
    g.cursor.execute('select AdminId from admin where AdminId = %s',(username,))
    flag = g.cursor.fetchone()
    if request.method == 'POST' and 'proccode' in request.form and 'procname' in request.form and 'cost' in request.form and flag != None:
        
        proccode = request.form['medcode']
        procname = request.form['mname']
        cost = request.form['mbrand']
        
        if not re.match(r'[a-zA-Z]{2}[0-9]{3}+',proccode):
            msg = 'procedure code should match pattern like AB123'
        elif not re.match(r'[a-zA-Z]+',procname):
            msg = 'procedure name should contain only alphabaet characters'
        elif not re.match(r'[0-9]+',cost):
            msg = 'cost should contain only numbers'
        else:
            g.cursor.execute('insert into department values(%s,%s,%s)',(proccode,procname,cost))
            msg = 'procedure {procname} successfully added'
            print(msg)
        
        return render_template('addProcedure.htm')
    
    
        