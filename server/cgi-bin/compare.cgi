#!/usr/bin/env python3

"Compares video frame hashes against those in a blockchain."

import sys
import getopt
import os
import subprocess

print ("Content-type: text/html\n\n")

from urllib.parse import parse_qs

formVars = parse_qs (os.getenv('QUERY_STRING'))

if 'v0' not in formVars:
  print('Go back to the previous page and type in a reference number to compare.')
  exit(0)
  
if not formVars['v0'][0].isdigit():
  print('Go back to the previous page and type in a reference number to compare.')
  exit(0)  
  
print(formVars)
exit(9)

cmpFr = formVars['path'][0]
cmpTo = formVars['v0'][0] # blockchain cookie # to compare to
       
#f = open('../{}/data.json'.format(cmpFr), 'r')
#lhashes = f.read().split('\n') # local hashes

import json
with open('../{}/data.json'.format(cmpFr)) as f:
    json_data = json.load(f)

lhashes = json_data['hashes']

status = 0
idx = 0
fhashes = []

while idx <= 60:
  command = "intkey show 25737.{}".format(idx)  # the shell command
  process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  output, error = process.communicate()
  status = process.returncode
  if status == 0:
    fhashes.append(output.split()[1])
  else:
    break
  idx += 1

# get rid of empty strings
lhashes = [x for x in lhashes if x]
fhashes = [x for x in fhashes if x]

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

