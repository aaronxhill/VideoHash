#!/bin/bash

echo 'Content-type: text/html'
echo 
echo '<HTML><HEAD><TITLE>File Upload</TITLE></HEAD><BODY>'

cd ..
VREF=$RANDOM
VREF=25737
VDREF=vid/$VREF

mkdir -p $VDREF
dd of=$VDREF/formdata bs=$CONTENT_LENGTH count=1 iflag=fullblock  # needs unbuffered copy 
tail -n +5 $VDREF/formdata > $VDREF/vidPre0.mp4  # TODO cut extra off end too
PATH="/home/ubuntu/bin:/home/ubuntu/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:$PATH"
./cgi-bin/vidHash.py -c $VDREF -i $VDREF/vidPre0.mp4 -o $VDREF/vid.mp4 > $VDREF/intkey.txt
rm -f $VDREF/formdata $VDREF/vidPre0.mp4

cgi-bin/ulPost.cgi $VREF

echo '</BODY>'
