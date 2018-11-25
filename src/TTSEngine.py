
import os
import tempfile
import gtts
from playsound import playsound
import threading
import pyttsx3
from multiprocessing import Process, Queue
import urllib2

# Check if internet is present
def checkOffline():
    try:

    	# Attempt to connect to google
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return False	# Not Offline
    except urllib2.URLError as err: 
        return True		# Offline


# Makes an API call to the GoogleTTS
def googleTTS(phrase,lang="en"):

	# Fetch mp3 from googleTTS
	tts = gtts.gTTS(text=phrase, lang="en")

	# Save to tempfile as .mp3
	with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
		tmpfile = f.name
		tts.save(tmpfile)

	# Play and remove
	playsound(tmpfile)
	os.remove(tmpfile)


# Offline TTS that is used as a backup. It's also faster!
def offlineTTS(phrase):

	# Offline TTS, stops parent process
	offlineTTS = pyttsx3.init()
	offlineTTS.say(phrase)
	offlineTTS.runAndWait()


# Multithreaded say function, designed to not block
# the parent process
def say(phrase, lang, offline=False):

	# Check connection 
	offline = offline or checkOffline()

	if offline == True:
		print("Offline")
		offlineTTS(phrase)
		# t = threading.Thread(name='googs', target=offlineTTS, args=[phrase])
	else:
		print("Online")
		t = threading.Thread(name='googs', target=googleTTS, args=[phrase,lang])

		t.start()
    

# Run Tests
if __name__ == '__main__':

	# Offline TTS
	offlineTTS("This is an Offline Test")
	googleTTS("This is an Online Test", "en")
	say("This is a test of the say method", "en")

	