CREATE DATABASE IF NOT EXISTS dbMovie;

USE dbMovie;

CREATE TABLE IF NOT EXISTS movies (
    show_id VARCHAR(10) PRIMARY KEY,
    type VARCHAR(10),
    title VARCHAR(255),
    director VARCHAR(255),
    country VARCHAR(255),
    date_added DATE,
    release_year INT,
    rating VARCHAR(10),
    duration INT,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS actors (
    actor_id INT AUTO_INCREMENT PRIMARY KEY,
    actor_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS show_actors (
    show_id VARCHAR(10),
    actor_id INT,
    FOREIGN KEY (show_id) REFERENCES movies(show_id),
    FOREIGN KEY (actor_id) REFERENCES actors(actor_id),
    PRIMARY KEY (show_id, actor_id)
);

CREATE TABLE IF NOT EXISTS genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS show_genres (
    show_id VARCHAR(10),
    genre_id INT,
    FOREIGN KEY (show_id) REFERENCES movies(show_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id),
    PRIMARY KEY (show_id, genre_id)
);


CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_type VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS watchlist (
    watchlist_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    show_id VARCHAR(10),
    status ENUM('watching', 'plan to watch', 'finished'),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (show_id) REFERENCES movies(show_id)
);