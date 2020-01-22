#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
#
#    This file is part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MFRC522-Python.  If not, see <http://www.gnu.org/licenses/>.
#

# import scanner library / GPIO / signal

import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import signal


# import socket programming library 

import socket 

  
# import thread module 

from _thread import *

import threading 

from time import sleep

# Create an object of the class MFRC522
MIFAREReader = MFRC522()

print_lock = threading.Lock() 

  
# thread function 

def threaded(c):

    while True: 

  

        # data received from client 

        data = c.recv(1024) 

        if not data: 

            print('Bye') 

              

            # lock released on exit 

            print_lock.release() 

            break

        # initilize scanner and scan

        uid = read_f()

        # message you send to client

        message = uid
  

        # send data to client 

        print("wait")

        c.send(message.encode('ascii'))


    # connection closed 

    c.close() 

  

  

def Main(): 

    host = "" 

  

    # reverse a port on your computer 

    # in our case it is 12345 but it 

    # can be anything 

    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    s.bind((host, port)) 

    print("socket binded to port", port) 

  

    # put the socket into listening mode 

    s.listen(5) 

    print("socket is listening") 

  

    # a forever loop until client wants to exit 

    while True: 


        # establish connection with client 

        c, addr = s.accept() 

  

        # lock acquired by client 

        print_lock.acquire() 

        print('Connected to :', addr[0], ':', addr[1]) 

  

        # Start a new thread and return its identifier 

        start_new_thread(threaded, (c,))

        sleep(1.5)

    s.close() 


# THIS SECTION IS FOR THE SCANNER

def clean():
    global continue_reading
    print("Script ends, ending read.")
    continue_reading = False
    GPIO.cleanup()

def read_f():

    continue_reading = True

    # Welcome message
    print("Welcome to the MFRC522 data read example")
    print("Press Ctrl-C to stop.")

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:
        
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print("Card detected")
        
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print("Card read UID: {},{},{},{}".format(uid[0], uid[1], uid[2], uid[3]))
        
            # # This is the default key for authentication
            keys = [[0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], # FF FF FF FF FF FF = factory default
            [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5], # A0 A1 A2 A3 A4 A5
            [0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5], # B0 B1 B2 B3 B4 B5
            [0x4D, 0x3A, 0x99, 0xC3, 0x51, 0xDD], # 4D 3A 99 C3 51 DD
            [0x1A, 0x98, 0x2C, 0x7E, 0x45, 0x9A], # 1A 98 2C 7E 45 9A
            [0xD3, 0xF7, 0xD3, 0xF7, 0xD3, 0xF7], # D3 F7 D3 F7 D3 F7
            [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF], # AA BB CC DD EE FF
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00], # 00 00 00 00 00 00
            [0XAB, 0XCD, 0XEF, 0X12, 0X34, 0X56]]  

            for key in keys:
                print(key)
                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                # Check if authenticated
                if status == MIFAREReader.MI_OK:
                    MIFAREReader.MFRC522_Read(8)
                    MIFAREReader.MFRC522_StopCrypto1()
                    print("Authentication success")
                    clean()
                    return ("{}{}{}{}".format(uid[0], uid[1], uid[2], uid[3]))
                else:
                    print("Authentication error")
                    return ("{}{}{}{}".format(uid[0], uid[1], uid[2], uid[3]))
                    
  

if __name__ == '__main__': 

    Main() 
