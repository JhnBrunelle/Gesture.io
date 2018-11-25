import json
import urllib2 as urlLib

# This class will output the results from our classifier
# The classifier was created using Azure ML
# A multi-class decision forest was used to achieve an average accuracy of 97%
class Classifier:
	def __init__(self):
		self.workspace = "db7b645d6af645e2940bac7cee56ef86"
		self.service = 	"fb12684fd6f4406d8828d813646ff718"
		self.requestUrl = "https://ussouthcentral.services.azureml.net/workspaces/" + self.workspace + "/services/" + self.service + "/execute?api-version=2.0&details=true"
		self.requestKey = "oRAtwvWmdXSopFXNaNzmi4DXbWH3py9hy45M3WgmJZl/PEIyl6PCUhqU42Gszfot70LgOr09HeAK1Q0BHWhg5w=="
		self.requestHeaders = {'Content-Type':'application/json', 'Authorization':('Bearer '+ self.requestKey)}

	# Takes the leap motion data and formats as a json message
	def getLeapDataJson(self, leapRawData):
		# Splitting the raw data into a csv style data structure, where null fields are treated as 0 instead
		#self.leapdata = leapRawData.split(",")
		#self.leapdata.insert(0, "")
		#print(leapRawData)
		# Taking our data and formatting it for Azure ML. Keep original column formatting and then Azure ML handles column selection
		self.dataToJson = {
			"Inputs": {
				"input1":{
					"ColumnNames": ["Symbol", "Number_of_Hands", "Number_of_Fingers", "Hand_Type", "Hand_Position_X", "Hand_Position_Y", "Hand_Position_Z", "Hand_Pitch", "Hand_Roll", "Hand_Yaw", "Arm_Direction_X", "Arm_Direction_Y", "Arm_Direction_Z", "Wrist_Position_X", "Wrist_Position_Y", "Wrist_Position_Z", "Elbow_Position_X", "Elbow_Position_Y", "Elbow_Position_Z", "Thumb_Length", "Thumb_Width", "Thumb_Metacarpal_Start_X", "Thumb_Metacarpal_Start_Y", "Thumb_Metacarpal_Start_Z", "Thumb_Metacarpal_End_X", "Thumb_Metacarpal_End_Y", "Thumb_Metacarpal_End_Z", "Thumb_Metacarpal_Direction_X", "Thumb_Metacarpal_Direction_Y", "Thumb_Metacarpal_Direction_Z", "Thumb_Metacarpal_Centre_X", "Thumb_Metacarpal_Centre_Y", "Thumb_Metacarpal_Centre_Z", "Thumb_Proximal_Start_X", "Thumb_Proximal_Start_Y", "Thumb_Proximal_Start_Z", "Thumb_Proximal_End_X", "Thumb_Proximal_End_Y", "Thumb_Proximal_End_Z", "Thumb_Proximal_Direction_X", "Thumb_Proximal_Direction_Y", "Thumb_Proximal_Direction_Z", "Thumb_Proximal_Centre_X", "Thumb_Proximal_Centre_Y", "Thumb_Proximal_Centre_Z", "Thumb_Intermediate_Start_X", "Thumb_Intermediate_Start_Y", "Thumb_Intermediate_Start_Z", "Thumb_Intermediate_End_X", "Thumb_Intermediate_End_Y", "Thumb_Intermediate_End_Z", "Thumb_Intermediate_Direction_X", "Thumb_Intermediate_Direction_Y", "Thumb_Intermediate_Direction_Z", "Thumb_Intermediate_Centre_X", "Thumb_Intermediate_Centre_Y", "Thumb_Intermediate_Centre_Z", "Thumb_Distal_Start_X", "Thumb_Distal_Start_Y", "Thumb_Distal_Start_Z", "Thumb_Distal_End_X", "Thumb_Distal_End_Y", "Thumb_Distal_End_Z", "Thumb_Distal_Direction_X", "Thumb_Distal_Direction_Y", "Thumb_Distal_Direction_Z", "Thumb_Distal_Centre_X", "Thumb_Distal_Centre_Y", "Thumb_Distal_Centre_Z", "Index_Length", "Index_Width", "Index_Metacarpal_Start_X", "Index_Metacarpal_Start_Y", "Index_Metacarpal_Start_Z", "Index_Metacarpal_End_X", "Index_Metacarpal_End_Y", "Index_Metacarpal_End_Z", "Index_Metacarpal_Direction_X", "Index_Metacarpal_Direction_Y", "Index_Metacarpal_Direction_Z", "Index_Metacarpal_Centre_X", "Index_Metacarpal_Centre_Y", "Index_Metacarpal_Centre_Z", "Index_Proximal_Start_X", "Index_Proximal_Start_Y", "Index_Proximal_Start_Z", "Index_Proximal_End_X", "Index_Proximal_End_Y", "Index_Proximal_End_Z", "Index_Proximal_Direction_X", "Index_Proximal_Direction_Y", "Index_Proximal_Direction_Z", "Index_Proximal_Centre_X", "Index_Proximal_Centre_Y", "Index_Proximal_Centre_Z", "Index_Intermediate_Start_X", "Index_Intermediate_Start_Y", "Index_Intermediate_Start_Z", "Index_Intermediate_End_X", "Index_Intermediate_End_Y", "Index_Intermediate_End_Z", "Index_Intermediate_Direction_X", "Index_Intermediate_Direction_Y", "Index_Intermediate_Direction_Z", "Index_Intermediate_Centre_X", "Index_Intermediate_Centre_Y", "Index_Intermediate_Centre_Z", "Index_Distal_Start_X", "Index_Distal_Start_Y", "Index_Distal_Start_Z", "Index_Distal_End_X", "Index_Distal_End_Y", "Index_Distal_End_Z", "Index_Distal_Direction_X", "Index_Distal_Direction_Y", "Index_Distal_Direction_Z", "Index_Distal_Centre_X", "Index_Distal_Centre_Y", "Index_Distal_Centre_Z", "Middle_Length", "Middle_Width", "Middle_Metacarpal_Start_X", "Middle_Metacarpal_Start_Y", "Middle_Metacarpal_Start_Z", "Middle_Metacarpal_End_X", "Middle_Metacarpal_End_Y", "Middle_Metacarpal_End_Z", "Middle_Metacarpal_Direction_X", "Middle_Metacarpal_Direction_Y", "Middle_Metacarpal_Direction_Z", "Middle_Metacarpal_Centre_X", "Middle_Metacarpal_Centre_Y", "Middle_Metacarpal_Centre_Z", "Middle_Proximal_Start_X", "Middle_Proximal_Start_Y", "Middle_Proximal_Start_Z", "Middle_Proximal_End_X", "Middle_Proximal_End_Y", "Middle_Proximal_End_Z", "Middle_Proximal_Direction_X", "Middle_Proximal_Direction_Y", "Middle_Proximal_Direction_Z", "Middle_Proximal_Centre_X", "Middle_Proximal_Centre_Y", "Middle_Proximal_Centre_Z", "Middle_Intermediate_Start_X", "Middle_Intermediate_Start_Y", "Middle_Intermediate_Start_Z", "Middle_Intermediate_End_X", "Middle_Intermediate_End_Y", "Middle_Intermediate_End_Z", "Middle_Intermediate_Direction_X", "Middle_Intermediate_Direction_Y", "Middle_Intermediate_Direction_Z", "Middle_Intermediate_Centre_X", "Middle_Intermediate_Centre_Y", "Middle_Intermediate_Centre_Z", "Middle_Distal_Start_X", "Middle_Distal_Start_Y", "Middle_Distal_Start_Z", "Middle_Distal_End_X", "Middle_Distal_End_Y", "Middle_Distal_End_Z", "Middle_Distal_Direction_X", "Middle_Distal_Direction_Y", "Middle_Distal_Direction_Z", "Middle_Distal_Centre_X", "Middle_Distal_Centre_Y", "Middle_Distal_Centre_Z", "Ring_Length", "Ring_Width", "Ring_Metacarpal_Start_X", "Ring_Metacarpal_Start_Y", "Ring_Metacarpal_Start_Z", "Ring_Metacarpal_End_X", "Ring_Metacarpal_End_Y", "Ring_Metacarpal_End_Z", "Ring_Metacarpal_Direction_X", "Ring_Metacarpal_Direction_Y", "Ring_Metacarpal_Direction_Z", "Ring_Metacarpal_Centre_X", "Ring_Metacarpal_Centre_Y", "Ring_Metacarpal_Centre_Z", "Ring_Proximal_Start_X", "Ring_Proximal_Start_Y", "Ring_Proximal_Start_Z", "Ring_Proximal_End_X", "Ring_Proximal_End_Y", "Ring_Proximal_End_Z", "Ring_Proximal_Direction_X", "Ring_Proximal_Direction_Y", "Ring_Proximal_Direction_Z", "Ring_Proximal_Centre_X", "Ring_Proximal_Centre_Y", "Ring_Proximal_Centre_Z", "Ring_Intermediate_Start_X", "Ring_Intermediate_Start_Y", "Ring_Intermediate_Start_Z", "Ring_Intermediate_End_X", "Ring_Intermediate_End_Y", "Ring_Intermediate_End_Z", "Ring_Intermediate_Direction_X", "Ring_Intermediate_Direction_Y", "Ring_Intermediate_Direction_Z", "Ring_Intermediate_Centre_X", "Ring_Intermediate_Centre_Y", "Ring_Intermediate_Centre_Z", "Ring_Distal_Start_X", "Ring_Distal_Start_Y", "Ring_Distal_Start_Z", "Ring_Distal_End_X", "Ring_Distal_End_Y", "Ring_Distal_End_Z", "Ring_Distal_Direction_X", "Ring_Distal_Direction_Y", "Ring_Distal_Direction_Z", "Ring_Distal_Centre_X", "Ring_Distal_Centre_Y", "Ring_Distal_Centre_Z", "Pinky_Length", "Pinky_Width", "Pinky_Metacarpal_Start_X", "Pinky_Metacarpal_Start_Y", "Pinky_Metacarpal_Start_Z", "Pinky_Metacarpal_End_X", "Pinky_Metacarpal_End_Y", "Pinky_Metacarpal_End_Z", "Pinky_Metacarpal_Direction_X", "Pinky_Metacarpal_Direction_Y", "Pinky_Metacarpal_Direction_Z", "Pinky_Metacarpal_Centre_X", "Pinky_Metacarpal_Centre_Y", "Pinky_Metacarpal_Centre_Z", "Pinky_Proximal_Start_X", "Pinky_Proximal_Start_Y", "Pinky_Proximal_Start_Z", "Pinky_Proximal_End_X", "Pinky_Proximal_End_Y", "Pinky_Proximal_End_Z", "Pinky_Proximal_Direction_X", "Pinky_Proximal_Direction_Y", "Pinky_Proximal_Direction_Z", "Pinky_Proximal_Centre_X", "Pinky_Proximal_Centre_Y", "Pinky_Proximal_Centre_Z", "Pinky_Intermediate_Start_X", "Pinky_Intermediate_Start_Y", "Pinky_Intermediate_Start_Z", "Pinky_Intermediate_End_X", "Pinky_Intermediate_End_Y", "Pinky_Intermediate_End_Z", "Pinky_Intermediate_Direction_X", "Pinky_Intermediate_Direction_Y", "Pinky_Intermediate_Direction_Z", "Pinky_Intermediate_Centre_X", "Pinky_Intermediate_Centre_Y", "Pinky_Intermediate_Centre_Z", "Pinky_Distal_Start_X", "Pinky_Distal_Start_Y", "Pinky_Distal_Start_Z", "Pinky_Distal_End_X", "Pinky_Distal_End_Y", "Pinky_Distal_End_Z", "Pinky_Distal_Direction_X", "Pinky_Distal_Direction_Y", "Pinky_Distal_Direction_Z", "Pinky_Distal_Centre_X", "Pinky_Distal_Centre_Y", "Pinky_Distal_Centre_Z", "Column 269"],
					"Values": [leapRawData, leapRawData,]
				},
			},
			"GlobalParameters": {}
		}

	# Used example code from azure, https://docs.microsoft.com/en-us/azure/machine-learning/studio/manage-web-service-endpoints-using-api-management
	def webRequest(self):
		self.requestBody = str.encode(json.dumps(self.dataToJson))
		# Trying to request the data

		#print(self.requestBody)
		try:
			request = urlLib.Request(self.requestUrl, self.requestBody, self.requestHeaders)
			response = urlLib.urlopen(request)
			resultFromRequest = response.read()
			#print "Result:" + resultFromRequest

			resultsInJSON = json.loads(resultFromRequest)

			predictedLetter = resultsInJSON["Results"]["output1"]["value"]["Values"][0][-1];
			print predictedLetter
			confidence = resultsInJSON["Results"]["output1"]["value"]["Values"][0][-2];
			print confidence
			#print resultsInJSON

			# TODO: Take JSON and extract the values we need 
			# return letter and confidence
			return predictedLetter

		except urlLib.HTTPError, error:
			print("The request failed with status code: " + str(error.code))
			print(error.info())
			print(json.loads(error.read()))

			


		
