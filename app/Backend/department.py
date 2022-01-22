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
    g.cursor.execute('select * from department')
    res = g.cursor.fetchall()
    print(res)
    return render_template('department/department.htm', res = res)

@dept.route('/add',methods = ["GET", "POST"])
def addDepartment():
    # username = session["username"]
    # g.cursor.execute('select AdminId from admin where AdminId = %s',(username,))
    # flag = g.cursor.fetchone()
    
    if request.method == 'POST' and 'id' in request.form and 'Dname' in request.form:
        try:
            dname = request.form['Dname']
            head = request.form.get('head','')
            
            if not re.match(r'[a-zA-Z]+',dname):
                msg = 'department name should contain only alphabaet characters'
            elif head not in "":
                if not re.match(r'[a-zA-Z]+',head):
                    msg = 'head name should contain only alphabaet characters'
            elif len(request.form['id']) != 3:
                msg = "depid should be of 3 digits"
            else:
                id = int(request.form['id'])
                g.cursor.execute('insert into department values(%d,%s,%s)',(id,dname,head))
                msg = 'department {dname} successfully added'
        
        except ValueError as e:
            msg = 'id should only contain numbers'
        
        finally:
            return render_template('add_department.htm',msg = msg)
        