import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.utils import np_utils

def preprocessing(path):
    df = pd.read_csv(path)
    df.emotion = df.emotion.replace(1,0) #combine label 1&0
    df.emotion = df.emotion.replace(5,2) #combine label 2&5
    df.emotion = df.emotion.replace(6,1) #change label 6 to 1

    #make X data
    img_array = df.pixels.apply(lambda x: np.array(x.split(' ')).reshape(48, 48, 1).astype('float32'))/255
    img_array = np.stack(img_array, axis=0)

    #make Y labels
    le = LabelEncoder()
    img_labels = le.fit_transform(df.emotion)
    img_labels = np_utils.to_categorical(img_labels)

    X_train, X, y_train, y = train_test_split(img_array, img_labels,
                                                        shuffle=True, stratify=img_labels,
                                                        test_size=0.3, random_state=10)
    X_val, X_test, y_val, y_test = train_test_split(X, y,
                                                        shuffle=True, stratify=y,
                                                        test_size=0.5, random_state=10)
    
    return X_train, y_train, X_val, y_val, X_test, y_test

