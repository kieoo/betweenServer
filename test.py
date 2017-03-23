# !/bin/env python
# !coding:utf-8
try:
    from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler, BaseRequestHandler
except:
    from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler, BaseRequestHandler
import sys
import socket
import struct

HOST = '127.0.0.1'
PORT = int(sys.argv[1])
TO_PORT = int(sys.argv[2])
CREAT_ADDR = (HOST, PORT)
TO_ADDR = (HOST, TO_PORT)


class MyClient:

    def __init__(self):
        self.s = socket.socket()

    def client_start(self):
        self.s.connect(TO_ADDR)
        return self.s.recv(1024)

    def client_send(self, send_cmd):
        try:
            self.s.sendall(send_cmd)
            response = self.s.recv(1024)
        except Exception as e:
            print(e)
            response = e
        print("receive from %r: %r" % (TO_ADDR, response))
        return response

    def client_close(self):
        self.s.close()


class MyRequestHandler(StreamRequestHandler):

    def handle(self):
        self.rbufsize = 1024
        while True:
            try:

                int_data = self.request.recv(1024)
                data = int_data.strip()
                print("receive from %r: %r" % (self.client_address, data))
                self.wfile.write(data.upper())
            except Exception as e:
                print(e)
                break


'''
class MyRequestHandler(BaseRequestHandler):

    my_c = MyClient

    def setup(self):
        print("%r connectting.......", self.client_address)
        helo_word = self.my_c.client_start()
        # helo_word = b'220 qa122.cn Anti-spam GT for Coremail System (demo-test1[20160627])\r\n'
        self.request.sendall(struct.pack('%ds' % len(helo_word), helo_word))

    def handle(self):
        tmp = b''
        while True:
            try:
                int_data = self.request.recv(1024)
                if not int_data:
                    break
                if len(int_data) <= 4:
                    tmp = struct.unpack('%ds' % len(int_data), int_data)[0]
                    print("receive from %r: %r" % (self.client_address, int_data.strip()))
                else:
                    data = str.encode(tmp) + int_data
                    print("receive from %r: %r" % (self.client_address, data.strip()))
                    self.request.sendall(self.my_c.client_send(data))
                    tmp = b''
            except Exception as e:
                print(e)
                break

    def finish(self):
        self.my_c.client_close()
        print("%r close!", self.client_address)

'''
class ThreadTCPServer(ThreadingMixIn, TCPServer):
    pass

if __name__ == '__main__':

    server = ThreadTCPServer(CREAT_ADDR, MyRequestHandler)
    server.serve_forever()