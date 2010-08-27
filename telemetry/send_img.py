# USAGE: python FileSender.py [file]

import sys, socket

HOST = '127.0.0.1'
CPORT = 12345
MPORT = 12346
FILE = sys.argv[1]

filename_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
filename_tcp.connect((HOST, CPORT))
filename_tcp.send("SEND " + FILE)
filename_tcp.close()

data_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_tcp .connect((HOST, MPORT))

print "data port connected..."

f = open(FILE, "rb")
data = f.read()
f.close()

data_tcp.send(data)
data_tcp.close()
