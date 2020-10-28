#!/usr/bin/env python3

#Create flat file for Bloomberg system

import logging
import datetime

date = datetime.datetime.now()
print (date.strftime("%Y-%m-%d %H:%M:%S"))

logging.basicConfig(
        filename='./logs/flint.log',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO)


f = open ("flat.dat", "a")

#Get user data
while True:
    SecurityIDType = input('SecurityIDType ')
    if SecurityIDType == '':                 #If user does not enter value, break
        break
    SecurityID = input('SecurityID ')
    Price = input('Price ')
    Date = input('Date ')
    
    #Join all user data, then type string and finally write to file
    mydata = (SecurityIDType+SecurityID.center(12)[:12]+Price.center(10)[:10]+Date.center(8)[:8]+"\n")
    mydata = str(mydata)
    f.write (mydata)

f.close()

print ('Have a nice day')
f = open ("flat.dat","r")
print (f.read())

f.close()

'''
SCHEMA:

2,12,10,8							   
							   
The price upload specification:
Byte 1-2: Security ID Type (Required)
Byte 3-14: Security ID (Required)
Byte 15-24: Price (Required)
Byte 25-32: Date (Required, YYYYMMDD)


'''
