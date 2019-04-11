# _*_ coding=utf-8 _*_
import socket
import json ,os

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #数据流
sock.connect(("127.0.0.1",9527))

while True:
    cmd = input(">>>:").strip()
    #cmd = raw_input()
    if not cmd : continue
    sock.send(cmd.encode("utf-8"))
    msg_header = sock.recv(300) #接收信息头
    print(msg_header)

    header = json.loads(msg_header.decode("utf-8"))  #反序列化取出文件的字典形式信息
    if header.get("error"):
        print(header.get("error"))
    else:
        #filename = header['filename']    #提取字典的值
        filename = "./receive.mp4"
        file_size = header['size']
        f = open(filename,"wb")
        received_size = 0

        while received_size < file_size :        #切片传输 一次接收8192 字节
            if file_size - received_size < 8192:#last time    #最后一次传输不足 8192 则计算剩余的大小接收 
                data = sock.recv(file_size - received_size)
            else:
                data = sock.recv(8192)

            received_size += len(data)    #已接收的文件大小 自增
            f.write(data)   #写入文件
            print("recv",received_size,file_size)   #显示 文件的接收过程 因为调用屏幕显示 会减慢传输速度
        else:
            print("file receive done....",filename,file_size)   #传输完毕打印完成
            f.close()   #关闭文件


sock.close()