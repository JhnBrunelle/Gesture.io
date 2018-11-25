import classifier
#Here, we are writing functions used to obtain data from the leap motion sensor and store it in an object

import Voice

import os, sys, inspect, thread, time

data = []

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
#arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap

#Listener class used for threading based on events that occur with the leap controller
class SampleListener(Leap.Listener):

	def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
		print "Disconnected"

	def on_exit(self, controller):
		print "Exited"

	def on_connect(self, controller):
		print "Connected"

	def on_frame(self, controller):

		global data


		data = []

		data.append("")

		frame = controller.frame(5)

		data.append("1")
		data.append("5")

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

		if len(data)>20:

			data[27] = "0"
			data[28] = "0"
			data[29] = "0"		
	#print(data)
	

def getDataFromLeap(controller):

	data = []

	data.append("")

	frame = controller.frame()

	data.append("1")
	data.append("5")




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
	
	if len(data)>20:

		data[27] = "0"
		data[28] = "0"
		data[29] = "0"
	
	return data




# Use def main as a safety check so if this app is run as a module, it will not execute main
def main():

	global data

	# Create leap classifier object
	leapClassifier = classifier.Classifier()

	

	listener = SampleListener()

	#Here, we create a controller object, which serves as our connection to the Leap Motion controller. We can get data using Controller.frame()
	#Asynchronous process, so we need to wait for process to complete before reading frame data.
	controller = Leap.Controller()

	speechObject = Voice.Voice()

	# Have the sample listener receive events from the controller by adding the listener object to the controller
	controller.add_listener(listener)


	while 1:
		userInput = raw_input("Please enter the letter gestured:\n\n");
		
		print("\n\n\n")

		#leapdatainput = ['', '1', '5', 'Right hand', '-4.14554929733', '146.584259033', '-22.7312965393', '-0.239263770574', '19.454877125', '6.33745683594', '0.0134669011459', '0.079182267189', '-0.996769189835', '-5.67141485214', '152.342941284', '49.5832977295', '-9.13945579529', '131.951660156', '306.274597168', '49.595451355', '17.5728721619', '-25.9671382904', '135.042434692', '26.5975990295', '-25.9671382904', '135.042434692', '26.5975990295', '0', '0', '0', '-25.9671382904', '135.042434692', '26.5975990295', '-25.9671382904', '135.042434692', '26.5975990295', '-59.8857192993', '133.378814697', '-6.10225248337', '0.719473838806', '0.0352883599699', '0.693622469902', '-42.9264297485', '134.210632324', '10.2476730347', '-59.8857192993', '133.378814697', '-6.10225248337', '-84.2192077637', '132.357498169', '-27.467956543', '0.751071155071', '0.0315236896276', '0.659468233585', '-72.0524597168', '132.868164062', '-16.7851047516', '-84.2192077637', '132.357498169', '-27.467956543', '-99.1256866455', '132.103271484', '-36.0395088196', '0.866803348064', '0.0147831393406', '0.498430937529', '-91.6724472046', '132.230377197', '-31.7537326813', '55.4009628296', '16.7856082916', '-25.1487216949', '155.376815796', '20.6626148224', '-25.0452899933', '141.380111694', '-48.0971412659', '-0.00147401692811', '0.199468627572', '0.979903161526', '-25.0970058441', '148.378463745', '-13.7172632217', '-25.0452899933', '141.380111694', '-48.0971412659', '-11.4758052826', '103.681976318', '-42.7554702759', '-0.335708290339', '0.932649731636', '-0.132152631879', '-18.2605476379', '122.531044006', '-45.4263076782', '-11.4758052826', '103.681976318', '-42.7554702759', '-10.7370786667', '101.063865662', '-20.141828537', '-0.0324334651232', '0.114946991205', '-0.992841959', '-11.1064414978', '102.372924805', '-31.4486503601', '-10.7370786667', '101.063865662', '-20.141828537', '-12.976439476', '107.020393372', '-9.48285007477', '0.180389136076', '-0.479821264744', '-0.858621776104', '-11.8567590714', '104.042129517', '-14.8123397827', '63.1429367065', '16.4856967926', '-14.2785453796', '159.575622559', '18.3902130127', '-5.57245492935', '149.344238281', '-46.7836303711', '-0.13083204627', '0.153753623366', '0.979409456253', '-9.92549991608', '154.45993042', '-14.1967086792', '-5.57245492935', '149.344238281', '-46.7836303711', '1.14513385296', '104.62664032', '-41.3478240967', '-0.14749379456', '0.981835603714', '-0.119350507855', '-2.21366047859', '126.985443115', '-44.0657272339', '1.14513385296', '104.62664032', '-41.3478240967', '-1.40221977234', '99.7427520752', '-15.1570892334', '0.0951794087887', '0.182481750846', '-0.978591442108', '-0.12854295969', '102.184692383', '-28.252456665', '-1.40221977234', '99.7427520752', '-15.1570892334', '-4.12945890427', '108.310516357', '-4.94434642792', '0.20043233037', '-0.629668653011', '-0.750562608242', '-2.7658393383', '104.026634216', '-10.0507183075', '60.7486114502', '15.6871862411', '-2.57275295258', '160.376953125', '18.3444023132', '13.6373462677', '154.213989258', '-38.8287086487', '-0.271319538355', '0.103153757751', '0.956945598125', '5.53229665756', '157.295471191', '-10.2421531677', '13.6373462677', '154.213989258', '-38.8287086487', '16.3088302612', '112.034477234', '-36.691078186', '-0.0631287097931', '0.99672627449', '-0.0505134426057', '14.9730882645', '133.124237061', '-37.7598953247', '16.3088302612', '112.034477234', '-36.691078186', '9.95808601379', '105.651054382', '-12.2200727463', '0.243556022644', '0.244809269905', '-0.938482165337', '13.1334581375', '108.842765808', '-24.455575943', '9.95808601379', '105.651054382', '-12.2200727463', '6.42811393738', '113.391830444', '-1.71953010559', '0.261198848486', '-0.572775542736', '-0.776983380318', '8.19309997559', '109.521438599', '-6.96980142593', '43.7529754639', '13.9345846176', '9.02832984924', '160.128463745', '22.5694541931', '30.2688751221', '159.201263428', '-28.4864063263', '-0.384056985378', '0.0167650002986', '0.923157095909', '19.648601532', '159.664855957', '-2.95847606659', '30.2688751221', '159.201263428', '-28.4864063263', '43.8132514954', '141.14100647', '-50.0830955505', '-0.433536022902', '0.578082859516', '0.691278994083', '37.0410614014', '150.171142578', '-39.2847518921', '43.8132514954', '141.14100647', '-50.0830955505', '51.0016021729', '131.555953979', '-61.5450210571', '-0.433535814285', '0.57808303833', '0.691278934479', '47.4074249268', '136.348480225', '-55.8140563965', '51.0016021729', '131.555953979', '-61.5450210571', '56.3322677612', '125.852622986', '-70.0591812134', '-0.461473435163', '0.493734925985', '0.737067162991', '53.666934967', '128.704284668', '-65.8021011353', '']
		
		#TODO: Create source for leap data input
		# Input the leap data to format for web request
		leapClassifier.getLeapDataJson(data)

		# Make the actual web request
		receivedChar = leapClassifier.webRequest()

		if receivedChar == '%':
			break

		speechObject.addChar(receivedChar)


		time.sleep(1)

	speechObject.speak()

	

	# Call tts service
	# tts.textToSpeech(result)

if __name__ == "__main__":
	main()