from flask import Flask, render_template, redirect, request, session
from hash import hash, check
from psql import sql_select, sql_write,get_secret_key
from service import get_questions, user_logged_in, fetch_data

app = Flask(__name__)
app.secret_key = get_secret_key().encode()

@app.route('/')
@app.route('/index')
def index():
    if user_logged_in():
        return redirect('/home')
    forgot = request.args.get('forgot', '')
    stage = "1"
    return render_template('index.html', forgot=forgot, stage=stage)

@app.route('/index_action', methods=['POST'])
def index_action():
    forgot = request.form.get('forgot', '')
    stage = request.form.get('stage', '')
    email = request.form.get('email').lower()
    answer = request.form.get('answer', '').lower()
    query = sql_select('SELECT user_id, question, answer, username FROM users WHERE email=%s', email)
    if query:
        response = query[0]        
        question = get_questions(response[1])        
        msg = ''
        if stage == "3":
            if not check(answer, response[2]):                
                stage = "2"
                msg = 'Incorrect! Please try again...'
        elif stage == "4":
            user_id = query[0][0] 
            new_password = hash(request.form.get('new_password'))
            sql_write('UPDATE users SET password =%s WHERE user_id=%s', new_password, user_id)
            msg = f"Password successfully updated for user '{response[3]}'"
            return render_template('index.html', msg=msg)
    else:
        stage = "1"
        question = ""
        msg = 'Invalid email address'
    return render_template('index.html', forgot=forgot, stage=stage, email=email, question=question, msg=msg)


@app.route('/login_action', methods=['POST'])
def login_action():
    email = request.form.get('email', '').lower()
    password = request.form.get('password', '')
    query = sql_select('SELECT * FROM users WHERE email=%s', email)        
    if query:
        response = query[0]
        if check(password, response[3]):
            session['user_id'] = response[0]
            session['username'] = response[1]
            session['admin'] = response[6]
            return redirect('/home')
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
    username = request.form.get('username', '').lower()
    email = request.form.get('email', '').lower()
    password = request.form.get('password', '')
    verify_password = request.form.get('verify_password', '')
    question = request.form.get('questions', '')
    answer = request.form.get('answer', '').lower()
    hash_answer = hash(answer)
    # Prompt user if failed password verification  ---SWITCH THESE CHECKS TO JAVASCRIPT VALIDATION?
    if password != verify_password:
        msg = "Passwords do not match"
        return render_template('signup.html', msg=msg)
    # Check if username in use
    query = sql_select('SELECT username FROM users WHERE username=%s', username)
    if query:
        msg = "Username already in use"
        return render_template('signup.html', msg=msg)
    # Check if email in use
    query = sql_select('SELECT email FROM users WHERE email=%s', email)
    if query:
        msg = f"{email} is already registered. Please sign in"
        return render_template('index.html', msg=msg)
    password = hash(password)
    sql_write('INSERT INTO users(username, email, password, question, answer, admin) VALUES(%s,%s,%s,%s,%s,%s)', username, email, password, question, hash_answer, False)
    msg = f"Account successfully created! Please sign in"
    return render_template('index.html', msg=msg)

# Logout current user and clear session data
@app.route('/logout_action')
def logout():
    msg = f"{session['username']} has been logged out successfully!"
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('admin', None)
    return render_template("index.html", msg=msg)

@app.route('/home')
def home():
    if user_logged_in():
        query = sql_select('SELECT card_id FROM achievements WHERE user_id=%s', session['user_id'])
        if query:
            card_list = []
            for card in query:
                data = sql_select('SELECT * FROM cards WHERE card_id=%s ORDER BY id', card)
                card_list.append({
                    'card_id': data[0][1],
                    'name': data[0][2],
                    'description': data[0][3],
                    'url': data[0][4],
                    'link': data[0][5]
                    })
            count = sql_select('SELECT count(*) FROM achievements WHERE user_id=%s', session['user_id'])[0][0]
            return render_template('home.html', card_list=card_list, count=count)
        msg="You have not earnt any cards..."        
        return render_template('home.html', msg=msg)
    else:
        return redirect('/')

# Use external API to populate page
@app.route('/play')
def play():
    if user_logged_in():
        data = fetch_data()
        character = data[0]
        attribute = data[1]
        button_names = data[2]['buttons']
        answer = data[2]['answer']
        return render_template('play.html', buttons=button_names, character=character, attribute=attribute, answer=answer)
    else:
        return redirect('/')

@app.route('/play_action', methods=['POST'])
def play_action():
    correct = request.form.get('clicked')
    if correct:
        card_id = request.form.get('id')
        name = request.form.get('name')
        description = request.form.get('description')
        link = request.form.get('link')
        image = request.form.get('image')
        sql_write('INSERT INTO cards(card_id, name, description, image, link) VALUES(%s,%s,%s,%s,%s)', card_id, name, description, image, link)
        sql_write('INSERT INTO achievements(user_id, card_id) VALUES(%s,%s)', session['user_id'], card_id)        
    return redirect('/play')    

# Allow anyone with the admin title to edit or delete other users
@app.route('/admin')
def admin():
    if user_logged_in():
        users = sql_select('SELECT * FROM users', None)
        return render_template('admin.html', users=users)
    else:
        return redirect('/')

# Modal popup for user preferences
@app.route('/settings')
def settings():
    if user_logged_in():
        return render_template('home.html', settings_clicked=True)
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)