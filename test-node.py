import sys, time
import RPi.GPIO as GPIO
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

testCard = "353w3d3w83q93w73l93e43j33d93/"

hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';' , 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'  }
lcd = LCD()

def waitForCardInput():
    # Open the interface the card reader sends info to
    fp = open('/dev/hidraw0', 'rb')
    ss = ""
    done = False

    while not done:
        # Get the card value from the HID
        buffer = fp.read(8)
        # Parse through each encoded character
        for c in buffer:
            if c > 0:
                # 40 is carriage return which signifies
                # we are done looking for characters
                if int(c) == 40:
                    done = True
                    break;
                else:
                    # If it is a '2' then it is the shift key
                    # which should be skipped
                    if int(c) != 2:
                        # scans the HID dictionary to decode the number
                        ss += hid[ int(c) ] 
    return ss

def printToLCD(line1, line2):
    lcd.text(line1, 1)
    lcd.text(line2, 2)
    
def clearLCD():
    lcd.clear()
    
def enableMachine():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, 1)
    
def disableMachine():
    GPIO.cleanup()
        
# ---------------START MAIN CODE------------------
while True:
    if(waitForCardInput() == testCard):
        printToLCD("Access Granted!", "Safety First!")
        enableMachine()
        time.sleep(3)
        clearLCD()
        disableMachine()
        time.sleep(3)

    else:
        printToLCD("Access Denied!", "Talk to mentor!")
        time.sleep(3)
        clearLCD()
