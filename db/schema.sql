-- TABLE CREATION --

CREATE TABLE users (            --SELECT *--
    user_id SERIAL PRIMARY KEY, --query[0]--
    username TEXT NOT NULL,     --query[1]--
    email TEXT NOT NULL,        --query[2]--
    password TEXT NOT NULL,     --query[3]--    
    question INTEGER NOT NULL,  --query[4]--
    answer TEXT NOT NULL,       --query[5]--
    admin BOOLEAN,              --query[6]--
    excluded TEXT NOT NULL      --query[7]--
);

CREATE TABLE cards (            --SELECT *--         
    id SERIAL PRIMARY KEY,      --query[0]-- 
    card_ID INTEGER NOT NULL,   --query[1]--  
    name TEXT NOT NULL,         --query[2]--
    description TEXT NOT NULL,  --query[3]--
    image TEXT NOT NULL,        --query[4]--
    link TEXT NOT NULL          --query[5]--
);

CREATE TABLE achievements (
    id SERIAL PRIMARY KEY,                          
    user_ID INTEGER NOT NULL REFERENCES users(user_id), 
    card_ID INTEGER NOT NULL
);