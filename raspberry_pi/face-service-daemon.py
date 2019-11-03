from config import *
import asyncio, io, glob, os, sys, time, uuid
import math, datetime, logging
import cv2
import requests
from multiprocessing import Queue, Process
from urllib.parse import urlparse
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, OperationStatusType


logging.basicConfig(\
	format="\033[1m%(asctime)s [%(levelname)-8s]\033[0m %(message)s", \
	level=logging.INFO, \
	datefmt='%Y-%m-%d %H:%M:%S')

TAKE_ATTENDANCE = False
TRY_MAX_COUNT = 5

leftMarginSeconds = CLASSTIME_LEFT_MARGIN['hour']*3600 + CLASSTIME_LEFT_MARGIN['minute']*60 + CLASSTIME_LEFT_MARGIN['second']
rightMarginSeconds = CLASSTIME_RIGHT_MARGIN['hour']*3600 + CLASSTIME_RIGHT_MARGIN['minute']*60 + CLASSTIME_RIGHT_MARGIN['second']

def fetchAndCheck():

	GETparameters = None
	
	for tryCount in range(TRY_MAX_COUNT):
		try:
			logging.info('[{}] Fetching schedule from \'{}\''.format(tryCount+1, API_GET_SCHEDULE))
			nextScheduleTime = requests.get(url=API_GET_SCHEDULE, params=GETparameters)
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
				return
		except ValueError as e:
			logging.error("Caught error: {}".format(e))
			if tryCount < TRY_MAX_COUNT-1:
				logging.info('Trying again in {} seconds'.format((tryCount+1)*5))
				time.sleep((tryCount+1)*5)
			else:
				logging.critical('Cannot parse into JSON. Invalid response from \'{}\''.format(API_GET_SCHEDULE))
				return

	nextScheduleTime = datetime.datetime.strptime(nextScheduleTime['date'], '%Y-%m-%d %H:%M:%S.%f')
	currentTime = datetime.datetime.now()
	leftTimeDelta = nextScheduleTime - datetime.timedelta(seconds=leftMarginSeconds)
	rightTimeDelta = nextScheduleTime + datetime.timedelta(seconds=rightMarginSeconds)

	logging.info('Next class scheduled for {} in classroom ID {}'.format(str(nextScheduleTime), CLASSROOM_ID))
	logging.info('Checking for current time between {} and {} seconds from scheduled time'.format(-leftMarginSeconds, rightMarginSeconds))
	
	return currentTime >= leftTimeDelta and currentTime <= rightTimeDelta

''' 
Error Handling and logging			|
to be done here						|
									V
'''
def captureImages(imageQueue):

	global TAKE_ATTENDANCE
	logging.info("<Thread 1> Starting the camera")
	try:
		cap = cv2.VideoCapture(0)
	except cv2.error as e:
		logging.error("<Thread 1> Caught error: {}".format(e))
		TAKE_ATTENDANCE = False
		return

	frameRate = cap.get(cv2.CAP_PROP_FPS)
	i = 0
	imageCount = 1
	
	while(TAKE_ATTENDANCE and cap.isOpened()):
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

def identifyFaces(imageQueue, face_client):

	global TAKE_ATTENDANCE

	imageCount = 1
	
	while(TAKE_ATTENDANCE):
		img = imageQueue.get(block=True)

		logging.info("<Thread 2> Received image {}".format(str(imageCount)))

		face_ids = []
		try:
			faces = face_client.face.detect_with_stream(img)
		except:
			logging.warning("Error")

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
					requests.post(url=API_POST_ATTENDANCE, data={'classroom_id':CLASSROOM_ID, 'student':objperson.name})
		imageCount += 1


def takeAttendance():

	global TAKE_ATTENDANCE
	# try:
	# 	logging.info("Configuring and authenticating Face API to create FaceClient object")
	# 	face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
	# 	logging.info("Successfully verified credentials and created FaceClient object")
	# except azure.cognitiveservices.vision.face.models._models_py3.APIErrorException as e:
	# 	logging.critical("Caught error:\n{}".format(e))
	# 	requests.post(API_POST_ERROR, data={""})

	logging.info("Configuring and authenticating Face API to create FaceClient object")
	face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
	logging.info("Successfully verified credentials and created FaceClient object")

	training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
	logging.info("Training status of the model: {}.".format(training_status.status))

	TAKE_ATTENDANCE = True
	imageQueue = Queue()
	capImg = Process(target=captureImages, args=([imageQueue]))
	idnFce = Process(target=identifyFaces, args=([imageQueue, face_client]))
	capImg.start()
	idnFce.start()
	capImg.join()
	idnFce.join()
	imageQueue.close()

'''
Upto here				/\
						||
						||
'''
		
def main():

	logging.info("Process started on device-{}".format(RASPBERRY_PI_ID))

	while True:
		scheduleReceived = fetchAndCheck()
		logging.info("Current time in the specified range around the scheduled time: {}".format(scheduleReceived))
		if scheduleReceived:
			scheduleReceived = False
			childPID = os.fork()
			if not childPID:
				takeAttendance()
				logging.info("Child process tasked with taking attendance is exiting")
				exit()
			else:
				logging.info("Parent process will again contact server for schedule in {} seconds".format(SLEEP_INTERVAL))
				time.sleep(SLEEP_INTERVAL)
		else:
			logging.info("Parent process will fetch again from server in {} seconds".format(FETCH_INTERVAL))
			time.sleep(FETCH_INTERVAL)

if __name__== '__main__' :
	main()



# for tryCount in range(TRY_MAX_COUNT):
# 	try:
# 		logging.info('[{}] Establishing connection with \'{}\''.format(tryCount+1, API_BASE_URL))
# 		requests.get(url=API_BASE_URL)
# 		logging.info('Connection established')
# 		break
# 	except requests.exceptions.RequestException as e:
# 		logging.error(e)
# 		if tryCount < TRY_MAX_COUNT-1:
# 			logging.info('Trying again in {} minutes'.format(tryCount+1))
# 			timer.sleep((tryCount+1)*60)
# 		else:
# 			logging.critical('Cannot connect to \'{}\''.format(API_BASE_URL))
# 