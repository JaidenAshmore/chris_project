
def get_questions(pos=None):
    questions = {
        1: 'Childhood pets name',
        2: 'Fathers middle name',
        3: 'Mothers maiden name',
        4: 'Favourite movie',
        5: 'Favourite food',
        6: 'Primary school name',
    }

    if pos != None:
        return questions[pos]
    else: 
        return questions



