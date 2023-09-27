import datetime
import threading
from database import cursor, db
from datetime import date

def borrow_books():
    print("-----BORROW BOOK-----")
    
    username = check_username()
    no = False 
    while(not no):
        book_id = check_book_existence_id()
        '''book_title = input("Enter book title: ")
        book_author= input("Enter book author: ")
        book_id = find_book(book_title, book_author)'''    
        find_customer_SQL = ("SELECT c.customer_id FROM customers c WHERE c.username = %s")
        val_c = (username, )
        cursor.execute(find_customer_SQL, val_c)
        customer_id = cursor.fetchone()

        now = date.today()
        formatted = now.strftime('%Y-%m-%d')
            
        for x in book_id:
            quantity = int(input("Enter how many books youd like to borrow: "))
            check_quantity_SQL = (("SELECT b.quantity_in_stock FROM books b WHERE b.quantity_in_stock >=1 AND b.book_id = %s"))
            val_q = (x, )
            cursor.execute(check_quantity_SQL, val_q) 
            quantity_in_stock = cursor.fetchone()
            if quantity_in_stock == None:
                print("There is no book available.")
            else:
                for q in quantity_in_stock:
                    while(True):
                        if quantity > q:
                                print("There is only {} book/s.".format(q))
                        else:
                            break
                    decrease_quantity_in_stock(x, quantity, quantity_in_stock)
                    for y in customer_id:
                        sql_borrow_n = ("SELECT * FROM book_status bs WHERE book_id = %s AND customer_id = %s and status = 'borrowed'")
                        val_borrow_n = (x, y, )
                        cursor.execute(sql_borrow_n, val_borrow_n)
                        m = cursor.fetchone()
                            
                        if m == None:
                                
                            stat = 'borrowed'
                            book_status_SQL = ("INSERT INTO book_status(book_id, customer_id, borrow_date, quantity, status) VALUES (%s, %s, %s, %s, %s)")
                            val_bs = (x, y, formatted, quantity, stat)
                            cursor.execute(book_status_SQL, val_bs)
                            db.commit()
                            print("---------SUCCESS-BORROWED BOOK--------")
                            start_time = threading.Timer(5, warning_return)
                            start_time.start()
                        else:
                            print("You cannot borrow same book twice.")
            print("Do you like to buy another book?")
            command = input("Enter Yes or No: ")
        if command == "Yes":
            continue
        else:
            no = True
            break  
def check_book_existence_id():
    while(True):
        book_title = input("Enter book title: ")
        book_author= input("Enter book author: ")
        
        find_book_SQL= ("SELECT b.book_id FROM books b WHERE b.title = %s AND b.author = %s")
        val_b = (book_title, book_author, )
        cursor.execute(find_book_SQL, val_b)
        book_id = cursor.fetchone()
        
        if book_id == None:
            print("There is no book with title {} and author {}, try again.".format(book_title, book_author))
        else:
            break
    return book_id

def check_book_existence():
    while(True):
        book_title = input("Enter book title: ")
        book_author= input("Enter book author: ")
        
        find_book_SQL= ("SELECT b.book_id FROM books b WHERE b.title = %s AND b.author = %s")
        val_b = (book_title, book_author, )
        cursor.execute(find_book_SQL, val_b)
        book_id = cursor.fetchone()
        
        if book_id == None:
            print("There is no book with title {} and author {}, try again.".format(book_title, book_author))
        else:
            break
    return book_title,book_author,book_id


def buying_book():
    print("-----BUYING BOOK-----")
    username= check_username()
    no = False
    while not no:
        book_title, book_author, book_id = check_book_existence()

        day = int(input("Enter day: "))
        month = int(input('Enter month: '))
        year = int(input('Enter year: '))
        purchase_date = date(year, month, day)
        
        find_customer_SQL = ("SELECT c.customer_id FROM customers c WHERE c.username = %s")
        val_c = (username, )
        cursor.execute(find_customer_SQL, val_c)
        customer_id = cursor.fetchone()
        
        for x in book_id:
            quantity = int(input("Enter how many books youd like to buy: "))
            check_quantity_SQL = (("SELECT b.quantity_in_stock FROM books b WHERE b.quantity_in_stock >=1 AND b.book_id = %s"))
            val_q = (x, )
            cursor.execute(check_quantity_SQL, val_q) 
            quantity_in_stock = cursor.fetchone()
            if quantity_in_stock == None:
                print("There is no book available.")
            else:
                for q in quantity_in_stock:
                    while(True):
                        if(quantity > q):
                            print("Book quantity with title {} and author {} is {}".format(book_title, book_author, quantity_in_stock)) 
                        else:
                            break
                                        
                    decrease_quantity_in_stock(x, quantity, quantity_in_stock)
                    for y in customer_id:
                        status = 'bought'
                        book_status_bought_SQL = ("INSERT INTO book_status(book_id, customer_id, purchase_date, quantity, status) VALUES (%s, %s, %s, %s, %s)")
                        val_bs = (x, y, purchase_date, quantity, status, )
                        cursor.execute(book_status_bought_SQL, val_bs)
                        db.commit()     
                        print("----SUCCESS-BOUGHT BOOK----")  
        print("Do you like to buy another book?")
        command = input("Enter Yes or No: ")
        if command == "Yes":
            continue
        else:
            no = True 
            break

def find_book(book_title, book_author):
    find_book_SQL= ("SELECT b.book_id FROM books b WHERE b.title = %s AND b.author = %s")
    val_b = (book_title, book_author, )
    cursor.execute(find_book_SQL, val_b)
    book_id = cursor.fetchone()
    
    for b in book_id:
        book_id = b
    return book_id

def return_book():
    print("-----RETURNING BOOK------")
    
    username = input("Enter your username: ")
    username_sql = ("SELECT c.customer_id FROM customers c WHERE c.username = %s")
    val_u = (username, )
    cursor.execute(username_sql, val_u)
    c_id = cursor.fetchone()
    for c in c_id:
        customer_id = c
        
   
    no = False
    while not no:
        book_title = input("Enter book title for returning: ")
        book_author= input("Enter book author for returning: ")
        book_id = find_book(book_title, book_author)
        quantity = int(input("Enter how many books you are returning: "))
        day = int(input("Enter return day: "))
        month = int(input('Enter return month: '))
        year = int(input('Enter return year: '))
        return_date = date(year, month, day)
        status_return_SQL = ("UPDATE book_status SET status = 'returned', return_date = %s WHERE customer_id = %s AND book_id = %s")
        val_r = (return_date, customer_id, book_id, )
        cursor.execute(status_return_SQL, val_r)
        db.commit()
        print("Do you want to return another book?")
        command = input("Enter Yes or No: ")
        if command == "Yes":
            continue
        else:
            no = True
            increase_quantity_in_stock(quantity, book_id)
            print("----SUCCESS-BOOK RETURNED----")
            break
            
    
            
def decrease_quantity_in_stock(x, quantity, quantity_in_stock):
    for q in quantity_in_stock:
        print(q)
        q -= quantity
        
        update_quantity_stock_SQL = ("UPDATE books SET quantity_in_stock = %s WHERE book_id = %s")
        val_u = (q, x, )
        cursor.execute(update_quantity_stock_SQL, val_u)
        db.commit()
        

def increase_quantity_in_stock(quantity, book_id):
    increase_quantity_in_stock_SQL = ("SELECT b.quantity_in_stock FROM books b where b.book_id = %s")
    val_i = (book_id, )
    cursor.execute(increase_quantity_in_stock_SQL, val_i)
    quan = cursor.fetchone()
    for q in quan:
        print(q)
        q += quantity
        
        update_quantity_stock_SQL = ("UPDATE books SET quantity_in_stock = %s WHERE book_id = %s")
        val_u = (q, book_id, )
        cursor.execute(update_quantity_stock_SQL, val_u)
        db.commit()
        



def warning_return():
    print("-----WARNING-----")
    check_status_SQL= ("SELECT b.status, b.customer_id FROM book_status b WHERE b.status = 'borrowed'")
    inn_j_cus_SQL = ("SELECT b.status, c.name, c.lastname FROM book_status b JOIN customers c ON b.customer_id = c.customer_id WHERE b.status = 'borrowed'")
    cursor.execute(inn_j_cus_SQL)
    all = cursor.fetchall()
    for a in all:
        print("Customer {} {}, did not return borrowed book/s. Warning!".format(a[1], a[2]))


def find_customer(c_id):
    find_customer_SQL= ("SELECT c.customer_id FROM customers c WHERE c.customer_id = %s")
    val_b = (c_id, )
    cursor.execute(find_customer_SQL, val_b)
    customer_id = cursor.fetchone()
    print("Customer id is {}".format(customer_id))
    for c in customer_id:
        return c
    

def check_username():
    while(True):
        username= input("Enter your username: ")
        
        check_username_SQL = ("SELECT c.username FROM customers c WHERE c.username = %s")
        val_d = (username, )
        cursor.execute(check_username_SQL, val_d)
        user = cursor.fetchone()
        if user == None:
            print("There is no entered username, try again.")
        else:
            break
    return username  
        
#check_quantity()
#borrow_books()
#buying_book()
#warning_return()
#return_book()
#check_username()
#check_book_existence()
#from_username_to_id()
#find_book()
