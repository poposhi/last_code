import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
matplotlib.use("Pdf")
import time
import os
import sys

#np.savez('array1.npz', data = data ,samplerate = rate,data_han= data_han)
l = np.load('new_2017_07_05_09_20_42.npz')

rate  =  l['samplerate']   #sample rate
print ('samplerate: ' + str(rate) )
data =l['data']
data_han =l['data_han']





#pic set
fig, (ax0, ax1) = plt.subplots(nrows=2 ,figsize=(12,8 ))
ax0.plot(range(100), data[:100]*5/1024)
ax0.set_ylabel('voltage(V)')
ax0.set_xlabel('tissme(n)')
n=data.shape[0]

#fft
p = np.abs(np.fft.fft(data))/n
f = np.linspace(0, rate/2, len(p))
freqs = np.fft.fftfreq(data.size, 1/rate)

#fft of han
p_han = np.abs(np.fft.fft(data_han))/n
print ('fft done')

#set the fft result to pic
idx = np.argsort(freqs)
idx2=idx[int(idx.shape[0]/2):] #int (idx.shape[0]/2+800) ]
ax1.set_xlabel("Frequence(Hz)")
ax1.set_ylabel("Amplitude")
ax1.set_title('Samplerate: {}   N: {}  '.format(rate,n), fontsize=16)
ax1.bar(freqs[idx2], p[idx2])
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.show()
'''
#save the pic
filename=time.strftime("%Y%m%d_%H%M%S",time.localtime())
dirPath=os.path.dirname(os.path.abspath(sys.argv[0]))
filePath=os.path.join(dirPath,filename+".jpg")
plt.savefig(filePath)
print("file: {}".format(filePath))

#han_pic
fig, (ax0,ax1) = plt.subplots(nrows=2 ,figsize=(12,8 ))
ax0.plot(range(100), data_han[:100]*5/1024)
ax0.set_ylabel('voltage(V)_han')
ax0.set_xlabel('tissme(n)')
ax1.set_title('Samplerate: {}   N: {}  '.format(rate,n), fontsize=16)

idx = np.argsort(freqs)
idx2=idx[int(idx.shape[0]/2):] #int (idx.shape[0]/2+800) ]
ax1.set_xlabel("Frequence(Hz)")
ax1.set_ylabel("Amplitude")
ax1.set_title('Samplerate: {}   N: {}  '.format(rate,n), fontsize=16)
ax1.bar(freqs[idx2], p_han[idx2])
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

filename=time.strftime("%Y%m%d_%H%M%S_wave_han",time.localtime())
dirPath=os.path.dirname(os.path.abspath(sys.argv[0]))
filePath=os.path.join(dirPath,filename+".jpg")
plt.savefig(filePath)
print("file: {}".format(filePath))
'''
