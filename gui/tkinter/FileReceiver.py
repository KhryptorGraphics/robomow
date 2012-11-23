# USAGE: python FileReciever.py

import socket, time, string, sys, urlparse
from threading import *

#------------------------------------------------------------------------

class FileReceiver ( Thread ):

    def __init__( this ):
        Thread.__init__( this )

    def run(this):
        this.process()

    def bindmsock( this ):
        this.msock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.msock.bind(('', 9090))
        this.msock.listen(2)
		#this.msock.settimeout(2)
        print '[Media] Listening on port 9090'

    def acceptmsock( this ):
        this.mconn, this.maddr = this.msock.accept()
        print '[Media] Got connection from', this.maddr
    
    def bindcsock( this ):
        this.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.csock.bind(('', 9091))
        this.csock.listen(2)
        #this.csock.settimeout(2)
        print '[Control] Listening on port 9091'

    def acceptcsock( this ):
        this.cconn, this.maddr = this.csock.accept()
        print '[Control] Got connection from', this.maddr
        
        while 1:
            data = this.cconn.recv(1024)
            if not data: break
            if data[0:4] == "SEND": this.filename = data[5:]
            print '[Control] Getting ready to receive "%s"' % this.filename
            break

    def transfer( this ):
        print '[Media] Starting media transfer for "%s"' % this.filename

        f = open(this.filename,"wb")
        while 1:
            data = this.mconn.recv(1024)
            if not data: break
            f.write(data)
        f.close()

        print '[Media] Got "%s"' % this.filename
        print '[Media] Closing media transfer for "%s"' % this.filename
    
    def close( this ):
        this.cconn.close()
        this.csock.close()
        this.mconn.close()
        this.msock.close()

    def process( this ):
        while 1:
            try:
		        this.bindcsock()
		        #time.sleep(1)
		        this.acceptcsock()
		        #time.sleep(1)
		        this.bindmsock()
		        #time.sleep(1)
		        this.acceptmsock()
		        #time.sleep(1)
		        this.transfer()
		        #time.sleep(1)
		        this.close()
		        time.sleep(.1)
            except:
                print "file xfer failed"
                this.close()
                time.sleep(.2)
                pass
#------------------------------------------------------------------------

#s = StreamHandler()
#s.start()
