#!/usr/bin/env python3

#------------------------------ Flint Trader -----------------------------------
#Summary: Flint is a FIX compliant, Order Management System (OMS) for trading various asset classes electronically. Flint is the trading client for order entry and management. The Flint Trader Platform (FTP), is the infrastructure that the trading client (Flint), is able to function.


import logging
import datetime

date = datetime.datetime.now()
print (date.strftime("%Y-%m-%d %H:%M:%S"))

logging.basicConfig(
        filename='./logs/flint.log',
        format='%(asctime)s %(levelname)-8s %(message)s',   
        level=logging.INFO)

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

def get_ftpstatus():
    '''
    What am I doing?

            Parameters:
                    a (parameter): what is this?
                    b (parameter): what is this?

            Returns:
                    what will you return?
    '''
    pass

print ('\nWelcome to Flint Trader!\n')

logging.warning('The program does nothing right now')
logging.info('Flint Trader started')

#Flint Trading Platform 10/28/20
