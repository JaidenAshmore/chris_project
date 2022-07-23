# Functions that return TRUE or FALSE values

from flask import session
 
def is_logged_in():
    if session['username']:
        return True
    else:
        return False