#-*- coding: UTF-8 -*-
import sys,os
import spidev
import time,datetime
import socket,struct
from adxl345_lib import ADXL345
import numpy as np 

ADXL_CS  = 25
adxl_times = 10000
adxl_samplerate =0.0




adxl345 = ADXL345(ADXL_CS)
print ("Device ID = 0x%x" % (adxl345.GetID()) )
adxl345.startup( [0b1111],[0b00001011] ) #(speed,range reg)

axis_offset = adxl345.GetOffsetsFromCalibration() #只是拿值
data =np.zeros([3,adxl_times ]) #zeros 預設是float [0~adxl_times] *3
ii =range(adxl_times) #0~adxl_times
#delay_time = 1/300
startTime = time.time()
for i in ii:
	a_data= adxl345.GetMeasures(axis_offset['x'], axis_offset['y'], axis_offset['z'])
	data[0][i]=a_data['x']
	data[1][i]=a_data['y']
	data[2][i]=a_data['z']
	#time.sleep(delay_time)
endTime=time.time()
print('startTime:  %.4f   endTime: %.4f ' %(startTime,endTime))
adxl_samplerate=adxl_times/(endTime-startTime)
print('adxl_samplerate : %.5f'%(adxl_samplerate) )
adxl345.Remove()


#傳送檔案用的
#save_array  data格式 [0~adxl_times] *3 rate >int
np.savez('adxl345.npz', data = data ,adxl_samplerate =adxl_samplerate)
#rename
dt =str(datetime.datetime.now())
name = time.strftime("%Y_%m_%d_%H_%M_%S_adxl.npz")
os.rename('adxl345.npz', name)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('192.168.43.62',12308))


'''我覺得路徑應該要可以輸出列表再輸入的'''
''' 或者直接用檔案路徑+name '''
filepath =os.getcwd()+'/'+name #(r'/home/pi/test/ftp-sync/tcp/'+name) #input('Please Enter chars:\r\n')		#輸入檔案路境
        #再rpi要用絕對路徑
if os.path.isfile(filepath):							#檔案存在
    print('into if begin send file info ')        
    fileinfo_size=struct.calcsize('!128si') #定义打包规则
	#定义文件头信息，包含文件名和文件大小
    fhead = struct.pack('!128si',bytes(os.path.basename(filepath) , 'utf-8' ),os.stat(filepath).st_size)
    #fhead = struct.pack('!128si',os.path.basename(filepath) ,os.stat(filepath).st_size)
	#把路徑跟大小打包進去 fhead
    s.sendall(fhead) 
    print ('client filepath: ',filepath)
	# with open(filepath,'rb') as fo: 这样发送文件有问题，发送完成后还会发一些东西过去
fo = open(filepath,'rb') #讀取檔案
while True:
#print('into while2')
    filedata = fo.read(1024)
    if not filedata:
        break
    s.send(filedata)
fo.close()
print ('send over...')
s.close()

