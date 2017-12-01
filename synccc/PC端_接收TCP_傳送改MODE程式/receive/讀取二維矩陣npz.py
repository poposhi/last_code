import numpy as np
import matplotlib.pyplot as plt
import time
import os
import sys

while 1:   
    print (os.listdir(os.getcwd()))
    name = input("whitch one ? ")
    filepath =os.getcwd()+'/'+name
    if (os.path.isfile(filepath)):
        break
l = np.load(filepath)

#l = np.load('new_2017_07_11_07_45_53.npz')

data = l['data']
samplerate = l['samplerate']

print ('samplerate is '+str(samplerate))
#plt.plot(l['sample_time'],l['sample_sin'])

print(data[:,0])
print('sys.exit()')
sys.exit()
#畫出來
plt.figure()
plt.subplot(311)
plt.plot(range(100), data[:100,0]*5/1024)
plt.show()


plt.subplot(312)
plt.plot(range(100), data[:100,1]*5/1024)
plt.show()

plt.subplot(313)
plt.plot(range(100), data[:100,2]*5/1024)
plt.show()

plt.figure()
plt.subplot(311)
plt.plot(range(100), data[:100,3]*5/1024)
plt.show()


plt.subplot(312)
plt.plot(range(100), data[:100,4]*5/1024)
plt.show()

plt.subplot(313)
plt.plot(range(100), data[:100,5]*5/1024)
plt.show()
'''
#save the pic
filename=time.strftime("%Y%m%d_%H%M%S",time.localtime())
dirPath=os.path.dirname(os.path.abspath(sys.argv[0]))
filePath=os.path.join(dirPath,filename+".jpg")
plt.savefig(filePath)
print("file: {}".format(filePath))
'''