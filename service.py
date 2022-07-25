from flask import session
import requests
from random import Random, randint, shuffle
import hashlib
import time
from psql import sql_select

# Check if the user is currently logged in
def user_logged_in():
    if session.get('username') is not None:
        return True

# Populate secret question options
# Record the key of the selected question to reference if they forget password
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

# Access marvel api (took a while to figure this out)
# Store results in new dict, ignoring results that do not have an image or description
def fetch_data():
    letter = chr(randint(ord('A'), ord('Z')))
    url = 'http://gateway.marvel.com/v1/public/characters'
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

    response = requests.get(url, params=payload).json()  
    attribute = response['attributionText'] # attribute Marvel for the use of the API
    characters = response['data']['results']
    
    dict = []
    for key in characters:
        query = sql_select('SELECT * FROM achievements WHERE user_ID=%s AND card_ID=%s', session['user_id'], key['id'])
        if (not query) and (key['thumbnail']['path'] != 'http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available') and (key['description'] != ""):
            dict.append({
                'id' : key['id'],
                'name' : key['name'],
                'description' : key['description'],
                'image' : key['thumbnail']['path'] + '.' + key['thumbnail']['extension'],
                'link' : key['urls'][0]['url'],
            })

    index = randint(0, len(dict)-1)
    selection = dict[index]

    # Generate random button names
    # Ensuring they are unique (to avoid duplicates)     
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

    # buttons = [selection['name'], random1, random2] 
    shuffle(buttons)
    return selection, attribute, choices


# Removes any unnecessary info from string
def split(string):
    if string.split("("):
        string = string.split("(")[0]
    if string.split("/"):
        string = string.split("/")[0]
    return string




        
    

