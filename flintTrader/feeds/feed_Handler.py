#!/usr/bin/env python3

#------------------------------ Market data Feeds -----------------------------------
#Summary: Market feeds 

'''
INSTALL:
pip3 install yahoo_fin


'''


import logging
import datetime

import time
from yahoo_fin import stock_info as si


date = datetime.datetime.now()
print (date.strftime("%Y-%m-%d %H:%M:%S"))

logging.basicConfig(
        filename='./logs/feed.log',
        format='%(asctime)s %(levelname)-8s %(message)s',   
        level=logging.INFO)


def menu():
    '''
    #Create email list

    #Create email

    #Send emails

    '''

    choice = input("""
        A: C
        B: Cr
        C: Se
        X: Just send IT

        Please select option: """)

    if choice == "A" or choice == "a":
        print ('***   Create email list   ***\n')

        #addressSource = input('\nEnter source file name: ')
        addressSource = 'addressSource.txt'
        extract_addresses(addressSource)

        for i in emails:
            print(i)
        print ('\n\n')

    elif choice == "B" or choice == "b":
        print ('\n***   Create email   ***\n')

        create_email()

    elif choice == "C" or choice == "c":
        print ('\n***   Send Emails   ***\n')

        #print ('Sending in 3 hours'); time.sleep(10800) #3 Hours

        #extract_addresses('addressSource.txt')
        for address in emails:       #PROD MODE NOW
            send_email(sender,address,body_plus) #(sender,target,body)

    elif choice == "X" or choice == "x":
        print ('\n***   Send Emails   ***\n')

        create_email()

        for address in X_emails:
            send_email(sender,address,body_plus) #(sender,target,body)

    else:
        print ('\nAre you drunk?')

def get_price(symbol):
    '''
    What am I doing?

            Parameters:
                    a (parameter): what is this?
                    b (parameter): what is this?

            Returns:
                    what will you return?
    '''
    #price=si.get_live_price(symbol) #Get price from Yahoo
    #price = round(price, 2)
    price=round((si.get_live_price(symbol)),2) #Get price from Yahoo
    print (price)

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

print ('\nMarket data feeds!\n')

get_price('IBM')

menu()

logging.warning('The program does nothing right now')
logging.info('Flint Trader started')

#Flint Trading Platform 10/28/20
