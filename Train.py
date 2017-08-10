# This code trains the Neural Network and gives an output score.

#All modules
import numpy as np
import os
import cv2
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD,Adagrad
from keras.utils import np_utils
from keras.models import model_from_json
from skimage import io
import cv2
#End of modules


# In[10]:

#All defination goes here
def preprocess(img):
    img = img[80:,:]
    ret,thresh1 = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)
    closing = cv2.pyrDown(closing)
    closing = cv2.pyrDown(closing)
    return closing
    

def get_data():
    path = '/home/srivatsa/Desktop/MachineLearningProject/NNRCar/original_data'
    data_array = []
    label = []
    for i in range(1,9):
        data = os.listdir(path+'/'+str(i))
        for file in data:
            img = cv2.imread(path+'/'+str(i)+'/'+file,0)
            img = preprocess(img)
            print img.shape
            #print img.flatten().shape
            data_array.append(img.flatten())
            if(file[-5]=='f'):
                label.append(0)
            elif(file[-5]=='l'):
                label.append(1)
            else:
                label.append(2)
    return data_array,label
#End of definations


# In[11]:

#Collect Data
print ('Begin data Extraction')
data,label = get_data()
print('End of data Extraction')
data = np.asarray(data, dtype=np.float32)
label = np.asarray(label)


# In[12]:

print('Splitting and Normalizing')
sc = StandardScaler()
data_train, data_test, label_train, label_test = train_test_split( data, label, test_size=0.2, random_state=1)
#data_train_std = sc.fit_transform(data_train)
data_train_std = data_train/255
data_test_std = data_test/255
#data_test_std = sc.transform(data_test)
label_train_ohe = np_utils.to_categorical(label_train)
label_test_ohe = np_utils.to_categorical(label_test)
#Data defined
print('Done')


# In[13]:

import matplotlib.pyplot as plt
from skimage import io
print data_train_std.shape
print data_train_std[16].reshape((20,30))
io.imshow(data_train_std[16].reshape((20,30)))
io.show()


# In[14]:

print('Defining Model')

#Neural Network Model
model = Sequential()
#Input Layer
model.add(Dense(100, input_dim=data_train_std.shape[1], init='uniform'))
model.add(Activation('sigmoid'))
model.add(Dropout(0.3))

#Hidden Layer 1
model.add(Dense(100, init='uniform'))
model.add(Activation('sigmoid'))
model.add(Dropout(0.3))

#Output Layer
model.add(Dense(3, init='uniform'))
model.add(Activation('softmax'))

#Optimizer
sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)

#Final Compiled Model
model.compile(loss='categorical_crossentropy', optimizer=sgd,metrics=['accuracy'])

print('Model Defination Complete')


# In[15]:

print('Fitting Data')

#Fitting
model.fit(data_train, label_train_ohe, nb_epoch=100, batch_size=30, verbose=1,show_accuracy=True,validation_split=0.1)

print('Fitting Complete')

#Checking Accuracy
score = model.evaluate(data_test, label_test_ohe, batch_size=30)
print score


# In[18]:

#Saving the model
print('Saving the model on system: ')

#Serialize model to json
model_json = model.to_json()
with open("model.json","w") as json_file:
    json_file.write(model_json)
    
#Serialize weights to HDF5
model.save_weights("model.h5")
print('Model Saved')
    
    


# In[ ]:



