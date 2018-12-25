import json
import socket
import struct
import time
import os

def send_request(sock,data):
    request = bytes(data, encoding = "utf8")
    length_prefix = struct.pack('I',len(request))
    sock.sendall(length_prefix)
    sock.sendall(request)



def rpc(sock,in_,params):
    request  = json.dumps({'in':in_,'params':params})
    send_request(sock,request)


    length = sock.recv(4)
    length, = struct.unpack('I',length)
    body = sock.recv(length)
    print(body)
    response = json.loads(body)
    print('response for func %s:%s' %(response['out'],response['result']) )

    # lenr = sock.recv(4)
    # lenr,= struct.unpack('I',lenr)
    # body = sock.recv(lenr)
    # response  =json.loads(body)
    
    # print(response)
    #return response['out'],response['result']


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
l=0
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,l)
s.connect(('127.0.0.1',6666))
for i in range(10):
    rpc(s,'ping',i)
    #print(result,response)
    print(i)
    time.sleep(1)

s.close()
