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

#print ('Arguments: ',len(sys.argv)) #QA


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
#qa_prices = [1,1.5,1.4,2,2,4,4,7,7.5,13,13,7,7,4,4.5,9,2,3,2,5,1,1,2,4,1,7,2,9,22,5,3,10,25,6] 
#qa_prices = [0,1000,10000,0,999,190.89,192.49,191.72,192.99,193.0,192.5,192.82,191.0,189.03,190.57,191.77,193.01,193.0,193.1,193.21,192.89,192.68,191.49,192.2,192.45,192.63,191.5,192.91,194.62,195.2,194.31,192.62,0,200,205,209,214,218,221,229,235,245,255,300,330,400,300,200,100,90,80,0,192.38,192.98,191.28,191.15,191.97,192.03,192.05,191.67,191.11,191.0,192.99,193.34,193.5,193.6,194.0,193.99,193.53,193.48,193.93,193.75,193.5,193.0,192.58,192.02,191.32,189.15,188.5,188.85,189.7,189.51,190.97,190.6,191.5,191.06,191.63,190.63,189.92,189.31,190.07,190.37,189.66,189.09,0,190.32,180,170,160,150,140,130,120,110,100,90,80,70,60,50,40,30,0,190.67,190.09,190.32,190.9,190.43,190.69,191.0,191.32,191.01,191.43,191.47,190.61,190.25,189.31,189.19,190.21,189.99,190.87,191.08,190.39,190.16,190.2,190.9,191.33,190.97,191.13,191.46,192.08,192.51,193.72,193.11,192.52,193.3,193.24,192.34,192.5,193.0,193.36,193.81,193.69,193.94,193.87,194.07,194.48,194.74,195.15,197.15,198.54,198.0,198.26,198.14,196.78,197.36,195.98,195.53,195.41,195.81,195.5,195.57,195.55,196.85,197.0,196.16,196.17,196.29,196.85,196.75,196.31,196.05,196.56,196.17,195.05,193.0,192.77,192.5,192.38,192.95,193.73,194.32,195.6,194.49,193.74,193.8,193.99,194.63,194.4,194.15,194.09,194.51,193.18,191.75,191.58,192.83,193.72,194.5,193.72,194.5,]

qa_prices = [237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9] #4PM price surge.

#Detect qa mode
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
    history_limit: how many ticks back in time to check for trends
    
    NOTES:
    Looking for $3 price movement in 5 minutes. With 13s interval, that is 13.8 tick checks
    
    '''
    global up, down, price, tick, PxDelta, trend_count
    history_limit = 7
    #history_limit = 13                               #How many ticks to check for trends
    trend_Threshold = 4                              #Net price move to trigger alert. Was 3 before
    
    
    if trend_count == history_limit:                 #Determines trend check interval. This is max count before reset
        playsound('sonar.wma')
        trend_count = 0
        message = (symbol)
        say(message)
        
        #Capture current time
        ctime = (time.strftime("%H:%M:%S"))
        
        #TREND DIRECTION CHECKS
        if sum(up) > sum(down):                                             #Check if trend is UP
            PxNetDelta = (sum(up)-sum(down)); PxNetDelta=(round(PxNetDelta, 2))          #Net price movement
            print ('PxNetDelta,',PxNetDelta) #QA
            if PxNetDelta > 4 and PxDelta < 7:
                print ('\n\n\n',symbol,'moving up!\n')
                playsound ('moneyupshaggy.wav')
            elif PxDelta > 6:
                print ('\n\n\n',symbol,'moving WAY up!!\n')
                playsound ('grindingWayne.wav')
            message = ('PxNetDelta,',PxNetDelta) #QA
            say(message)#QA
            if PxNetDelta > trend_Threshold:
                say('Trending up. UP UP and AWAY')
                message = (symbol,'moved up to',price)
                say(message)
                
                with open("trends.dat","a+") as f:
                    message = (ctime+','+symbol+','+str(price)+','+str(sum(up))+'\n')
                    str(message)
                    f.write(message)
                    #f.write(str(symbol,price)); comma = ','; f.write(comma); f.write(str(sum(up))); f.write('\n')
        else:                                         #If trend not up, do this.
            if sum(down) > trend_Threshold:
                PxNetDelta = (sum(down)-sum(up)); PxNetDelta=(round(PxNetDelta, 2))
                print ('PxNetDelta,',PxNetDelta) #QA
                message = ('PxNetDelta,',PxNetDelta)#QA
                say(message)#QA
                if PxNetDelta > trend_Threshold:
                    say('Trending down. DOWN goes FRASER')
                    if PxNetDelta > 4 and PxDelta < 7:
                            print ('\n\n\n!!!!   ',symbol,'moving DOWN  !!!!\n')
                            playsound ('gameDead.wav')
                    elif PxNetDelta > 6:
                            print ('\n\n\n!!!!   ',symbol,'moving WAY DOWN  !!!!\n')
                            playsound ('trendDownBig.wma')
                    message = ('WARNING,',symbol,'fell down to',price)
                    say(message)
                    with open("trends.dat","a+") as f:
                        message = (ctime+','+symbol+','+str(price)+','+str(sum(up))+'\n')
                        str(message)
                        f.write(message)
                        #f.write(str(symbol,price)); comma = ','; f.write(comma); f.write(str(sum(down))); f.write('\n')



        #When you have less than 5 up/down values, give total net movement. When you have 5 or more, only give net of last 5.
            
        
        
    else:
        trend_count += 1                  #Add to trend count
    
    
    if PxDelta > 0:                       #Check if price moved. Store in PxDelta if true
        if tick == 'up':
            up.append(PxDelta)
           
        if tick == 'down':
            down.append(PxDelta)
            

    print ('up/down: ',up,'/',down)   #QA


    #TRUNCATE list if greater than history_limit
    if len(up) > history_limit:
        #print('popping UP list           ^^^^^^^^^^^^^^^^^^^^^^^^')
        time.sleep(1)
        up.pop(0)
        
    if len(down) > history_limit:
        #print('popping DOWN list          VVVVVVVVVVVVVVVVVVVVVVV')
        time.sleep(1)
        down.pop(0)


    
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
    unch_count = 0
    
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

        
        
        #                CRITICAL TRIGGER
        #HIGH PRICE
        if price > criticalHigh:
            os.system('color 4f') # sets the background to red
            message = (symbol,price,'Above high limit')
            say(message)
            playsound('highPrice_Belize.wav')
            print ('**************   ',symbol,' PRICE ',price,' !!          ***************\n\nLOG INTO Brokerage account NOW! *****\n\n\n\nHIGH price trigger\n')
                    
        #LOW PRICE
        if price < criticalLow:
            os.system('color 4f') # sets the background to red
            message = (symbol,price,'Below low limit!')
            say(message)
            playsound('criticalAlert.wav')
            print ('**************   ',symbol,' PRICE ',price,' !!          ***************\n\nLOG INTO Brokerage account NOW! *****\n\n\n\nLOW price trigger\n')
        
        
        #FIRST ITERATION CHECK: Check if last price set
        
        if lastPx == "NULL":        #If lastPx not set yet, set it.(1st run)
            lastPx = price; continue
        
        #CHECK FOR STATIC PRICE; possible halt
        if lastPx == price:                            #If no price change, then loop again
                print ('UNCH'); time.sleep(2)
                unch_count += 1
                if unch_count == 1:
                    print (symbol,'\n!!!!!!     possibly halted or market issue.    !!!!!!!!\n',unch_count,'times with no price change.\n')
                    playsound ('unchLoud.mp3')
                    continue
            
                if unch_count <= 11:                        #Start playing subtle alert after 5 but < 11 times static
                    print (symbol,'possibly halted or market issue.',unch_count,'times with no price change.')
                    playsound('unch.wav')
                    time.sleep(5)
                    continue
                
                if unch_count > 11:                                        #Greater than 10 times, start 30s intervals
                    print (symbol,'possibly halted or market issue.',unch_count,'times with no price change.\n\nSLEEPING 30 seconds!')
                    playsound('giveup.wma')
                    time.sleep(30)
                    continue
                    
                else:
                    message = (symbol,'possibly halted or market issue.',unch_count,'times with no price change.')
                    say (message)
                        
                    continue
        else:
            unch_count -= 1
        
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
        
        #import pdb; pdb.set_trace()
        ctime = (time.strftime("%H:%M:%S"))
        with open("prices.dat","a+") as f:
            price = str(price)
            ctime = (time.strftime("%H:%M:%S"))
            message = (ctime+','+symbol+','+price+'\n')
            f.write(message); 
            #comma = ","; f.write(comma)
            
        
        #Sleep interval for QA mode and PROD
        if test_mode == 'qa':
            #time.sleep(1)  #QA interval
            print ('\n\nMODE: QA\n')
        else:
            print (time.strftime("%H:%M:%S"))
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
