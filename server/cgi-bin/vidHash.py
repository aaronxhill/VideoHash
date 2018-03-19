#!/usr/bin/env python3

'''Embeds hashes of first 60 MP4 frames in metadata and loads them in a blockchain.'''

import sys
import getopt
# import pylab
# import imageio

fileIn = ''
fileOut = ''
cookie = '' # randomly assigned txn #

try:
   opts, args = getopt.getopt(sys.argv[1:],"hi:o:c:")
except getopt.GetoptError:
   print ('test.py -i <inputfile>')
   sys.exit(2)

for opt, arg in opts:
   if opt == '-h':
       print ('test.py -i <inputfile>')
       sys.exit()
   elif opt in ("-i"):
       fileIn = arg
   elif opt in ("-o"):
       fileOut = arg
   elif opt in ("-c"):
       cookie = arg

#print ("Loading: " + fileIn)

import cv2
import numpy as np
import hashlib
import os

framesForTwoSec = 60
hashes = ""

cap = cv2.VideoCapture(fileIn)
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

buf = np.empty((1, frameHeight, frameWidth, 3), np.dtype('uint8')) # space for one frame

fc = 0
ret = True

#file = open('hashes.out','w') 
jDict = {'hashes':[]}

while (fc < frameCount and fc < 60 and ret):
    ret, buf[0] = cap.read()
    #hash32 = int(hashlib.sha224(buf[0]).hexdigest(), 16)&(2**32)-1 # bottom 32 dec bits
    hash32 = hashlib.sha224(buf[0]).hexdigest()[-8:] # bottom 32 hex bits
    #print (hash32)
    jDict['hashes'].append(str(hash32))
    hashes += hash32 + "-"
    #file.write (str(hash32).zfill(10) + '\n') # write hash
    fc += 1
    
   
cap.release()
print ("Total Frames: " + str(fc))

import json
with open(cookie + '/data.json', 'w') as outfile:
  json.dump(jDict, outfile) 
  
hashes = hashes[0:-1] # rid of last char

#METADATA https://wiki.multimedia.cx/index.php/FFmpeg_Metadata#QuickTime.2FMOV.2FMP4.2FM4A.2Fet_al.
os.system ("ffmpeg -y -i '" + fileIn + "'  -metadata title='{}' -metadata synopsis='{}' -metadata description='{}' -metadata comment='{}' '".format(cookie, hashes[0:255], hashes[255:510], hashes[510:]) + fileOut + "' 2> {}/convert.txt".format(cookie) )

# from intkey code https://github.com/hyperledger/sawtooth-core/blob/master/sdk/examples/intkey_python/sawtooth_intkey/processor/handler.py
# MAX_VALUE = 4294967295
# MAX_NAME_LENGTH = 20

step = 8
for num, h in enumerate(hashes.split('-')):
  for i in range(0, len(h), step):
    buf = h[i:i+step]
    os.system ('intkey set {}.{} {} --keyfile /home/ubuntu/.sawtooth/keys/sawtooth.priv'.format(os.path.basename(cookie), num , int(buf, 16)))
    # print('intkey set {}.{} {} --keyfile .sawtooth/keys/sawtooth.priv'.format(cookie, "%0.2d"%num + str(int(i/step)) , int(buf, 16))) # if we move to > 32 bit keys

## TO DISPLAY
# cv2.namedWindow('frame 10')
# cv2.imshow('frame 10', buf[9])
# cv2.waitKey(0)
