import spidev
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

spi = spidev.SpiDev(0,0) # create spi object connecting to /dev/spidev0.1
spi.max_speed_hz = 1000 # set speed to 1 Mhz
spi.mode = 0

try:
	spi.xfer2([0b01110111,0b11111100]) # write two byte
finally:
	spi.close() # always close the port before exit