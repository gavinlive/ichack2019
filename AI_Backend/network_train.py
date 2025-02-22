from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense
from keras.utils import np_utils
import numpy as np
import tensorflow as tf
import imageio

#Starting a tensorflow session with global variables
sess = tf.InteractiveSession()
init_g = tf.global_variables_initializer()
init_l = tf.local_variables_initializer()
sess.run(init_g)
sess.run(init_l)

#Parameters:
pixels1 = 100
pixels2 = 100

#No of training images:
train_im_no = 982
train_type1 = 492   # Training images of type 1
train_type1_loc = "trainingdata/Apple Red 1/"
train_type2 = 490   # Training images of type 2
train_type2_loc = "trainingdata/Banana/"

#No of test images
test_im_no = 330
test_type1 = 164     # Test images of type 1
test_type1_loc = "testdata/Apple Red 1/"
test_type2 = 166     # Test images of type 2
test_type2_loc = "testdata/Banana/"

#No of colours (B/W: 1, RGB: 3)
colours = 3

#Loading training images:
imtrain = np.zeros((train_im_no,pixels1,pixels2,colours))

for i in range(train_type1):
    imtrain[i] = imageio.imread(train_type1_loc + str(i+1) + ".jpg")
for i in range(train_type2):
    imtrain[i+train_type1] = imageio.imread(train_type2_loc + str(i+1) + ".jpg")

#Loading test images:
imtest = np.zeros((test_im_no,pixels1,pixels2,colours))

for i in range(test_type1):
    imtest[i] = imageio.imread(test_type1_loc + str(i+1) + ".jpg")
for i in range(test_type2):
    imtest[i+test_type1] = imageio.imread(test_type2_loc + str(i+1) + ".jpg")

#Defining y_train
y_train = np.zeros(train_im_no)
y_train[train_type1:] = 1 

#Defining y_test
y_test = np.zeros(test_im_no)
y_test[test_type2:] = 1

# Load data
(x_train, y_train), (x_test, y_test) = (imtrain, y_train), (imtest, y_test)

#Format images
x_train = x_train.reshape(train_im_no, pixels1, pixels2, colours)
x_test = x_test.reshape(test_im_no, pixels1, pixels2, colours)
x_train = x_train.astype('float32') #use floats so we can scale below
x_test = x_test.astype('float32')

#Scale inputs to 0-1 rather than 0-255
x_train /= 255
x_test /= 255

# Make labels have one-hot encoding
y_train = np_utils.to_categorical(y_train, 2)
y_test = np_utils.to_categorical(y_test, 2)

# Initialise layers
inputlayer = Input(shape = (pixels1, pixels2, colours))
hidden = Conv2D(32, 8, strides=(1, 1), activation='tanh')(inputlayer)
hidden = MaxPooling2D()(hidden)
hidden = Conv2D(32, 8, strides=(1, 1), activation='tanh')(hidden)
hidden = MaxPooling2D()(hidden)
outputlayer = Flatten()(hidden)
outputlayer = Dense(30, activation='sigmoid')(outputlayer)
outputlayer = Dense(30, activation='sigmoid')(outputlayer)
outputlayer = Dense(2, activation='sigmoid')(outputlayer)

# Make an instance of the model with the above layers, choose its optimizer/loss etc., and train it
model = Model(inputlayer, outputlayer)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=32, epochs=2)

x = tf.placeholder(tf.float32, shape=[pixels1, pixels2, colours])
y = tf.placeholder(tf.float32, shape=[None, 2])

tensor_info_x = tf.saved_model.utils.build_tensor_info(x)
tensor_info_y = tf.saved_model.utils.build_tensor_info(y)

prediction_signature = (
        tf.saved_model.signature_def_utils.build_signature_def(
                inputs={'images': tensor_info_x},
                outputs={'scores': tensor_info_y},
                method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME))

#SAVE MODEL
export_path = 'C:/Users/Tudor Trita/Desktop/ichack2019/AI_Backend/ModelSaved'
print('Exporting trained model to', export_path)
builder = tf.saved_model.builder.SavedModelBuilder(export_path)
builder.add_meta_graph_and_variables(
      sess, [tf.saved_model.tag_constants.SERVING], signature_def_map={'predict_images':prediction_signature})
builder.save()

# Evaluate trained network
score = model.evaluate(x_test, y_test, batch_size=32)
print('Test score:', score[0])
print('Test accuracy:', score[1])

# Make lists of which test images were correct and incorrect
predicted_classes = model.predict(x_test) # lists of probabilities of each class
predicted_classes = [np.argmax(example) for example in predicted_classes] # pick out the associated number
y_test = np.argmax(y_test, axis=1) #undo one-hot encoding on y_test, so we can compare
correct_indices = np.nonzero(predicted_classes == y_test)[0]
incorrect_indices = np.nonzero(predicted_classes != y_test)[0]


sess.close()



# See some incorrectly-classes images
#fig, axes = plt.subplots(nrows=3, ncols=3)
#fig.tight_layout()
#random.shuffle(incorrect_indices)
#for i, incorrect in enumerate(incorrect_indices[:9]):
#    plt.subplot(3,3,i+1)
#    plt.imshow(x_test[incorrect].reshape(pixels1,pixels2), cmap='gray', interpolation='none')
#    plt.title('Predicted %s, Actual %s' %(predicted_classes[incorrect], y_test[incorrect]))
#plt.show()






