import pymysql
from flask import Blueprint, session, request, g,redirect,render_template,url_for,flash

room = Blueprint('room', __name__,template_folder='templates')
from pymysql.constants import CLIENT

@room.before_request
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


@room.teardown_request
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
     
@room.route('/')
def department():
    g.cursor.execute('select Type,Available from Rooms')
    res = g.cursor.fetchall()
    print(res)
    return res

@room.route('/add',methods = ["GET", "POST"])
def bookRoom():
    user = session["user"]
    
    if request.method == 'POST' and 'selectedRoom' in request.form and user == 'admin':
                
        selectedRoom = request.form['selectedRoom']
        
        g.cursor.execute('update table Rooms set ')
        msg = 'department {dname} successfully added'
            
    g.cursor.execute('select Type,Available,Total from Rooms')
    res = g.cursor.fetchall()
    return render_template('bookRoom.htm',res = res)