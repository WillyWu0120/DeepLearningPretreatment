import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from tensorflow.keras.utils import to_categorical

gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)


class Network:
    def __init__(self) -> None:
        self.model = Sequential()
        self.model.add(Conv2D(filters=32, kernel_size=(3, 3),
                              input_shape=(100, 50, 1), activation='relu',
                              padding='same'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(filters=64, kernel_size=(3, 3),
                              activation='relu', padding='same'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Flatten())
        self.model.add(Dropout(0.2))
        self.model.add(Dense(1024))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(5, activation='softmax'))
        self.model.compile(optimizer='adam', loss='categorical_crossentropy',
                           metrics=['accuracy'])
        print(self.model.summary())

    def load_data(self):
        # 載入資料集
        self.dataset = np.load('data.npz')
        self.train_images, self.test_images, self.train_labels, self.test_labels = train_test_split(
            self.dataset['images'], self.dataset['duration'], test_size=0.33, )
        self.preprocessing()

    def load_weights(self, path):
        self.model.load_weights(path)

    def save_weights(self, path):
        self.model.save_weights(path)

    def preprocessing(self):
        # 資料前處理
        self.train_images = self.train_images.astype('float32') / 255
        self.train_images = self.train_images.reshape(
            self.train_images.shape+(1, ))
        self.test_images = self.test_images.astype('float32') / 255
        self.test_images = self.test_images.reshape(
            self.test_images.shape+(1, ))
        self.train_labels = to_categorical(self.train_labels, 5)
        self.test_labels = to_categorical(self.test_labels, 5)

    def train(self):
        # 訓練階段
        self.model.fit(self.train_images,
                       self.train_labels, epochs=30, batch_size=50)

    def evaluate(self):
        # 測試階段
        test_loss, test_acc = self.model.evaluate(
            self.test_images, self.test_labels)
        print("Test Accuracy:", test_acc)


if __name__ == '__main__':
    network = Network()
    network.load_data()
    network.train()
    # network.load_weights('./checkpoints/checkpoint')
    network.evaluate()
    network.save_weights('./checkpoints/checkpoint')
