#!/usr/bin/env bash

#cvlc "udp://:8554" -Idummy --network-caching 4000 --sout '#transcode{vcodec=FLV1,acodec=mp3,samplerate=11025,threads=2,fps=25}:std{access=rtmp,mux=ffmpeg{mux=flv},dst=rtmp://a.rtmp.youtube.com/live2/fufy-gqa6-za53-3h4b'

YOUTUBE_URL="rtmp://a.rtmp.youtube.com/live2"
YOUTUBE_KEY="fufy-gqa6-za53-3h4b"
VBR="500k"
FPS="25"
QUAL="ultrafast"


ffmpeg -i 'udp://:8554' -fflags nobuffer -f:v mpegts -probesize 8192 \
    -vcodec libx264 -pix_fmt yuv420p -preset ${QUAL} -r ${FPS} -g $(($FPS * 2)) -b:v ${VBR} \
    -acodec libmp3lame -ar 11025 -b:a 16k -af "volume=0" -threads 6 -bufsize 3968k \
    -tune zerolatency -maxrate 1984k \
    -flags +global_header -f flv "$YOUTUBE_URL/$YOUTUBE_KEY"
