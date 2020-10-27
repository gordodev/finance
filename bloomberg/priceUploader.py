
#Create flat file

f = open ("flat.dat", "a")

while True:
    SecurityIDType = input('SecurityIDType ')
    if SecurityIDType == '':
        break
    SecurityID = input('SecurityID ')
    Price = input('Price ')
    Date = input('Date ')

    mydata = (SecurityIDType+SecurityID.center(12)[:12]+Price.center(10)[:10]+Date.center(8)[:8]+"\n")
    mydata = str(mydata)
    f.write (mydata)
    #Insert into file
    #Break if empty, continue if not

f.close()

print ('Have a nice day')
f = open ("flat.dat","r")
print (f.read())

f.close()

'''

2,12,10,8							   
							   
The price upload specification:
Byte 1-2: Security ID Type (Required)
Byte 3-14: Security ID (Required)
Byte 15-24: Price (Required)
Byte 25-32: Date (Required, YYYYMMDD)


'''


