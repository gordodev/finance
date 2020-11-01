#!/usr/bin/env python3

#------------------------------ Flint Trader -----------------------------------
#Summary: Flint is a FIX compliant, Order Management System (OMS) for trading various asset classes electronically. Flint is the trading client for order entry and management. The Flint Trader Platform (FTP), is the infrastructure that the trading client (Flint), is able to function.


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


#   ++++++++++++++++++++++++++++++++++++++++++  FUNCTIONS

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
    time.sleep(2)

    print ('System status OK\nReady for trading!\n\n')


def insert_order():
    '''
    Insert random order into db

            Parameters:
                    a (symbol): Symbol you want to trade

    '''
    pass
    logging.info('Function called: insert_order')

def start_db_order_loop():
    '''
    inserting random orders into the database

    '''
    logging.info('Function called: start_db_order_loop')
    logging.info('load tickers')
    OrderID=1000; ClientOrderIDNum=11000; ClOrderID=('CARL_'+str(ClientOrderIDNum))
    print ('\n\nInserting random orders into the DB\n\n')

    while True:
        logging.info('Inserting order in DB')
        #ticker=(random.choice(tickers).decode("utf-8"))
        print ('Inserting order in DB\n')

        get_random_values()
        cursor = connection.cursor()

        #               INSERT RECORDS INTO DB ==============================

        #INSERT RANDOM ORDER
        cursor.execute('INSERT INTO orders (OrderID,ClOrderID, SenderID, SenderSubID, TargetID, TargetSubID,Side, Symbol, Quantity, Price) VALUES (?,?,"Carl_Trading","CarlX","BIDS","Bret",?,?,?,?)',(OrderID,ClOrderID,Side,Symbol,Quantity,Price))
       
        #INSERT RANDOM EXECUTION
        cursor.execute('INSERT INTO executions (BeginString, BodyLength, MsgType, SenderCompID, TargetCompID, SenderSubID, MsgSeqNum, SendingTime, DeliverToCompID, Account, AvgPx, ClOrdID, CumQty, Currency, ExecID, LastPx, LastQty, OrderID, OrderQty, OrdStatus, OrdType, OrderCapacity, Side, Symbol, TimeInForce, TransactTime, SettlType, SettlDate, TradeDate, ClientID, ExecTransType, CheckSum, executions_key) VALUES ("FIX.4.0", "0291", "8", "GOLD", "CARLYLE3", "BDBH", "171", "20060609-11:48:07", "OPCOWR", "X937101002", ?, ?, "0", "USD", "3490404", "0.00000000", "0", ?, ?, "0", "1", "P", ?, ?, "0", "20060609-11:48:07", "0", "20060614", "20060609", "OPCOERROR", "0", "001", "customkey0124244")',(Price,ClOrderID,OrderID,Quantity,Side,Symbol))


        #Exec queries:  OrderID,WOrderID,ClOrderID,SenderID,SenderSubID,TargetID,TargetSubID,OnBehalfOfID,OnBehalfOfSubID,DeliverToID,DeliverToSubID,AssignedUserID,OrigOrderDateTime,Side,Symbol,Quantity,WorkingQty,”14”=Makes,Leaves,OrderType,Price,Text,ModOrderType,ModPrice,ModQuantity,State,CxlState,Type,DestinationName,BranchSeqNum,XferStatus,*


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
    Price = (random.randint(1, 500))
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
#  --------------------------------------------  END FUNCTIONS

#                  MAIN

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


#          -----------    TASK LIST    -----------------

#Generate FIX orders periodically

#Phase 1: Output single order to FIX log

#Phase 2: Generate 1 order ever 10 seconds

#Phase 3: Randomize stock from list

#Phase 4: Randomize Px from list

#Phase 5: Randomize MARKETABLE Px

#Flint Trading Platform 10/28/20
