#!/bin/bash

echo Starting Server...

IP=`ifconfig eth0 2>/dev/null|awk '/inet addr:/ {print $2}'|sed 's/addr://'`
echo Server started.  Proceed to http://$IP:8000/

./thttpd -p 8000 -h localhost -c 'cgi-bin/*.cgi'
# echo ./thttpd -p 8000 -h $IP -c 'cgi-bin/*.cgi'
./thttpd -p 8000 -h $IP -c 'cgi-bin/*.cgi'

read -p "Press enter to kill server"
killall thttpd


