from flask import Blueprint, session, request, g, redirect, render_template, url_for
import re
import pymysql

auth = Blueprint('auth', __name__,
                 template_folder='templates')


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
                                   port=3306)
            print('connection established')
            return g.db
    except Exception as e:
        print('error in establishing connection')


@auth.teardown_request
def db_disconnect(exception):
    if exception:
        print('error')
    elif 'db' not in g:
        print('connection not opened at all')
    else:
        g.db.close()
        print('connection closed')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = g.db.cursor()
        cursor.execute(
            'SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@auth.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = g.db.cursor()
        cursor.execute(
            'SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute(
                'INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            g.db.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.htm', msg=msg)


