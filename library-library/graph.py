from database import cursor, db
from datetime import date
import numpy as np
import matplotlib.pyplot as plt

def graph():

    title = []
    id_count = []
    book_info_SQL = ("SELECT b.title, COUNT(bs.book_id) AS bid FROM books b JOIN book_status bs ON (bs.book_id = b.book_id) WHERE bs.status = 'bought' GROUP BY b.book_id, b.title ORDER BY b.title")
    cursor.execute(book_info_SQL)
    bi = cursor.fetchall()
    print(bi)
    for b in bi:
        title.append(b[0])
        id_count.append(b[1])
        #print(b[0])
        #print(b[1])
    print("Title = ", title)
    print("Book id = ", id_count)

    plt.bar(id_count, title, width = 0.5, color = ['red', 'blue'])
    plt.xlim(0, 5)
    plt.ylabel("Title")
    plt.xlabel("Sold books")
    #plt.xticks(rotation=90)
    plt.grid()
    plt.show()

#graph()