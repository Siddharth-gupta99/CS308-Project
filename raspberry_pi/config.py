#v=01

# =========================================================================
# !! IMPORTANT !!
# Do not change the first line of this config.py file.
# Doing so may result in errors during the starting of process.
# It is to keep track of changes in the config file 
# locally versus on the server.
# =========================================================================

# Time in seconds to wait between successive requests to the server.
# This wait interval is only used when the time to the latest upcoming
# lecture is greater then this interval.
FETCH_INTERVAL = 600

# Time in seconds to wait before checking for the next scheduled class.
# This wait interval is used when the current time is in the given
# range of the scheduled time and the system starts the attendance process.
SLEEP_INTERVAL = 3600

# Time before the scheduled time from which the system should start
# the attendance process.
CLASSTIME_LEFT_MARGIN = {'hour':0, 'minute':10, 'second':0}

# Time after the scheduled time upto which the system should continue
# the attendance process. After this time the attendance marking will
# stop and next schedule will be fetched after the system wakes up. 
CLASSTIME_RIGHT_MARGIN = {'hour':0, 'minute':2, 'second':0}

# --------------------------------------------------------------------------
# Time in seconds between successive captures of images while
# the attendance process is running.
IMAGE_CAPTURE_RATE = 5

# --------------------------------------------------------------------------
# API Endpoint to get the current time.
API_GET_CURRENT_TIME = 'http://10.8.12.183:8000/api/lecture/current-time'

# API Endpoint to get the schedule using GET request.
API_GET_SCHEDULE = 'http://10.8.12.183:8000/api/lecture/'

# API Endpoint to submit the identified students' information using
# POST request.
API_POST_ATTENDANCE = 'http://10.8.12.183:8000/api/lecture/s'

# --------------------------------------------------------------------------
# Format in which the time is sent from the server
FETCH_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+05:30'

# --------------------------------------------------------------------------
# Endpoint of the Microsoft Azure Face Service to be used.
ENDPOINT = 'https://shreyanshkulsface.cognitiveservices.azure.com/'

# Key for the Microsoft Azure Face Service to be used.
KEY = '010e13de1bc946e2b83d2363f6c640ae'

# Person group ID for the dataset on the Microsoft Azure Face Service Server.
PERSON_GROUP_ID = 'my-unique-person-group'

# Threshold of confidence for a student to be identified and
# his/her attendance getting marked.
THRESHOLD = 0.4
