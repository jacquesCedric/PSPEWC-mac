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
#    This class receives the string (something like 11001000100000100)
#    and simulate some key presses and mouse movements

import sys
import os
import time
from Quartz.CoreGraphics import CGEventCreateKeyboardEvent
#Mouse
from Quartz.CoreGraphics import CGEventCreateMouseEvent, kCGEventMouseMoved, kCGMouseButtonLeft, kCGMouseButtonRight, kCGEventLeftMouseDown, kCGEventLeftMouseUp, kCGEventRightMouseUp, kCGEventRightMouseDown, CGEventGetLocation, CGPointMake

from Quartz.CoreGraphics import CGEventCreate
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGHIDEventTap

#Definitiona
PROTOCOL_INDEX = 0
UP_INDEX = 1
DOWN_INDEX = 2
LEFT_INDEX = 3
RIGHT_INDEX = 4
SQUARE_INDEX = 5
CIRCLE_INDEX = 6
CROSS_INDEX = 7
TRIANGLE_INDEX = 8
LTRIGGER_INDEX = 9
RTRIGGER_INDEX = 10
START_INDEX = 11
DANALOG_INDEX = 12
UANALOG_INDEX = 13
RANALOG_INDEX = 14
LANALOG_INDEX = 15
SELECT_INDEX = 16

#Keycodes
#DPAD
K_UP = 0x7E
K_DOWN = 0x7D
K_LEFT = 0x7B
K_RIGHT = 0x7C
#FACE (CounterClockwise from X)
K_A = 0x06
K_B = 0x00
K_C = 0x01
K_D = 0x07
#TRIGGERS
K_E = 0x0C
K_F = 0x0D
#START
K_ENTER = 0x24
#ANALOG
K_G = 0x11
K_H = 0x12
K_I = 0x13
K_J = 0x14
#SELECT
K_BACKSPACE = 0x38

#How much the pointer will run in each iteration - change it as your will
POINTER_STEP = 1
#Mouse step in PX
MOUSE_STEP = 15
MOUSE_KEYS = [K_G, K_H, K_I, K_J]

class Controller:
	#This list holds the state of all the buttons on the psp. They are 0 or 1
	keystates = ['0']*17 #why cant it start with self.?
	mouse = 0

	def getCursorPosition(self):
		point = CGEventGetLocation(CGEventCreate(None))
		return point

	def moveMouseTo(self, x, y):
		return CGEventPost(
			kCGHIDEventTap, 
			CGEventCreateMouseEvent(
				None, kCGEventMouseMoved,
				CGPointMake(x, y),
				kCGMouseButtonLeft)
			);

	def mouseMove(self, k, k2 = None):
		cursor = self.getCursorPosition()
		if(k2):
			#UP + RIGHT
			if(k == K_I and k2 == K_H):
				cursor.x+=MOUSE_STEP/2
				cursor.y-=MOUSE_STEP/2
			#DOWN + RIGHT
			elif(k == K_J and k2 == K_H):
				cursor.x+=MOUSE_STEP/2
				cursor.y+=MOUSE_STEP/2
			#UP + LEFT
			if(k == K_I and k2 == K_G):
				cursor.x-=MOUSE_STEP/2
				cursor.y+=MOUSE_STEP/2
			#DOWN + LEFT
			elif(k == K_J and k2 == K_G):
				cursor.x-=MOUSE_STEP/2
				cursor.y-=MOUSE_STEP/2
		else:
			if(k == K_G):
				cursor.x-=MOUSE_STEP
			elif(k == K_H):
				cursor.x+=MOUSE_STEP
			elif(k == K_I):
				cursor.y-=MOUSE_STEP
			elif(k == K_J):
				cursor.y+=MOUSE_STEP

		return self.moveMouseTo(cursor.x, cursor.y)

	def mouseLeftClick(self):
		cursor = self.getCursorPosition()
		time.sleep(0.0001)
		CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (cursor.x, cursor.y), kCGMouseButtonLeft))
		CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (cursor.x, cursor.y), kCGMouseButtonLeft))
		time.sleep(0.0001)

	def mouseRightClick(self):
		cursor = self.getCursorPosition()
		time.sleep(0.100)
		CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventRightMouseDown, (cursor.x, cursor.y), kCGMouseButtonRight))
		CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventRightMouseUp, (cursor.x, cursor.y), kCGMouseButtonRight))
		
	def KeyDown(self, k):
			time.sleep(0.0001)
			CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, k, True))
			time.sleep(0.0001)
	
	def KeyUp(self, k):
	    time.sleep(0.0001)
	    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, k, False))
	    time.sleep(0.0001)

	def KeyPress(self, k):
	    time.sleep(0.0001)
	    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, k, True))
	    time.sleep(0.0001)
	    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, k, False))
	    time.sleep(0.0001)

	def handle_string(self, received_string):
		# Check we're getting the right messages from the PSP
		if len(received_string) != 17:
			print 'Unrecognized string received! Exiting...'
			os._exit(0)
		else:
			#Up
			if received_string[UP_INDEX] == '1':
				if self.keystates[UP_INDEX] == '0':
					self.KeyDown(K_UP)
					self.keystates[UP_INDEX] = '1'
			else:
			 	if self.keystates[UP_INDEX] == '1':
			 		self.KeyUp(K_UP)
			 		self.keystates[UP_INDEX] = '0'

			#Down
			if received_string[DOWN_INDEX] == '1':
				if self.keystates[DOWN_INDEX] == '0':
					self.KeyDown(K_DOWN)
					self.keystates[DOWN_INDEX] = '1'
			else:
				if self.keystates[DOWN_INDEX] == '1':
					self.KeyUp(K_DOWN)
					self.keystates[DOWN_INDEX] = '0'

			#Left
			if received_string[LEFT_INDEX] == '1':
				if self.keystates[LEFT_INDEX] == '0':
					self.KeyDown(K_LEFT)
					self.keystates[LEFT_INDEX] = '1'
			else:
				if self.keystates[LEFT_INDEX] == '1':
					self.KeyUp(K_LEFT)
					self.keystates[LEFT_INDEX] = '0'

			#Right
			if received_string[RIGHT_INDEX] == '1':
				if self.keystates[RIGHT_INDEX] == '0':
					self.KeyDown(K_RIGHT)
					self.keystates[RIGHT_INDEX] = '1'
			else:
				if self.keystates[RIGHT_INDEX] == '1':
					self.KeyUp(K_RIGHT)
					self.keystates[RIGHT_INDEX] = '0'

			#Cross
			if received_string[CROSS_INDEX] == '1':
				if self.keystates[CROSS_INDEX] == '0':
					self.KeyDown(K_A)
					self.keystates[CROSS_INDEX] = '1'
			else:
				if self.keystates[CROSS_INDEX] == '1':
					self.KeyUp(K_A)
					self.keystates[CROSS_INDEX] = '0'

			#Square
			if received_string[SQUARE_INDEX] == '1':
				if self.keystates[SQUARE_INDEX] == '0':
					self.KeyDown(K_B)
					self.keystates[SQUARE_INDEX] = '1'
			else:
				if self.keystates[SQUARE_INDEX] == '1':
					self.KeyUp(K_B)
					self.keystates[SQUARE_INDEX] = '0'

			#Triangle
			if received_string[TRIANGLE_INDEX] == '1':
				if self.keystates[TRIANGLE_INDEX] == '0':
					self.KeyDown(K_C)
					self.keystates[TRIANGLE_INDEX] = '1'
			else:
				if self.keystates[TRIANGLE_INDEX] == '1':
					self.KeyUp(K_C)
					self.keystates[TRIANGLE_INDEX] = '0'
				
			#Circle
			if received_string[CIRCLE_INDEX] == '1':
				if self.keystates[CIRCLE_INDEX] == '0':
					self.KeyDown(K_D)
					self.keystates[CIRCLE_INDEX] = '1'
			else:
				if self.keystates[CIRCLE_INDEX] == '1':
					self.KeyUp(K_D)
					self.keystates[CIRCLE_INDEX] = '0'

			#Start
			if received_string[START_INDEX] == '1':
				if self.keystates[START_INDEX] == '0':
					self.KeyDown(K_ENTER)
					self.keystates[START_INDEX] = '1'
			else:
				if self.keystates[START_INDEX] == '1':
					self.KeyUp(K_ENTER)
					self.keystates[START_INDEX] = '0'

			if(self.mouse):
				if received_string[UANALOG_INDEX] == '1' and received_string[RANALOG_INDEX] == '1':
					#print "UP + RIGHT"
					self.mouseMove(K_I, K_H)
				elif received_string[DANALOG_INDEX] == '1' and received_string[RANALOG_INDEX] == '1':
					#print "DOWN + RIGHT"
					self.mouseMove(K_J, K_H)
				elif received_string[UANALOG_INDEX] == '1' and received_string[LANALOG_INDEX] == '1':
					#print "UP + LEFT"
					self.mouseMove(K_J, K_G)
				elif received_string[DANALOG_INDEX] == '1' and received_string[LANALOG_INDEX] == '1':
					#print "DOWN + LEFT"
					self.mouseMove(K_I, K_G)

			#L-Trigger
			if received_string[LTRIGGER_INDEX] == '1':
				if(self.mouse):
					if self.keystates[LTRIGGER_INDEX] == '0':
						self.mouseLeftClick();
						self.keystates[LTRIGGER_INDEX] = '1'
				else:
					if self.keystates[LTRIGGER_INDEX] == '0':
						self.KeyDown(K_E)
						self.keystates[LTRIGGER_INDEX] = '1'
			else:
				if self.keystates[LTRIGGER_INDEX] == '1':
					self.KeyUp(K_E)
					self.keystates[LTRIGGER_INDEX] = '0'

			#R-Trigger
			if received_string[RTRIGGER_INDEX] == '1':
				if(self.mouse):
					if self.keystates[RTRIGGER_INDEX] == '0':
						self.mouseRightClick();
						self.keystates[RTRIGGER_INDEX] = '1'
				else:
					if self.keystates[RTRIGGER_INDEX] == '0':
						self.KeyDown(K_F)
						self.keystates[RTRIGGER_INDEX] = '1'
			else:
				if self.keystates[RTRIGGER_INDEX] == '1':
					self.KeyUp(K_F)
					self.keystates[RTRIGGER_INDEX] = '0'
			
			#Up Analog
			if received_string[UANALOG_INDEX] == '1':
				if(self.mouse):
					self.mouseMove(K_I)
				else:
					if self.keystates[UANALOG_INDEX] == '0':
						self.KeyDown(K_I)
						self.keystates[UANALOG_INDEX] = '1'
			else:
				if self.keystates[UANALOG_INDEX] == '1':
					self.KeyUp(K_I)
					self.keystates[UANALOG_INDEX] = '0'

			#Down Analog
			if received_string[DANALOG_INDEX] == '1':
				if(self.mouse):
					self.mouseMove(K_J)
				else:
					if self.keystates[DANALOG_INDEX] == '0':
						self.KeyDown(K_J)
						self.keystates[DANALOG_INDEX] = '1'
			else:
				if self.keystates[DANALOG_INDEX] == '1':
					self.KeyUp(K_J)
					self.keystates[DANALOG_INDEX] = '0'

			#Left Analog
			if received_string[LANALOG_INDEX] == '1':
				if(self.mouse):
					self.mouseMove(K_G)
				else:
					if self.keystates[LANALOG_INDEX] == '0':
						self.KeyDown(K_G)
						self.keystates[LANALOG_INDEX] = '1'
			else:
				if self.keystates[LANALOG_INDEX] == '1':
					self.KeyUp(K_G)
					self.keystates[LANALOG_INDEX] = '0'

			#Right Analog
			if received_string[RANALOG_INDEX] == '1':
				if(self.mouse):
					self.mouseMove(K_H)
				else:
					if self.keystates[RANALOG_INDEX] == '0':
						self.KeyDown(K_H)
						self.keystates[RANALOG_INDEX] = '1'
			else:
				if self.keystates[RANALOG_INDEX] == '1':
					self.KeyUp(K_H)
					self.keystates[RANALOG_INDEX] = '0'

			#Select
			if received_string[SELECT_INDEX] == '1':
				if self.keystates[SELECT_INDEX] == '0':
					self.KeyDown(K_BACKSPACE)
					self.keystates[SELECT_INDEX] = '1'
			else:
				if self.keystates[SELECT_INDEX] == '1':
					self.KeyUp(K_BACKSPACE)
					self.keystates[SELECT_INDEX] = '0'

