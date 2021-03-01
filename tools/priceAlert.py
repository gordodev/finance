import time
from yahoo_fin import stock_info as si
from playsound import playsound
import sys


lastPx = "NULL"
PxDelta = 0


def get_symbol():
    global symbol
    symbol=input('Enter symbol: ')
    
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
            playsound('criticalAlert.wav')
            print ('**************   ',symbol,' PRICE ',price,' !!          ***************\n\nLOG INTO MERRILL NOW! *****\n\n\n\n\n')
        
        
        #Check last price set
        
        if lastPx == "NULL":        #If lastPx not set yet, set it.(1st run)
            lastPx = price; continue
        
        elif lastPx == price: #If no price change, then loop again
                continue

        
        #            UPTICK ALERT ---------
        
        if price > lastPx:          #Checking if price increased
            
            uptick = "yes"
            PxDelta = round((price-lastPx),2)
            
            if PxDelta > 2:         #Checking if uptick is large
                playsound('Ring06.wav')
                print ('^\n^\n^\nuptick - (',PxDelta,') ',price)
            
        #            DOWNTICK ALERT ---------
            
        elif price < lastPx:       #Checking if price decreased
            
            PxDelta = round((lastPx-price),2)
            uptick = "no"
            
            
            
            if PxDelta > 2:         #Checking if downtick is large
                playsound('down.wav')
                print ('^\n^\n^\downtick - (',PxDelta,') ',price)
                             
        if PxDelta > 3:
            playsound('AlarmClock.mp3')
            print ("PRICE JUMP: ",PxDelta," [Last: ",lastPx," | Price: ",price,']\n')
            
        #Medium level alarm for uptick/downtick should be here, then use uptick variable to indicate up/down. Consider change variable to tick=up/down
        
        lastPx = price
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
