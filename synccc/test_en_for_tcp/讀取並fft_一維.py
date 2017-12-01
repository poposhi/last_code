#-*- coding: UTF-8 -*-
import numpy as np
import time
import os
import sys
import matplotlib
# solve the bug for myself 
# It maybe not necessary 
#matplotlib.use("Pdf")
import matplotlib.pyplot as plt

def average_fft ( x , fft_size ): #輸入矩陣，與一次要分析的大小
	    n = len ( x ) // fft_size * fft_size 
	    tmp = x [: n ] . reshape ( - 1 , fft_size ) #  把n切個乘很多小段
	    #tmp *= signal . hann ( fft_size , sym = 0 )  #乘上窗函數，把一個很多段的array乘上hann，代表每一段都乘上
	    xf = np . abs ( np . fft . rfft ( tmp ) / fft_size ) #傅立葉
	    avgf = np . average ( xf , axis = 0 ) #二维数组纵向求和，每一段的第幾個數求平均
	    return 20 * np . log10 ( avgf )  #傳回大小
def average(x , size):
    n = len ( x ) // fft_size * fft_size 
    tem = x [: n ] . reshape ( - 1 , fft_size ) #  把n切個乘很多小段
    #tem = x  .reshape(-1,size)
    #tem = tem * signal.hann(size,sym=0)
    xf = np.abs(np.fft.rfft(tem)) / size
    avgf = np.average(xf,axis=0)
    return 20*np.log10(avgf)
while 1:
    print (os.listdir(os.getcwd()))
    #name = input("whitch one ? ")
    name = 'new_2017_07_12_05_20_08.npz'
    filepath =os.getcwd()+'/'+name
    if (os.path.isfile(filepath)):
        break
result = np.load(filepath)

#l = np.load('new_2017_07_11_07_45_53.npz')

data = result['data']
#n=data.shape[0] 
data= data[:,0]
samplerate = l['samplerate']
rate =int(samplerate)
print ('samplerate is '+str(samplerate))
xxx= len(data)

#fft
p = np.abs(np.fft.fft(data))/n
f = np.linspace(0, rate/2, len(p))
#p =20*np.log10(p) #
freqs = np.fft.fftfreq(data.size, 1/rate)

#pic set
fig, (ax0, ax1) = plt.subplots(nrows=2 ,figsize=(12,8 ))
ax0.plot(range(100), data[:100]*5/1024)
ax0.set_ylabel('voltage(V)')
ax0.set_xlabel('tissme(n)')
n=data.shape[0]
print(n)

#set the fft result to pic
idx = np.argsort(freqs)
idx2=idx[int((idx.shape[0]/2)+1):] #int (idx.shape[0]/2+800) ]
ax1.set_xlabel("Frequence(Hz)")
ax1.set_ylabel("Amplitude")
ax1.set_title('Samplerate: {}   N: {}  '.format(rate,n), fontsize=16)
#ax1.ylim(0,1000)
#ax1.yscale('log')
ax1.plot(freqs[idx2], p[idx2]) #bar畫很慢
#plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.show()
'''
#fft
fft_size =4096
p = average(data[:,3],fft_size)
print(p)
#p = np.abs(np.fft.fft(data[;100]))/n
#f = np.linspace(0, rate/2, len(p))
#freqs = np.fft.fftfreq(data.size, 1/rate)
#idx = np.argsort(freqs)
#idx2=idx[int(idx.shape[0]/2):] #int (idx.shape[0]/2+800) ]
freqs  =  np . linspace ( 0 ,  rate / 2 ,  fft_size / 2 + 1 )
#--------------------
plt.figure(figsize = ( 8 , 4 ))
#plt.subplot(311)
plt.plot(freqs, p)
plt.show()
'''