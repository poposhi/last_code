#-*- coding: UTF-8 -*-
''' 傳輸的也可以寫成一個物件，ADXL現在只有每一次量測的FUNC，可寫成一個物件'''
import sys,os
import spidev
import time,datetime
import socket,struct
from adxl345_lib import ADXL345
from new_BCMMCP3008 import MCP3008
import numpy as np 
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM) 
# GPIO 21 set up as an input, pulled down, connected to 3V3 on button press  
GPIO.setup(21, GPIO.IN)

print('dasedeqad')
def intrrupt():
	print('intrruptupt')
	sys.exit()
#adxl parameter
ADXL_CS  = 25
adxl_times = 1000
adxl_samplerate =0.0
#mcp
mcp_times=1000
SPI_PORT= 0#其實port要再read_adc_loop裡面調
SPI_DEVICE = 0
chnum=1  #ch1
#輸入cS腳 取樣次數 取樣頻率，只有腳位跟取樣次數有用，回傳壓縮檔(是FTP)
def adxl_func(ADXL_CS,adxl_times,adxl_samplerate):
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
	return
	#輸入取樣次數與通道，通道數沒用，用一行而已
def mcp_func(mcp_times,chnum):
	print('begin mcp')
	mcp = MCP3008()
	result=mcp.read_adc_loop(mcp_times)

	data=np.array(result["data"]) #translate to nparray
	#data [第幾次,第幾隻腳] plt.plot(range(100), data[:100,0]*5/1024)
	rate=result["samplerate"]

	#save_array
	np.savez('array1.npz', data = data ,samplerate = rate)
	''' data是一個二為矩陣不知道行不行'''
	#rename
	dt =str(datetime.datetime.now())
	name = time.strftime("%Y_%m_%d_%H_%M_%S_mcp.npz")
	os.rename('array1.npz', name)



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
	return
	



if __name__ == '__main__':
	#GPIO.add_event_detect(21, GPIO.RISING, callback=intrrupt(), bouncetime=2000) 
	#read and convert to float
	try:
		while True:
			result=[] 
			with open('parameter.txt','r') as f: 
				for line in f: 
					result.append(list(map(float,line.split(',')))) 
				print (result) 
			print ("mcp秒數: "+str(result[0][0]))  #mcp
			print ("adxl秒數: "+str(result[1][0]))  #adxl
			print ("要不要reload : "+str(result[2][0]))  #reload
			if result[2][0]==1:
				f= open('parameter.txt','w' )
				f.write(str(result[0][0])+'\n')  #把我讀到得東西放進去
				f.write(str(result[1][0])+'\n')  
				f.write('0 \n')
				f.write('148\n')			
				f.close()
			i=0
			try:
				while True:
					result=[]
					with open('parameter.txt','r') as f: 
						for line in f: 
							result.append(list(map(float,line.split(','))))
					if result[2][0]==1:
						break
					if i % result[0][0] ==0:
						print('do mcp 取樣間隔 is %s'%(i))
						mcp_func(mcp_times,chnum=1)
					if i % result[1][0] ==0:
						pass
						#adxl_func(ADXL_CS,adxl_times,adxl_samplerate)
					time.sleep(1)
					i = i+1
					

			except KeyboardInterrupt:
				print('etime:', datetime.datetime.now())
				sys.exit()
	except KeyboardInterrupt:
		print('etime:', datetime.datetime.now())				
	#adxl_func(ADXL_CS,adxl_times,adxl_samplerate)
	#mcp_func(mcp_times,chnum)
	