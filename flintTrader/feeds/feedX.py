import random
import time

#Generate random prices within range

#prices = ['','','','','','']


#Functions +++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_interval():
    intervals = ['.1'] * 10 + ['.5'] * 50 + ['.8'] * 40
    return random.choice(intervals)

def get_price():
    '''
    print ('getting price',random.randint(50,80))
    random.randint(50,80)
    '''
    global price
    direction = ['up','down']
    direction = random.choice(direction)
    ticks = ['1','2','0.8']
    tick = int(float(random.choice(ticks)))
    print ('tick: ',tick)

    #Change Price
    if direction == 'up':
        price += tick

    print (direction,tick)
    print (price)

def price_init():
    '''
    set initial price
    '''
    return random.randint(50,80)


#Functions ------------------------------------------------------------

#Set initial price

price = price_init()
print ('price is: ',price)

while True:
    #print(get_interval())
    global interval
    #interval = int(float(get_interval()))
    interval = 1
    get_price()
    time.sleep(1)




