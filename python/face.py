from time import perf_counter
import numpy as np
import cv2
import requests

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

def request_task(x):
  
    # r = s.get(f'http://192.168.124.50/5/{x}')
    r = requests.get(f'http://192.168.4.1/?State={x}')

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        roi_gray = gray[y:y+w, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        smile= smile_cascade.detectMultiScale(roi_gray, 1.8, 20)  
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
        for (ex, ey, ew, eh) in smile:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 255), 3)
        try:
            eyeshape=eyes.shape   
        except:
            eyeshape=[]
        try:
            smaileShape=smile.shape
        except:
            smaileShape=[]
    
        if(eyeshape  == (1, 4)and smaileShape   ==  (1, 4) ):
                # x1= " smile and one eye detected"
                true_eye_x=eyes[0][0]+faces[0][0]
                mid=faces[0][0]+faces[0][2]/2
                # print("mid:",mid)
                # print("true_eye_x:",true_eye_x)
                if(true_eye_x>mid):
                    x1= "smile and right eye detected"
                else:
                    x1= "smile and left eye detected"
                
            #set_data("44")
        
        elif(eyeshape==  (2, 4)):
            last_one_eye= perf_counter()
            x1= " two Eyes detected"
            if(smaileShape  ==  (1, 4)):
                x1= "smile detected"

        elif(eyeshape  == (1, 4)):
            # print("************************************************************************************")
            # print("width:",faces[0][2])
            # print("height:",faces[0][3])
            # print("x:",faces[0][0])
            # print("y:",faces[0][1])
            # print("x+width:",faces[0][0]+faces[0][2])
            # print("y+height:",faces[0][1]+faces[0][3])
            # print("x+width/2:",xxxxx)
            # print("y+height/2:",faces[0][1]+faces[0][3]/2)
            # print("width of eye:",eyes[0][2])
            # print("height of eye:",eyes[0][3])
            # print("x of eye:",eyes[0][0])
            # print("y of eye:",eyes[0][1])
            # print("************************************************************************************")
            # time.sleep(2)
            true_eye_x=eyes[0][0]+faces[0][0]
            mid=faces[0][0]+faces[0][2]/2
            # print("mid:",mid)
            # print("true_eye_x:",true_eye_x)
            if(true_eye_x>mid):
                x1= "right eye detected"
            else:
                x1= "left eye detected"
            
            request_task(x1)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()