# PSQL Database functions
import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=project2')

# Get secret key from server, or set to default
def get_secret_key():
    return os.environ.get('SECRET_KEY', 'abc')

# SQL Select query
def sql_select(query, paramater=None):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    if paramater is None:
        cursor.execute(query)
    else:
        cursor.execute(query, [paramater])    
    response = cursor.fetchall()
    connection.close()
    return response

# SQL Write query
def sql_write(query, *parameters):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    connection.commit()
    connection.close()
    return
