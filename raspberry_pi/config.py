#v=01

RASPBERRY_PI_ID = 1
CLASSROOM_ID = 1

FETCH_INTERVAL = 600 # Seconds
SLEEP_INTERVAL = 2400 # Seconds
CLASSTIME_LEFT_MARGIN = {'hour':0, 'minute':20, 'second':0}
CLASSTIME_RIGHT_MARGIN = {'hour':0, 'minute':60, 'second':0}

IMAGE_CAPTURE_RATE = 3 # Seconds delay

API_GET_SCHEDULE = 'https://students.iitmandi.ac.in/~b17062/API/generic/path/endpoint1/index.php'
API_POST_ATTENDANCE = 'https://students.iitmandi.ac.in/~b17062/API/generic/path/endpoint1/post.php'
API_POST_ERROR = 'http://students.iitmandi.ac.in/~b17062/API/generic/path/endpoint1/index.php'

FETCH_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

ENDPOINT = 'https://westcentralus.api.cognitive.microsoft.com/'
KEY = 'abddb967436d4acea1a3fd149d3ad3d1'
PERSON_GROUP_ID = 'my-unique-person-group'
THRESHOLD = 0.6
