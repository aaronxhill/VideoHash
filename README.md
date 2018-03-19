## Overview

This is a web frontend which uploads an mp4 and create hashes of every frame.  Hashes will be written to a blockchain backend and, (given enough space) to the file metadata.

## Setup

To start the server do the following:
```
git clone http://github.com/wolfm2/VideoHash
cd VideoHash/server/
./start.sh  (press return again to exit server)
```
Note:
Make sure the blockchain servers and transaction processors are running.
```
sudo systemctl start sawtooth-validator
sudo systemctl start sawtooth-rest-api
sudo systemctl start sawtooth-intkey-tp-python
sudo systemctl start sawtooth-settings-tp
```

## Usage

Each uploaded video will get a reference key number.  Use this number to reference this video in the future.

  Intkey is a transaction processor client which stores key value pairs in the blockchain.  Each hash will be stored by the client separately in the form reference#.frame.  If your video reference was "25736", the name associated with the third hash value would be "25736.2" and could be retrieved by starting a bash session and typing:

```
intkey show 25736.2
```

See intkey for other options.

  When a video is loaded, you can play and download the video from within the inline viewer.  Check the "Output" section to review the ffmpeg output (including metadata), and blockchain ReST addresses for the hash entry transactions.
  
  Lastly, If you want to compare this video to another, enter the number of the other (previously uploaded) video into the "Video Reference Number" form and hit submit.  Assuming each video has the same number of frames, the foreign video's hashes will be retrieved from the blockchain and any differences highlighted.

