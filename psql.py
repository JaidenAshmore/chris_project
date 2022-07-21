# PSQL read/write functions

# >>>> UPDATE DATABASE NAME ONCE SETUP <<<<

import psycopg2

def sql_select(query, paramater=None):
    connection = psycopg2.connect("dbname=UPDATE")
    cursor = connection.cursor()

    if paramater is None:
        cursor.execute(query)
    else:
        cursor.execute(query, [paramater])
    
    response = cursor.fetchall()
    connection.close()
    return response

def sql_write(query, *parameters):
    connection = psycopg2.connect("dbname=UPDATE")
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    connection.commit()
    connection.close()
    return 