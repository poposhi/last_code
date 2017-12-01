#-*- coding: UTF-8 -*-
import socket,struct,os,threading,time
host='192.168.43.62'
port=12308
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #定义socket类型
s.bind((host,port)) #绑定需要监听的Ip和端口号，tuple格式
s.listen(1)

 
def conn_thread(connection,address):   #傳送的內容 與地址
  while True:
    try:
      connection.settimeout(600) #設定傳輸時間，假如超過就跳到except
      fileinfo_size=struct.calcsize('!128sl') #檔案的type要預先設定
      buf = connection.recv(fileinfo_size) #第一次先接收檔案的大小 格式 (filename,filesize)
      if buf: #如果不加这个if，第一个文件传输完成后会自动走到下一句
        filename,filesize =struct.unpack('!128sl',buf)  #把buf解壓 解壓出兩個??(filename,filesize)
            #filename是 byte like object 要轉成str
        
        filename_f = filename.strip(bytes('\00' , 'utf-8' ))
        #print('filename_f byte is '+repr(filename_f) )
        filename_f = str(filename_f.strip(bytes('\'' , 'utf-8' )))
        filename_f = filename_f.strip('b\'')#把前面的'砍掉
        print('先接收檔案格式  檔名 : '+filename_f)
        #filepath =os.getcwd()+'\receive'
        filenewname = os.path.join(str(r'C:\Users\IDEA\Desktop\pi\ftp-sync\0804_total\synccc\test_en_for_tcp') ,('new_'+ filename_f))
        #print ('file new name is')# %s, filesize is %s' %filenewname,%filesize)，str(r'C:\Users\IDEA\Desktop\pi\python\tcp\receive')
        recvd_size = 0 #定义接收了的文件大小
		#知道要接收的檔案大小後，並設定好新的名字
        file = open(filenewname,'wb')
        print ('開始接收檔案')
	#開始接收
        while not recvd_size == filesize: #大小不同
          if filesize - recvd_size > 1024: #假如還很多還沒收就接收1024
            rdata = connection.recv(1024) #沒地方釋放?好像又不用清空data了
            recvd_size += len(rdata)
          else: #最後收剩下的部分
            rdata = connection.recv(filesize - recvd_size) 
            recvd_size = filesize
          file.write(rdata)
        file.close()
        print ('接收完畢')  
        break
        #connection.close()
    except socket.timeout:
        print("連線超時")
        connection.close()
    return
	  
while True:
    print('開始等待')
    connection,address=s.accept()
    print('Connected by ',address)
	  #thread = threading.Thread(target=conn_thread,args=(connection,address)) #使用threading也可以
	  #thread.start()
    t = threading.Thread(target=conn_thread,args = (connection,address) )
    #開始
    t.start()
    time.sleep(1)
    print('往下一輪while')#while 沒有中斷
s.close()