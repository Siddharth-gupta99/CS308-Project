from config import *
import asyncio, io, glob, os, sys, time, uuid
import math, datetime, logging
import cv2
import requests
from multiprocessing import Queue, Process, Value
from urllib.parse import urlparse
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, OperationStatusType

# Classroom ID to identify in which classroom the particular device
# is installed in. This ID helps in fetching the appropriate schedule
# times for the classes to be held in the particular classroom.
CLASSROOM_ID = 1

# Location of the log file.
logPath = 'Logs/'

# Name of the log file.
logFileName = datetime.datetime.now().strftime("%d-%b-%Y_%H.%M.%S")

# Configuration for logging.
logging.basicConfig(
	format="\033[1m%(asctime)s [%(levelname)-8s]\033[0m %(message)s", 
	level=logging.INFO,
	datefmt='%Y-%m-%d %H:%M:%S',
	handlers=[
		logging.FileHandler("{0}/{1}.log".format(logPath, logFileName)),
		logging.StreamHandler()
	])

# Initialized global variables.
LECTURE_ID = 0					# Fetched from server.
TAKE_ATTENDANCE = False			# Flag to start/stop taking attendance.
TRY_MAX_COUNT = 5				# Maximum number of times a failed method should retry.

# leftMarginSeconds and rightMarginSeconds are the time periods before
# and after the scheduled time (in seconds) for which the taking attendance 
# process must run.
leftMarginSeconds = CLASSTIME_LEFT_MARGIN['hour']*3600 + CLASSTIME_LEFT_MARGIN['minute']*60 + CLASSTIME_LEFT_MARGIN['second']
rightMarginSeconds = CLASSTIME_RIGHT_MARGIN['hour']*3600 + CLASSTIME_RIGHT_MARGIN['minute']*60 + CLASSTIME_RIGHT_MARGIN['second']


# Method to fetch the first upcoming lecutre schedule along with the 
# lecture ID. This function returns two values: A boolean telling if the 
# attendance process should be started and a time data object.
#
# False, None                  - When the current time is not in the given interval of the schedule.
# False, <sleep_time>          - When the time remaining in the lecture is less than the FETCH_INTERVAL.
# True, <start_time, end_time> - When the current time is in the given interval.
def fetchAndCheck():
	
	global LECTURE_ID
	
	for tryCount in range(TRY_MAX_COUNT):

		# Try and fetch the latest schedule from the server using GET request.
		try:
			logging.info('[{}] Fetching schedule from \'{}\''.format(tryCount+1, API_GET_SCHEDULE))
			nextScheduleTime = requests.get(url=API_GET_SCHEDULE+str(CLASSROOM_ID))
			nextScheduleTime = nextScheduleTime.json()
			logging.info('Fetched data successfully')
			break

		except requests.exceptions.RequestException as e:
			logging.error("Caught error: {}".format(e))

			if tryCount < TRY_MAX_COUNT-1:
				logging.info('Trying again in {} seconds'.format((tryCount+1)*5))
				time.sleep((tryCount+1)*5)

			else:
				logging.critical('Cannot fetch data from \'{}\''.format(API_GET_SCHEDULE))
				return False, None

		except Error as e:
			logging.error("Caught error: {}".format(e))

			if tryCount < TRY_MAX_COUNT-1:
				logging.info('Trying again in {} seconds'.format((tryCount+1)*5))
				time.sleep((tryCount+1)*5)

			else:
				logging.critical('Cannot parse into JSON. Invalid response from \'{}\''.format(API_GET_SCHEDULE))
				return False, None

	# Check for valid response from the server which should send
	# "id" and "time" keys back to the client when class is scheduled.
	if "id" in nextScheduleTime.keys() and "time" in nextScheduleTime.keys():

		nextTime = datetime.datetime.strptime(nextScheduleTime['time'], FETCH_TIME_FORMAT)
		currentTime = datetime.datetime.now()

		# datetime objects to make comparision easier between the current
		# time and the window endpoints.
		leftTimeDelta = nextTime - datetime.timedelta(seconds=leftMarginSeconds)
		rightTimeDelta = nextTime + datetime.timedelta(seconds=rightMarginSeconds)

		logging.info('Next class scheduled for {} in classroom ID {}'.format(str(nextTime), CLASSROOM_ID))
		logging.info('Checking for current time between {} and {} seconds from scheduled time'.format(-leftMarginSeconds, rightMarginSeconds))

		# If the time is in the given window around the scheduled time, 
		# return True and the start and end time for taking attendance.
		if currentTime >= leftTimeDelta and currentTime <= rightTimeDelta:
			logging.info("Attendance taking to be started now.")
			LECTURE_ID = nextScheduleTime["id"]
			return True, {'start':leftTimeDelta, 'end':rightTimeDelta}

		# If the time remaining till the next lecture is less than the 
		# FETCH_INTERVAL, return False along with the remaining time in seconds.
		elif currentTime <= leftTimeDelta and (leftTimeDelta-currentTime).total_seconds() < FETCH_INTERVAL:
			timeRemaining = (leftTimeDelta-currentTime).total_seconds()
			logging.info("Attendance for next lecture to be started in {} seconds.".format(int(timeRemaining)))
			return False, timeRemaining

		else:
			return False, None

	else:
		logging.error('Invalid response from \'{}\''.format(API_GET_SCHEDULE))
		return False, None

# Function to capture images 
def captureImages(imageQueue, shutdownSignal, timeObject):

	logging.info("<Thread 1> Starting the camera")
	try:
		cap = cv2.VideoCapture('/dev/video0')
	except cv2.error as e:
		logging.error("<Thread 1> Caught error: {}".format(e))
		shutdownSignal.value = 1
		return

	cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
	frameRate = cap.get(cv2.CAP_PROP_FPS)
	i = 0
	imageCount = 1
	
	while(datetime.datetime.now() <= timeObject['end'] and cap.isOpened()):
		if shutdownSignal.value == 1:
			break
		ret, frame = cap.read()
		if (ret != True):
			break
		if (i % math.floor(frameRate*IMAGE_CAPTURE_RATE) == 0):
			logging.info("<Thread 1> Captured image {}".format(str(imageCount)))
			ret,buf = cv2.imencode('.jpg', frame)
			imageQueue.put(io.BytesIO(buf), block=True)
			imageCount += 1
		i+=1

	cap.release()

def identifyFaces(imageQueue, shutdownSignal, face_client, timeObject):

	global LECTURE_ID

	imageCount = 1

	while(datetime.datetime.now() <= timeObject['end']):
		if shutdownSignal.value == 1:
			break

		img = imageQueue.get(block=True)

		logging.info("<Thread 2> Received image {}".format(str(imageCount)))

		face_ids = []
		try:
			faces = face_client.face.detect_with_stream(img)
		except:
			logging.warning("<Thread 2> Error while detecting faces in image {}".format(str(imageCount)))

		for face in faces:
			face_ids.append(face.face_id)

		if not faces:
			logging.warning('<Thread 2> No faces detected')
		else:
			results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
		
			logging.info('<Thread 2> Identifying faces')
			
			if not results:
				logging.warning('<Thread 2> No person identified')
			for person in results:
				if person.candidates != [] and person.candidates[0].confidence > THRESHOLD:
					objperson = face_client.person_group_person.get(PERSON_GROUP_ID, person.candidates[0].person_id)
					logging.info('<Thread 2> Person is \033[1;32m{} \033[21;0mwith a confidence of \033[1;32m{}.\033[21;0m'.format(objperson.name, person.candidates[0].confidence)) # Get topmost confidence score
					paramsData = {"lecture_id":LECTURE_ID, "roll_number":objperson.name}
					requests.post(url=API_POST_ATTENDANCE, data=paramsData)
		imageCount += 1

# The main function which takes the attendance by running
# two helper funtions in parallel, one which captures pictures and
# other identifies the face from the dataset on the Azure server.
def takeAttendance(timeObject):

	# Make a face_client object by authenticating the endpoint and passphrase.
	# If it fails the funtion will return.
	try:
		logging.info("Configuring and authenticating Face API to create FaceClient object")
		face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
		logging.info("Successfully verified credentials and created FaceClient object")
	except Error as e:
		logging.critical("Caught error:\n{}".format(e))
		logging.error("Cannot authenticate the Azure Face Service.")
		return

	# Get the training status of the model on the server.
	training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
	logging.info("Training status of the model: {}.".format(training_status.status))

	# The queue is a multiprocessing object which can be accessed by
	# multiple processes while being ensured of synchronisation.
	# The imageCapture thread clicks pictures that are pushed to the thread and
	# the identifyFace threads reads the images on the other end from the 
	# queue to complete the process of face recognition.
	imageQueue = Queue()
	shutdownSignal = Value('i', 0)
	capImg = Process(target=captureImages, args=([imageQueue, shutdownSignal, timeObject]))
	idnFce = Process(target=identifyFaces, args=([imageQueue, shutdownSignal, face_client, timeObject]))

	logging.info("Starting image capturing thread.")
	capImg.start()
	logging.info("Starting the face detection and identification thread")
	idnFce.start()
	
	# Wait for the threads to complete their execution.
	logging.info("Waiting for the threads to complete.")
	capImg.join()
	idnFce.join()
	logging.info("Threads joined successfully.")
	imageQueue.close()

# Main function, handling the checking and taking attendance.
def main():

	logging.info("Process started on device")

	# Flag to indicate if a attendance process is already running.
	takingAttendance = False

	while True:

		# fetchAndCheck method returns two objects: a boolean and a time object.
		startAttendance, timeObject = fetchAndCheck()

		# If the current time is in the interval window of the scheduled time,
		# Attendance marking process will start.
		if startAttendance:

			# Check if another process is already running and if running,
			# wait for 2 minutes and check again until previous process finshes.
			while takingAttendance:
				logging.warning("Another process running taking attendance.")
				logging.info("Process will wait for 2 minutes.")
				time.sleep(120)
				
			takingAttendance = True

			logging.info("Attendance marking started.")
			logging.info("Attendance to be taken from {} till {}".format(timeObject['start'], timeObject['end']))
			
			# Make a separate process to mark attendance, meanwhile the original
			# process will keep running its usual routine, i.e. sleeping for FETCH_INTERVAL
			# and again checking for lecture schedule.
			childPID = os.fork()

			# Child process will have a 'ZERO' childPID value whereas parent process will
			# have the process ID of the child in the childPID.
			if not childPID:

				takeAttendance(timeObject)
				
				logging.info("Process tasked with taking attendance is exiting")
				takingAttendance = False					# Reset the flag.
				exit()
			else:
				logging.info("Process going to sleep for {} seconds".format(SLEEP_INTERVAL))
				time.sleep(SLEEP_INTERVAL)

		# If the current time is out of the window for taking attendance for 
		# a particular lecture and if the timeObject has a time value which is 
		# the time in seconds before the process needs to start taking attendance,
		# the process will sleep for given time.			
		elif timeObject:
				time.sleep(timeObject)

		else:
			logging.info("Process will check again in {} seconds for schedule".format(FETCH_INTERVAL))
			time.sleep(FETCH_INTERVAL)


if __name__== '__main__' :

	# Fetch current time from the server and set the local
	# time equal to the fetched time formatted appropriately.
	currentTimeData = requests.get(url=API_GET_CURRENT_TIME).json()
	currentTimeData = currentTimeData['current_time'].replace('T', ' ')
	os.system("sudo timedatectl set-time '{}'".format(currentTimeData[:-7]))
	main()
