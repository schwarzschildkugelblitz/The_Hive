# Importing Libraries
import serial
import time


class Serial_Communication:
    
    def __init__(self, port, baudrate):
        self.arduino = serial.Serial(port='COM4', baudrate=912600)
        time.sleep(2)

    def send(self, message):
        self.arduino.write(message)