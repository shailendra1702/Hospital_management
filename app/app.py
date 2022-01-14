from flask import Flask, request, g, render_template
import pymysql
from Backend.authentication import auth
from pymysql.constants import CLIENT

app = Flask(__name__)
app.register_blueprint(auth)
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


@app.route("/", methods=["GET", "POST"])
def hello():
    print('during view')
    return render_template('hello.htm', name=None)


# main driver function
if __name__ == '__main__':
    table()
    app.run(port=8000, debug=True)
