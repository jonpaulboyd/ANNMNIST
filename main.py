from keras.datasets import mnist
from keras import models
from keras import layers
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import time
from contextlib import contextmanager


@contextmanager
def timer(title):
    t0 = time.time()
    yield
    print('{} - done in {:.0f}s'.format(title, time.time() - t0))


class MnistDigits:

    def __init__(self):
        self.train_images = None
        self.train_labels = None
        self.test_images = None
        self.test_labels = None
        self.network = None
        self.test_loss = None
        self.test_acc = None

    def load_data(self):
        (self.train_images, self.train_labels), (self.test_images, self.test_labels) = mnist.load_data()
        print(self.train_images.ndim)   # 3D tensor
        print(self.train_images.dtype)  # Data type uint3
        print(self.train_images.shape)  # array of 60000 matrices of 28x28 integers
        print(len(self.train_labels))
        print(self.test_images.shape)
        print(len(self.test_labels))

    def build_network(self):
        # Network architecture
        self.network = models.Sequential()
        self.network.add(layers.Dense(512, activation='relu', input_shape=(28*28,)))
        self.network.add(layers.Dense(10, activation='softmax'))

        # Compilation
        self.network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

        # Prepare data by reshaping as network expects, and scale 0-1
        self.train_images = self.train_images.reshape((60000, 28 * 28))
        self.train_images = self.train_images.astype('float32') / 255
        self.test_images = self.test_images.reshape((10000, 28 * 28))
        self.test_images = self.test_images.astype('float32') / 255

        # Encode labels
        self.train_labels = to_categorical(self.train_labels)
        self.test_labels = to_categorical(self.test_labels)

        # Train network with fit
        self.network.fit(self.train_images, self.train_labels, epochs=5, batch_size=128)

    def evaluate_network(self):
        self.test_loss, self.test_acc = self.network.evaluate(self.test_images, self.test_labels)
        print('Loss {}\t\tAccuracy {}'.format(self.test_loss, self.test_acc))

    def viz_samples(self):
        for i in range(10):
            digit = self.train_images[i]
            plt.imshow(digit, cmap=plt.cm.binary)
            plt.show()

    def viz_sample_slicing(self):
            # Full digit
            digit = self.train_images[7]
            print(digit.shape)
            plt.imshow(digit, cmap=plt.cm.binary)
            plt.show()

            # Tensor slicing for top left 15x15
            digit = self.train_images[7, :15, :15]
            print(digit.shape)
            plt.imshow(digit, cmap=plt.cm.binary)
            plt.show()

            # Tensor slicing for top right 15x15
            digit = self.train_images[7, :15, 15:]
            print(digit.shape)
            plt.imshow(digit, cmap=plt.cm.binary)
            plt.show()

            # Tensor slicing for bottom left 15x15
            digit = self.train_images[7, 15:, :15]
            print(digit.shape)
            plt.imshow(digit, cmap=plt.cm.binary)
            plt.show()

            # Tensor slicing for bottom right 15x15
            digit = self.train_images[7, 15:, 15:]
            print(digit.shape)
            plt.imshow(digit, cmap=plt.cm.binary)
            plt.show()

            # Tensor slicing for middle
            digit = self.train_images[7, 7:-7, 7:-7]
            print(digit.shape)
            plt.imshow(digit, cmap=plt.cm.binary)
            plt.show()


def main():
    mnistdigits = MnistDigits()
    with timer('Loading Data'):
        mnistdigits.load_data()
    with timer('Visualize Samples'):
        mnistdigits.viz_samples()
    with timer('Vis Sample Slicing'):
        mnistdigits.viz_sample_slicing()
    with timer('Building Network'):
        mnistdigits.build_network()
    with timer('Evaluating Network'):
        mnistdigits.evaluate_network()


if __name__ == '__main__':
    with timer('Main'):
        main()

