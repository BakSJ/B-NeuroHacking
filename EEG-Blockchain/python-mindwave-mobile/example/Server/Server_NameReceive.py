# Python 3 version
# Client file name --> server, then Server send file 
import socketserver
from os.path import exists
 
HOST = 'localhost'
PORT = 9009
 
class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data_transferred = 0
        print('[%s] Connected' %self.client_address[0])
        filename = self.request.recv(1024) 
        filename = filename.decode()
        if not exists(filename): 
            return
 
        print('File [%s] Transfer...' %filename)
        with open(filename, 'rb') as f:
            try:
                data = f.read(1024)
                while data:
                    data_transferred += self.request.send(data)
                    data = f.read(1024)
            except Exception as e:
                print(e)
 
        print('Finish File [%s], Byte[%d]' %(filename,data_transferred))
 
 
def runServer():
    print('++++++Starting File Server++++++')
    print("+++End Server 'Ctrl + C' Press")
 
    try:
        server = socketserver.TCPServer((HOST,PORT),MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('++++++File Server End.++++++')
 
 
runServer()


