-- Drop tables if they already exist
DROP TABLE IF EXISTS favorite;
DROP TABLE IF EXISTS "user";

-- User Table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(150) NOT NULL
);

-- Favorite Table
CREATE TABLE favorite (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    drink_id VARCHAR NOT NULL,
    drink_name VARCHAR NOT NULL,
    drink_image VARCHAR NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "user" (id)
);
