from asyncio.windows_events import NULL
from flask import Flask, render_template,Blueprint
import pymysql
from pymysql.constants import CLIENT

app = Flask(__name__)

from Backend.authentication import auth
from Backend.department import dept
from Backend.medication import med
from Backend.rooms import room

app.register_blueprint(auth,url_prefix="/auth")
app.register_blueprint(dept,url_prefix="/dept")
app.register_blueprint(med,url_prefix="/med")
app.register_blueprint(room,url_prefix="/room")


app.secret_key = "3f46e7936cd92e18c66af8eb7b0575058aba97e6972fc1bce3fd53d3e11b4861"


def table():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='Ayush17!@#&%',
                         database='hospital_management',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor,
                         client_flag=CLIENT.MULTI_STATEMENTS)

    cursor = db.cursor()
    with app.open_resource('schema.sql', mode='r') as f:
        cursor.execute(f.read())
    db.commit()
    cursor.close()
    db.close()
    print("sql script executed")
    
table()

@app.route("/")
def hello():
    print('during view')
    return render_template('hello.htm', name=None)

# main driver function
if __name__ == '__main__':
    app.run(port=7000, debug=True)
    