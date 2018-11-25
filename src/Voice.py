'''
	Main voice API

	va = Voice() to generate a new speech section
	
	va.add('H') to add a character

	va.speak()
'''

import TTSEngine
from sets import Set

special = {
	"%": " "
}

specialDict = Set(special.keys())

class Voice:
	def __init__(self):
		self.text = ""
		self.onlineEngine = True

    # Adds a character to the phrase
	def addChar(self, char):
		# Check if we have a special character
		if char in specialDict:
			char = specialDict.get(char)

		# Concat char
		if char != None:
			self.text = self.text + char

    # Remove last character
	def backspace(self, char):
		self.text = self.text[:-1]

    # Call TTSEngine to output audio
	def speak(self):
		TTSEngine.say(self.text, self.onlineEngine)


# Test 
if __name__ == '__main__':	

	v = Voice()

	v.addChar("h")
	v.addChar("e")
	v.addChar("l")
	v.addChar("l")
	v.addChar("o")
	v.addChar("%")
	v.addChar("m")
	v.addChar("y")
	v.addChar("%")
	v.addChar("d")
	v.addChar("u")
	v.addChar("d")
	v.addChar("e")
	v.addChar("s")

	# Check multithreading
	for x in range(100):
		if x == 50:
			v.speak()
		print(x)

	print('Done')
	
