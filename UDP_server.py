# _*_ coding=utf-8 _*_
import socket
import os,json

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(("127.0.0.1",9527))
filename = "./data/server_client_data/server_test.mp4"
if os.path.isfile(filename):
	os.remove(filename)


while True:
	msg,addr = sock.recvfrom(65535)
	print('recv:',msg,addr)
	f = open(filename,"ab")
	data=msg
	f.write(data)

sock.close() #关闭端口和服务