import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from tensorflow.keras.utils import to_categorical

gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)

# 載入資料集
dataset = np.load('data.npz')
train_images, test_images, train_labels, test_labels = train_test_split(dataset['images'], dataset['pitch'], test_size=0.33, )

# 建立卷積神經網路
network = Sequential( )
network.add( Conv2D( filters = 32, kernel_size = ( 3, 3 ), 
	         input_shape = ( 100, 50, 1 ), activation = 'relu', 
	         padding = 'same' ) )
network.add( MaxPooling2D( pool_size = ( 2, 2 ) ) )
network.add( Conv2D( filters = 64, kernel_size = ( 3, 3 ), 
	                 activation = 'relu', padding = 'same' ) )
network.add( MaxPooling2D( pool_size = ( 2, 2 ) ) )	
network.add( Flatten( ) )
network.add(Dropout(0.2))
network.add( Dense( 1024) )
network.add(Activation('relu'))
network.add(Dropout(0.2))
network.add( Dense( 10, activation = 'softmax' ) )
network.compile( optimizer = 'adam', loss = 'categorical_crossentropy', 
	             metrics = ['accuracy'] )
print( network.summary() )
 
# 資料前處理
train_images = train_images.astype( 'float32' ) / 255
train_images = train_images.reshape(train_images.shape+(1, ))
test_images = test_images.astype( 'float32' ) / 255
test_images = test_images.reshape(test_images.shape+(1, ))
train_labels = to_categorical( train_labels )
test_labels = to_categorical( test_labels, 10 )

print(train_labels.shape)
print(test_labels.shape)

# 訓練階段
network.fit( train_images, train_labels, epochs = 30, batch_size = 50 )

# 測試階段
test_loss, test_acc = network.evaluate( test_images, test_labels )
print( "Test Accuracy:", test_acc )
