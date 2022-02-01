import pymysql
from flask import Blueprint, session, request, g,redirect,render_template,url_for,flash

med = Blueprint('med', __name__, template_folder='templates')
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
                                   client_flag=CLIENT.MULTI_STATEMENTS
            )
            g.cursor = g.db.cursor()
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
    return render_template('medication/medication.htm',res = res)

@med.route('/add',methods = ["GET", "POST"])
def addMedication():
    msg = ''
    if request.method == 'POST' and 'medcode' in request.form and 'mname' in request.form and 'mbrand' in request.form and 'desc' in request.form:
        try:
            medcode = request.form['medcode']
            mname = request.form['mname']
            mbrand = request.form['mbrand']
            desc = request.form['desc']
            
            if not re.match(r'[a-zA-Z]{2}[0-9]{3}',medcode):
                msg = 'medcode should match pattern like AB123'
            elif not re.match(r'[a-zA-Z]+',mname):
                msg = 'med name should contain only alphabaet characters'
            elif not re.match(r'[a-zA-Z]+',mbrand):
                msg = 'brand name should contain only alphabaet characters'
            else:
                g.cursor.execute('insert into medication values(%s,%s,%s,%s)',(medcode,mname,mbrand,desc))
                g.db.commit()
                msg = f"medcode {medcode} successfully added"
        except Exception as e:
            print(e)

        finally:
            return render_template('medication/add_medication.htm',msg = msg)
    elif request.method == "POST":
        msg = "please fill up the form"
        return render_template('medication/add_medication.htm',msg = msg)
    else:
        return render_template('medication/add_medication.htm',msg = msg)

@med.route('/proc')
def procedure():
    user = session['user']
    g.cursor.execute('select * from medproc')
    res = g.cursor.fetchall()
 
    return render_template('medication/procedure.htm',res = res,user = user)

@med.route('/proc/add',methods = ["GET", "POST"])
def addProcedure():
    msg = ''
    if request.method == 'POST' and 'proccode' in request.form and 'procname' in request.form and 'cost' in request.form:    
        try:
            proccode = request.form['proccode']
            procname = request.form['procname']
            cost = request.form['cost']
            
            if not re.match(r'[0-9]{5}',proccode):
                msg = 'procedure code should match pattern like 12345'
            elif not re.match(r'[a-zA-Z]+',procname):
                msg = 'procedure name should contain only alphabaet characters'
            elif not re.match(r'[0-9]+',cost):
                msg = 'cost should contain only numbers'
            else:
                g.cursor.execute('insert into medproc values(%s,%s,%s)',(proccode,procname,cost))
                g.db.commit()
                msg = f'procedure {procname} successfully added'
        except Exception as e:
            print(e)
        finally:
            return render_template('medication/add_procedure.htm',msg = msg)
            
    elif request.method == "POST" :
        msg = "please fill up the form"
        return render_template('medication/add_procedure.htm',msg = msg)
    else:
        return render_template('medication/add_procedure.htm',msg = msg)
    
@med.route('/patient-summary')
def details():
    user = session['user']
    username = session['username']
    
    if user =='patient':
        g.cursor.execute('select D.Fname,M.Proc_name,B.Room_type,B.issued_date,B.Total_amt from doctor D,medproc M, details B where D.DocId = B.DocId and M.Proc_code = B.Proc_code and B.PatId = %s',(username,))
    else:
        g.cursor.execute('select B.PatId,B.DocId, M.Proc_name,B.Room_type,B.issued_date,B.Total_amt from medproc M, details B where M.Proc_code = B.Proc_code')
        
    res = g.cursor.fetchall()
    return render_template("medication/details.htm",user = user, res = res)

@med.route('/patient-summary/add',methods = ["GET", "POST"])
def addDetails():
    # username = session["username"]
    # username = 'shail702'
    # g.cursor.execute('select AdminId from admin where AdminId = %s',(username,))
    # flag = g.cursor.fetchone()
    # print(flag)
    msg = ''
    g.cursor.execute("select Room_type from room")
    res = g.cursor.fetchall()
    g.cursor.execute('select DocId,Fname,Speciality from doctor')
    res1 = g.cursor.fetchall()
    
    if request.method == 'POST' and 'patid' in request.form and 'docid' in request.form and 'proccode' in request.form and 'roomtype' in request.form:
        
        try:
            patid = request.form['patid']
            docid = request.form['docid']
            proccode = request.form['proccode']
            roomtype = request.form['roomtype']
            
            if not re.match(r'[0-9]{5}',proccode):
                msg = 'procedure code should match pattern like 12345'
            elif not re.match(r'[a-zA-Z0-9]+',patid):
                msg = 'username is in incorrect form'
            # elif not re.match(r'[0-9]+',cost):
            #     msg = 'cost should contain only numbers'
            else:
                g.cursor.execute('insert into details(PatId,DocId,Proc_code,Room_type,issued_date) values(%s,%s,%s,%s,curdate())',(patid,docid,proccode,roomtype))
                g.db.commit()
                msg = f'procedure {patid} successfully added'
        except Exception as e:
            print(e)
        finally:
            return render_template('medication/add_details.htm',msg = msg,res = res, res1 = res1)
            
    elif request.method == "POST":
        msg = "please fill up the form"
        return render_template('medication/add_details.htm',msg = msg,res =res, res1= res1)
    else:
        return render_template('medication/add_details.htm',msg = msg,res = res,res1 =res1)
    

    
    
        