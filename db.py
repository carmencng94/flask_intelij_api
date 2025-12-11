import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="sakila",
        cursorclass=pymysql.cursors.DictCursor
    )
