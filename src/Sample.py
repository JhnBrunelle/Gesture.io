import os, sys, inspect, thread, time

#Variable used to store the csv:
csv = 0

#Declare a list to take the data from the frames.
data = []

#Below, we identify if the system is 64-bit or 32-bit and obtain the corresponding Hex file

finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

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

	def on_frame(self, controller):

		global data

		frame = controller.frame()



		data = []

		print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
			frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

		data.append(str(len(frame.hands)))
		data.append(str(len(frame.fingers)))

		# Get hands
		for hand in frame.hands:

			handType = "Left hand" if hand.is_left else "Right hand"

			#print "  %s, id %d, position: %s" % (
			#	handType, hand.id, hand.palm_position)

			data.append(handType)
			data.append(str(hand.palm_position[0]))
			data.append(str(hand.palm_position[1]))
			data.append(str(hand.palm_position[2]))

			# Get the hand's normal vector and direction
			normal = hand.palm_normal
			direction = hand.direction

			# Calculate the hand's pitch, roll, and yaw angles
			#print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
			#	direction.pitch * Leap.RAD_TO_DEG,
			#	normal.roll * Leap.RAD_TO_DEG,
			#	direction.yaw * Leap.RAD_TO_DEG)

			data.append(str(direction.pitch * Leap.RAD_TO_DEG))
			data.append(str(normal.roll * Leap.RAD_TO_DEG))
			data.append(str(direction.yaw * Leap.RAD_TO_DEG))

        	# Get arm bone
			arm = hand.arm
			#print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
			#	arm.direction,
			#	arm.wrist_position,
			#	arm.elbow_position)

			data.append(str(arm.direction[0]))
			data.append(str(arm.direction[1]))
			data.append(str(arm.direction[2]))
			data.append(str(arm.wrist_position[0]))
			data.append(str(arm.wrist_position[1]))
			data.append(str(arm.wrist_position[2]))
			data.append(str(arm.elbow_position[0]))
			data.append(str(arm.elbow_position[1]))
			data.append(str(arm.elbow_position[2]))

			# Get fingers
			for finger in hand.fingers:

			#	print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
			#		finger_names[finger.type],
			#		finger.id,
			#		finger.length,
			#		finger.width)

				data.append(str(finger.length))
				data.append(str(finger.width))

            	# Get bones
				for b in range(0, 4):
					bone = finger.bone(b)
			#		print "      Bone: %s, start: %s, end: %s, direction: %s, centre: %s" % (
			#			bone_names[bone.type],
			#			bone.prev_joint,
			#			bone.next_joint,
			#			bone.direction,
			#			bone.center)

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

		# Get tools
		for tool in frame.tools:

			print "  Tool id: %d, position: %s, direction: %s" % (
				tool.id, tool.tip_position, tool.direction)

def main():

	global data
	#Create a sample listener object that we can use for threading based on leap controller events
	listener = SampleListener()

	#Here, we create a controller object, which serves as our connection to the Leap Motion controller. We can get data using Controller.frame()
	#Asynchronous process, so we need to wait for process to complete before reading frame data.
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller by adding the listener object to the controller
	controller.add_listener(listener)

	exists = os.path.isfile('LeapMotionData.csv')
	if exists:
			# Store configuration file values
		download_dir = "LeapMotionData.csv" #where you want the file to be downloaded to 
		csv = open(download_dir, "a")
	else:
    	# Keep presets
		download_dir = "LeapMotionData.csv" #where you want the file to be downloaded to 
		csv = open(download_dir, "w")
		columnTitleRow = "Symbol, Number_of_Hands, Number_of_Fingers, Hand_Type, Hand_Position_X, Hand_Position_Y, Hand_Position_Z, Hand_Pitch, Hand_Roll, Hand_Yaw, "
		columnTitleRow = columnTitleRow + "Arm_Direction_X, Arm_Direction_Y, Arm_Direction_Z, Wrist_Position_X, Wrist_Position_Y, Wrist_Position_Z, Elbow_Position_X, Elbow_Position_Y, Elbow_Position_Z, Thumb_Length, Thumb_Width, "
		columnTitleRow = columnTitleRow + "Thumb_Metacarpal_Start_X, Thumb_Metacarpal_Start_Y, Thumb_Metacarpal_Start_Z, Thumb_Metacarpal_End_X, Thumb_Metacarpal_End_Y, Thumb_Metacarpal_End_Z, Thumb_Metacarpal_Direction_X, Thumb_Metacarpal_Direction_Y, Thumb_Metacarpal_Direction_Z, Thumb_Metacarpal_Centre_X, Thumb_Metacarpal_Centre_Y, Thumb_Metacarpal_Centre_Z, "
		columnTitleRow = columnTitleRow + "Thumb_Proximal_Start_X, Thumb_Proximal_Start_Y, Thumb_Proximal_Start_Z, Thumb_Proximal_End_X, Thumb_Proximal_End_Y, Thumb_Proximal_End_Z, Thumb_Proximal_Direction_X, Thumb_Proximal_Direction_Y, Thumb_Proximal_Direction_Z, Thumb_Proximal_Centre_X, Thumb_Proximal_Centre_Y, Thumb_Proximal_Centre_Z, "
		columnTitleRow = columnTitleRow + "Thumb_Intermediate_Start_X, Thumb_Intermediate_Start_Y, Thumb_Intermediate_Start_Z, Thumb_Intermediate_End_X, Thumb_Intermediate_End_Y, Thumb_Intermediate_End_Z, Thumb_Intermediate_Direction_X, Thumb_Intermediate_Direction_Y, Thumb_Intermediate_Direction_Z, Thumb_Intermediate_Centre_X, Thumb_Intermediate_Centre_Y, Thumb_Intermediate_Centre_Z, "
		columnTitleRow = columnTitleRow + "Thumb_Distal_Start_X, Thumb_Distal_Start_Y, Thumb_Distal_Start_Z, Thumb_Distal_End_X, Thumb_Distal_End_Y, Thumb_Distal_End_Z, Thumb_Distal_Direction_X, Thumb_Distal_Direction_Y, Thumb_Distal_Direction_Z, Thumb_Distal_Centre_X, Thumb_Distal_Centre_Y, Thumb_Distal_Centre_Z, "
		columnTitleRow = columnTitleRow + "Index_Length, Index_Width, "
		columnTitleRow = columnTitleRow + "Index_Metacarpal_Start_X, Index_Metacarpal_Start_Y, Index_Metacarpal_Start_Z, Index_Metacarpal_End_X, Index_Metacarpal_End_Y, Index_Metacarpal_End_Z, Index_Metacarpal_Direction_X, Index_Metacarpal_Direction_Y, Index_Metacarpal_Direction_Z, Index_Metacarpal_Centre_X, Index_Metacarpal_Centre_Y, Index_Metacarpal_Centre_Z, "
		columnTitleRow = columnTitleRow + "Index_Proximal_Start_X, Index_Proximal_Start_Y, Index_Proximal_Start_Z, Index_Proximal_End_X, Index_Proximal_End_Y, Index_Proximal_End_Z, Index_Proximal_Direction_X, Index_Proximal_Direction_Y, Index_Proximal_Direction_Z, Index_Proximal_Centre_X, Index_Proximal_Centre_Y, Index_Proximal_Centre_Z, "
		columnTitleRow = columnTitleRow + "Index_Intermediate_Start_X, Index_Intermediate_Start_Y, Index_Intermediate_Start_Z, Index_Intermediate_End_X, Index_Intermediate_End_Y, Index_Intermediate_End_Z, Index_Intermediate_Direction_X, Index_Intermediate_Direction_Y, Index_Intermediate_Direction_Z, Index_Intermediate_Centre_X, Index_Intermediate_Centre_Y, Index_Intermediate_Centre_Z, "
		columnTitleRow = columnTitleRow + "Index_Distal_Start_X, Index_Distal_Start_Y, Index_Distal_Start_Z, Index_Distal_End_X, Index_Distal_End_Y, Index_Distal_End_Z, Index_Distal_Direction_X, Index_Distal_Direction_Y, Index_Distal_Direction_Z, Index_Distal_Centre_X, Index_Distal_Centre_Y, Index_Distal_Centre_Z, "

		columnTitleRow = columnTitleRow + "Middle_Length, Middle_Width, "
		columnTitleRow = columnTitleRow + "Middle_Metacarpal_Start_X, Middle_Metacarpal_Start_Y, Middle_Metacarpal_Start_Z, Middle_Metacarpal_End_X, Middle_Metacarpal_End_Y, Middle_Metacarpal_End_Z, Middle_Metacarpal_Direction_X, Middle_Metacarpal_Direction_Y, Middle_Metacarpal_Direction_Z, Middle_Metacarpal_Centre_X, Middle_Metacarpal_Centre_Y, Middle_Metacarpal_Centre_Z, "
		columnTitleRow = columnTitleRow + "Middle_Proximal_Start_X, Middle_Proximal_Start_Y, Middle_Proximal_Start_Z, Middle_Proximal_End_X, Middle_Proximal_End_Y, Middle_Proximal_End_Z, Middle_Proximal_Direction_X, Middle_Proximal_Direction_Y, Middle_Proximal_Direction_Z, Middle_Proximal_Centre_X, Middle_Proximal_Centre_Y, Middle_Proximal_Centre_Z, "
		columnTitleRow = columnTitleRow + "Middle_Intermediate_Start_X, Middle_Intermediate_Start_Y, Middle_Intermediate_Start_Z, Middle_Intermediate_End_X, Middle_Intermediate_End_Y, Middle_Intermediate_End_Z, Middle_Intermediate_Direction_X, Middle_Intermediate_Direction_Y, Middle_Intermediate_Direction_Z, Middle_Intermediate_Centre_X, Middle_Intermediate_Centre_Y, Middle_Intermediate_Centre_Z, "
		columnTitleRow = columnTitleRow + "Middle_Distal_Start_X, Middle_Distal_Start_Y, Middle_Distal_Start_Z, Middle_Distal_End_X, Middle_Distal_End_Y, Middle_Distal_End_Z, Middle_Distal_Direction_X, Middle_Distal_Direction_Y, Middle_Distal_Direction_Z, Middle_Distal_Centre_X, Middle_Distal_Centre_Y, Middle_Distal_Centre_Z, "

		columnTitleRow = columnTitleRow + "Ring_Length, Ring_Width, "
		columnTitleRow = columnTitleRow + "Ring_Metacarpal_Start_X, Ring_Metacarpal_Start_Y, Ring_Metacarpal_Start_Z, Ring_Metacarpal_End_X, Ring_Metacarpal_End_Y, Ring_Metacarpal_End_Z, Ring_Metacarpal_Direction_X, Ring_Metacarpal_Direction_Y, Ring_Metacarpal_Direction_Z, Ring_Metacarpal_Centre_X, Ring_Metacarpal_Centre_Y, Ring_Metacarpal_Centre_Z, "
		columnTitleRow = columnTitleRow + "Ring_Proximal_Start_X, Ring_Proximal_Start_Y, Ring_Proximal_Start_Z, Ring_Proximal_End_X, Ring_Proximal_End_Y, Ring_Proximal_End_Z, Ring_Proximal_Direction_X, Ring_Proximal_Direction_Y, Ring_Proximal_Direction_Z, Ring_Proximal_Centre_X, Ring_Proximal_Centre_Y, Ring_Proximal_Centre_Z, "
		columnTitleRow = columnTitleRow + "Ring_Intermediate_Start_X, Ring_Intermediate_Start_Y, Ring_Intermediate_Start_Z, Ring_Intermediate_End_X, Ring_Intermediate_End_Y, Ring_Intermediate_End_Z, Ring_Intermediate_Direction_X, Ring_Intermediate_Direction_Y, Ring_Intermediate_Direction_Z, Ring_Intermediate_Centre_X, Ring_Intermediate_Centre_Y, Ring_Intermediate_Centre_Z, "
		columnTitleRow = columnTitleRow + "Ring_Distal_Start_X, Ring_Distal_Start_Y, Ring_Distal_Start_Z, Ring_Distal_End_X, Ring_Distal_End_Y, Ring_Distal_End_Z, Ring_Distal_Direction_X, Ring_Distal_Direction_Y, Ring_Distal_Direction_Z, Ring_Distal_Centre_X, Ring_Distal_Centre_Y, Ring_Distal_Centre_Z, "

		columnTitleRow = columnTitleRow + "Pinky_Length, Pinky_Width, "
		columnTitleRow = columnTitleRow + "Pinky_Metacarpal_Start_X, Pinky_Metacarpal_Start_Y, Pinky_Metacarpal_Start_Z, Pinky_Metacarpal_End_X, Pinky_Metacarpal_End_Y, Pinky_Metacarpal_End_Z, Pinky_Metacarpal_Direction_X, Pinky_Metacarpal_Direction_Y, Pinky_Metacarpal_Direction_Z, Pinky_Metacarpal_Centre_X, Pinky_Metacarpal_Centre_Y, Pinky_Metacarpal_Centre_Z, "
		columnTitleRow = columnTitleRow + "Pinky_Proximal_Start_X, Pinky_Proximal_Start_Y, Pinky_Proximal_Start_Z, Pinky_Proximal_End_X, Pinky_Proximal_End_Y, Pinky_Proximal_End_Z, Pinky_Proximal_Direction_X, Pinky_Proximal_Direction_Y, Pinky_Proximal_Direction_Z, Pinky_Proximal_Centre_X, Pinky_Proximal_Centre_Y, Pinky_Proximal_Centre_Z, "
		columnTitleRow = columnTitleRow + "Pinky_Intermediate_Start_X, Pinky_Intermediate_Start_Y, Pinky_Intermediate_Start_Z, Pinky_Intermediate_End_X, Pinky_Intermediate_End_Y, Pinky_Intermediate_End_Z, Pinky_Intermediate_Direction_X, Pinky_Intermediate_Direction_Y, Pinky_Intermediate_Direction_Z, Pinky_Intermediate_Centre_X, Pinky_Intermediate_Centre_Y, Pinky_Intermediate_Centre_Z, "
		columnTitleRow = columnTitleRow + "Pinky_Distal_Start_X, Pinky_Distal_Start_Y, Pinky_Distal_Start_Z, Pinky_Distal_End_X, Pinky_Distal_End_Y, Pinky_Distal_End_Z, Pinky_Distal_Direction_X, Pinky_Distal_Direction_Y, Pinky_Distal_Direction_Z, Pinky_Distal_Centre_X, Pinky_Distal_Centre_Y, Pinky_Distal_Centre_Z \n"

		csv.write(columnTitleRow)

	while 1:
		userInput = raw_input("Please enter the letter gestured:\n\n");

		dataRow = userInput + ", "

		for item in data:
			dataRow = dataRow + item + ", "

		dataRow = dataRow + "\n"

		csv.write(dataRow)



    # Keep this process running until Enter is pressed
	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	main()