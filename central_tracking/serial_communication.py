# Importing Libraries
import serial
import time


class Serial_Communication:
    """
    Handels serial communication with the transmitter Arduino
    at specified port and baudrate

    Since no signal is received but only transmitted, there is 
    no need for a receive method
    """
    
    def __init__(self, port, baudrate):
        self.arduino = serial.Serial(port=port, baudrate=baudrate)
        time.sleep(2)

    def send(self, byte_string):
        """
        Transmits given byte string to the arduino
        """
        self.arduino.write(byte_string)