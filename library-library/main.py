import decimal
from database import cursor, db
import book, graph
import os

def main_menu():
    login = False
    while not login:
        print("-------MENU-------")
        print("1. Register Customer")
        print("2. Login")
        print("-------------------")
        while(True):
            try:
                command = int(input("Enter desired option: "))
                while(not(command >= 1 and command <= 2)):
                    command = int(input("Try again you are not loged in: "))
                break
            except ValueError:
                print("Error. You did not enter number.")

        if command == 1:
            register_customer()
        elif command == 2:
            login_customer()    
            login = True

    while login:  
        check()
def check():
        print("-------MENU 2-------")
        print("3. See available books")
        print("4. Borrow Book")
        print("5. Buy Book")
        print("6. Return Book")
        print("7. Add new book to library")
        print("8. Graph")
        print("-------------------") 
        while(True):
            try:
                command = int(input("Enter desired option: "))
                while(not(command >= 3 and command <= 8)):
                    command = int(input("Try again: "))
                break
            except ValueError:
                print("Error. You did not enter number.")                  
        if command == 3:
            available_books()
        elif command == 4:
            book.borrow_books()
        elif command == 5:
            book.buying_book()
        elif command == 6:
            book.return_book()
        elif command == 7:
            add_book_to_library()
        elif command == 8:
            graph.graph()
    
def register_customer():
    print("-------CUSTOMER REGISTRATION-------\n")
    name = input("Enter name: ")
    lastname = input("Enter lastname: ")
    while (True):
        email = input("Enter email: ")
        if '@' not in email:
            print("Email has to contain @")
        else:
            break

    while(True):
        password = input("Enter password: ")
        if(len(password) == 0):
            continue
        else:
            break

    while(True):
        username = input("Enter username: ")
        username_duplicate_SQL = ("SELECT c.username FROM customers c WHERE c.username = %s")
        val_u = (username, )
        cursor.execute(username_duplicate_SQL, val_u)
        dupes = cursor.fetchone()
        #print(dupes)
        #print("There is {} in database".format(dupes))
        if dupes == None:
            #print("Dodacu u bazu {}".format(username))
            registration_succ_SQL = ("INSERT INTO customers(name, lastname, email, password, username) VALUES (%s, %s, %s, %s, %s)")
            val_reg = (name, lastname, email, password, username, )
            cursor.execute(registration_succ_SQL, val_reg)
            db.commit()
            print("-----SUCCESSFULLY REGISTRATED-----") 
            break
        else:
            print("This username {} is taken try another one.".format(username))
            continue


def login_customer():
    print("--------LOGIN---------")
    while(True):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        check_data_SQL = ("SELECT c.username, c.password FROM customers c WHERE c.username = %s AND c.password = %s")
        val_d = (username, password, )
        cursor.execute(check_data_SQL, val_d)
        data = cursor.fetchone()
        #print("User with data {}".format(data))
        if data == None:
            print("User with this information does not exist.")
            continue
        else:
            print("----SUCCESSFULLY LOGED IN----")
            break
def add_book_to_library():
    title = input("Enter book title: ")
    author= input("Enter book author: ")
    price = float(input("Enter book price: "))
    quantity_in_stock = int(input("Enter quantity: "))
    add_new_book_SQL = ("INSERT INTO books(title, author, price, quantity_in_stock) VALUES(%s, %s, %s, %s)")
    val_a = (title, author, price, quantity_in_stock, )
    cursor.execute(add_new_book_SQL, val_a)
    db.commit()
    print("----SUCCESSFULLY ADDED BOOK----")

def available_books():
    available_books_SQL = ("SELECT b.title, b.author, b.price FROM books b")
    cursor.execute(available_books_SQL)
    ab = cursor.fetchall()
    for a in ab:
        print(a)
#register_customer()
#login_customer()
#available_books()
main_menu() 
#add_book_to_library()