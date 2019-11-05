import asyncio, io, glob, os, sys, time, uuid, requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType


# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = 'abddb967436d4acea1a3fd149d3ad3d1'

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "https://westcentralus.api.cognitive.microsoft.com/"

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# Used in the Person Group Operations,  Snapshot Operations, and Delete Person Group examples.
# You can call list_person_groups to print a list of preexisting PersonGroups.
# SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
PERSON_GROUP_ID = 'my-unique-person-group'
# Used for the Snapshot and Delete Person Group examples.
TARGET_PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)

'''
Identify a face against a defined PersonGroup
'''
# Reference image for testing against
group_photo = '/home/rohitagarwal/Desktop/Academics/5th/LAP_lab/Project/MS_API/Microsoft_Api/face/mrinal2.jpg'
IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))

# Get test image
test_image_array = glob.glob(os.path.join(IMAGES_FOLDER, group_photo))
image = open(test_image_array[0], 'r+b')

#-------------------------------------------------------------------------------
# Get the data from MS API 
                # import http.client, urllib.request, urllib.parse, urllib.error, base64

                # headers = {
                #     # Request headers
                #     'Ocp-Apim-Subscription-Key': '{KEY}',
                # }

                # params = urllib.parse.urlencode({
                #     # Request parameters
                #     'start': '{string}',
                #     'top': '1000',
                # })

                # try:
                #     conn = http.client.HTTPSConnection('https://westcentralus.api.cognitive.microsoft.com/')
                #     conn.request("GET", "/face/v1.0/persongroups/{PERSON_GROUP_ID}/persons?%s" % params, "{body}", headers)
                #     response = conn.getresponse()
                #     data = response.read()
                #     print(data)
                #     conn.close()
                # except Exception as e:
                #     print("ROhit")
                #     # print("[Errno {0}] {1}".format(e.errno, e.strerror))

#----------------------------------------------------------------------------

# Train the person group
face_client.person_group.train(PERSON_GROUP_ID)
training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
print("Training status: {}.".format(training_status.status))

# Detect faces
face_ids = []
faces = face_client.face.detect_with_stream(image)
print(faces)
for face in faces:
    print("face is detected!")
    face_ids.append(face.face_id)

# Identify faces
results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
print('Identifying faces in {}')
if not results:
    print('No person identified in the person group for faces from the {}.'.format(os.path.basename(image.name)))
for person in results:
	print("I'm in for loop")
	if person.candidates != []:
	    print('Person for face ID {} is identified in {} with a confidence of {}.'.format(person.face_id, os.path.basename(image.name), person.candidates[0].confidence)) # Get topmost confidence score
	    # print(diction[person.candidates[0].person_id])
	    objperson = face_client.person_group_person.get(PERSON_GROUP_ID, person.candidates[0].person_id)
	    print(objperson.name)
