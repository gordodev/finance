#!/usr/bin/env python3

#------------------------------ Flint Trader Support Module -----------------------------------
#Summary: Make sure all applications are running as expected.


import logging
import datetime
import os

date = datetime.datetime.now()
print (date.strftime("%Y-%m-%d %H:%M:%S"))

logging.basicConfig(
        filename='./logs/FTP_Monitor.log',
        format='%(asctime)s %(levelname)-8s %(message)s',   
        level=logging.INFO)

def check_status():
    '''
    Make sure all applications are up and running

            Parameters:
                    a (feed): Check feed status
                    b (flint): Check Flint Trader status

            Returns:
                    STATUS:
                        OK: Some applications down but all critical apps are up
                        GOOD: All applications are up
                        FAIL: At least one critical application is down
    '''
    pass

print ('\nWelcome to Flint Trader, SUPPORT MODULE!\n')



#Menus driven system status checker and alerter

'''
Development phases:

Phase 1: Basic menu system
Phase 2: Operational menu system (choice confirm only)

***LINUX Dev phase***
Phase 4: Use OS module to check memory
Phase 5: Use OS module to check CPU
Phase 6: Use OS module to check disk space

*Phase 7: Add alert module
Phase 8:  Add CPU alert(default trigger)
Phase 9:  Add memory alert(default trigger)
Phase 10: Add disk alert (default trigger)
Phase 11: Add alert threshold param setting for all triggers
Phase 12: Add interval setting via XML or menu
'''

#Present menu

print("Choose an option below: ")

print("1) Check memory")
print("2) Check CPU")
print("3) Check disk space")

#Choice logic

choice=input("\nType number above: \n")

if choice == "1":
    print ("\nYou have none, forgetful Joe")
elif choice == "":
    print ("\nPlease enter valid value!")
else:
    print ("\n*******\n\n!! Invalid or inactive value!! \n")
#Choice 2



#Choice 3


#___________________________________________________________________________



logging.warning('The program does nothing right now')
logging.info('Flint Trader started')

#Flint Trading Platform 10/28/20
