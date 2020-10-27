import pandas as pd
import sqlite3
import time

table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
df.to_csv('/home/csws/dev/github/finance/downloader/S&P500-Info.csv')
df.to_csv("/home/csws/dev/github/finance/downloader/S&P500-Symbols.csv", columns=['Symbol'])


connection = sqlite3.connect('/home/csws/dev/github/finance/tradingPlatform/db/test.db')
cursor = connection.cursor()
#cursor.execute("CREATE TABLE student_details(id INTEGER, name TEXT)")  #Works
cursor.execute("INSERT INTO student_details(id, name) VALUES(1, 'student 1')")
cursor.execute("INSERT INTO student_details(id, name) VALUES(2, 'student 2')")
connection.commit()
connection.close()



time.sleep(3)

#Connecting to sqlite
conn = sqlite3.connect('/home/csws/dev/github/finance/tradingPlatform/db/test.db')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

# Preparing SQL queries to INSERT a record into the database.

cursor.execute ('''INSERT INTO orders
             VALUES(1, 'Alex')''')


#cursor.execute('''INSERT INTO orders(
#   price,symbol) VALUES 
#   ('F', 9000)''')


'''
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    #except Error as e:
    #    print(e)

    #return conn

    create_connection('/home/csws/dev/github/finance/tradingPlatform/db/test')
'''
