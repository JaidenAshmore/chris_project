-- TABLE CREATION --

CREATE TABLE users (                --SELECT *--
    id SERIAL PRIMARY KEY,          --query[0]--
    username TEXT NOT NULL,         --query[1]--
    email TEXT NOT NULL,            --query[2]--
    password TEXT NOT NULL,         --query[3]--    
    sec_question INTEGER NOT NULL,  --query[4]--
    sec_answer TEXT NOT NULL,       --query[5]--
    is_admin BOOLEAN                --query[6]--
);