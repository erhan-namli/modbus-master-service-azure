import mysql.connector
import pandas as pd
from flask import Flask, render_template, request

df = pd.read_csv('mysqldata.csv')

data = df['RegValue']

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="deneme"
)

RegNo = data[0][0]
RegVal = data[0][1]

mycursor = mydb.cursor()

print(RegNo, RegVal)

# sql = "UPDATE  registers ( RegNo, Value) VALUES (%s, %s)"
# val = (RegNo, RegVal)
# mycursor.execute(sql, val)

# mydb.commit()

# print(mycursor.rowcount, "record inserted.")