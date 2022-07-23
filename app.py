from operator import is_
from flask import Flask, render_template, redirect, request, session

from hash import hash, check
from psql import sql_select, sql_write,get_secret_key
from service import get_questions, is_logged_in

app = Flask(__name__)
app.secret_key = get_secret_key().encode()

@app.route('/')
@app.route('/index')
def index():
    # if user is logged in, skip login screen
    if is_logged_in():
        return render_template('home.html')

    forgot = request.args.get('forgot', '')
    stage = "1"
    return render_template('index.html', forgot=forgot, stage=stage)

@app.route('/index_action', methods=['POST'])
def index_action():
    forgot = request.form.get('forgot', '')
    stage = request.form.get('stage', '')
    email = request.form.get('email').lower()
    answer = request.form.get('answer', '').lower()

    query = sql_select('SELECT id, question, answer FROM users WHERE email=%s', email)
    if query:        
        question = get_questions(query[0][1])        
        msg = ''
        if stage == "3":
            if not check(answer, query[0][2]):                
                stage = "2"
                msg = 'Incorrect answer'
        elif stage == "4":
            user_id = query[0][0] 
            new_password = hash(request.form.get('new_password'))
            sql_write('UPDATE users SET password =%s WHERE id=%s', new_password, user_id)
            return redirect('/')
    else:
        stage = "1"
        question = ""
        stored_answer = ""
        msg = 'invalid email address'
    return render_template('index.html', forgot=forgot, stage=stage, email=email, question=question, msg=msg)


@app.route('/login_action', methods=['POST'])
def login_action():
    email = request.form.get('email').lower()
    password = request.form.get('password')

    query = sql_select('SELECT * FROM users WHERE email=%s', email)        
    if query:
        query = query[0]
        if check(password, query[3]):
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
    hash_answer = hash(answer)

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
    password = hash(password)
    sql_write('INSERT INTO users(username, email, password, question, answer) VALUES(%s,%s,%s,%s,%s)', username, email, password, question, hash_answer)
    msg = f"Account successfully created! Please sign in"
    return render_template('index.html', msg=msg)

@app.route('/logout_action')
def logout():
    msg = f"{session['username']} has been logged out successfully!"
    session.pop('username', None)
    return render_template("index.html", msg=msg)

if __name__ == "__main__":
    app.run(debug=True)