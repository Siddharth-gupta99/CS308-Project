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

face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
print("Deleted the person group {} from the source location.".format(PERSON_GROUP_ID))
print()

''' 
Create the PersonGroup
'''
# Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
print('Person group:', PERSON_GROUP_ID)
face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

'''
Detect faces and register to correct person
'''
class dictionary(dict):
    # __init__ function 
    def __init__(self): 
        self = dict() 

    # Function to add key:value 
    def add(self, key, value):
        self[key] = value 

diction = dictionary()
# Find all jpg images of friends in working directory
for student_name in os.listdir('./Dataset'):
    # Define a student friend 
    student = face_client.person_group_person.create(PERSON_GROUP_ID, student_name)
    # Add studentName and corresponding personId i diction
    diction.add(student.person_id ,student_name)
    path = './Dataset' + '/' + student_name
    student_images = student_name + "_images"
    # Take all images of a student in one tensor
    student_images = [file for file in os.listdir(path)]
    print(student_images)
    for image in student_images:
        image_path = path + '/' + image
        w = open(image_path, 'r+b')
        try:
            # Add face to corresponding student
            face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, student.person_id, w)
        except:
            print("NO face is detected ")
        # shreyansh_images = [file for file in glob.glob('*.jpg') if file.startswith("shreyansh")]
        # siddharth_images = [file for file in glob.glob('*.jpg') if file.startswith("siddharth")]

# diction = {rohit.person_id: 'Rohit', shreyansh.person_id: 'Shreyansh', siddharth.person_id: 'Siddharth'}

# Add to a woman person
# for image in rohit_images:
#     w = open(image, 'r+b')
#     face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, rohit.person_id, w)

# # Add to a man person
# for image in shreyansh_images:
#     m = open(image, 'r+b')
#     face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, shreyansh.person_id, m)

# # Add to a child person
# for image in siddharth_images:
#     ch = open(image, 'r+b')
#     face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, siddharth.person_id, ch)

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
