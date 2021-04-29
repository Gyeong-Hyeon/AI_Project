import numpy as np
import cv2
from keras.preprocessing import image
import time

#-----------------------------
#opencv initialization

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#-----------------------------
#face expression recognizer initialization
from keras.models import model_from_json
model = model_from_json(open("./models/facial_expression_model_structure.json", "r").read()) #use another model
model.load_weights('./models/facial_expression_model_weights.h5') #use another weight
#-----------------------------

emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')

cap = cv2.VideoCapture('./test/testvideo/opening.mp4') #process videos
#cap = cv2.VideoCapture(0) #process real time web-cam
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # or cap.get(3)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc('M','J','P','G') #codec
out = cv2.VideoWriter('./test/output/opening_out.avi', fourcc, fps, (int(width), int(height)))

frame = 0

while(True):
    ret, img = cap.read()
    
    img = cv2.resize(img, (640, 360))
    img = img[0:308,:]
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x,y,w,h) in faces:
        if w > 5: #trick: ignore small faces
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #draw rectangle to main image
            
            detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face
            detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
            detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48
            
            img_pixels = image.img_to_array(detected_face)
            img_pixels = np.expand_dims(img_pixels, axis = 0)
            
            img_pixels /= 255 #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]
            
            predictions = model.predict(img_pixels) #store probabilities of 7 expressions
            
            #find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
            max_index = np.argmax(predictions[0])
            
            emotion = emotions[max_index]
            
            #write emotion text above rectangle
            cv2.putText(img, emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
					
			#-------------------------
    out.write(img)
    cv2.imshow('img',img)
    
    frame = frame + 1
	#print(frame)
	
	#---------------------------------        
    if cv2.waitKey(1) & 0xFF == ord('q'): #press q to quit
        break

#kill open cv things
cap.release()
out.release()
cv2.destroyAllWindows()