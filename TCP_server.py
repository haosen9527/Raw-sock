# _*_ coding=utf-8 _*_
import socket
import os,json
import time

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(("127.0.0.1",9527))
sock.listen(1)

def pack_msg_header(header,header_size):    #文件信息字典处理函数   接收字典和字典指定大小参数
    bytes_header = bytes(json.dumps(header) ,encoding="utf-8")     #转换文件信息字典为 bytes

    if len(bytes_header ) < header_size :#需要补充0       # 计算下变成字节的字典长度   并与指定的字典大小做比较,如果字典小于指定数值
        header['fill'].zfill( header_size - len(bytes_header) )   #向 字典中的 fill 元素 补充对应的零
        bytes_header = bytes(json.dumps(header), encoding="utf-8")  #重新 转换 更改后的字典
    return bytes_header   #返回更改后的字典

while True:

    conn,addr = sock.accept() #等待、阻塞
    print("got a new customer",conn,addr)

    while True:
        raw_cmd = conn.recv(1024) # get test.log      #接收用户输入的指令
        cmd,filename = raw_cmd.decode("utf-8").split(" ")   #切分用户输入的指令 并赋值cmd 和 filename
        print("raw_cmd is ",raw_cmd)
        print("cmd is ",cmd)
        print("filename is ",filename)
        if cmd == "get":    #如果cmd 为 get
            msg_header = {"fill": ''}   #创建字典,并初始创建一个fill元素用于控制头文件大小
            if os.path.isfile(filename):      #判断文件是否存在

                msg_header["size"] =  os.path.getsize(filename)     #获取文件大小并添加到字典中
                msg_header["filename"] =  filename            #获取文件名并添加到字典中
                msg_header["ctime"] =  os.stat(filename).st_ctime
                bytes_header = pack_msg_header(msg_header,300)     #调用函数并接收返回值

                conn.send(bytes_header)   #发送给客户端  头部信息

                f = open(filename,"rb")   #以字节模式打开 客户端请求的文件
                for line in f:     #循环取出文件内容并发送
                    conn.send(line)
                    time.sleep(0.001)

                else:       #如果文件发送完毕 则  打印信息
                    print("file send done....")
                f.close()     #操作文件完毕关闭文件
            else:      # <============================:如果文件判断不存在则发送相应的信息给客户端
                msg_header['error'] = "file %s on server does not exist " % filename
                bytes_header = pack_msg_header(msg_header, 300)
                conn.send(bytes_header)


sock.close() #关闭端口和服务