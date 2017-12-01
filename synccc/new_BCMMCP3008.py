# -*- coding: utf-8 -*-
# Copyright (c) 2016 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import RPi.GPIO as GPIO
import spidev
import numpy as np
import time
import binascii
from  libbcm2835._bcm2835 import *
import ctypes
class MCP3008(object):
    """Class to represent an Adafruit MCP3008 analog to digital converter.
    """

    def __init__(self):
        """Initialize MAX31855 device with software SPI on the specified CLK,
        CS, and DO pins.  Alternatively can specify hardware SPI by sending an
        Adafruit_GPIO.SPI.SpiDev device in the spi parameter.
        """
        # Handle hardware SPI

    def read_adc(self, adc_number):
        """Read the current value of the specified ADC channel (0-7).  The values
        can range from 0 to 1023 (10-bits).
        """
        assert 0 <= adc_number <= 7, 'ADC number must be a value of 0-7!'
        # Build a single channel read command.
        # For example channel zero = 0b11000000
        command = 0b11 << 6                  
        # Start bit, single channel read
        command |= (adc_number & 0x07) << 3  # Channel number (in 3 bits)
        # Note the bottom 3 bits of command are 0, this is to 
        # 
        # account for the
        # extra clock to do the conversion, and the low null bit returned at
        # the start of the response.
        resp = self._spi.xfer2([command, 0x0, 0x0])
        # Parse out the 10 bits of response data and return it.
        result = (resp[0] & 0x01) << 9

        result |= (resp[1] & 0xFF) << 1
        result |= (resp[2] & 0x80) >> 7
        return result & 0x3FF

#NEW FUNCTION by myself
    def read_adc_loop(self,Times):

        if not bcm2835_init():
            return
        #init spi set
        bcm2835_spi_begin()
        bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST)      # The default
        bcm2835_spi_setDataMode(BCM2835_SPI_MODE0)                   # The default           
        bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_64)
        bcm2835_spi_chipSelect(BCM2835_SPI_CS1)                      # The default
        bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW)      # the default

        #Times是總回數
        times=range(Times)
        total_ch = 6
        total_channel = range(total_ch)
        Data=np.zeros([Times,total_ch,3]).astype(np.uint8)
        #從第三航開始改不然很奇怪，array的從新定義好像不行
        num=1
        chcommand = 0b11 << 6                  
        chcommand |= (num-1 & 0x07) << 3
        command1=np.array([chcommand,0,0])
        command1_c=command1.ctypes.data_as(ctypes.POINTER(ctypes.c_char))
        num=2
        chcommand = 0b11 << 6                  
        chcommand |= (num-1 & 0x07) << 3
        command2=np.array([chcommand,0,0])
        command2_c=command2.ctypes.data_as(ctypes.POINTER(ctypes.c_char))
        num=3
        chcommand = 0b11 << 6                  
        chcommand |= (num-1 & 0x07) << 3
        command3=np.array([chcommand,0,0])
        command3_c=command3.ctypes.data_as(ctypes.POINTER(ctypes.c_char))
        num=4
        chcommand = 0b11 << 6                  
        chcommand |= (num-1 & 0x07) << 3
        command4=np.array([chcommand,0,0])
        command4_c=command4.ctypes.data_as(ctypes.POINTER(ctypes.c_char))
        num=5
        chcommand = 0b11 << 6                  
        chcommand |= (num-1 & 0x07) << 3
        command5=np.array([chcommand,0,0])
        command5_c=command5.ctypes.data_as(ctypes.POINTER(ctypes.c_char))
        num=6
        chcommand = 0b11 << 6                  
        chcommand |= (num-1 & 0x07) << 3
        command6=np.array([chcommand,0,0])
        command6_c=command6.ctypes.data_as(ctypes.POINTER(ctypes.c_char))
        
        #init the C char* array   for C
        result1_c={}
        result2_c={}
        result3_c={}
        result4_c={}
        result5_c={}
        result6_c={}
        for i in times:
            result1_c[i]=Data[i,0].ctypes.data_as(ctypes.POINTER(ctypes.c_char))
            result2_c[i]=Data[i,1].ctypes.data_as(ctypes.POINTER(ctypes.c_char))
            result3_c[i]=Data[i,2].ctypes.data_as(ctypes.POINTER(ctypes.c_char))
            result4_c[i]=Data[i,3].ctypes.data_as(ctypes.POINTER(ctypes.c_char))
            result5_c[i]=Data[i,4].ctypes.data_as(ctypes.POINTER(ctypes.c_char))
            result6_c[i]=Data[i,5].ctypes.data_as(ctypes.POINTER(ctypes.c_char))
            
        
        startTime = time.time()
        for i in times:
            bcm2835_spi_transfernb(command1_c,result1_c[i],3)
            bcm2835_spi_transfernb(command2_c,result2_c[i],3)
            bcm2835_spi_transfernb(command3_c,result3_c[i],3)
            bcm2835_spi_transfernb(command4_c,result4_c[i],3)
            bcm2835_spi_transfernb(command5_c,result5_c[i],3)
            bcm2835_spi_transfernb(command6_c,result6_c[i],3)
            
        #[bcm2835_spi_transfernb(command_c,result_c[i],3) for i in times]

        endTime=time.time()
        samplerate=Times/(endTime-startTime)
        print('samplerate:{samplerate}'.format(samplerate=samplerate))
       
        #generate the array the smae size as Times in order to save the Data in it
        result=np.ndarray([Times,total_ch]).astype(np.uint16)
        for i in times:
            for ii in range(total_ch):
                result[i,ii] = (Data[i,ii,0] & 0x01) << 9
                result[i,ii] |= (Data[i,ii,1] & 0xFF) << 1
                result[i,ii] |= (Data[i,ii,2] & 0x80) >> 7

        return  {"data":result,"samplerate":samplerate}



    def read_adc_difference(self, differential):
       
        assert 0 <= differential <= 7, 'Differential number must be a value of 0-7!'
        # Build a difference channel read command.
        command = 0b10 << 6                  # Start bit, differential read
        command |= (differential & 0x07) << 3  # Channel number (in 3 bits)
        # Note the bottom 3 bits of command are 0, this is to account for the
        # extra clock to do the conversion, and the low null bit returned at
        # the start of the response.
        resp = self._spi.xfer2([command, 0x0, 0x0])
        # Parse out the 10 bits of response data and return it.
        result = (resp[0] & 0x01) << 9
        result |= (resp[1] & 0xFF) << 1
        result |= (resp[2] & 0x80) >> 7

        return result & 0x3FF
