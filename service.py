from flask import session
import requests
from random import randint, shuffle
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
    pub = 'd609fc87a5b2e7b633e37e0e4cdf5553'
    pvt = '082dff72dc33db36fd9194479cc71a83b9cf62d9'
    ts = str(time.time())
    string = ts + pvt + pub
    hashed = hashlib.md5(string.encode()).hexdigest()
    
    response = requests.get(f'http://gateway.marvel.com/v1/public/characters?ts={ts}&apikey={pub}&hash={hashed}&limit=100&nameStartsWith={letter}').json()  
    attribute = response['attributionText'] # attribute Marvel for the use of the API
    characters = response['data']['results']
    
    dict = []
    for key in characters:
        query = sql_select('SELECT * FROM achievements WHERE user_ID=%s AND card_ID=%s', session['user_id'], key['id'])
        if (not query) and (key['thumbnail']['path'] != 'http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available') and (key['description'] != ""):
            dict.append({
                'id' : key['id'],
                'name' : key['name'].split("(")[0],
                'description' : key['description'],
                'image' : key['thumbnail']['path'] + '.' + key['thumbnail']['extension'],
                'link' : key['urls'][0]['url'],
            })

    index = randint(0, len(dict)-1)
    selection = dict[index]

    # Generate random button names
    # Ensuring they are unique (to avoid duplicates) 
    # Removing any unnecessary info from name string
    num1 = randint(0, len(characters)-1)    
    random1 = characters[num1]['name']    
    while random1 == selection['name']:
        num1 = randint(0, len(characters)-1)    
        random1 = characters[num1]['name']
    if random1.split("("):
        random1 = random1.split("(")[0]
    if random1.split("/"):
        random1 = random1.split("/")[0]

    num2 = randint(0, len(characters)-1)
    random2 = characters[num2]['name']
    while random2 == selection['name'] or random2 == random1:
        num2 = randint(0, len(characters)-1)    
        random2 = characters[num2]['name']    
    if random2.split("("):
        random2 = random2.split("(")[0]   
    if random2.split("/"):
        random2 = random2.split("/")[0] 

    buttons = [selection['name'], random1, random2] 
    shuffle(buttons)

    return selection, attribute, buttons








        
    

