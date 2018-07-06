#!/usr/bin/env python

#/* ---------------------------------------------------------------------------
#** This software is in the public domain, furnished "as is", without technical
#** support, and with no warranty, express or implied, as to its usefulness for
#** any purpose.
#** -------------------------------------------------------------------------*/
#
#    Use Protocol 1 (PSP in keypad #1 mode) to simulate regular buttons. The analog stick should control the mouse.
#
#    This program will receive a string of keystates and simulate key presses and mouse events. 
#    This string is 17-char long and  contain '0's and '1's acording to that key state. This  
#    software was conceived as a port of the PSPEWC (http://PSPEWC.blogspot.com) server,  Anyway, 
#    which runs on Microsoft Windows systems.it can work with any other client that sends a similar
#    string at the port 30666 of this UDP socket.
#    Use Protocol 1 (PSP in keypad #1 mode) to simulate regular buttons. The analog stick also simulates key presses,
#    so you can use it in regular emulators, for example.should control the mouse.


import EWCnetworking
import EWCcontroller
import rumps
import threading
import time

srv = EWCnetworking.Server()
ctrl = EWCcontroller.Controller()

VERSION = 'Version: 0.4'
SERVER = srv.localaddr
MOUSE = 'Enable mouse'

def rumpsGUI():
	@rumps.clicked('Quit')
	def clean_up_before_quit(_):
	    print 'execute clean up code'
	    rumps.quit_application()
	
	@rumps.clicked(MOUSE)
	def not_actually_prefs(sender):
		ctrl.mouse = 1
		sender.state = not sender.state
		
	app = rumps.App(u"\U0001F579", menu=['PSP Wireless Controller', VERSION, SERVER, MOUSE, None, None, 'Quit'], quit_button=None)
	app.run()

def runServer():
	while 1:
		srv.receive()
		ctrl.handle_string(srv.message)

##Start test
class ThreadingExample(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
			srv.receive()
			ctrl.handle_string(srv.message)

example = ThreadingExample()
rumpsGUI()
print('Bye')
