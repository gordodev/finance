import time
from yahoo_fin import stock_info as si
from playsound import playsound
import sys
import os

os.system('color 0f') # activate defaul color scheme 

#Text to speech libraries
import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 255)  #Speed


#Latest changes:
'''
3/10
[x] change uptick/downtick to tick
[x] Finish trends tracking
[ ] Tweak trends tracking
[ ] Cleaned up main display

'''


#Initiate variables:
lastPx = "NULL"
pxHistory = []; last5_AVG = []
up = []; down = []   #for tracking direction trends
tick = "NULL"
trend_count = 0
price = 0

#print ('Arguments: ',len(sys.argv)) #QA

#SET SENSITIVITY LEVELS BASED ON USER ARGUMENTS OR DEFAULTS
if len(sys.argv) > 5:
    PxDelta = 0; delta1=0.3*float(sys.argv[5]); delta2=0.45*float(sys.argv[5]) #PxDelta levels 1/2
else:
    PxDelta = 1.8; delta1=2.5; delta2=0.6                           #PxDelta levels default

#Detect qa mode
if len(sys.argv) > 4: 
    if (sys.argv[4]) == 'qa':
        #print ('>4 args')
        test_mode = 'qa'  #Activate QA mode
        print ('\n\n\n==================== TEST MODE ====================\n\nTEST\n\nTEST\n\nTEST\n\n')
    else:
       print ('else')   #QA
       test_mode = 0
       print ('\n\n\n==================== PROD MODE ====================\n\n')
       


'''
Setting delta levels of 2 and 3 is pretty quiet even for volatile stock like GME. Only alerts when thing are really moving

'''


#QA Mode TEST PRICE DATA
#qa_prices = [1,1.5,2,2,4,4,7,7.5,13,13,7,7,4,4.5,2,2,1,1]
#qa_prices = [1,1.5,1.4,2,2,4,4,7,7.5,13,13,7,7,4,4.5,9,2,3,2,5,1,1,2,4,1,7,2,9,22,5,3,10,25,6] 
#qa_prices = [0,1000,10000,0,999,190.89,192.49,191.72,192.99,193.0,192.5,192.82,191.0,189.03,190.57,191.77,193.01,193.0,193.1,193.21,192.89,192.68,191.49,192.2,192.45,192.63,191.5,192.91,194.62,195.2,194.31,192.62,0,200,205,209,214,218,221,229,235,245,255,300,330,400,300,200,100,90,80,0,192.38,192.98,191.28,191.15,191.97,192.03,192.05,191.67,191.11,191.0,192.99,193.34,193.5,193.6,194.0,193.99,193.53,193.48,193.93,193.75,193.5,193.0,192.58,192.02,191.32,189.15,188.5,188.85,189.7,189.51,190.97,190.6,191.5,191.06,191.63,190.63,189.92,189.31,190.07,190.37,189.66,189.09,0,190.32,180,170,160,150,140,130,120,110,100,90,80,70,60,50,40,30,0,190.67,190.09,190.32,190.9,190.43,190.69,191.0,191.32,191.01,191.43,191.47,190.61,190.25,189.31,189.19,190.21,189.99,190.87,191.08,190.39,190.16,190.2,190.9,191.33,190.97,191.13,191.46,192.08,192.51,193.72,193.11,192.52,193.3,193.24,192.34,192.5,193.0,193.36,193.81,193.69,193.94,193.87,194.07,194.48,194.74,195.15,197.15,198.54,198.0,198.26,198.14,196.78,197.36,195.98,195.53,195.41,195.81,195.5,195.57,195.55,196.85,197.0,196.16,196.17,196.29,196.85,196.75,196.31,196.05,196.56,196.17,195.05,193.0,192.77,192.5,192.38,192.95,193.73,194.32,195.6,194.49,193.74,193.8,193.99,194.63,194.4,194.15,194.09,194.51,193.18,191.75,191.58,192.83,193.72,194.5,193.72,194.5,]

#qa_prices = [237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9] #4PM price surge.



#qa_prices = [282.73,283.2,286.0,287.18,291.98,294.8,293.81,296.0,293.54,291.99,291.55,289.0,289.05,287.5,289.51,288.55,291.55,291.49,291.59,290.63,290.73,290.98,290.42,290.98,291.14,290.85,292.21,292.05,290.31,289.73,289.82,290.73,291.57,291.42,292.07,292.04,292.5,293.52,292.34,291.5,292.02,291.24,289.21,290.23,290.32,290.04,290.95,291.21,291.22,291.0,294.52,293.86,293.2,291.91,293.29,296.0,294.4,294.5,294.58,300.9,297.98,294.21,297.61,295.03,294.74,295.0,296.23,295.8,296.59,294.0,292.69,291.98,291.42,291.71,291.5,291.75,290.6,291.53,292.61,293.74,293.75,293.4,296.17,295.23,294.84,294.39,294.0,293.89,293.84,293.45,292.55,292.25,292.02,289.14,287.9,286.24,287.12,288.58,290.0,289.14,286.85,288.18,288.1,287.55,287.46,286.58,286.54,288.81,288.03,290.66,290.88,292.35,292.16,291.79,290.98,290.15,290.78,290.35,289.61,290.83,290.28,290.03,289.15,289.0,288.85,289.95,289.0,289.42,289.9,288.82,288.69,288.14,286.2,284.11,285.69,286.8,287.82,287.56,288.9,288.84,288.27,288.68,290.0,289.72,289.22,293.83,293.0,292.8,295.0,295.17,296.0,295.88,296.42,296.89,296.3,294.49,295.53,294.68,294.38,294.97,295.4,293.33,293.92,293.25,293.79,294.2,294.28,293.95,294.53,294.34,293.51,298.81,298.9,300.09,325.26,326.22,331.96,330.64,331.0,329.6,329.82,327.0,328.24,326.76,327.15,328.29,330.31,329.09,328.83,328.33,328.02,328.06,329.87,328.19,332.12,330.46,329.0,324.9,328.59,327.9,329.61,331.51,334.95,330.78,331.23,331.35,330.65,330.8,332.76,338.08,336.46,336.34,336.9,338.0,339.0,339.62,338.79,338.57,339.54,340.06,341.5,341.3,342.89,344.83,345.0,346.29,344.89,345.38,344.3,344.0,343.8,345.21,342.56,340.11,341.48,339.43,339.11,341.0,340.62,341.48,342.9,344.03,343.63,343.61,346.0,342.39,342.03,342.43,343.5,341.53,341.2,342.58,341.83,343.38,344.13,344.49,345.16,346.32,346.86,347.47,345.37,347.0,345.4,344.9,344.1,346.03,345.76,347.0,344.87,343.42,344.15,343.61,344.4,343.3,336.65,332.56,327.68,330.83,305.97,302.68,281.0,277.05,282.36,228.31,176.64,189.82,203.5,268.83,244.54,269.04,264.27,266.45,263.46,254.54,256.45,260.99,258.13,260.1,260.49,261.41,264.64,263.95,264.57,262.94,263.92,263.88,266.16,266.63,267.88,266.12,268.53,266.62,266.97,267.87,270.57,270.18,269.01,268.45,265.09,267.56,265.6,264.89,264.32,263.0,264.74,265.73,265.94,267.57,266.98,266.66,268.07,268.01,268.8,268.83,269.5,269.19,268.35,265.01,266.43,267.58,267.1,268.2,268.0,267.1,267.48,265.11,266.35,267.9,272.27,271.65,272.76,271.0,265.0,264.1,266.31,265.2,266.0,263.1,265.79,267.78,267.02,267.05,266.01,267.26,268.0,266.06,262.0,260.44,260.09,261.7,261.99,261.5,262.87,265.08,266.11,266.7,266.06,266.01,264.62,266.18,265.36,266.72,265.25,265.0,265.26,264.0,262.45,264.01,264.82,265.5,264.78,264.0,263.6,263.8,260.67,263.43,261.5,251.11,245.99,242.49,234.0,240.86,238.51,239.0,234.14,228.5,232.68,235.28,236.16,236.72,239.19,241.88,243.32,240.29,240.16,240.0,238.64,237.86,239.0,238.75,239.84,239.64,239.65,241.45,241.59,243.0,242.74,240.72,241.55,239.93,241.0,240.32,241.39,242.7,242.69,243.4,241.66,238.2,235.5,238.21,236.64,236.84,237.04,239.66,240.0,240.11,242.35,242.38,243.18,243.42,242.39,242.2,241.27,242.2,241.84,245.91,248.34,253.37,252.16,253.32,254.41,255.63,254.32,251.2,252.31,251.25,252.0,252.93,253.0,251.77,250.53,249.28,248.8,249.0,250.0,249.02,249.06,250.94,250.93,249.01,248.2,249.0,249.02,249.0,248.61,244.69,244.54,246.49,246.5,247.18,247.62,247.23,246.15,246.88,246.0,248.63,253.0,252.73,250.34,252.66,251.36,251.04,251.75,250.34,250.0,251.77,251.51,252.45,253.2,254.23,253.9,253.35,256.09,255.57,259.7,257.91,257.87,260.0,260.8,259.43,261.63,261.94,257.72,258.9,259.26,259.99,261.5,260.93,259.03,257.96,259.29,259.33,260.11,260.09,259.28,258.05,256.36,258.42,258.2,258.44,257.6,256.93,256.11,255.95,255.77,256.67,257.94,258.04,257.27,257.55,259.0,256.62,257.18,257.56,257.69,257.85,257.8,256.39,255.0,254.72,256.02,255.68,255.28,255.05,254.0,255.0,253.0,251.0,251.55,252.86,253.0,253.54,253.5,253.8,254.85,253.74,253.33,254.0,252.0,251.37,252.86,251.36,250.0,248.03,249.89,248.39,247.92,246.6,246.18,249.69,249.75,252.45,254.0,255.79,256.29,254.35,255.92,256.25,255.89,254.56,255.9,256.85,255.36,256.04,257.46,257.48,256.01,254.34,255.12,255.0,254.22,254.13,254.43,254.02,253.8,253.7,253.2,254.84,254.85,237.35,238.15,238.14,238.17,237.61,237.64,237.58,237.64,237.55,237.28,236.11,236.91,237.2,236.6,236.81,236.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,237.2,236.6,236.81,236.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,273.9,274.7,266.0,266.61,264.74,263.3,263.27,264.5,262.67,262.0,263.44,264.73,263.65,262.73,262.69,262.7,260.6,260.57,261.5,261.75,263.19,263.72,263.75,262.24,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9,237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9,237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9,237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9,237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,237.35,238.15,238.14,238.17,237.61,237.64,270.58,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9,237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9,237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9,237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9,237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9,237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9,237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9,237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15,236.5,236.79,237.43,238.06,237.68,237.79,237.86,238.22,238.9,238.68,238.54,238.02,238,238.05,238.67,238.66,238.26,238.49,238.71,239.43,239.49,238.67,238.57,237.56,237.93,237.19,237.03,237.9,237.83,237.47,238.01,241.86,241.95,242.41,242.3,241.52,241.63,242.02,242.4,241.84,241.18,240.6,241,240.15,240.49,242.6,241.01,241.96,241.59,241.68,241.87,241,241.57,242.14,242.35,242.13,242.46,242.7,241.58,241.05,240.56,240.84,241.26,241.49,241.32,242.01,242.24,242.28,242.1,242.02,241.66,242.08,242.64,242.67,242.7,242.59,242.38,243.46,244.16,244.19,243.95,244.19,243.72,244.11,244.62,245.32,246.45,247.4,247.2,247.83,249.06,249.67,249.66,248.34,248.01,244.44,246.71,246.9,237.43,237.35,238.15,238.14,238.17,237.61,237.64,270.58,287.64,297.55,23.28,23.11,23.91,180.2,170.6,160.81,150.86,236.85,236.59,236.08,236.12,236.28,235.5,236.15]

#11:30AM 3/10 GME rise to 340+ and crash to 170, then up to 250
qa_prices = [293.95,294.53,294.34,293.51,298.81,298.9,300.09,325.26,326.22,331.96,330.64,331.0,329.6,329.82,327.0,328.24,326.76,327.15,328.29,330.31,329.09,328.83,328.33,328.02,328.06,329.87,328.19,332.12,330.46,329.0,324.9,328.59,327.9,329.61,331.51,334.95,330.78,331.23,331.35,330.65,330.8,332.76,338.08,336.46,336.34,336.9,338.0,339.0,339.62,338.79,338.57,339.54,340.06,341.5,341.3,342.89,344.83,345.0,346.29,344.89,345.38,344.3,344.0,343.8,345.21,342.56,340.11,341.48,339.43,339.11,341.0,340.62,341.48,342.9,344.03,343.63,343.61,346.0,342.39,342.03,342.43,343.5,341.53,341.2,342.58,341.83,343.38,344.13,344.49,345.16,346.32,346.86,347.47,345.37,347.0,345.4,344.9,344.1,346.03,345.76,347.0,344.87,343.42,344.15,343.61,344.4,343.3,336.65,332.56,327.68,330.83,305.97,302.68,281.0,277.05,282.36,228.31,176.64,189.82,203.5,268.83,244.54,269.04,264.27,266.45,263.46,254.54,256.45,260.99,258.13,260.1,260.49,261.41,264.64,263.95,264.57,262.94,263.92,263.88,266.16,266.63,267.88,266.12,268.53,266.62,266.97,267.87,270.57,270.18,269.01,268.45,265.09,267.56,265.6,264.89,264.32,263.0,264.74,265.73,265.94,267.57,266.98,266.66,268.07,268.01,268.8,268.83,269.5,269.19,268.35,265.01,266.43,267.58,267.1,268.2,268.0,267.1,267.48,265.11,266.35,267.9,272.27,271.65,272.76,271.0,265.0,264.1,266.31,265.2,266.0,263.1,265.79,267.78,267.02,267.05,266.01,267.26,268.0,266.06,262.0,260.44,260.09,261.7,261.99,261.5,262.87,265.08,266.11,266.7,266.06,266.01,264.62,266.18,265.36,266.72,265.25,265.0,265.26,264.0,262.45,264.01,264.82,265.5,264.78,264.0,263.6,263.8,260.67,263.43,261.5,251.11,245.99,242.49,234.0,240.86,238.51,239.0,234.14,228.5,232.68,235.28,236.16,236.72,239.19,241.88,243.32,240.29,240.16,240.0,238.64,237.86,239.0,238.75,239.84,239.64,239.65,241.45,241.59,243.0,242.74,240.72,241.55,239.93,241.0,240.32,241.39,242.7,242.69,243.4,241.66,238.2,235.5,238.21,236.64,236.84,237.04]


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
        trend_count = 0
        print ('\n\n\nCHECKING FOR PRICE TRENDS\n\n')
        
        #Capture current time
        ctime = (time.strftime("%H:%M:%S"))
        
        #TREND DIRECTION CHECKS
        if sum(up) > sum(down):                                             #Check if trend is UP ---------------- UP UP UP UP
            playsound('sonar.wma')
            PxNetDelta = (sum(up)-sum(down)); PxNetDelta=(round(PxNetDelta, 2))          #Net price movement
            print ('Price moved, $'+str(PxNetDelta)) #QA
            
            #             2 LEVELS OF PRICE UP SOUNDS
            if PxNetDelta > 4 and PxNetDelta < 7:              #LEVEL 1 SOUNDS
                print ('\n\n\n',symbol,'moving up!\n')
                say (symbol)
                say ('MILLIONAIRE!')
                print ('\n\n\n',symbol,'moving up!\n')
                playsound ('moneyupshaggy.wav')
                say ('SWEET Tendies!')
                say ('Moving on up to the west side!')
            
            elif PxDelta > 6:                                  #LEVEL 2 SOUNDS
                print ('\n\n\n',symbol,'moving WAY up!!\n')
                say (symbol)
                say('BILLIONAIRE!')
                playsound ('grindingWayne.wav')
                say ('Moon launch in progress. Please take me with you!')
            
            #message = ('Price moved up, $'+str(PxNetDelta)) #QA
            #say(message)#QA

            if PxNetDelta > trend_Threshold:
                #say('Trending up. UP UP and AWAY')
                message = (symbol,'moved up to $'+str(price))
                say(message)
                
                with open("trends.dat","a+") as f:
                    message = (ctime+','+symbol+','+str(price)+','+str(sum(up))+'\n')
                    str(message)
                    f.write(message)
                    #f.write(str(symbol,price)); comma = ','; f.write(comma); f.write(str(sum(up))); f.write('\n')
        
        else:                                                                 #Check if trend is DOWN ---------------- DOWN DOWN DOWN DOWN
            if sum(down) > trend_Threshold:
                playsound('sonarDown.wma')                #plays only if move down more than threshold
                PxNetDelta = (sum(down)-sum(up)); PxNetDelta=(round(PxNetDelta, 2))
                if PxNetDelta > trend_Threshold:
                    print ('Price moved down,'+str(PxNetDelta)) #QA
                    message = ('Price moved down, $'+str(PxNetDelta))#QA
                    say(message)#QA
                
                    if PxNetDelta > trend_Threshold:
                        say('Trending down. DOWN goes FRASER')
                    
                        if PxNetDelta > 4 and PxDelta < 7:
                                print ('\n\n\n!!!!   ',symbol,'moving DOWN  !!!!\n')
                                playsound ('gameDead.wav')
                                say ('Here comes da paper hands. Wow. Just wow.')
                                say ('Are you still trading meme stocks? You ape. Stay off Wall Street bets man. Seriously.')
                        
                        elif PxNetDelta > 6:
                                print ('\n\n\n!!!!   ',symbol,'moving WAY DOWN  !!!!\n')
                                playsound ('trendDownBig.wma')
                                say ('Now lets see if you really have, diamond hands. I Doubt it.')
                                say ('Dont mind me, Im just a program. Im less than even a Reddit, ape.')
                        
                        message = ('WARNING, WARNING',symbol,'fell down to $'+str(price),'Sad bruh. Just sad. Are you gonna be OK?')
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
            

    #print ('up/down: ',up,'/',down)   #QA


    #TRUNCATE list if greater than history_limit
    if len(up) > history_limit:
        #print('popping UP list           ^^^^^^^^^^^^^^^^^^^^^^^^')   #QA
        #time.sleep(1)                                                #QA
        up.pop(0)
        
    if len(down) > history_limit:
        #print('popping DOWN list          VVVVVVVVVVVVVVVVVVVVVVV')   #QA
        #time.sleep(1)                                                #QA
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
        
        #                                              MAIN DISPLAY
        if test_mode == 'qa':
            price = qa_prices[count]
            ctime = (time.strftime("%H:%M:%S"))
            print ('\n\n\n\n\n\n\n',ctime,'  CURRENT PRICE:','['+symbol+' $'+str(price),']')
            ctime = (time.strftime("%H:%M:%S"))
            
           
            #print ('count: ',count) #QA
            #print ('price list len: ',len(qa_prices))  #QA
            if count < (prices_len - 1):
                count += 1
            else:
                count = 0
                #break
        
        
        else:
            get_price(symbol)
            #print ('\n\n\n\n\n\n\nMonitoring Price changes------------:','['+symbol+'@',price,']            PROD')
            #print (price)
            print ('\n\n\n\n\n\n\n',ctime,'  CURRENT PRICE:','['+symbol+'$'+str(price),']\n','Delta 1/2: ',delta1,delta2,'PROD alternate')

        
        
        #                CRITICAL TRIGGER
        #HIGH PRICE
        if price > criticalHigh:
            os.system('color 4f') # sets the background to red
            print ('**************   ',symbol,' PRICE ',price,' !!          ***************\n\nLOG INTO Brokerage account NOW! *****\n\n\n\nHIGH price trigger\n')
            message = (symbol,price,'Above high limit')
            say(message)
            playsound('highPrice_Belize.wav')
            say ('high price breached')
                    
        #LOW PRICE
        if price < criticalLow:
            os.system('color 4f') # sets the background to red
            print ('**************   ',symbol,' PRICE ',price,' !!          ***************\n\nLOG INTO Brokerage account NOW! *****\n\n\n\nLOW price trigger\n')
            message = (symbol,price,'Below low limit!')
            say(message)
            playsound('criticalAlert.wav')
            say ('low price breached')
        
        
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
            if unch_count > 0:
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
                print ('\n\ndowntick - (',PxDelta,') ',price)
                             
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
    print ('Welcome to Price Alert!, Low alert: ',criticalLow,'High alert: ',criticalHigh)
    message = ('Welcome to Price Alert!, Low alert: ',criticalLow,'High alert: ',criticalHigh)
    say (message)

print('Price moves that will trigger price move alerts are, $'+str(delta1)+' $'+str(delta2))
message = ('Price moves, that will trigger alerts are $'+str(delta1)+' and $'+str(delta2))
say (message)
playsound('introBeat.wma')
#time.sleep(3)

#Begin price alert loop
price_alert()
