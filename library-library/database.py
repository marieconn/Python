import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database = "library"
)

cursor = db.cursor() 
