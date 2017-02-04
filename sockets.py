# -*- coding: utf-8 -*-
import socket
import os, os.path
import time
import zmq

path = "/tmp/socksample"

# zmq context
context = zmq.Context()

# Socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

# Set up context
if os.path.exists( path ):
  os.remove( path )
 
print "Opening socket..."
server = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
server.bind( path )
 
print "Listening..."
while True:
  datagram = server.recv( 1024 )
  if not datagram:
    break
  else:
    print "-" * 20
    print datagram
    sender.send(datagram)
print "-" * 20
print "Shutting down..."
server.close()
os.remove( path )
print "Done"
