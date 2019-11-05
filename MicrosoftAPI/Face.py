import asyncio, io, glob, os, sys, time, uuid, requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = 'e805c37461b94a17a1135552cb8b40d7'

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

face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
print("Deleted the person group {} from the source location.".format(PERSON_GROUP_ID))
print()

''' 
Create the PersonGroup
'''
# Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
print('Person group:', PERSON_GROUP_ID)
face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

# Define woman friend 
rohit = face_client.person_group_person.create(PERSON_GROUP_ID, "Rohit")
# Define man friend
shreyansh = face_client.person_group_person.create(PERSON_GROUP_ID, "Shreyansh")
# Define child friend
siddharth = face_client.person_group_person.create(PERSON_GROUP_ID, "Siddharth")

'''
Detect faces and register to correct person
'''
# Find all jpg images of friends in working directory
rohit_images = [file for file in glob.glob('*.jpg') if file.startswith("rohit")]
shreyansh_images = [file for file in glob.glob('*.jpg') if file.startswith("shreyansh")]
siddharth_images = [file for file in glob.glob('*.jpg') if file.startswith("siddharth")]

diction = {rohit.person_id: 'Rohit', shreyansh.person_id: 'Shreyansh', siddharth.person_id: 'Siddharth'}

# Add to a woman person
for image in rohit_images:
    w = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, rohit.person_id, w)

# Add to a man person
for image in shreyansh_images:
    m = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, shreyansh.person_id, m)

# Add to a child person
for image in siddharth_images:
    ch = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, siddharth.person_id, ch)

''' 
Train PersonGroup
'''
print()
print('Training the person group...')
# Train the person group
face_client.person_group.train(PERSON_GROUP_ID)

while (True):
    training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
    print("Training status: {}.".format(training_status.status))
    print()
    if (training_status.status is TrainingStatusType.succeeded):
        break
    elif (training_status.status is TrainingStatusType.failed):
        sys.exit('Training the person group has failed.')
    time.sleep(5)

'''
Identify a face against a defined PersonGroup
'''
# Reference image for testing against
# group_photo = '/home/rohitagarwal/Pictures/photos/personal/RohitAgarwal_fb.jpg'
group_photo = '/home/rohitagarwal/Desktop/Academics/5th/LAP_lab/Project/MS_API/Microsoft_Api/face/test-image.jpg'
IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))

# Get test image
test_image_array = glob.glob(os.path.join(IMAGES_FOLDER, group_photo))
image = open(test_image_array[0], 'r+b')

# Detect faces
face_ids = []
faces = face_client.face.detect_with_stream(image)
print(faces)
for face in faces:
    face_ids.append(face.face_id)

# Identify faces
results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
print('Identifying faces in {}')
if not results:
    print('No person identified in the person group for faces from the {}.'.format(os.path.basename(image.name)))
for person in results:
	if person.candidates != []:
	    print('Person for face ID {} is identified in {} with a confidence of {}.'.format(person.face_id, os.path.basename(image.name), person.candidates[0].confidence)) # Get topmost confidence score
	    print(diction[person.candidates[0].person_id])
