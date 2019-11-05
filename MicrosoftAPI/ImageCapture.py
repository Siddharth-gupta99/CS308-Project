import os 
import cv2
import time
import math
if not os.path.exists('./Dataset'):
    os.mkdir('./Dataset')




# Check if the webcam is opened correctly
# if not cap.isOpened():
#    raise IOError("Cannot open webcam")

print("------------------------------------------ \n")
print("Instructions : \n")
print("1. Provide your name and enroll number \n")
print("2. Make sure to see towards the web cam when camera is on\n")
print("3. Enter ? if you want to exit in place of name \n" )
print("------------------------------------------ \n")
Num = 1
name = input("Give me your name: ")
while name != "?" :
    Roll_no = input("Give me your Enrollment Number: ")
    Num = 1
    if not os.path.exists('./Dataset/' + Roll_no):
        os.mkdir('./Dataset/' +  Roll_no)
        cap = cv2.VideoCapture(1)
        cap.set(3,1920)
        cap.set( 4,1080)
        framerate = cap.get(cv2.CAP_PROP_FPS)
        i = 1
        while Num < 4 :
            ret, frame = cap.read()
            #cv2.imshow('Camera', frame)
            #cv2.waitKey(0)
            if (i%math.floor(framerate)==0):
                
                #frame = cv2.resize(frame, None, fx=1.0, fy=1.0, interpolation=cv2.INTER_AREA)
                cv2.imwrite('./Dataset/' +  Roll_no + "/" + Roll_no + str(Num) + ".jpg",frame)
                
                print(name+ str(Num))
                Num = Num + 1
            i+=1
        cap.release()
        name = input("\nGive me your name: ")
    else:
        print("Sorry, you are already registered !! \n")
        name = input("Give me your name: ")
        

# cv2.destroyAllWindows()
