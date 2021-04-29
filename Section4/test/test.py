import numpy as np
import cv2
from keras.models import load_model
from keras.preprocessing import image
import time
import tensorflow as tf
import yaml

#-----------------------------
#opencv initialization

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#-----------------------------
#face expression recognizer initialization
with open('./models/model_DCNN.yaml', 'r') as f:
	model = tf.keras.models.model_from_yaml(f)
model.load_weights('./models/model_DCNN.h5') #load weights
#-----------------------------

emotions = ('Angry', 'Neutral', 'Surprised', 'Happy', 'Sad')


cap = cv2.VideoCapture('./test/testvideo/neu.gif') #process videos - input your video path
#cap = cv2.VideoCapture(0) #process real time web-cam
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # or cap.get(3)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'DIVX') #codec
out = cv2.VideoWriter('./test/output/neu.avi', fourcc, fps, (int(width), int(height))) #Videowritter- set your videoname_out

frame = 0

while(True):
	ret, img = cap.read()
	
	img = cv2.resize(img, (640, 360))
	img = img[0:308,:]

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for (x,y,w,h) in faces:
		if w > 3: #trick: ignore small faces
			#cv2.rectangle(img,(x,y),(x+w,y+h),(64,64,64),2) #highlight detected face
			
			detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face
			detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
			detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48
			
			img_pixels = image.img_to_array(detected_face)
			img_pixels = np.expand_dims(img_pixels, axis = 0)
			
			img_pixels /= 255 #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]
			
			#------------------------------
			
			predictions = model.predict(img_pixels) #store probabilities of 7 expressions
			max_index = np.argmax(predictions[0])
			
			#background of expression list
			overlay = img.copy()
			opacity = 0.4
			cv2.rectangle(img,(x+w+10,y-25),(x+w+150,y+115),(64,64,64),cv2.FILLED)
			cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)
			
			#connect face and expressions
			cv2.line(img,(int((x+x+w)/2),y+15),(x+w,y-20),(255,255,255),1)
			cv2.line(img,(x+w,y-20),(x+w+10,y-20),(255,255,255),1)
			
			emotion = ""
			for i in range(len(predictions[0])):
				emotion = "%s %s%s" % (emotions[i], round(predictions[0][i]*100, 2), '%')
				
				"""if i != max_index:
					color = (255,0,0)"""
					
				color = (255,255,255)
				
				cv2.putText(img, emotion, (int(x+w+15), int(y-12+i*20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
				
			#-------------------------
	out.write(img)
	cv2.imshow('img',img)
	
	frame = frame + 1
	#print(frame)
	
	#---------------------------------
	
	if frame > 10000:
		break
	
	if cv2.waitKey(1) & 0xFF == ord('q'): #press q to quit
		break

#kill open cv things
cap.release()
out.release()
cv2.destroyAllWindows()