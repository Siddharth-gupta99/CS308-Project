import requests
import os
import subprocess

checkURL = "http://students.iitmandi.ac.in/~b17062/API/generic/path/endpoint1/updateConfig.php"
configFile = None

def checkServer():
	returnData = requests.post(url=checkURL, data={"passphrase":"h23a0ec924"})
	returnData = returnData.json()
	return returnData['returnURL']

def updateConfigFile(returnURL):
	newData = requests.post(url=returnURL, data={'passphrase':'a71a3bd277'})
	newData = newData.json()

	with open('config.py', 'r') as configFile:
		firstLine = configFile.readline()

	version = firstLine[3:].rstrip('\n')
	print(version, newData['version'])
	
	if newData['version'] == version:
		print("No")
		return
	else:
		print("Yes")
		with open('config.py', 'w') as configFile:
			configFile.write(newData['content'])

def main():
	returnURL = checkServer()
	if returnURL != None:
		updateConfigFile(returnURL)
	subprocess.check_call(['python', 'face-service-daemon.py'])
	# exec(open('face-service-daemon.py').read())

if __name__== '__main__' :
	main()
