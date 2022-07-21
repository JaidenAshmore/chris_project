# Functions that return TRUE or FALSE values

import psycopg2

def is_logged_in():
    connection = psycopg2.connect('dbname=UPDATE')
    cursor = connection.cursor() 
    cursor.execute("SELECT name FROM users WHERE active = 'Y';")
    if cursor.rowcount == 0:
        return False
    else:
        return True