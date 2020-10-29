#!/usr/bin/env python3

#------------------------------ Flint Trader Support Module -----------------------------------
#Summary: Make sure all applications are running as expected.


import logging
import datetime
import os
import subprocess      #so we can process the values returned from the shell
import time

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
    logging.info('def check_status')
    print ('\n\nChecking status\n')

def check_memory():
    # Define RAM variables
    logging.info('Function called: check_memory')
    TotalRAM=subprocess.check_output(['free -h  | grep ^Mem | tr -s \' \' | cut -d \' \' -f 2'], shell= True)
    RAMUsed=subprocess.check_output(['free -h  | grep ^Mem | tr -s \' \' | cut -d \' \' -f 3'], shell= True)
    RAMFree=subprocess.check_output(['free -h  | grep ^Mem | tr -s \' \' | awk \'{print $4}\''], shell= True)
    TESTVALUE=subprocess.check_output(["date"])
    Threshold_RAM_Usage=2048000

    print ("\n\nChecking RAM Usage...")
    print (" Your total RAM Capacity is: ", TotalRAM.decode('ascii'))
    print (" Now, your system is using: ", RAMUsed.decode('ascii'))
    print (" And, you have free RAM Capacity of: ", RAMFree.decode('ascii'))
    #print ("Here is test value: ", TESTVALUE.decode('ascii'))

    # Check if RAM is overused
    RAMfreeValue=int(subprocess.check_output(['free   | grep ^Mem | tr -s \' \' | cut -d \' \' -f 4'], shell= True))

    if RAMfreeValue <= Threshold_RAM_Usage:  # I also converted the string to integer using int ()
                print("Alert: Now, you only have the following amount of free RAM: ",  RAMFree)

def check_cpu():
    # Define CPU variables
    logging.info('Function called: check_cpu')
    print ('\n\nChecking CPU')

def check_space():
    # Define DISK variables
    logging.info('Function called: check_space')
    print ('\n\nChecking disk space')

def shutdown():
    #Shutdown application (do any clean up required)
    logging.info('Function called: shutdown')
    print ('\n\n\nShutting down Flint Trader Support Module\n')

    #Clear temp files
    #Close open files

#--------------------------------------------------------------------------MAIN

print ('\nWelcome to Flint Trader, SUPPORT MODULE!\n')
logging.info('Flint Trader started')



#Menus driven system status checker and alerter

'''
Development phases:

Phase 1: Basic menu system
Phase 2: Operational menu system (choice confirm only)

  ***    LINUX Dev phase ***
Phase 4: Use OS module to check memory
Phase 5: Use OS module to check CPU
Phase 6: Use OS module to check disk space

  ***    Add alert module
Phase 7: Add CPU alert(default trigger@90%)
Phase 8: Add memory alert(default trigger@2GB FREE)
Phase 9: Add disk alert (default trigger@75% usage)
Phase 10: Add alert threshold param setting for all triggers
Phase 11: Add interval setting via CSV or menu(Create csv config file)

'''
while True:

    #Present menu

    print("Choose an option below: ")

    print("1) Check memory")
    print("2) Check CPU")
    print("3) Check disk space")

    #Choice logic

    choice=input("\nType number above: \n")

    if choice == "1":
        check_memory()

    elif choice == "2":
        check_cpu()

    elif choice == "3":
        check_space()

    elif choice == "":
        print ("\nPlease enter valid value!")

    else:
        print ("\n*******\n\n!! Invalid or inactive value!! \n")
        logging.warning('User entered unknown value. Shutting down.')
        time.sleep(2)
        break


#___________________________________________________________________________


logging.info('Shutting down Flint Trader')
shutdown()

#Flint Trading Platform 10/28/20
