#-*- coding: UTF-8 -*-
import sys,os #系統 讀檔案
import spidev #傳輸
import time,datetime
import socket,struct #網路
import numpy as np 
import RPi.GPIO as GPIO 




#Define Variables
delay = 1
ldr_channel = 0
Vreff = 5
#Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
 
def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data
    
 
while True:
    ldr_code = readadc(ldr_channel)
    voltage = float(ldr_code)/1024*Vreff
    print ("---------------------------------------")
    print("LDR Value: %d  voltage: %s" % (ldr_code,voltage) )
    #print(''%voltage )
    time.sleep(delay)