from flask import Flask, render_template, redirect, request, session
from hash import hash, check
from psql import sql_select, sql_write,get_secret_key
from service import get_questions, user_logged_in, fetch_data, reset_password, get_leaderboard, get_users, delete_user, log_out
from psycopg2.extensions import AsIs 

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
            leaderboard = get_leaderboard()
            return render_template('home.html', leaderboard=leaderboard)
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
    excluded_letters = 'EGJKLOQ'
    auto_admin = False
    sql_write('INSERT INTO users(username, email, password, question, answer, admin, excluded) VALUES(%s,%s,%s,%s,%s,%s, %s)', username.capitalize(), email, password, question, hash_answer, auto_admin, excluded_letters)
    msg = f"Account successfully created! Please sign in"
    return render_template('index.html', msg=msg)

# Logout current user and clear session data
@app.route('/logout_action')
def logout():
    msg = f"{session['username']} has been logged out successfully!"
    log_out()
    return render_template("index.html", msg=msg)

@app.route('/home')
def home():
    if user_logged_in():
        query = sql_select('SELECT card_id FROM achievements WHERE user_id=%s', session['user_id'])
        if query:
            card_list = []            
            for card in query:
                data = sql_select('SELECT * FROM cards WHERE card_id=%s', card)
                card_list.append({
                    'id': data[0][0],
                    'card_id': data[0][1],
                    'name': data[0][2],
                    'description': data[0][3],
                    'url': data[0][4],
                    'link': data[0][5]
                    })
            #Check for filter to order results            
            filters = request.args.get('filter', 'card_id/False')
            type = filters.split('/')[0]
            direction = filters.split('/')[1]
            if direction == 'False':
                direction = False
            else:
                direction = True
            print(f'$$$$$$$$$$ SORT BY: {type} $$$$$$$')
            print(f'$$$$$$$$$$ REVERSE: {direction} $$$$$$$')
            card_list.sort(key=lambda x: x.get(f'{type}'), reverse=direction)
            count = sql_select('SELECT count(*) FROM achievements WHERE user_id=%s', session['user_id'])[0][0]
            leaderboard = get_leaderboard()
            return render_template('home.html', card_list=card_list, count=count, leaderboard=leaderboard)

        msg="You have not earnt any cards..."        
        return render_template('home.html', msg=msg)
    else:
        return redirect('/')

# Fetch data from external API and randomise choices
@app.route('/play')
def play():
    if user_logged_in():
        data = fetch_data()
        character = data[0]
        attribute = data[1]
        button_names = data[2]['buttons']
        answer = data[2]['answer']
        leaderboard = get_leaderboard()
        return render_template('play.html', buttons=button_names, character=character, attribute=attribute, answer=answer, leaderboard=leaderboard)
    else:
        return redirect('/')

# If users guess is correct, add their new card to the cards table and link to achievements Table
@app.route('/play_action', methods=['POST'])
def play_action():
    correct = request.form.get('clicked')
    if correct:
        card_id = request.form.get('id')
        name = request.form.get('name')
        description = request.form.get('description')
        link = request.form.get('link')
        image = request.form.get('image')
        card_exists = sql_select('SELECT * FROM cards WHERE card_id=%s', card_id)
        if not card_exists:
            sql_write('INSERT INTO cards(card_id, name, description, image, link) VALUES(%s,%s,%s,%s,%s)', card_id, name, description, image, link)
        sql_write('INSERT INTO achievements(user_id, card_id) VALUES(%s,%s)', session['user_id'], card_id)        
    return redirect('/play')    

# Allow anyone with the admin title to edit or delete other users
@app.route('/admin')
def admin():    
    if user_logged_in():
        users = get_users()
        leaderboard = get_leaderboard()
        return render_template('admin.html', users=users, leaderboard=leaderboard)
    else:
        return redirect('/')

@app.route('/delete_user', methods=["POST"])
def delete_action():
    fire = request.form.get('fire', '')
    id = request.form.get('id', '')
    name = request.form.get('name', '')
    confirmed = request.form.get('confirm_delete', '')
    if fire:
        delete_user(id)
        msg = f"{name.capitalize()} was led to the card incineration room. They didn't leave. \n\nREST IN PEACE {name.upper()}!!"
        return render_template('index.html', msg=msg)
    if confirmed:
        delete_user(id)
        return redirect('/admin')
    if id:
        users = get_users(id)
        leaderboard = get_leaderboard()
        return render_template('admin.html', id=id, users=users, confirm_delete=True, leaderboard=leaderboard)
    else:
        msg = 'An error has occured'
        return render_template("admin.html", msg=msg)

@app.route('/edit_user', methods=["POST"])
def edit_user():
    id = request.form.get('id', '')
    if id:
        users = get_users(id)
        leaderboard = get_leaderboard()
        return render_template('admin.html', users=users, edit_user=True, leaderboard=leaderboard)

@app.route('/edit_action', methods=["POST"])
def edit_action():
    id = request.form.get('id', '')
    reset = request.form.get('reset', '')
    wipe = request.form.get('wipe', '')
    remove = request.form.get('remove_admin', '')
    add = request.form.get('make_admin', '')
    msg = ''
    if reset:
        new_password = reset_password()
        msg += f'\nNEW PASSWORD SET TO: {new_password}'
        new_password = hash(new_password)
        sql_write('UPDATE users SET password=%s WHERE user_id=%s', new_password, id)
    if wipe:
        sql_write('DELETE FROM achievements WHERE user_id=%s', id)
        msg += f'\nCARDS WIPED FROM USER ID: {id}'
    if remove:
        admin_count = sql_select('SELECT count(admin) FROM users WHERE admin=True')[0][0]
        if admin_count == 1:
            msg += '\nCANNOT REMOVE ADMIN - You must have at least one active admin!'
        else:
            sql_write('UPDATE users SET admin=False WHERE user_id=%s', id)
            msg += f'\nADMIN REMOVED FROM USER ID: {id}'
    if add:
        sql_write('UPDATE users SET admin=True WHERE user_id=%s', id)
        msg += f'\nADMIN ADDED TO USER ID: {id}'
    users = get_users()
    leaderboard = get_leaderboard()
    return render_template('admin.html', users=users, msg=msg, leaderboard=leaderboard)


# Modal popup for user preferences
@app.route('/settings')
def settings():
    if user_logged_in():
        leaderboard = get_leaderboard()
        return render_template('home.html', settings_clicked=True, leaderboard=leaderboard)
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)