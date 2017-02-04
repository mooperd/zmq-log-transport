# -*- coding: utf-8 -*-

import socket
import os, os.path
import time
import zmq

from daemon import runner

path = "/tmp/socksample"

class DaemonApp(object):  
    """Daemon App."""

    def __init__(self):
        """Initialize Daemon."""
        self.stdin_path = '/dev/null'
        self.stdout_path = 'out.log'
        self.stderr_path = 'out.log'
        self.pidfile_path = '/tmp/daemon.pid'
        self.pidfile_timeout = 1

    def run(self):
        """Main Daemon Code."""
        # zmq context
        context = zmq.Context()

        # zmq socket to send messages to
        sender = context.socket(zmq.PUSH)
        sender.connect("tcp://10.141.0.33:5558")

        # Set up file path
        if os.path.exists( path ):
            os.remove( path )
        
        # Opening socket
        server = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
        server.bind( path )

        # main loop
        while True:
            datagram = server.recv( 1024 )
            sender.send(datagram)

if __name__ == '__main__':  
    app = DaemonApp()
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.do_action()

