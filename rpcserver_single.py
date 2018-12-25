import json
import socket
import struct
import time
import threading


def handleConn(sock,addr,handlers,taskid):
    while True:
        len_prefix = sock.recv(4)
        if not len_prefix:
            print(addr,"bye")
            sock.close()
            break
        len_prefix, = struct.unpack('I',len_prefix)
        body = sock.recv(len_prefix)
        #print(body)
        request = json.loads(body)
        handlers[request['in']](sock,str(request['params'])+":"+str(taskid))
        #print(response)


def send_result(sock,out,params):
    response = json.dumps({'out':out,'result':params})
    response = bytes(response, encoding = "utf8")
    length_prefix = struct.pack('I',len(response))
    sock.sendall(length_prefix)
    sock.sendall(response)



def ping(sock,param):
    print('ping function...%s'%param)
    send_result(sock,'pong',param)


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,b'')
s.bind(('127.0.0.1',6666))
s.listen()

handlers={'ping':ping}



#handleConn(s1,addr,handlers)
taskcnt = 0
while True:
    s1 ,addr = s.accept()
    threading._start_new_thread(handleConn,(s1,addr,handlers,taskcnt))
    taskcnt+=1

s.close()
