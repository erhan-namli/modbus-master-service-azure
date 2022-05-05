import mysql.connector
import pandas as pd
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)


df = pd.read_csv('../mysqldata.csv')


data = df['RegValue']

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'deneme'

RegNo = data[0][0]
Value = data[0][1]

mysql = MySQL(app)
cur = mysql.connection.cursor()
cur.execute("INSERT INTO registers (RegNo, Value) VALUES (%s, %s)", (RegNo, Value))
mysql.connection.commit()
cur.close()


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == "POST":
#         details = request.form
#         RegNo = data[0]
#         Value = data[1]
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO registers (RegNo, Value) VALUES (%s, %s)", (RegNo, Value))
#         mysql.connection.commit()
#         cur.close()
#         return 'success'
#     return render_template('index.html')


# if __name__ == '__main__':
#     app.run()