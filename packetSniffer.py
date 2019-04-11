# _*_ coding=utf-8 _*_

import socket
import struct
import binascii
import os

#UDP
def parse_udp(packet):
    udp_header_b = packet[34:42]
    udp_header_s = struct.unpack("!2s2s2s2s",udp_header_b)
    # print("udp_header_s is " , udp_header_s)
    # print("udp source port is " , binascii.hexlify(udp_header_s[0][0:2]))
    # print("udp destination  port is " , binascii.hexlify(udp_header_s[1][0:2]))
    # print("udp data length is " ,str(binascii.hexlify(udp_header_s[2][0:2]),encoding='utf-8'))
    udp_data_length =str(binascii.hexlify(udp_header_s[2][0:2]),encoding='utf-8')


    if ((int(udp_data_length,16))==1032 or (int(udp_data_length,16)) >= 800):
    	print(int(udp_data_length,16))
    	udp_data=packet[42:]
    	f = open(filename,"ab")
    	f.write(udp_data)
    	print('udp_data=',udp_data)

#   TCP
def parse_tcp(packet):
    tcp_header_b = packet[34:54]
    tcp_header_s = struct.unpack("!2s2s4s4s1s1s2s2s2s",tcp_header_b)
    len_tcp_header_b=binascii.hexlify(tcp_header_s[4][0:1])
    len_tcp_header_str=str(len_tcp_header_b,encoding='utf-8')
    len_tcp_header=int(len_tcp_header_str[0],16)*4
    print("tcp header length is " , len_tcp_header)
    print("tcp_header_s is " , tcp_header_s)
    print("tcp source port is " , binascii.hexlify(tcp_header_s[0][0:2]))
    print("tcp destination  port is " , binascii.hexlify(tcp_header_s[1][0:2]))
    print("tcp sequence No is " , binascii.hexlify(tcp_header_s[2][0:4]))
    print("tcp confirm No is " , binascii.hexlify(tcp_header_s[3][0:4]))
    tcp_data=packet[54+len_tcp_header-20:]
    print(len_tcp_header-20)
    tcp_port = str(binascii.hexlify(tcp_header_s[0][0:2]),encoding='utf-8')
    if int(tcp_port,16)==9527 and tcp_data!='' and tcp_data!='\n' and len_tcp_header-20==12:
    	if int(tcp_port,16)!=46784:
    		if tcp_data!=" " :
    			if tcp_data!="\n":
    				print('tcp_data=',tcp_data)
    				filename_tcp = "./data/Sniffer_data_TCP/TCP_result.mp4"
    				f_tcp = open(filename_tcp,"ab")
    				f_tcp.write(tcp_data)




filename = "./data/Sniffer_data/Sniffer_result.mp4"
if os.path.isfile(filename):
	os.remove(filename)
rawSocket = socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))
i=0

while True:
	print("-----------------------------",i)
	i=i+1
	data = rawSocket.recvfrom(65535)

	packet =data[0]
	# print('len=',len(packet),'packet=',packet)

	header_b = data[0][0:14]   #提取以太网帧头
	header_s = struct.unpack("!6s6s2s",header_b) #6字节目的mac地址，6字节源mac地址，2字节协议类型

	source_Mac_Addr =binascii.hexlify(header_s[0])
	dest_Mac_Addr = binascii.hexlify(header_s[1])
	proto_type = binascii.hexlify(header_s[2])
	#show
	# print('Souce MAC address is ',source_Mac_Addr)
	# print('Destination MAC address is ',dest_Mac_Addr)
	# print('Protocol type is ',proto_type)

	ip_header_b = data[0][14:34]#提取IP协议头，不包含option和padding字段。
	ip_header_s = struct.unpack("!12s4s4s",ip_header_b)
	# ！标示转换网络字节序，前12字节为版本、头部长度、服务类型、总长度、标志等其他选项，后面的两个四字节依次为源IP地址和目的IP地址。
	#show
	# print("ip_header_s is " , ip_header_s)
	# print("IP packet ver & head length is " , binascii.hexlify(ip_header_s[0][0:1]))
	# print("IP packet length is " , binascii.hexlify(ip_header_s[0][2:4]))

	ip_protocol=str(binascii.hexlify(ip_header_s[0][9:10]),encoding='utf-8')
	# print("Protocol is " , ip_protocol)
	# print("Source IP address is " + socket.inet_ntoa(ip_header_s[1]))
	# print("Destination IP address is " + socket.inet_ntoa(ip_header_s[2]))

	#check UDP 
	if ip_protocol=='11':
		parse_udp(packet)
	if ip_protocol=='06':
		parse_tcp(packet)
	else:
		print('it is not UDP TCP protocol!')

rawSocket.close()
# tcpHeader = data[0][34:54]
# tcp_hdr = struct.unpack("!HH16s",tcpHeader)

# print tcp_hdr