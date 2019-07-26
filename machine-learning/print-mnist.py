import sys

sys.path.append('./python-lib')
sys.path.append('./python-lib/mnist')

import util
import network
import train
import imagePrinter
import numpy as np

# load MNIST data
mnist_training_data, mnist_validation_data, mnist_test_data = util.load_mnist()

test_image = mnist_test_data[0]

# print the first 100 images
printer = imagePrinter.ImagePrinter((10,10),"image.mnist")
for i in range(100):
    printer.addImagePair(test_image[i], test_image[i])
printer.printFirst('MNIST')
