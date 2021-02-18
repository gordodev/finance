#!/usr/bin/env python3

#------------------------------ Flint Trader -----------------------------------
'''
Summary: Flint is a FIX compliant, Order Management System (OMS) for trading various asset classes electronically. Flint is the trading client for order entry and management. The Flint Trader Platform (FTP), is the infrastructure that the trading client (Flint), is able to function.
'''

import logging
import datetime
import time
import sqlite3
import csv
import random

date = datetime.datetime.now()
print (date.strftime("%Y-%m-%d %H:%M:%S"))

logging.basicConfig(
        filename='/home/csws/dev/github/finance/flintTrader/logs/flint.log',
        format='%(asctime)s %(levelname)-8s %(message)s',   
        level=logging.INFO)

connection = sqlite3.connect('/home/csws/dev/github/finance/flintTrader/db/FTP_Database.db')
tickers  = '/home/csws/dev/github/finance/flintTrader/data/nasdaqlisted.txt' #QA is this bug? Conflict with list?


#   ---------------------------------------------------------------------------------  FUNCTIONS
def init_db():
    '''
    Initialize DB connection
    '''

    logging.info('Function called: init_db')

    OrderID = 1000; ClientOrderIDNum = 11000; ClOrderID = ('CARL_' + str(ClientOrderIDNum))

    connection = sqlite3.connect('/home/csws/dev/github/finance/flintTrader/db/XFTP_Database.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT VERSION()")

    except sqlite3.Error:
        logging.exception('')    #Log exceptions/traceback
        print ("ERROR IN CONNECTION")


def load_tickers():
    '''
    load tickers into list
    '''
    logging.info('Function called: load_tickers')
    logging.info('Loading tickers')
    global tickers

    with open ('/home/csws/dev/github/finance/flintTrader/data/nasdaqlisted.txt', mode='r') as infile:
        reader = csv.reader(infile,delimiter='|')
        tickers = [rows[0] for rows in reader]


def new_order():
    '''
    What am I doing?

            Parameters:
                    a (parameter): what is this?
                    b (parameter): what is this?

            Returns:
                    what will you return?
    '''
    pass
    logging.info('Function called: new_order')   


def get_symbol(symbol):
    '''
    What am I doing?

            Parameters:
                    a (parameter): what is this?
                    b (parameter): what is this?

            Returns:
                    what will you return?
    '''
    pass
    logging.info('Function called: get_symbol')


def get_price(symbol):
    '''
    What am I doing?

            Parameters:
                    a (parameter): what is this?
                    b (parameter): what is this?

            Returns:
                    what will you return?
    '''
    pass
    logging.info('Function called: get_price')


def get_platform_status():
    '''
    Check system status for entire trading platform

    '''
    logging.info('Function called: get_platform_status')
    
    print ('\nChecking system status\n\n')
    time.sleep(.5)

    print ('System status OK\nReady for trading!\n\n')


def insert_order():
    '''
    Insert random order into db

            Parameters:
                    a (symbol): Symbol you want to trade

    '''

    logging.info('Function called: insert_order')
    logging.info('Inserting order in DB')
    # ticker=(random.choice(tickers).decode("utf-8"))
    print('Inserting order in DB\n')

    get_random_values()
    cursor = connection.cursor()

    #               INSERT RECORDS INTO DB

    # INSERT ORDER
    cursor.execute(
        'INSERT INTO orders (OrderID,ClOrderID, SenderID, SenderSubID, TargetID, TargetSubID,Side, Symbol, Quantity, Price) VALUES (?,?,"Carl_Trading","CarlX","BIDS","Bret",?,?,?,?)',
        (OrderID, ClOrderID, Side, Symbol, Quantity, Price))

    logging.info('DB insert complete')
    connection.commit()
    logging.info('commit DB insert')

    # INCREMENT VALUES:    OrderID += 1; ClOrderID = CARL += 1
    OrderID += 1
    ClientOrderIDNum += 1
    ClOrderID = ('CARL_' + str(ClientOrderIDNum))
    print("\n\nsleeping\n")


def start_db_order_loop():
    '''
    inserting random orders into the database

    '''
    logging.info('Function called: start_db_order_loop')
    logging.info('load tickers')
    OrderID=1000; ClientOrderIDNum=11000; ClOrderID=('CARL_'+str(ClientOrderIDNum))
    #YYYMMDD
    TradeDate = (date.strftime("%Y%m%d"))
    TransactTime = (date.strftime("%Y%m%d-%H:%M:%S"))

    print ('\n\nInserting random orders into the DB\n\n')

    while True:
        logging.info('Inserting order in DB')
        #ticker=(random.choice(tickers).decode("utf-8"))
        print ('Inserting order in DB\n')

        get_random_values()
        cursor = connection.cursor()

        #               INSERT RECORDS INTO DB

        #INSERT RANDOM ORDER
        cursor.execute('INSERT INTO orders (OrderID,ClOrderID, SenderID, SenderSubID, TargetID, TargetSubID,Side, Symbol, Quantity, Price) VALUES (?,?,"Carl_Trading","CarlX","BIDS","Bret",?,?,?,?)',(OrderID,ClOrderID,Side,Symbol,Quantity,Price))


        #INSERT RANDOM EXECUTION
        logging.info('Inserting execution in Executions')
        cursor.execute('INSERT INTO executions (BeginString, BodyLength, MsgType, SenderCompID, TargetCompID, SenderSubID, MsgSeqNum, SendingTime, DeliverToCompID, Account, AvgPx, ClOrdID, CumQty, Currency, ExecID, LastPx, LastQty, OrderID, OrderQty, OrdStatus, OrdType, OrderCapacity, Side, Symbol, TimeInForce, TransactTime, SettlType, SettlDate, TradeDate, ClientID, ExecTransType, CheckSum, executions_key) VALUES ("FIX.4.0", "0291", "8", "GOLD", "CARLYLE3", "EQD", "171", ?, "OPCOWR", "X937101002", ?, ?, "0", "USD", "3490404", "0.00000000", "0", ?, ?, "0", "1", "P", ?, ?, "0", ?, "0", "20060614", ?, "OPCOERROR", "0", "001", "customkey0124244")',(TransactTime,Price,ClOrderID,OrderID,Quantity,Side,Symbol,TransactTime,TradeDate))




        logging.info('DB insert complete')
        connection.commit()
        logging.info('commit DB insert')

        #OrderID += 1; ClOrderID = CARL += 1
        OrderID += 1
        ClientOrderIDNum += 1
        ClOrderID = ('CARL_'+str(ClientOrderIDNum))
        print ("\n\nsleeping\n")
        #time.sleep(300)
        time.sleep(1)


def get_random_values():
    '''
    Generating random values

    '''
    logging.info('Function called: get_random_values')
    logging.info('generating random values')
    global Quantity; global Price; global Side; global Symbol
    Sides=['BUY','SELL']

    Quantity = (random.randint(1, 900000))
    Price = round(random.uniform(1.5, 501.9),2)

    Side = (random.choice(Sides))
    Symbol = (random.choice(tickers))
    print('Side=' + Side, 'Quantity=' + str(Quantity), 'Symbol=' + Symbol, 'Price=' + str(Price))

    '''
    while True:
        Quantity = (random.randint(1,900000))
        Price = (random.randint(1,500))
        Side = (random.choice(Sides))
        Symbol = (random.choice(tickers))
        print ('Side='+Side,'Quantity='+str(Quantity),'Symbol='+Symbol,'Price='+str(Price))
        time.sleep(0.2)
    '''
#   ---------------------------------------------------------------------------------  END FUNCTIONS

#                                               MAIN   ---------------------------------------------
init_db() #QA
print ('\nWelcome to Flint Trader!\n\n')

logging.warning('The program is still in development')
get_platform_status(); logging.info('Check platform status')
logging.info('Flint Trader started')
load_tickers()


while True:
    #Display menu
    print ('###############   MENU  ###########\n')
    print ('(n) new order')
    print ('(g) get price')
    print ('(r) random values loop')
    print ('(e) exit')
    print ('(d) start insert order into DB loop')

    choice = input('\n\nPress letter above, to select choice & then press enter.\n\n')

    if choice == 'n':
        new_order()

    elif choice == 'g':
        break

    elif choice == 'r':
        get_random_values()  # QA
        break

    elif choice == 'd':
        start_db_order_loop()
        break

    elif choice == 'x':
        print ('exiting menu')
        logging.info('User selected x, for exit menu')
        
        logging.info('Closing db connection')
        connection.close()
        break

#                                               MAIN      =========================================


# -----------    TASK LIST    -----------------

#Generate FIX orders periodically

#Phase 1: Output single order to FIX log

#Phase 2: Generate 1 order ever 10 seconds

#Phase 3: Randomize stock from list

#Phase 4: Randomize Px from list

#Phase 5: Randomize MARKETABLE Px

#Flint Trading Platform 10/28/20

#====================================================================================================================
#                                                  DEV
#====================================================================================================================