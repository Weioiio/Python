# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 04:21:48 2019

@author: hihih
"""
import os
import sha2
import time
from sha2 import *



tStart = time.time()

filename = input('Plz input your filename:')
filesize = os.path.getsize(filename)

#print(filesize)
f = open(filename, 'rb')

f224 = open('sha224.txt','w')
f256 = open('sha256.txt','w')
f384 = open('sha384.txt','w')
f512 = open('sha512.txt','w')

b = f.read()
f.close()
SHA = sha224.SHA224(b).hexdigest()
f224.write(SHA)
print('SHA224 Ciphertext :'+SHA)
SHA = sha256.SHA256(b).hexdigest()
f256.write(SHA)
print('SHA256 Ciphertext :'+SHA)
SHA = sha384.SHA384(b).hexdigest()
f384.write(SHA)
print('SHA384 Ciphertext :'+SHA)
SHA = sha512.SHA512(b).hexdigest()
f512.write(SHA)
print('SHA512 Ciphertext :'+SHA)

tEnd = time.time()
costtime = tEnd - tStart
bs = filesize/costtime
print('效能分析 : ' , bs ,  '(bytes/second)')

f224.close()
f256.close()
f384.close()
f512.close()



