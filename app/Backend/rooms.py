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
            g.cursor = g.db.cursor()
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
def roomDetails():
    user = session['user']
    g.cursor.execute('select * from Room')
    res = g.cursor.fetchall()
    return render_template('room/room.htm',res = res, user = user)

@room.route('/add',methods = ["GET", "POST"])
def bookRoom():
    
    msg = ''
    try:
        if request.method == 'POST':
                    
            selectedRoom = request.form.getlist('roomtype')
            print(selectedRoom)
            
            g.cursor.executemany('update Room set Booked = Booked+1,\
                                Unbooked = Unbooked-1 where Room_type = %s',selectedRoom)
            g.db.commit()
            msg = 'room booked successfully'
    except Exception as e:
        print(e)
       
    g.cursor.execute('select * from Room') 
    res = g.cursor.fetchall()
    return render_template('room/room_select.htm',res = res,msg=msg)

@room.route('/vacate',methods = ["GET","POST"])
def vacateBed():
    msg = ''
    try:
        if request.method == 'POST':
                    
            selectedRoom = request.form.getlist('roomtype')
            print(selectedRoom)
            
            g.cursor.executemany('update Room set Booked = Booked-1,\
                                Unbooked = Unbooked+1 where Room_type = %s',selectedRoom)
            g.db.commit()
            msg = 'room vacated successfully'
    except Exception as e:
        print(e)
       
    g.cursor.execute('select Room_type,Booked from Room where Booked > 0') 
    res = g.cursor.fetchall()
    return render_template('room/room_vacate.htm',res = res,msg=msg)