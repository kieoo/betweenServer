# !/bin/env python
# !coding:utf-8

try:
    from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler, BaseRequestHandler
except:
    from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler, BaseRequestHandler
import sys
import socket
import struct
import time

HOST = '0.0.0.0'
PORT = int(sys.argv[1])
TO_PORT = int(sys.argv[2])
CREAT_ADDR = (HOST, PORT)
TO_ADDR = (HOST, TO_PORT)
SLOW_TIME = 1  # 1s


class MyClient:

    def __init__(self):
        self.s = socket.socket()

    def client_start(self):
        response = b''
        self.s.connect(TO_ADDR)
        response = self.s.recv(1024)
        # response = b'220 qa122.cn Anti-spam GT for Coremail System (demo-test1[20160627])\r\n'
        return response

    def client_send_recv(self, send_cmd):
        response = b''
        try:
            self.s.sendall(send_cmd)
            response = self.s.recv(1024)
            print("response from %r: %r" % (TO_ADDR, response))
        except Exception as e:
            print(e)
            print("%r closed a connect!" % (TO_ADDR,))
            response = e
        return response

    def client_send(self, send_cmd):
        try:
            self.s.sendall(send_cmd)
        except Exception as e:
            print(e)
            print("%r closed a connect!" % (TO_ADDR,))

    def client_close(self):
        # self.s.shutdown(2)
        self.s.close()
        print("closed a connect %r" % (TO_ADDR,))

'''
class MyRequestHandler(StreamRequestHandler):

    def handle(self):
        self.rbufsize = 1024
        while True:
            try:
                int_data = self.rfile.read(1)
                if not int_data:
                    break
                data = int_data.strip()
                print("receive from %r: %r" % (self.client_address, data))
                # self.wfile.write(client(data))
            except Exception as e:
                print(e)
                break
'''


class MyRequestHandler(StreamRequestHandler):

    def handle(self):
        connect_success = 1
        my_c = MyClient()
        print("%r, connecting..." % (TO_ADDR, ))
        try:
            helo_word = my_c.client_start()
            # helo_word = b'220 qa122.cn Anti-spam GT for Coremail System (demo-test1[20160627])\r\n'
            # self.request.sendall(struct.pack('%ds' % len(helo_word), helo_word))
            self.request.sendall(helo_word)
        except Exception as e:
            print(e)
            print("%r refuse a connect!" % (TO_ADDR,))
            connect_success = 0
        while connect_success:
            try:
                int_data = self.request.recv(1024)
                # int_data = self.rfile.readline()
                if not int_data:
                    break
                print("receive from %r: %r" % (self.client_address, int_data.strip()))
                self.request.sendall(my_c.client_send_recv(int_data))
            except Exception as e:
                print(e)
                print("closing connect %r!" % (self.client_address, ))
                break
        my_c.client_close()


class MyRequestHandlerCut(StreamRequestHandler):
    def handle(self):
        connect_success = 1
        my_c = MyClient()
        print("%r, connecting..." % (TO_ADDR, ))
        try:
            helo_word = my_c.client_start()
            self.request.sendall(helo_word)
        except Exception as e:
            print(e)
            print("%r refuse a connect!" % (TO_ADDR,))
            connect_success = 0
        while connect_success:
            try:
                int_data = self.request.recv(1024)
                # int_data = self.rfile.readline()
                if not int_data:
                    break
                print("receive from %r: %r" % (self.client_address, int_data.strip()))
                cut_content = raw_input('--------------if cut the content? y/n ').strip()
                if cut_content == 'y':
                    send_len = int(raw_input('how much bytes before cut(total: %d): ' % len(int_data.strip())).strip())
                    # send_data = struct.unpack('%ds%ds' % (send_len, len(int_data)-send_len), int_data)
                    send_data = int_data[0:send_len]
                    print("send data : %r" % send_data)
                    my_c.client_send(send_data)
                    time.sleep(5)
                    print("closing connect %r" % (self.client_address, ))
                    break
                else:
                    all_content = my_c.client_send_recv(int_data)
                    time.sleep(SLOW_TIME)
                    self.request.sendall(all_content)
            except Exception as e:
                print(e)
                print("closing connect %r!" % (self.client_address, ))
                break
        my_c.client_close()


class ThreadTCPServer(ThreadingMixIn, TCPServer):
    pass

if __name__ == '__main__':

    server = ThreadTCPServer(CREAT_ADDR, MyRequestHandlerCut)
    server.serve_forever()
