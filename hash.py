# Password hash functions - create and authenticate

import bcrypt

# create hashed password
def hash_pw(input_pw):   
    return bcrypt.hashpw(input_pw.encode(), bcrypt.gensalt()).decode()

# authenticate user input with hashed password
def check_pw(input_pw, stored_pw):
    return bcrypt.checkpw(input_pw.encode(), stored_pw.encode())