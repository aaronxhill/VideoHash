#!/usr/bin/env python3

import os
import sys
import random

#vref = str(random.randrange(1,2**16))
vref = sys.argv[1]
vdref = 'vid/' + vref
clen = os.getenv('CONTENT_LENGTH')
ip = os.getenv('REMOTE_ADDR')
port = os.getenv('SERVER_PORT')

path = 'PATH="/home/ich/anaconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/android-sdk-linux/tools:/usr/local/android-sdk-linux/platform-tools:$PATH"'

cmds = [
'mkdir -p {0}'.format(vdref),
'dd of={0}/formdata bs={1} count=1'.format(vdref, clen), # needs unbuffered copy
'tail -n +5 {0}/formdata > {0}/vidPre0.mp4'.format(vdref),   # TODO cut extra off end too
'{1};./cgi-bin/vidHash.py -c {0} -i {0}/vidPre0.mp4 -o {0}/vid.mp4 > {0}/hashes.txt'.format(vdref, path),
'rm -f {0}/formdata {0}/vidPre0.mp4'.format(vdref)
]

# echo 'Your video with hashes is <a href='{0}'> here </a>.
header = '''
<pre>
The reference for this video is: <b>{0}</b>
Access this video again by appending it to the url.  E.g.:  http://ip address:{2}/vid/{0}
'''.format(vref, ip, port)

footer= '''
</pre>
<br>
<video controls>
  <source src='../{0}/vid.mp4' type="video/mp4">
  Your browser does not support the video tag.
</video>
<br>
<br>
To download your video with hashes hit the download button in the viewer.

<br>
Files may be cleaned up after 24hrs.
<br>
<br>
Output: <a href='../{0}/convert.txt'> Processing Output </a>, <a href='../{0}/intkey.txt'> Blockchain Transaction </a>
<br>'
<br>
<b>Type the reference number of a second video to compare local hashes to those in the blockchain.</b>
<br>
<br>
<form action="compare.cgi" method="get">
   Video Reference Number: <input type="text" name="v0"><br>
   
   <input type="hidden" name="path" value="{0}">
   
  <input type="submit" value="Submit">
</form>
</BODY>
'''.format(vdref)

# print ("Content-type: text/html\n\n")
print(header)

# TODO python still having issues w unbuffered reading.  Blocks process.
#import shutil
#import sys

# with open('file') as f:
#with sys.stdin as f:
#f = sys.stdin
#while True:
#        buffer = f.buffer.read(1) # Returns *at most* 1024 bytes, maybe less
#        if buffer == '':
#            break

#pty.setraw(sys.stdin.fileno())
#with os.fdopen(sys.stdin.fileno(), 'rb') as input_file,\
#     open('{}/formdata'.format(vdref), 'wb') as output_file:
#    shutil.copyfileobj(input_file, output_file, int(clen))

#for c in cmds:
#  print(c)
#  print(os.system(c))
  
print(footer)  

exit (0)
