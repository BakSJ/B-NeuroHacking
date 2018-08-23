import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = 'localhost'     # Get local machine name
port = 9997                    # Reserve a port for your service.

s.connect((host, port))

with open('EEGdata.txt', 'wb') as f:
    print ('file opened')
    while True:
        print('receiving data...')
        data = s.recv(1024)
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')
