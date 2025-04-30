import mysql.connector as mysql

def connect_db():
    return mysql.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "onlineshop" 
    )
