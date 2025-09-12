import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # change to your MySQL username
        password="Madhumit09*",   # change to your MySQL password
        database="madhumitha"
    )
    return conn
