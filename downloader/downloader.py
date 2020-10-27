import pandas as pd
import sqlite3

table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
df.to_csv('/home/csws/dev/github/finance/downloader/S&P500-Info.csv')
df.to_csv("/home/csws/dev/github/finance/downloader/S&P500-Symbols.csv", columns=['Symbol'])


connection = sqlite3.connect('/home/csws/dev/github/finance/tradingPlatform/db/test.db')
cursor = connection.cursor()
quantity = input('Enter quantity: \n')
command = "INSERT INTO orders(symbol,side,price,quantity) VALUES('GE','SELL',50,"+quantity+")"
cursor.execute(command)
connection.commit()
connection.close()













































'''
df.to_csv("S&P500-Info.csv")
df.to_csv("S&P500-Symbols.csv", columns=['Symbol'])



/home/csws/dev/github/finance/downloader/S&P500-Symbols.csv
'''
