from time import sleep
import serial

class SerialDriver:
	def __init(self,port):
		self.port = port

	def readButtonPress(self):
		ser = serial.Serial('com16', 9600)
		if ser.readline() == 0:
			return False
		else:
			return True

	def writeRGB(self, color):
		ser = serial.Serial('com16', 9600)
		ser.write(color)
