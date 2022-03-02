ALTER TABLE wishlist DROP FOREIGN KEY fk_book;
ALTER TABLE wishlist DROP FOREIGN KEY fk_user;

-- drop tables if they exist
DROP TABLE IF EXISTS store;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS wishlist;
DROP TABLE IF EXISTS user;

/*
    Create table(s)
*/
CREATE TABLE store (
    store_id    INT             NOT NULL    AUTO_INCREMENT,
    locale      VARCHAR(500)    NOT NULL,
    PRIMARY KEY(store_id)
);

CREATE TABLE book (
    book_id     INT             NOT NULL    AUTO_INCREMENT,
    book_name   VARCHAR(200)    NOT NULL,
    author      VARCHAR(200)    NOT NULL,
    details     VARCHAR(500),
    PRIMARY KEY(book_id)
);

CREATE TABLE user (
    user_id         INT         NOT NULL    AUTO_INCREMENT,
    first_name      VARCHAR(75) NOT NULL,
    last_name       VARCHAR(75) NOT NULL,
    PRIMARY KEY(user_id) 
);

CREATE TABLE wishlist (
    wishlist_id     INT         NOT NULL    AUTO_INCREMENT,
    user_id         INT         NOT NULL,
    book_id         INT         NOT NULL,
    PRIMARY KEY (wishlist_id),
    CONSTRAINT fk_book
    FOREIGN KEY (book_id)
        REFERENCES book(book_id),
    CONSTRAINT fk_user
    FOREIGN KEY (user_id)
        REFERENCES user(user_Id)
);

/*
    insert store record 
*/
INSERT INTO store(locale)
    VALUES('123 Fake St, Clarence, WY 85037');

/*
    insert book records 
*/
INSERT INTO book(book_name, author, details)
    VALUES('The House on Mango Street', 'Sandra Cisneros', 'Young Latina girl growing up in Chicago');

INSERT INTO book(book_name, author, details)
    VALUES('El Laberinto de la Soledad', 'Octavio Paz', 'A reflexion from the author of the nature and constitution of Mexico');

INSERT INTO book(book_name, author, details)
    VALUES('Memoirs of Pancho Villa', 'Martin Luis Guzman', 'Pancho Villa talking about battles and all the men he encountered');

INSERT INTO book(book_name, author)
    VALUES('The Bluest Eye', 'Toni Morrison');

INSERT INTO book(book_name, author)
    VALUES('The Collected Poems of Langston Hughes', 'Arnold Rampersad');

INSERT INTO book(book_name, author)
    VALUES('To Kill A Mockingbird', 'Harper Lee');

INSERT INTO book(book_name, author)
    VALUES('The Great Gatsby', 'F. Scott Fitzgerald');

INSERT INTO book(book_name, author)
    VALUES('Lies my teacher told me', 'James W. Loewen');

INSERT INTO book(book_name, author)
    VALUES('The Power of Positive Thinking', 'Norman Vincent Peale');

/*
    insert user
*/ 
INSERT INTO user(first_name, last_name) 
    VALUES('Carlos', 'Ignacio');

INSERT INTO user(first_name, last_name)
    VALUES('Norma', 'Silva');

INSERT INTO user(first_name, last_name)
    VALUES('Theano', 'Paleochoriti');

/*
    insert wishlist records 
*/
INSERT INTO wishlist(user_id, book_id) 
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Carlos'), 
        (SELECT book_id FROM book WHERE book_name = 'Memoirs of Pancho Villa')
    );

INSERT INTO wishlist(user_id, book_id)
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Norma'),
        (SELECT book_id FROM book WHERE book_name = 'The Great Gatsby')
    );

INSERT INTO wishlist(user_id, book_id)
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Theano'),
        (SELECT book_id FROM book WHERE book_name = 'The Bluest Eye')
    );
