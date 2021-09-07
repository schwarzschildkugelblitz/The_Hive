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
        0-3 bits address 
        case 1 - angle(in degrees)  2 decimal precision 
               - distance (in cm ) 2 decimal places
        case 2 - 0 stop 1 right 2 left 3 drop 4 slow drive   
        """
        self.arduino.write(byte_string)
