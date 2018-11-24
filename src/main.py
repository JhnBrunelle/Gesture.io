import classifier

# Use def main as a safety check so if this app is run as a module, it will not execute main
def main():

	# Create leap classifier object
	leapClassifier = Classifier()

	#TODO: Create source for leap data input
	# Input the leap data to format for web request
	leapClassifier.getLeapDataJson(leapdatainput)

	# Make the actual web request
	result = leapClassifier.webRequest()

	# Call tts service
	tts.textToSpeech(result)

if __name__ == "__main__":
	main()