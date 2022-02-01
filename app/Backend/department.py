import pymysql
from flask import Blueprint, session, request, g,redirect,render_template,url_for,flash

dept = Blueprint('dept', __name__,template_folder='templates')
from pymysql.constants import CLIENT

@dept.before_request
def db_connect():
    try:
        if 'db' not in g:
            g.db = pymysql.connect(host='localhost',
                                   user='root',
                                   password='Ayush17!@#&%',
                                   database='hospital_management',
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor,
                                   client_flag=CLIENT.MULTI_STATEMENTS,
            )
            g.cursor = g.db.cursor()
            print('connection established')
    except Exception as e:
        print('error in establishing connection')


@dept.teardown_request
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
     
@dept.route('/')
def department():
    user = session['user']
    g.cursor.execute('select * from department')
    res = g.cursor.fetchall()
    print(res)
    return render_template('department/department.htm', res = res, user = user)

@dept.route('/add',methods = ["GET", "POST"])
def addDepartment():
    # username = session["username"]
    # g.cursor.execute('select AdminId from admin where AdminId = %s',(username,))
    # flag = g.cursor.fetchone()
    msg = ''
    if request.method == "POST" and "id" in request.form and "Dname" in request.form:
        try:
            id = request.form['id']
            dname = request.form['Dname']
            head = request.form['head']
            
            if not re.match(r'[a-zA-Z]+',dname):
                msg = 'department name should contain only alphabet characters'
            elif not re.match(r'[0-9]+',head):
                msg = 'HOD id should be number'
            else:
                g.cursor.execute('insert into department values (%s,%s,%s)',(id,dname,head))
                g.db.commit()
                msg = f'department {dname} successfully added'
                print(msg)
        
        except Exception as e:
            print(e) 
            msg = 'id should only contain numbers'
        
        finally:
            return render_template('department/add_department.htm',msg = msg)
    elif request.method == "POST":
        msg = "please fill up the form"
        return render_template('department/add_department.htm',msg = msg)
    else:
        return render_template('department/add_department.htm',msg = msg)
        