import re
import pymysql
from flask import Blueprint, session, request, g,redirect,render_template,url_for,flash

auth = Blueprint('auth', __name__,template_folder='templates')
from pymysql.constants import CLIENT

@auth.before_request
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


@auth.teardown_request
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


@auth.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        
        username = request.form['username']
        password = request.form['password']
        g.cursor.execute(
            'SELECT * FROM Patient WHERE PatId = % s AND password = % s', (username, password, ))
        account = g.cursor.fetchone()
    
        if account:
            session['loggedin'] = True
            session['username'] = account['PatId']
           
            return redirect(url_for('hello')) #has to changed to dashboard.htm
        else:
            g.cursor.execute(
            'SELECT * FROM Doctor WHERE DocId = % s AND password = % s', (username, password, ))
            account1 = g.cursor.fetchone()
            if account1:
                session['loggedin'] = True
                session['username'] = account['DocId']
                msg = 'Logged in successfully !'
                return redirect(url_for('hello')) #has to changed to dashboard.htm
            msg = 'Incorrect username / password !'
         
    return render_template('login.htm', msg=msg)


@auth.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@auth.route('/register', methods=['GET',"POST"])
def register():
    session.clear()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'Fname' in request.form and 'Lname' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        Fname = request.form['Fname']
        Lname = request.form['Lname']
        Phone = int(request.form.get('Phone',"0000000000"))
        g.cursor.execute(
            'SELECT * FROM patient WHERE PatId = % s', (username,))
        account = g.cursor.fetchone()
        if account:
            msg = 'Account already exists !'
            flash('Account already exists !','info')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
            flash('Invalid email address !','error')
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
            flash('Username must contain only characters and numbers !','error')
        elif not re.match(r'[A-Za-z]+', Fname) and not re.match(r'[A-Za-z]+', Lname):
            msg = 'Name should contain only alphabet characters'
            flash('Name should contain only alphabet characters','error')
        else:
            g.cursor.execute(
                'INSERT INTO patient VALUES (%s, %s, %s,%s,%s,%d)', (username,Fname,Lname,email,password, Phone))
            g.db.commit()
            flash("successfully registered",'info')    
        return render_template('register.htm')

    
    elif request.method == 'POST':
        flash('fill out the form','info')
        
    
    return render_template('register.htm')


