# Task sink
# Binds PULL socket to tcp://localhost:5558
# Collects results from workers via that socket
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import sys
import time
import zmq
import socket

context = zmq.Context()
logSocket = '/dev/log'

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

# Connect to log socket
logSocketConnection = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
logSocketConnection.settimeout(1)
logSocketConnection.connect(logSocket)

# Wait for start of batch
s = receiver.recv()

# Start our clock now
tstart = time.time()

# Process 100 confirmations
for task_nbr in range(1000000):
    s = receiver.recv()
    sys.stdout.write(s + '\n')
    sys.stdout.flush()
    logSocketConnection.send(s)
    

# Calculate and report duration of batch
tend = time.time()
print("Total elapsed time: %d msec" % ((tend-tstart)*1000))
