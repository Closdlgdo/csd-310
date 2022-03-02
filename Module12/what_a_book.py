import sys
import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "root",
    "password": "Theano03192021!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

def show_menu():
    print("\nMain Menu: ")

    print("    1. View Books\n    2. View Store Location\n    3. View My Account\n    4. Exit The Program")

    try:
        choice = int(input('      <Enter a number to view respective menu(1:3)>: '))

        return choice
    except ValueError:
        print("\n  Invalid number! Program has been terminated! (please restart if you'd like to begin)\n")

        sys.exit(0)

def show_books(_cursor):
    # this will inner join the query 
    _cursor.execute("SELECT book_id, book_name, author, details from book")

    # this will get the results from the cursor object 
    books = _cursor.fetchall()

    print("\n  -- BOOK LISTING --")
    
    # this will iterate over the player data set and display the results 
    for book in books:
        print("  Name of book: {}\n  Author: {}\n  Details: {}\n".format(book[0], book[1], book[2]))

def show_locations(_cursor):
    _cursor.execute("SELECT store_id, locale from store")

    locations = _cursor.fetchall()

    print("\n  -- STORE LOCATION --")

    for location in locations:
        print("  Locale: {}\n".format(location[1]))

def validate_user():
    #this will validate the users ID 

    try:
        user_id = int(input('\n      Enter a customer id <Example: 1 (for user_id 1:3)>: '))

        if user_id < 0 or user_id > 3:
            print("\n  Invalid number! Program has been terminated! (please restart if you'd like to begin)\n")
            sys.exit(0)

        return user_id
    except ValueError:
        print("\n  Invalid number! Program has been terminated! (please restart if you'd like to begin)\n")

        sys.exit(0)

def show_account_menu():
    #this will show the users account menu

    try:
        print("\n      -- Customer Menu --")
        print("        1. Wishlist\n        2. Add a Book\n        3. Go to Main Menu")
        account_option = int(input('        <Example: 1 (for wishlist)>: '))

        return account_option
    except ValueError:
        print("\n  Invalid number! Program has been terminated! (please restart if you'd like to begin)\n")

        sys.exit(0)

def show_wishlist(_cursor, _user_id):
    #this will query the database for a list of books added to the users wishlist

    _cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " + 
                    "FROM wishlist " + 
                    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
                    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
                    "WHERE user.user_id = {}".format(_user_id))
    
    wishlist = _cursor.fetchall()

    print("\n        -- WISHLIST --")

    for book in wishlist:
        print("        Book Name: {}\n        Author: {}\n".format(book[4], book[5]))

def show_books_to_add(_cursor, _user_id):
    # this will show the query the database for a list of books not in the users wishlist 

    query = ("SELECT book_id, book_name, author, details "
            "FROM book "
            "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})".format(_user_id))

    print(query)

    _cursor.execute(query)

    books_to_add = _cursor.fetchall()

    print("\n        -- BOOKS AVAILABLE --")

    for book in books_to_add:
        print("        Book Id: {}\n        Name of Book: {}\n".format(book[0], book[1]))

def add_book_to_wishlist(_cursor, _user_id, _book_id):
    _cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})".format(_user_id, _book_id))

try:
    #this will try/catch block for handling potential MySQL database errors 

    db = mysql.connector.connect(**config) # this will connect to the WhatABook database I created

    cursor = db.cursor() # cursor for MySQL queries

    print("\n  Welcome to WhatABook! ")

    user_selection = show_menu() # show the main menu 

    # while the user's selection is not 4
    while user_selection != 4:

        # this will show if the user selects option 1, then it will call the show_books method and display the books
        if user_selection == 1:
            show_books(cursor)

        # this will show if the user selects option 2, then it will call the show_locations method and display the configured locations
        if user_selection == 2:
            show_locations(cursor)

        # this will show if the user selects option 3, then it will call the validate_user method to validate the entered user_id 
        # this will call the show_account_menu() to show the account settings menu
        if user_selection == 3:
            my_user_id = validate_user()
            account_option = show_account_menu()

            # while account option does not equal 3
            while account_option != 3:

                # this will show if the use selects option 1, call the show_wishlist() method to show the current users 
                # this will show configured wishlist items 
                if account_option == 1:
                    show_wishlist(cursor, my_user_id)

                # this will show if the user selects option 2, call the show_books_to_add function to show the user 
                # this will show the books not currently configured in the users wishlist
                if account_option == 2:

                    # this will show the books not currently configured in the users wishlist
                    show_books_to_add(cursor, my_user_id)

                    # get the entered book_id 
                    book_id = int(input("\n        Please enter the id of the book you'd like to add: "))
                    
                    # add the selected book the users wishlist
                    add_book_to_wishlist(cursor, my_user_id, book_id)

                    db.commit() # commit the changes to the database 

                    print("\n        The book with the id: {} was added to your wishlist!".format(book_id))

                # this will show if the selected option is less than 0 or greater than 3, display an invalid user selection 
                if account_option < 0 or account_option > 3:
                    print("\n      The option you selected is invalid, please try again")

                # will show the account menu 
                account_option = show_account_menu()
        
        # will show if the user selection is less than 0 or greater than 4, display an invalid user selection
        if user_selection < 0 or user_selection > 4:
            print("\n      The option you selected is invalid, please try again")
            
        # this will show the main menu
        user_selection = show_menu()

    print("\n\n  The program has been terminated...")

except mysql.connector.Error as err:
    #this will handle errors 

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The username or password is invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    #this will close the connection to MySQL

    db.close()
