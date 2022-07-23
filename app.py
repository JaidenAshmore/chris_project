from flask import Flask, render_template, redirect, request, session

from hash import hash_pw, check_pw
from psql import sql_select, sql_write, sql_insert, get_secret_key
from service import get_questions

app = Flask(__name__)
app.secret_key = get_secret_key().encode()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_action', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')

    query = sql_select('SELECT * FROM users WHERE email=%s', email)        
    if query:
        query = query[0]
        if check_pw(password, query[3]):
            session['username'] = query[1]
            msg = f"signed in as {session['username']}"
        else:
            msg = "Incorrect username and/or password"
        return render_template('index.html', msg=msg, query=query)
    else:
        msg = "Incorrect username and/or password"
        return render_template('index.html', msg=msg, query=query)     

@app.route('/signup')
def signup():
    questions = get_questions()
    return render_template('signup.html', questions=questions)

@app.route('/signup_action', methods=['POST'])
def signup_action():
    username = request.form.get('username').lower()
    email = request.form.get('email').lower()
    password = request.form.get('password')
    verify_password = request.form.get('verify_password')
    question = request.form.get('questions')
    answer = request.form.get('answer').lower()

    # Prompt user if failed password verification  ---SWITCH THESE CHECKS TO JAVASCRIPT VALIDATION!
    if password != verify_password:
        msg = "Passwords do not match"
        return render_template('index.html', msg=msg)
    # Check if username in use
    query = sql_select('SELECT username FROM users WHERE username=%s', username)
    if query:
        msg = "Username already in use"
        return render_template('index.html', msg=msg)
    # Check if email in use
    query = sql_select('SELECT email FROM users WHERE email=%s', email)
    if query:
        msg = f"{email} is already registered. Please sign in"
        return render_template('index.html', msg=msg)
    password = hash_pw(password)
    sql_insert(username, email, password, question, answer)
    msg = f"Account successfully created! Please sign in"
    return render_template('index.html', msg=msg)

if __name__ == "__main__":
    app.run(debug=True)