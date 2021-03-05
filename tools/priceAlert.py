import time
from yahoo_fin import stock_info as si
from playsound import playsound
import sys
import os

#Text to speech libraries
import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 255)  #Speed


#from Tkinter import *

import os
os.system('color 0f') # activate defaul color scheme 

lastPx = "NULL"

print ('Arguments: ',len(sys.argv))
print (sys.argv)
time.sleep(2)


if len(sys.argv) > 5:
    PxDelta = 0; delta1=0.3*float(sys.argv[5]); delta2=0.8*float(sys.argv[5]) #PxDelta levels 1/2
else:
    PxDelta = 1.8; delta1=2.5; delta2=0.6                           #PxDelta levels default


'''
Setting delta levels of 2 and 3 is pretty quiet even for volatile stock like GME. Only alerts when thing are really moving

'''
price = 0

#QA Mode
qa_prices = [1,1.5,2,2,4,4,7,7.5,13,13,7,7,4,4.5,2,2,1,1]
#import pdb; pdb.set_trace()    #QA
if len(sys.argv) > 4: 
    if (sys.argv[4]) == 'qa':
        print ('>4 args')
        test_mode = 'qa'  #Activate QA mode
    else:
       print ('else')   #QA
       test_mode = 0


#                          FUNCTIONS

def get_symbol():
    global symbol
    symbol=input('Enter symbol: ')
    
def say(words):
    #global speech
    engine.say(words)
    engine.runAndWait()

def get_price(name):
    '''
    Get price from Yahoo
    '''
    global symbol, price
    
    try:
            #print ('Try')
            
            #criticalHigh = int(sys.argv[3])
            
            price=si.get_live_price(name) #Get price from Yahoo
            #price=si.get_live_price(symbol) #Get price from Yahoo
            #print (price)
            price = round(price, 2)
            #print (price)
    except:
            print ('NO DATA')
            playsound('crashEcho.mp3')
        
    #print ('Passed')
    
    return price

def price_alert():
    '''
    Loop; Checking price and alerting if target prices hit or price outside of bounds
    
    PxDelta=Difference in price(last vs current)
    criticalHigh = Major alarm for target high price 
    criticalLow = Major alarm for target low price
    uptick/downtick = Is current price higher/lower than lastPx?
    
    '''
    global lastPx,PxDelta,price,test_mode,qa_prices
    
    prices_len = len(qa_prices)
    count = 0
    
    
    while True:
        
        
        #test_mode = 'qa'
        #import pdb; pdb.set_trace()
        
        if test_mode == 'qa':
            price = qa_prices[count]
            print ('\n\n\n\n\n\n\nMonitoring Price changes:','['+symbol+'@',price,']\n','Delta 1/2: ',delta1,delta2)
            #print (price)
            #print (price)
            #time.sleep(2)
            if count < prices_len:
                count += 1
            else:
                count = 0
                break
        
        
        else:
            get_price(symbol)
            #print ('\n\n\n\n\n\n\nMonitoring Price changes------------:','['+symbol+'@',price,']            PROD')
            #print (price)
            print ('\n\n\n\n\n\n\nMonitoring Price changes:','['+symbol+'@',price,']\n','Delta 1/2: ',delta1,delta2,'PROD alternate')

        
        
        #CRITICAL TRIGGER
        if price > criticalHigh or price < criticalLow:
            os.system('color 4f') # sets the background to red
            message = (symbol,price)
            say(message)
            playsound('criticalAlert.wav')
            print ('**************   ',symbol,' PRICE ',price,' !!          ***************\n\nLOG INTO MERRILL NOW! *****\n\n\n\n\n')
        
        
        #FIRST ITERATION CHECK: Check if last price set
        
        if lastPx == "NULL":        #If lastPx not set yet, set it.(1st run)
            lastPx = price; continue
        
        elif lastPx == price: #If no price change, then loop again
                print ('UNCH'); time.sleep(2)
                continue

        
        #            UPTICK ALERT ---------    ^
        
        if price > lastPx:          #Checking if price increased
            
            uptick = "yes"
            PxDelta = round((price-lastPx),2)
            os.system('color 02') # sets the foreground green
            
            if PxDelta > delta1:         #Checking if uptick is large
                os.system('color af') # sets the background to light green
                message = (symbol,price,'up',PxDelta)
                say(message)
                playsound('Ring06.wav')
                print ('^\n^\n^\nuptick - (',PxDelta,') ',price)
                
            if PxDelta > delta2:         #Checking if uptick is large
                message = (symbol,price,'High Volatility, up',PxDelta)
                say(message)
            
        #            DOWNTICK ALERT ---------   V
            
        elif price < lastPx:       #Checking if price decreased
            
            PxDelta = round((lastPx-price),2)
            uptick = "no"
            os.system('color 04') # sets the foreground red
            
            if PxDelta > delta1:         #Checking if downtick is large
                os.system('color cf') # sets the background to light red
                message = (symbol,price,'down',PxDelta)
                say(message)
                playsound('down.wav')
                print ('^\n^\n^\downtick - (',PxDelta,') ',price)
                             
            if PxDelta > delta2:
                os.system('color 4f') # sets the background to red
                message = (symbol,price,'High Volatility, down',PxDelta)
                say(message)
                playsound('AlarmClock.mp3')
                print ("PRICE DROP: ",PxDelta," [Last: ",lastPx," | Price: ",price,']\n')
        '''    
        Medium level alarm for uptick/downtick should be here, then use uptick variable to indicate up/down. Consider change variable to tick=up/down
        
        Avg Px pattern display: Maybe on larger price moves, display last 5 average prices:
            Create average price list and price list, then sum(list)/len(list) > average price list
            display last 5 values in average price list
        
        '''
        
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
    criticalLow = float(sys.argv[2])
    criticalHigh = float(sys.argv[3])

#Begin price alert loop
price_alert()
