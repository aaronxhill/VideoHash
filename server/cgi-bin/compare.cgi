#!/usr/bin/env python3

"Compares video frame hashes against those in a blockchain."

import sys
import getopt
import os

print ("Content-type: text/html\n\n")

from urllib.parse import parse_qs

formVars = parse_qs (os.getenv('QUERY_STRING'))

if 'v0' not in formVars:
  print('Go back to the previous page and type in a reference number to compare.')
  exit(0)
  
if not formVars['v0'][0].isdigit():
  print('Go back to the previous page and type in a reference number to compare.')
  exit(0)  
  
# print(formVars)

cmpFr = formVars['path'][0]
cmpTo = formVars['v0'][0] # blockchain cookie # to compare to

try:
   opts, args = getopt.getopt(sys.argv[1:],"hc:")
except getopt.GetoptError:
   print ('compare.py -c <cookie>')
   sys.exit(2)

for opt, arg in opts:
   if opt == '-h':
       print ('compare.py -c <cookie>')
       sys.exit()
   elif opt in ("-c"):
       cmpTo = arg
       
#f = open('../{}/data.json'.format(cmpFr), 'r')
#lhashes = f.read().split('\n') # local hashes

import json
with open('../{}/data.json'.format(cmpFr)) as f:
    json_data = json.load(f)

lhashes = json_data['hashes']

#import subprocess
#subprocess.check_output(["ls", "-l", "/dev/null"])
fhashes = [  #hard coding for now
'3009043928',
'3009043928',
'3009043928',
'3009043927',
'3009043928',
'3009043928',
'3009043928',
'3009043928',
'3009043928',
'3009043928',
'3009043928',
'3009043928',
'3009043928',
'3009043928',
'3009043928',
'3009043928',
'3009043928',
'3009043928',
'3009043928',
'2409110966',
'4053183407',
'2544822133',
'0246095977',
'1790115166',
'2652776294',
'0369940768',
'1009171709',
'1231654161',
'1866152371',
'4280962192',
'0742550864',
'3838267001',
'2437550984',
'3500389059',
'3141623961',
'2998525548',
'1890626438',
'1555467454',
'2373719633',
'0426918669',
'1635148543',
'3891120316',
'3268503622',
'3631634328',
'3563508334',
'3124308690',
'1748268765'
]

# get rid of empty strings
lhashes = [x for x in lhashes if x]
fhashes = [x for x in fhashes if x]

for i in range(0, len(lhashes)-1):
  print("intkey show {}.{}".format(cmpTo, i))
  
if not len(lhashes) == len(fhashes):
  print('<center><h2>The videos have different numbers of frames!<br>')
  print('Local Hashes: {}, Foreign Hashes:{}</h2></center>'.format(len(lhashes), len(fhashes)))
  exit(0)
  
print('<center><h2>Comparing local video and blockchain hashes<h2>')
print('<table style="width:60%">')
print('<tr><th>Local</th><th>Foreign</th></tr>')
for i in range(0, len(lhashes)):
  color = 'style="background-color: crimson;"'
  if int(lhashes[i], 16) == int(fhashes[i]):
    color = 'style="background-color: lightgreen;"'
  print('<tr><td {0}>{1}</td><td {0}>{2}</td></tr>'.format(color, str(int(lhashes[i], 16)), fhashes[i]))
print('</table></center>')

