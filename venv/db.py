import pymysql

def get_db_connection():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="Madhumit09*",
        database="madhumitha",
       cursorclass=pymysql.cursors.DictCursor
    )
    return conn
