from flask import session

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




