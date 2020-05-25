import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from keras.layers import InputLayer
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.models import Model
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint, EarlyStopping
sys.stderr =stderr

def visible(x):
    model.add(InputLayer(input_shape=(x,x,3)))
    
def convolution(x,y):
    model.add(Convolution2D( filters=x , kernel_size=(y,y), activation='relu' ,padding='same') )

def pooling(x):
    model.add(MaxPooling2D( pool_size=(x,x) ))
    
def flatten():
    model.add(Flatten())

def dense(x):
    model.add(Dense(units=x, activation='relu') )
    
def output(x):
    model.add(Dense(units=x, activation='softmax'))
    
def compiler(x):
    model.compile(optimizer=Adam(learning_rate=x),loss='categorical_crossentropy', metrics=['accuracy'])
    
def train():  
    train_data_dir = 'Faces/train/'
    validation_data_dir = 'Faces/validation/'

    save =sys.stdout
    sys.stdout = open("output.txt","w+")
    train_datagen = ImageDataGenerator(
          rescale=1./255,
          rotation_range=20,
          width_shift_range=0.2,
          height_shift_range=0.2,
          horizontal_flip=True,
          fill_mode='nearest')

    validation_datagen = ImageDataGenerator(
          rescale=1./255,
          rotation_range=20,
          width_shift_range=0.2,
          height_shift_range=0.2,
          horizontal_flip=True,
          fill_mode='nearest')

    # Change the batchsize according to your system RAM
    train_batchsize = 16
    val_batchsize = 10

    global history
    train_generator = train_datagen.flow_from_directory(
            train_data_dir,
            target_size=(64, 64),
            batch_size=1,
            class_mode='categorical',
            shuffle=True)

    validation_generator = validation_datagen.flow_from_directory(
            validation_data_dir,
            target_size=(64, 64),
            batch_size=1,
            class_mode='categorical',
            shuffle=True)
    
    sys.stdout.close()
    sys.stdout = save
    
    checkpoint = ModelCheckpoint("project.h5",
                                 monitor="val_accuracy",
                                 mode="max",
                                 save_best_only = True,
                                 verbose=0)

    earlystop = EarlyStopping(monitor = 'val_accuracy', 
                              min_delta = 0, 
                              patience = 3,
                              verbose = 0,
                              restore_best_weights = True)

    # we put our call backs into a callback list
    callbacks = [earlystop, checkpoint]

    # Note we use a very small learning rate 
    model.compile(loss = 'categorical_crossentropy',
                  optimizer = RMSprop(lr = 0.001),
                  metrics = ['accuracy'])

    nb_train_samples = 1065
    nb_validation_samples = 412
    epochs = 3
    batch_size = 16

    history = model.fit_generator(
        train_generator,
        epochs = epochs,
        callbacks = callbacks,
        validation_data = validation_generator,
        verbose=0)

def tweaker():
    global c
    if c==0 :
        global f
        if (f+1) < len(filter_arr):
            f=f+1
        else :
            c=c+1
    elif c==1 :
        if c2 == 1 :
            f=f-1
        global k
        if (k+1) < len(kernal_arr):
            k=k+1
        else :
            c=c+1
    elif c==2 :
        if c2==1 :
            k=k-1
        global p
        if (p+1) < len(pool_arr):
            p=p+1
        else :
            c=c+1
    elif c==3 :
        if c2 == 1 :
            p=p-1
        global d
        if (d+1) < len(dense_arr):
            d=d+1
        else :
            c=c+1
    elif c==4 :
        if c2 == 1 :
            d=d-1
        global l
        if (l+1) < len(layer_arr):
            l=l+1
        else :
            c=c+1
    elif c==5 :
        if c2 == 1 :
            l=l-1
        global dl
        if (dl+1) < len(dense_layer_arr):
            dl=dl+1
        else :
            c=c+1
    
filter_arr=[32,64,128,256,512]
kernal_arr=[2,3,4,5]
pool_arr=[2,3,4]
dense_arr=[16,32,64,128,256,512]
lr_arr=[0.1,0.01,0.001]
layer_arr=[1,2,3]
dense_layer_arr=[1,2,3,4]
accuracy=[0]
f,k,p,d,l,c,i,dl=0,0,0,0,0,0,1,0

print("\nCurrent Counter 1")
print("Number of Convolutional Layers {}".format(layer_arr[l])) 
print("Number of dense layer {}".format(dense_layer_arr[dl]))
print("Number of Filters {}".format(filter_arr[f]))
print("Size of Kernal {}".format(kernal_arr[k]))
print("Size of Pool {}".format(pool_arr[p]))
print("Size of Dense {}\n".format(dense_arr[d]))
while accuracy[0] < 0.95 and c < 6 :
    model = Sequential()
    visible(64)
    for j in range(layer_arr[l]):
        if (f-j) >= 0 :
            convolution(filter_arr[f-j],kernal_arr[k])
    pooling(pool_arr[p])
    if c > 4 :
        for k in range(layer_arr[l]):
            if (f-j) >= 0 :
                convolution(filter_arr[f-j],kernal_arr[k])
        pooling(pool_arr[p])
    flatten()
    for z in range(dense_layer_arr[dl]):
        if (d-z) >= 0:
            dense(dense_arr[d])
    output(4)
    print(model.summary())
    compiler(0.001)
    train()
    if c < 5:
        print("\n---------------------------------------------------------------------------------------------------------------------------------\nITERATION NUMBER : {}".format(i))
    i=i+1
    accuracy.append(max(history.history['val_accuracy']))
    if accuracy[-1] > accuracy[-2] :
        c2=0
        if c < 6:
            print("Accuracy INCREASED")
            tweaker()
        else :
            break
    else :
        if c < 6 :
            print("Accuracy DECREASED")
        c=c+1
        c2=0
        c2=c2+1
        if c < 6 :
            print("Moving to Counter {}".format(c+1))
            tweaker()
        else :
            dl=dl-1
            break
    
    if c>4 :
        print("Number of Convolutional Layers {}".format(2*layer_arr[l]))
        print("Number of Pooling Layers {}".format(2*1))
    else :
        print("Number of Convolutional Layers {}".format(layer_arr[l]))
        print("Number of Pooling Layers {}".format(1))
    print("Number of Dense Layer {}".format(dense_layer_arr[dl]))
    print("Number of Filters {}".format(filter_arr[f]))
    print("Size of Kernal {}".format(kernal_arr[k]))
    print("Size of Pool {}".format(pool_arr[p]))
    print("Size of Dense {}\n\n".format(dense_arr[d]))
    print(accuracy)