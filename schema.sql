CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE blogs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    username TEXT,
    title TEXT,
    uploaded_at TIMESTAMP,
    content TEXT
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    blog_id INTEGER REFERENCES blogs ON DELETE CASCADE,
    username TEXT,
    content TEXT,
    sent_at TIMESTAMP
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    blog_id INTEGER REFERENCES blogs ON DELETE CASCADE,
    UNIQUE (user_id, blog_id)    
);

CREATE TABLE drafts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    title TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
