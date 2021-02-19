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

while True:
    #print(get_interval())
    global interval
    #interval = int(float(get_interval()))
    interval = 1
    get_price()
    time.sleep(1)




#Functions ------------------------------------------------------------
