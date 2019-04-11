#!/usr/bin/env python3.6
# coding: utf-8
import socket
import struct
import binascii

#   TCP
def parse_tcp(packet):
    tcp_header_b = packet[34:54]
    tcp_header_s = struct.unpack("!2s2s4s4s1s1s2s2s2s",tcp_header_b)
    print("tcp_header_s is " , tcp_header_s)
    print("tcp source port is " , binascii.hexlify(tcp_header_s[0][0:2]))
    print("tcp destination  port is " , binascii.hexlify(tcp_header_s[1][0:2]))
    print("tcp sequence No is " , binascii.hexlify(tcp_header_s[2][0:4]))
    print("tcp confirm No is " , binascii.hexlify(tcp_header_s[3][0:4]))
    len_tcp_header_b=binascii.hexlify(tcp_header_s[4][0:1])
    len_tcp_header_str=str(len_tcp_header_b,encoding='utf-8')
    len_tcp_header=int(len_tcp_header_str[0],16)*4
    print("tcp header length is " , len_tcp_header)
    tcp_data=packet[54+len_tcp_header-20:]
    print('tcp_data=',tcp_data)

#   UDP
def parse_udp(packet):
    udp_header_b = packet[34:42]
    udp_header_s = struct.unpack("!2s2s2s2s",udp_header_b)
    print("udp_header_s is " , udp_header_s)
    print("udp source port is " , binascii.hexlify(udp_header_s[0][0:2]))
    print("udp destination  port is " , binascii.hexlify(udp_header_s[1][0:2]))
    print("udp data length is " , binascii.hexlify(udp_header_s[2][0:2]))
    udp_data=packet[42:]
    print('udp_data=',udp_data)

#   ICMP
def parse_icmp(packet):
    icmp_header_b = packet[34:42]
    icmp_header_s = struct.unpack("!1s1s2s4s",icmp_header_b)
    print("icmp_header_s is " , icmp_header_s)
    print("ICMP type is " , binascii.hexlify(icmp_header_s[0][0:1]))
    print("ICMP code is " , binascii.hexlify(icmp_header_s[1][0:1]))
    print("ICMP checksum is" , binascii.hexlify(icmp_header_s[2][0:2]))
    print("ICMP option is" , binascii.hexlify(icmp_header_s[3][0:4]))
    icmp_data=packet[42:]
    print('ICMP_data=',icmp_data)

s = socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))
for xx in range(1000):
    data = s.recvfrom(65535)
    print('\nFrame number is %d:' % xx)
#    print('len=',len(data),'data=',data)
    packet=data[0]
    print('len=',len(packet),'packet=',packet)
#   link
    frame_header_b = packet[0:14]
    frame_header_s = struct.unpack("!6s6s2s",frame_header_b)
    source_MAC_Addr=binascii.hexlify(frame_header_s[0])
    dest_MAC_Addr=binascii.hexlify(frame_header_s[1])
    proto_type=binascii.hexlify(frame_header_s[2])
    print('Souce MAC address is ',source_MAC_Addr)
    print('Destination MAC address is ',dest_MAC_Addr)
    print('Protocol type is ',proto_type)
#   IP
    ip_header_b = packet[14:34]
    ip_header_s = struct.unpack("!12s4s4s",ip_header_b)
    print("ip_header_s is " , ip_header_s)
    print("IP packet ver & head length is " , binascii.hexlify(ip_header_s[0][0:1]))
    print("IP packet length is " , binascii.hexlify(ip_header_s[0][2:4]))
    ip_protocol=str(binascii.hexlify(ip_header_s[0][9:10]),encoding='utf-8')
    print("Protocol is " , ip_protocol)
    print("Source IP address is " + socket.inet_ntoa(ip_header_s[1]))
    print("Destination IP address is " + socket.inet_ntoa(ip_header_s[2]))
    if ip_protocol=='06':
        parse_tcp(packet)
    elif ip_protocol=='11':
        parse_udp(packet)
    elif ip_protocol=='01':
        parse_icmp(packet)
    if ip_protocol == '11':
        parse_udp(packet)
    else:
        print('it is not TCP, UDP, ICMP, IGMP, unknow protocol!')

s.close()