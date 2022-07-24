-- TABLE CREATION --

CREATE TABLE users (            --SELECT *--
    user_ID SERIAL PRIMARY KEY, --query[0]--
    username TEXT NOT NULL,     --query[1]--
    email TEXT NOT NULL,        --query[2]--
    password TEXT NOT NULL,     --query[3]--    
    question INTEGER NOT NULL,  --query[4]--
    answer TEXT NOT NULL,       --query[5]--
    admin BOOLEAN               --query[6]--
);

CREATE TABLE cards (            --SELECT *--         
    card_ID INTEGER NOT NULL,   --query[0]--  
    name TEXT NOT NULL,         --query[1]--
    description TEXT NOT NULL,  --query[2]--
    image TEXT NOT NULL,        --query[3]--
    link TEXT NOT NULL          --query[4]--
);

CREATE TABLE achievements (                             
    user_ID INTEGER NOT NULL REFERENCES users(user_ID), 
    card_ID INTEGER NOT NULL  
);


            dict.append({
                'id' : key['id'],
                'name' : key['name'],
                'description' : key['description'],
                'image' : key['thumbnail']['path'] + '.' + key['thumbnail']['extension'],
                'link' : key['urls'][0]['url'],
                # 'status' : status
            })