DROP TABLE IF EXISTS users;

CREATE TABLE users (
        created TIMESTAMP DEFAULT NOW(),
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        login VARCHAR(64) UNIQUE,
        passhash CHAR(32),
        role VARCHAR(32)
    ) DEFAULT CHARSET=utf8;

INSERT INTO users (login, passhash, role) VALUES('root','63a9f0ea7bb98050796b649e85481845','admin');