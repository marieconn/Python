import mysql.connector
from database import cursor, db
from mysql.connector import errorcode

DB_NAME = 'library'

def create_database():
    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(DB_NAME))
    print("Database {} created".format(DB_NAME))

TABLES = {}

TABLES['books'] = (
   "CREATE TABLE books ("
    " book_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT, "
    " title varchar(50) NOT NULL, "
    " author varchar(50) NOT NULL, "
    " price float, "
    " quantity_in_stock int not null"
    ")"
)

TABLES['book_status'] = (
    "CREATE TABLE book_status (" 
    "bs_id INT NOT NULL AUTO_INCREMENT,"
    "book_id INT NOT NULL,"
    "customer_id INT NOT NULL,"
    "borrow_date DATE NULL DEFAULT NULL,"
    "return_date DATE NULL DEFAULT NULL,"
    "purchase_date DATE NULL DEFAULT NULL,"
    "quantity INT NOT NULL,"
    "status VARCHAR(50) NULL DEFAULT NULL,"
    "PRIMARY KEY (bs_id, book_id),"
    "CONSTRAINT fk_bs_customers FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON UPDATE CASCADE,"
    "CONSTRAINT fk_bs_products FOREIGN KEY (book_id) REFERENCES books (book_id) ON UPDATE CASCADE"
    ")"
    
)

TABLES['customers'] = (
    "CREATE TABLE customers ("
    " customer_id int(11) PRIMARY KEY AUTO_INCREMENT," 
    " name varchar(50) NOT NULL, "
    " lastname varchar(50) NOT NULL,"
    " email varchar(50) NOT NULL, "
    " password varchar(50) NOT NULL, "
    " username varchar(50) NOT NULL"
    ")"
)

def insert():
    insert_book_status_sql = ("INSERT INTO book_status (bs_id, book_id, customer_id, borrow_date, return_date, purchase_date, quantity, status) VALUES (1,1,1,'2023-08-05',NULL,NULL,1,'borrowed'), "
        "(2,2,2,'2023-02-05','2023-03-03',NULL,1,'returned'), "
        "(3,3,3,NULL,'2023-03-04','2023-01-12',1,'returned'), "
        "(4,4,4,'2023-03-04','2023-03-04',NULL,2,'returned'), "
        "(5,5,5,'2023-03-04','2023-03-12',NULL,1,'returned'), "
        "(6,6,6,'2023-03-05','2023-05-13',NULL,1,'returned'), "
        "(7,2,2,NULL,NULL,'2023-06-06',2,'bought'), "
        "(8,5,4,NULL,NULL,'2023-06-08',3,'bought'), "
        "(9,1,9,NULL,NULL,'2023-03-12',2,'bought')")
    
    insert_books_sql = ("INSERT INTO books (book_id,title,author,price,quantity_in_stock) "
                        "VALUES (1,'Animal Farm','George Orwell',259.99,5), "
                                "(2,'Ulysses','James Joyce',290.99,6), "
                                "(3,'Lolita','Vladimir Nabokov',360.99,3), "
                                "(4,'The Lord Of The Rings','J.R.R. Tolkien',875.99,10), "
                                "(5,'Anna Karenina','Leo Tolstoy',604.99,1), "
                                "(6,'Moja Knjiga','Moja',234.4,5)")
    
    insert_customers_sql = ("INSERT INTO customers (customer_id,name,lastname,email,password,username) VALUES (1,'Babara','MacCaffrey','barbara@gmail.com','barbara','barbara'), "
        "(2,'Ines','Brushfield','ines@gmail.com','ines','ines'), "
        "(3,'Freddi','Boagey','freddi@gmail.com','freddi','freddi'), "
        "(4,'Ambur','Roseburgh','ambur@gmail.com','ambur','ambur'), "
        "(5,'Levy','Mynett','levy@gamil.com','levy','levy'), "
        "(6,'Mary','Alice','malice@gmail.com','malice','malice'), "
        "(7,'Nikol','Peter','npeter@gmail.com','npeter','npeter'), "
        "(8,'Alice','Chai','alicec@gmail.com','alicec','alicec'), "
        "(9,'boris','urosev','bu@gmail.com','boris','boris'), "
        "(10,'ela','ela','ela@ela.com','ela','ela')")
    cursor.execute(insert_book_status_sql)
    db.commit()
    print("Successfully inserted")

def create_tables():
    cursor.execute("USE {}".format(DB_NAME))

    for table_name in TABLES:
        table_desc = TABLES[table_name]
        try:
            print("Creating table ({}) ".format(table_name), end="")
            cursor.execute(table_desc)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Already exists")
            else:
                print(err.msg)

#create_database()
#create_tables()
#insert()