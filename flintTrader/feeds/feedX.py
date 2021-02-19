import random
import time

#Generate random prices within range

support = 2
resistance = 400

#Functions +++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_interval():
    intervals = ['0.2'] * 10 + ['0.8'] * 50 + ['1.3'] * 40
    return random.choice(intervals)

def get_price():
    '''
    print ('getting price',random.randint(50,80))
    random.randint(50,80)
    '''
    global price, f
    direction = ['up','down']
    direction = random.choice(direction)
    ticks = ['1','2','0.8']
    tick = float(random.choice(ticks))
    #print ('tick: ',tick)

    #Check if price outside bands

    if price > resistance:
        direction = 'down'
    elif price < support:
        direction = 'up'

    #Change Price
    if direction == 'up':
        price += tick
    else:
        price -= tick

    #print (direction,tick)
    price = round((price),2); Px = str(price)
    print (price); f.write(Px); f.flush() 

def price_init():
    '''
    set initial price
    '''
    return random.randint(50,80)

def open_datafile():
    global f
    f = open ("./logs/NYSE.dat","w")

#Functions ------------------------------------------------------------

#Set initial price

price = price_init()
print ('price is: ',price)

open_datafile()

while True:
    #print(get_interval())
    global interval
    interval = int(float(get_interval()))
    #interval = 1
    open_datafile(); get_price()
    time.sleep(interval)




