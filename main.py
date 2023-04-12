import mysql.connector

 

connection = mysql.connector.connect(user = "root", database = "example", password = "Krishna#1")
cursor = connection.cursor() 

cursor = connection.cursor()

 

testQuery = ("SELECT * FROM new_table")

 

cursor.execute(testQuery)

 

for item in cursor:

    print(item)

 

cursor.close()

connection.close()