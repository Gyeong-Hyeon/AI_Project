 🔥 Facial Emotion Recognition (FER) using deep learning - Tensorflow 🔥 
===============

<center><img width="300" alt="abouttime" src="https://user-images.githubusercontent.com/75717579/116502006-4b5c7c80-a8ed-11eb-958c-bbf70fc4ba90.gif"></center>

Introduction 🙋
---------------
 This project aims to classify the emotion on a person's face into one of **five categories** - Angry, Neutral, Happy, Surprised, Sad - using several models. The final code in python files is for DCNN model which predicted emotions most correctly on test set.

You can check codes for all models & the details of this project on ```Facial_emotion_recognition.ipynb``` file :)

Dataset 💻
---------------

[Facial Expression Recognition(FER) Challenge](https://www.kaggle.com/ashishpatel26/facial-expression-recognitionferchallenge) - Kaggle

The original dataset has 7 emotions as a label but I reduced it to 5 by combining angry with disgusted and fear with surprised.

Models 👾
---------------
|**Models**|**Train acc**|**Val acc**|**Test acc**|**Macro Avg**|**Learning time**|
|------|---|---|---|---|---|
|T-SNE+SVM|0.34|0.31|0.32|-|3h 45m|
|DCNN|0.76|0.71|0.71|0.70|27m|
|DCNN+LSTM|0.93|0.69|0.68|0.66|40m|
|Mobilenet|0.63|0.60|0.60|0.57|30m|
|VGG+Resnet|0.65|0.61|0.61|0.59|3h 7m|
|Xception|0.73|0.67|0.67|0.65|34m|


About python files 📁
-----------------

* Please run the files at the root folder - ```Section4```
* To install the required packages, run ```pip install -r requirements.txt```
* FER data is saved in data folder. You can change it to any data you want to train the model.
* Train folder has py files related with training models - preprocessing data/ build a model/ training model.
* Test folder has py file to test a video in test/testvideo file.

How to test? 🎯
-----------------

1. Select which type of prediction you want to print on your video.

**VERSION 1)** Draw a square box around the detected faces and print only one label with highest prediction rate > Please use ```videosq.py```file for testing.

<center><img width="300" alt="neu" src="https://user-images.githubusercontent.com/75717579/116504181-ba889f80-a8f2-11eb-9af8-32f4c44417fc.gif"></center>

**VERSION 2)** Print all labels with predicted percentage of each class on a translucent box. > Please use ```test.py```file for testing.

<p align='center'><img width="400" alt="https://user-images.githubusercontent.com/75717579/116504426-3682e780-a8f3-11eb-844a-e4a138b20980.gif"></p>


2. Select a model you want to use.

* If you want to use my model, you can use model_DCNN.yaml and model_DCNN.h5
* If you want to use a model trained from others:
   ```Models``` folder has 2 sample model & weight files. You can use it if you want.
    If you want to use any other model, please save model file & weight file in ```Models``` folder.
    And change the code for loading model and weight (```videosq.py - #14 & #15``` and ```test.py - #16~#18```)

3. Input your video name: ```cv2.VideoCapture('yourvideoname')```

4. Run ```python test/test.py``` or ```python test/videosq.py``` in your terminal

5. Output video will be saved in ```test/output``` folder once the process is finished


How to train? 🤹
------------------

1. Save your data set in ```data``` folder

2. Change ```line#10 of train.py``` to your dataset name

3. Run ```python train/train.py``` in your terminal

4. The CNN model & weight trained by your dataset will be saved in ```models``` folder once training is finished


_Feedback is always welcome_ 🥳

