#/* ---------------------------------------------------------------------------
#** This software is in the public domain, furnished "as is", without technical
#** support, and with no warranty, express or implied, as to its usefulness for
#** any purpose.
#**
#**
#** -------------------------------------------------------------------------*/
#
#    Use Protocol 1 (PSP in keypad #1 mode) to simulate regular buttons. The analog stick also simulates key presses,
#    so you can use it in regular emulators, for example.should control the mouse.
#
#    This class wraps some UDP socket stuff.

import socket

HOST = ''
PORT = 30666
BUFFERSIZE = 17 #PSP sends a 17-char string. 1 char = 1 byte.

class Server:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.addr = (HOST, PORT)
		self.sock.bind(self.addr)

		#try this on several machines to make sure it always do well.
		self.localaddr = socket.gethostbyname_ex(socket.gethostname())[2][0]
		#self.localaddr = socket.getfqdn()
		

	def receive(self):
		self.message, self.remoteaddr = self.sock.recvfrom(BUFFERSIZE)
		
