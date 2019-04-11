# _*_ coding=utf-8 _*_
import socket
import os
import stat
import struct
import time

#config
MAX_PACK_SIZE = 1024
DEST_IP = "127.0.0.1"
DEST_PORT = 9527

filename = raw_input("input filename")

filesize = os.stat(filename)[stat.ST_SIZE]

f = open(filename, "rb")

chList = []
for i in range(0, filesize):
    (ch,) = struct.unpack("B", f.read(1))
    chList.append(ch)

#UDP client
client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

packSize = 0
string = ""
args = []
for i in range(0, filesize):
    packSize = packSize + 1
    string = string + struct.pack("B", chList[i])
    if (MAX_PACK_SIZE == packSize or i == filesize - 1):
        client.sendto(string, (DEST_IP, DEST_PORT))
        packSize = 0
        string = ""
        time.sleep(0.002)
print("send done")
client.close()