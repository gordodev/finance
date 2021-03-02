import time
from yahoo_fin import stock_info as si
from playsound import playsound
import sys

import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 255)

#from Tkinter import *

import os
os.system('color 0f') # sets the background to black

lastPx = "NULL"
PxDelta = 0


def get_symbol():
    global symbol
    symbol=input('Enter symbol: ')
    
def say(words):
    #global speech
    engine.say(words)
    engine.runAndWait()
    
def get_price():
    '''
    Loop; Checking price and alerting if target prices hit or price outside of bounds
    
    PxDelta=Difference in price(last vs current)
    criticalHigh = Major alarm for target high price 
    criticalLow = Major alarm for target low price
    uptick/downtick = Is current price higher/lower than lastPx?
    
    '''
    global lastPx,PxDelta
    
    print ('\n\n\n\n\n\n\nMonitoring Price changes')
    
    while True:
        price=si.get_live_price(symbol) #Get price from Yahoo
        price = round(price, 2)
        
        #CRITICAL TRIGGER
        if price > criticalHigh or price < criticalLow:
            os.system('color 4f') # sets the background to red
            message = (symbol,price)
            say(message)
            playsound('criticalAlert.wav')
            print ('**************   ',symbol,' PRICE ',price,' !!          ***************\n\nLOG INTO MERRILL NOW! *****\n\n\n\n\n')
        
        
        #Check last price set
        
        if lastPx == "NULL":        #If lastPx not set yet, set it.(1st run)
            lastPx = price; continue
        
        elif lastPx == price: #If no price change, then loop again
                continue

        
        #            UPTICK ALERT ---------    ^
        
        if price > lastPx:          #Checking if price increased
            
            uptick = "yes"
            PxDelta = round((price-lastPx),2)
            os.system('color 02') # sets the foreground green
            
            if PxDelta > 2:         #Checking if uptick is large
                os.system('color af') # sets the background to light green
                message = (symbol,price,'up',PxDelta)
                say(message)
                playsound('Ring06.wav')
                print ('^\n^\n^\nuptick - (',PxDelta,') ',price)
            
        #            DOWNTICK ALERT ---------   V
            
        elif price < lastPx:       #Checking if price decreased
            
            PxDelta = round((lastPx-price),2)
            uptick = "no"
            os.system('color 04') # sets the foreground red
            
            if PxDelta > 2:         #Checking if downtick is large
                os.system('color cf') # sets the background to light red
                message = (symbol,price,'down',PxDelta)
                say(message)
                playsound('down.wav')
                print ('^\n^\n^\downtick - (',PxDelta,') ',price)
                             
        if PxDelta > 3:
            os.system('color 4f') # sets the background to red
            message = (symbol,price,'High Volatility, down',PxDelta)
            say(message)
            playsound('AlarmClock.mp3')
            print ("PRICE JUMP: ",PxDelta," [Last: ",lastPx," | Price: ",price,']\n')
            
        #Medium level alarm for uptick/downtick should be here, then use uptick variable to indicate up/down. Consider change variable to tick=up/down
        
        lastPx = price              #Set last price to current price before starting again
        time.sleep(13)

#     MAIN   -------------------------------------------------------------------    
'''
Loop: Checking price and alerting if target prices hit or price outside of bounds
'''

#If user did not enter command line parameters, then use defaults
if len(sys.argv) < 2:               #DEFAULT PARAMS
    symbol = "NULL"
    criticalHigh = 144
    criticalLow = 100
    get_symbol()                    #Get symbol from user
    
#Load command line paramerters into variables
else:
    symbol = sys.argv[1]
    criticalLow = int(sys.argv[2])
    criticalHigh = int(sys.argv[3])

#Begin price alert loop
get_price()
