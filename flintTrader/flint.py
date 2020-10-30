#!/usr/bin/env python3

#------------------------------ Flint Trader -----------------------------------
#Summary: Flint is a FIX compliant, Order Management System (OMS) for trading various asset classes electronically. Flint is the trading client for order entry and management. The Flint Trader Platform (FTP), is the infrastructure that the trading client (Flint), is able to function.


import logging
import datetime
import time

date = datetime.datetime.now()
print (date.strftime("%Y-%m-%d %H:%M:%S"))

logging.basicConfig(
        filename='/home/csws/dev/github/finance/flintTrader/logs/flint.log',
        format='%(asctime)s %(levelname)-8s %(message)s',   
        level=logging.INFO)

#   ++++++++++++++++++++++++++++++++++++++++++  FUNCTIONS

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
    print ('\n\nInserting random orders into the DB\n\n')

    while True:
        logging.info('Inserting order in DB')
        print ('Inserting order in DB\n')
        time.sleep(5)


#  --------------------------------------------  END FUNCTIONS


print ('\nWelcome to Flint Trader!\n\n')

logging.warning('The program does nothing right now')
get_platform_status(); logging.info('Check platform status')
logging.info('Flint Trader started')


while True:
    #Display menu
    print ('###############   MENU  ###########\n')
    print ('(n) new order')
    print ('(g) get price')
    print ('(x) get')
    print ('(e) exit')
    print ('(x) start insert order into DB loop')

    choice = input('\n\nPress letter above, to select choice & then press enter.\n\n')

    if choice == 'n':
        start_db_order_loop()

    elif choice == 'g':
        break

    elif choice == 'x':
        break

    elif choice == 'e':
        break

    elif choice == 'x':
        print ('exiting menu')
        info.logging('User selected x, for exit menu')
        break


#          -----------    TASK LIST    -----------------

#Generate FIX orders periodically

#Phase 1: Output single order to FIX log

#Phase 2: Generate 1 order ever 10 seconds

#Phase 3: Randomize stock from list

#Phase 4: Randomize Px from list

#Phase 5: Randomize MARKETABLE Px

#Flint Trading Platform 10/28/20
