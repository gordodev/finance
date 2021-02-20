#Trading OMS that will track positions and P/L

from os import system, name 
import time
from statistics import mean

position = 0
buying_power = 1000000
side = 'NULL'
cost = 0
quote = 'NULL'
price_history = []
avg_px = 0
account_value = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# clear function 
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def enter_order():
    global side, position, quantity, quote, avg_px, price_history, account_value
    print ('6 - Buy 100')
    print ('7 - Buy 1000')
    print ('8 - Buy 10000\n')
    print ('3 - Sell 100')
    print ('4 - Sell 100')
    print ('5 - Buy 100')
    print ('-')
    print ('a - Profit Algo')

    print ('\nPosition =',position)
    print ('Buying power =',buying_power)
    print ('AvgPx =',avg_px)
    print ('Account value =',account_value)
    print ('')

    option = input ('Select order: ')
    print ('')
    
    #Set side & quantity
    if option == '6':
        side = 'buy'; quantity = 100
   
    if option == '7':
        side = 'buy'; quantity = 1000

    if option == '8':
        side = 'buy'; quantity = 10000

    if option == '3':
        side = 'sell'; quantity = 100

    if option == '4':
        side = 'sell'; quantity = 1000

    if option == '5':
        side = 'sell'; quantity = 10000

    if option == 'a':
        print ('')


    quote=float(get_quote()) 
    position_update()        #Update position & buying power  
    avg_px = round((mean(price_history)),2)

    print ('NBBO: ',get_quote(),'\n')
    #ENTER ORDER ^^

def auto_trader():
    while True:
        quote=float(get_quote()); price_history.append(quote)


def position_update():
    global position, buying_power, account_value

    if side == 'buy':
        #Reject if not enough money
        if (buying_power - float(quote * quantity)) < 0:
            print (f"{bcolors.WARNING}ORDER REJECT: Insufficient funds{bcolors.ENDC}"); return
        position += quantity
        cost = float(quote * quantity); buying_power -= round((cost),2)
        price_history.append(quote)#Get price - add to history
        account_value = buying_power + (position * quote)
        print ('Account value: ',account_value,buying_power,position,quote,'Done')
        print ('Bought ',quantity)

    elif side == 'sell':
        #Reject if not enough shares
        if quantity > position:
            print (f"{bcolors.WARNING}ORDER REJECT: Insufficient shares{bcolors.ENDC}")
            print ('You tried to sell',quantity,'shares, but you only have',position,'!\n\n')
            return
        position -= quantity
        cost = float(quote * quantity); buying_power += cost
        price_history.append(quote)#Get price - add to history
        account_value = buying_power + (position * quote)
        print ('Account value: ',account_value,buying_power,position,quote,'Done')
        print ('Sold ',quantity)

    time.sleep(1)
    clear()


def get_quote():
    f = open ("./logs/NYSE.dat")
    return f.readline()
    #print (quote)

#MAIN

while True:
    enter_order()
