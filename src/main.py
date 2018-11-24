import classifier
#Here, we are writing functions used to obtain data from the leap motion sensor and store it in an object

import os, sys, inspect, thread, time

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
#arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap

#Listener class used for threading based on events that occur with the leap controller
class SampleListener(Leap.Listener):

	def on_connect(self, controller):
		print "Connected"

def getDataFromLeap(controller):

	data = []

	data.append("")

	frame = controller.frame()

	data.append(str(len(frame.hands)))
	data.append(str(len(frame.fingers)))

			# Get hands
	for hand in frame.hands:

		handType = "Left hand" if hand.is_left else "Right hand"

		data.append(handType)
		data.append(str(hand.palm_position[0]))
		data.append(str(hand.palm_position[1]))
		data.append(str(hand.palm_position[2]))

		normal = hand.palm_normal
		direction = hand.direction

		data.append(str(direction.pitch * Leap.RAD_TO_DEG))
		data.append(str(normal.roll * Leap.RAD_TO_DEG))
		data.append(str(direction.yaw * Leap.RAD_TO_DEG))

            # Get arm bone
		arm = hand.arm

		data.append(str(arm.direction[0]))
		data.append(str(arm.direction[1]))
		data.append(str(arm.direction[2]))
		data.append(str(arm.wrist_position[0]))
		data.append(str(arm.wrist_position[1]))
		data.append(str(arm.wrist_position[2]))
		data.append(str(arm.elbow_position[0]))
		data.append(str(arm.elbow_position[1]))
		data.append(str(arm.elbow_position[2]))


		for finger in hand.fingers:

			data.append(str(finger.length))
			data.append(str(finger.width))

            	# Get bones
			for b in range(0, 4):

				bone = finger.bone(b)

				data.append(str(bone.prev_joint[0]))
				data.append(str(bone.prev_joint[1]))
				data.append(str(bone.prev_joint[2]))

				data.append(str(bone.next_joint[0]))
				data.append(str(bone.next_joint[1]))
				data.append(str(bone.next_joint[2]))

				data.append(str(bone.direction[0]))
				data.append(str(bone.direction[1]))
				data.append(str(bone.direction[2]))

				data.append(str(bone.center[0]))
				data.append(str(bone.center[1]))
				data.append(str(bone.center[2]))

	data.append("")
	return data




# Use def main as a safety check so if this app is run as a module, it will not execute main
def main():

	# Create leap classifier object
	leapClassifier = classifier.Classifier()

	

	listener = SampleListener()

	#Here, we create a controller object, which serves as our connection to the Leap Motion controller. We can get data using Controller.frame()
	#Asynchronous process, so we need to wait for process to complete before reading frame data.
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller by adding the listener object to the controller
	controller.add_listener(listener)

	while 1:
		userInput = raw_input("Please enter the letter gestured:\n\n");
		
		leapdatainput = getDataFromLeap(controller);

		print(len(leapdatainput))
		
		#TODO: Create source for leap data input
		# Input the leap data to format for web request
		leapClassifier.getLeapDataJson(leapdatainput)

		# Make the actual web request
		leapClassifier.webRequest()

	

	# Call tts service
	# tts.textToSpeech(result)

if __name__ == "__main__":
	main()