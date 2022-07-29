from flask import session
import requests
from random import randint, shuffle
import hashlib
import time
from psql import sql_select, sql_write

# Check if the user is currently logged in
def user_logged_in():
    if session.get('username') is not None:
        return True

# Log out user
def log_out():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('admin', None)
    return

# Get all user data for admin table
def get_users(id=None):
    if id == None:
        users = sql_select('SELECT user_id, username, email, admin FROM users ORDER BY user_id ASC', None)
    else:
        users = sql_select('SELECT user_id, username, email, admin FROM users WHERE user_id=%s', id)
    list = []
    for user in users:
        list.append(
            {
            'id': user[0],
            'name': user[1].capitalize(),
            'email': user[2],
            'admin': user[3]
            }
        )
    return users 

# Get users (top 5) with the most number of cards
def get_leaderboard():
    leaderboard = sql_select('SELECT username, count(card_id) FROM users INNER JOIN achievements AS ACH ON users.user_id = ACH.user_id GROUP BY username ORDER BY count(card_id) DESC LIMIT 5')
    list = []
    position = 1
    for leader in leaderboard:
        list.append(
            {   
                'position': position,
                'name': leader[0].capitalize(),
                'cardcount': leader[1]
            }
        )
        position += 1
    return list

# Populate secret question options
def get_questions(pos=None):
    questions = {
        1: 'What was your childhood pets name?',
        2: 'What is your Fathers middle name?',
        3: 'What is your Mothers maiden name?',
        4: 'What is your favourite movie?',
        5: 'What is your favourite food?',
        6: 'What was your primary school name?',
    }
    if pos != None:
        return questions[pos]
    else: 
        return questions

# Main function to gather data from API and return focus hero + random choices
def fetch_data():
    excluded_letters = get_excluded_letters()    
    letter = generate_random_letter(excluded_letters) 

    url = 'http://gateway.marvel.com/v1/public/characters'
    payload = get_payload(letter)

    response = requests.get(url, params=payload).json()
    attribute = response['attributionText'] 
    characters = response['data']['results']

    dict = update_dict(characters)            
    if not dict:
        return handle_excluded_letters(excluded_letters, letter)

    selection = select_character(dict)     
    choices = create_buttons(selection, characters)    
    return selection, attribute, choices

# Retrieve users 'excluded letters' as a string
def get_excluded_letters():
    query = sql_select('SELECT excluded FROM users WHERE user_id=%s', session['user_id'])
    excluded_letters = query[0][0]
    print(f'$$$$$$$$$ EXCLUDED LETTERS: {excluded_letters} $$$$$$$$$')
    return excluded_letters

# Generate a random letter that isnt already in the excluded list
def generate_random_letter(excluded_letters):
    letter = chr(randint(ord('A'), ord('Z')))
    while letter in excluded_letters:
        letter = chr(randint(ord('A'), ord('Z')))
    return letter

# Prepare payload for API query
def get_payload(letter):
    public = 'd609fc87a5b2e7b633e37e0e4cdf5553'
    private = '082dff72dc33db36fd9194479cc71a83b9cf62d9'
    timestamp = str(time.time())
    string = timestamp + private + public
    hashed = hashlib.md5(string.encode()).hexdigest()
    
    payload = {
        'ts': timestamp,
        'apikey': public,
        'hash': hashed,
        'limit': 100,
        'nameStartsWith': letter
    }
    return payload

# Create dictionary of character choice - ensuring that an image is available & its not already in players collection
def update_dict(characters):
    dict = []
    for key in characters:
        query = sql_select('SELECT * FROM achievements WHERE user_ID=%s AND card_ID=%s', session['user_id'], key['id'])
        if (not query) and (key['thumbnail']['path'] != 'http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available'):
            dict.append({
                'id' : key['id'],
                'name' : key['name'],
                'description' : key['description'],
                'image' : key['thumbnail']['path'] + '.' + key['thumbnail']['extension'],
                'link' : key['urls'][0]['url'],
            })
    return dict

# Log letter caushing crash and add it to the users excluded letters. Restart fetch_data function
def handle_excluded_letters(excluded_letters, letter):
    print(f'$$$$$$$$$$$$ CRASH DETECTED FROM: {letter} $$$$$$$$$$$$')
    update_excluded = str(excluded_letters) + str(letter)
    sql_write('UPDATE users SET excluded=%s WHERE user_id=%s', update_excluded, session['user_id'])
    return fetch_data()   

# Randomly select a hero 
def select_character(dict):
    index = randint(0, len(dict)-1)
    selection = dict[index]
    return selection

# Generate random button names (1 correct, 2 incorrect)
def create_buttons(selection, characters):
    choices = {
        'buttons': [split(selection['name'])],
        'answer': split(selection['name'])
    }
    buttons = choices['buttons']
    count = 0
    while count < 2:
        num = randint(0, len(characters)-1)
        random_name = split(characters[num]['name'])
        if random_name not in buttons:
            buttons.append(random_name)
            count += 1
    shuffle(buttons)
    return choices

# Removes any unnecessary info from string
def split(string):
    if string.split("("):
        string = string.split("(")[0]
    if string.split("/"):
        string = string.split("/")[0]
    string = string.strip()
    return string

# Reset password to a random string
def reset_password():
    number = randint(3, 5)
    new_password = ''
    n = 0
    while n < number:
        letter = chr(randint(ord('A'), ord('Z')))
        no = randint(0, 9)
        new_password += letter + str(no)
        n += 1
    return new_password

# Handle deleting a user and their cards. Remove card data from DB if not owned by any other user
def delete_user(id):
    card_ids = sql_select('SELECT card_id FROM achievements WHERE user_id=%s', id)
    for card in card_ids:
        count = sql_select('SELECT count(*) FROM achievements WHERE card_id=%s', card)
        if count == 1:
            sql_write('DELETE FROM cards WHERE card_id=%s', card)

    sql_write('DELETE FROM achievements WHERE user_id=%s', id)
    sql_write('DELETE FROM users WHERE user_id=%s', id)
    log_out()
    return


        
    

