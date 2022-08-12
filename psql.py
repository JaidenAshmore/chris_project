# PSQL Database functions
import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=project2')

# Get secret key from server, or set to default
def get_secret_key():
    return os.environ.get('SECRET_KEY', 'abc')

# SQL Select query
def sql_select(query, *params):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)    
    response = cursor.fetchall()
    connection.close()
    return response

# SQL Write query
def sql_write(query, *params):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    connection.close()
    return
