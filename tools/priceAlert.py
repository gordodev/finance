import time
from yahoo_fin import stock_info as si
from playsound import playsound
import sys
import os

#Text to speech libraries
import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 255)  #Speed

#Latest changes:
'''
3/7
[ ] change uptick/downtick to tick
[ ] Finish trends tracking


'''

#from Tkinter import *

import os
os.system('color 0f') # activate defaul color scheme 

#Initiate variables:
lastPx = "NULL"
pxHistory = []; last5_AVG = []
up = []; down = []   #for tracking direction trends
tick = "NULL"
trend_count = 0

print ('Arguments: ',len(sys.argv))
print (sys.argv)
time.sleep(2)


if len(sys.argv) > 5:
    PxDelta = 0; delta1=0.3*float(sys.argv[5]); delta2=0.45*float(sys.argv[5]) #PxDelta levels 1/2
else:
    PxDelta = 1.8; delta1=2.5; delta2=0.6                           #PxDelta levels default


'''
Setting delta levels of 2 and 3 is pretty quiet even for volatile stock like GME. Only alerts when thing are really moving

'''
price = 0

#QA Mode
#qa_prices = [1,1.5,2,2,4,4,7,7.5,13,13,7,7,4,4.5,2,2,1,1]
qa_prices = [1,1.5,1.4,2,2,4,4,7,7.5,13,13,7,7,4,4.5,9,2,3,2,5,1,1,2,4,1,7,2,9,22,5,3,10,25,6]  #Price trends

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
    
def get_trend():
    '''
    figure out price trend by comparing average or last 5 prices vs previous average.
    
    pxHistory: List with all prices
    pxTrend: Last 5 prices
    
    NOTES:
    Looking for $3 price movement in 5 minutes. With 13s interval, that is 13.8 tick checks
    
    '''
    global up, down, price, tick, PxDelta, trend_count

    print (tick,tick) 
    
    if trend_count == 13:                 #Determines trend check interval. This is max count before reset
        trend_count = 0
    else:
        trend_count += 1                  #Add to trend count
    
    
    if PxDelta > 0:                       #Check if price moved. Store in PxDelta if true
        if tick == 'up':
            up.append(PxDelta)
           
        if tick == 'down':
            down.append(PxDelta)
            

    print ('up/down: ',up,'/',down)

    if trend_count == 13:                       #Only check for trends every 30 ticks
        if len(up) > 13 or len(down) > 13.8:      #Check if either list is greater than 13.8
            print ('up or down has now past 13.8')
            say('Trend check active')
            
            #Trucate list if greater than 13
            if len(up) > 13:
                say('popping UP')
                up.pop(0)
            elif len(down) > 13:
                say('popping DOWN')
                down.pop(0)
                
            if sum(up) > sum(down):
                if sum(up) > 3:
                    say('Price trending up. UP UP and AWAY')
                    message = ('Price up to',price)
                    say(message)
                    with open("trends.dat","a+") as f:
                        f.write(str(price)); comma = ','; f.write(comma); f.write(str(sum(up))); f.write('\n')
            else:
                if sum(down) > 3:
                    say('Price trending down. DOWN goes FRASER')
                    message = ('Price down to',price)
                    say(message)
                    with open("trends.dat","a+") as f:
                        f.write(str(price)); comma = ','; f.write(comma); f.write(str(sum(down))); f.write('\n')
        

  
    #When you have less than 5 up/down values, give total net movement. When you have 5 or more, only give net of last 5.
    
    
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
    tick = Is current price higher/lower than lastPx?
    
    '''
    global lastPx,PxDelta,price,test_mode,qa_prices,tick
    
    prices_len = len(qa_prices)
    count = 0
    
    
    while True:
        
        
        #test_mode = 'qa'
        #import pdb; pdb.set_trace()
        
        if test_mode == 'qa':
            price = qa_prices[count]
            print ('\n\n\n\n\n\n\nMonitoring Price changes:','['+symbol+'@',price,']\n','Delta 1/2: ',delta1,delta2)
           
            print ('count: ',count)
            print ('price list len: ',len(qa_prices))
            if count < (prices_len - 1):
                count += 1
            else:
                count = 0
                #break
        
        
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
            
            tick = "up"
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
            tick = "down"
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
        Medium level alarm for uptick/downtick should be here, then use tick variable to indicate up/down. 
        
        Avg Px pattern display: Maybe on larger price moves, display last 5 average prices:
            Create average price list and price list, then sum(list)/len(list) > average price list
            display last 5 values in average price list
        
        '''
        
        lastPx = price              #Set last price to current price before starting again
        get_trend()
        
        #Store price data
        
        with open("prices.dat","a+") as f:
            f.write(str(price)); comma = ','; f.write(comma)
            
        
        #Sleep interval for QA mode and PROD
        if test_mode == 'qa':
            #time.sleep(1)  #QA interval
            print ('\n\nMODE: QA\n')
        else:
            time.sleep(13) #DEFAULT Interval
        
        

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
