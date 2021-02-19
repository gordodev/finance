#Trading OMS that will track positions and P/L

from os import system, name 
import time

position = 0
buying_power = 100000
side = 'NULL'
cost = 0
quote = 'NULL'


# clear function 
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def enter_order():
    global side, position, quantity
    print ('6 - Buy 100')
    print ('7 - Buy 1000')
    print ('8 - Buy 10000\n')
    print ('3 - Sell 100')
    print ('4 - Sell 100')
    print ('5 - Buy 100')

    print ('\nposition=',position)
    print ('Buying power=',buying_power)
    print ('')

    option = input ('Select order: ')
    print ('')
    
    if option == '6':
        side = 'buy'; quantity = 100
        #print ('Run position update')
        position_update()


    print (position)
    print(get_quote())

def position_update():
    global position, buying_power

    #print ('side: ',side)
    if side == 'buy':
        print ('side is buy')
        position += quantity
        cost = int(quote * quantity)#; buying_power -= cost 
        print ('cost: ',cost,'buyingp:',buying_power)
    time.sleep(2)
    clear()


def get_quote():
    f = open ("./logs/NYSE.dat")
    return f.readline()
    #print (quote)

#MAIN

while True:
    enter_order()
