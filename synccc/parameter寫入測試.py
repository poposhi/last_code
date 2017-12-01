#!/usr/bin/python
# -*- coding: utf-8 -*-

# read txt for while loop
#data type
import sys



result=[]

with open('parameter.txt','r') as f: 
		for line in f: 
			result.append(list(map(float,line.split(',')))) 
		print (result) 


print (result[0][0])  #mcp
print (result[1][0])  #adxl
print (result[2][0])  #reload
f= open('parameter.txt','w' )
f.write(str(result[0][0])+'\n')  #把我讀到得東西放進去
#f.write('\n')
f.write(str(result[1][0])+'\n')  
f.write('0 \n')
f.write('last write by write test \n')
f.close()
