from flask import Flask
import pymysql

app = Flask(__name__)
  
connection = pymysql.connect(host='localhost', 
                             user='root',
                             password='Ayush17!@#&%',
                             database='hospital_management',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

query = 'create table if not exists Doctor(\
        doc_id varchar(10) primary key, fname varchar(20), lname varchar(20), address varchar(30),\
        phone_no bigint(10));'
  
@app.route('/')
def hello_world():
    return 'Hello World'

cur = connection.cursor()

cur.execute(query)
cur.execute('show tables')
output = cur.fetchall()
print(output)
# To close the connection
connection.close()
  
# main driver function
if __name__ == '__main__':
    app.run(debug = True)