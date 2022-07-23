# PSQL Database functions

import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=project2')

def get_secret_key():
    return os.environ.get('SECRET_KEY', 'abc')

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

# def sql_select_one(query1, query2, condition):
#     connection = psycopg2.connect(DATABASE_URL)
#     cursor = connection.cursor()
#     cursor.execute('SELECT %s FROM users WHERE %s=%s', [query1, query2, condition])    
#     response = cursor.fetchall()
#     connection.close()
#     return response

def sql_write(query, *parameters):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    connection.commit()
    connection.close()
    return

def sql_insert(*params):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users(username, email, password, sec_question, sec_answer) VALUES(%s,%s,%s,%s,%s)', params)
    connection.commit()
    connection.close()
    return

