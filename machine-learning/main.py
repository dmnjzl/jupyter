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
'''
test_image, test_label = mnist_test_data

# change MNIST data to the required format for Network object to use
training_data, validation_data, test_data = util.change_data_format(
        mnist_training_data, mnist_validation_data, mnist_test_data)
'''
test_image = mnist_test_data[0]

#training_data, test_data = util.prepare_data(mnist_training_data, mnist_test_data)

# create Network model
net = network.Network([784, 30, 10])
trainer = train.Train(net)
trainer.training(mnist_training_data, mnist_test_data, 1)

# change test data background color
# 0 = black
# 1 = white
background = 0.2 
image, label = mnist_test_data
changed_test_image = []
size = len(image)
for i in range(size):
    img = image[i].copy()
    # loop through each point of the image
    for k in range(len(img)):
        if img[k] < background:
            img[k] = background
    changed_test_image.append(img)
changed_test_data = (changed_test_image, label)
'''
# print the first 100 images
printer = imagePrinter.ImagePrinter((10,10),"image-"+str(background))
for i in range(100):
    printer.addImagePair(test_image[i], changed_test_image[i])
printer.printHorizontal('original and test data')
'''
'''
# change changed_test_data to the required format for Network object to test
test_inputs = [np.reshape(x, (784, 1)) for x in changed_test_data[0]]
changed_test_data = zip(test_inputs, changed_test_data[1])


changed_test_data = list(changed_test_data)
print("background {} : {} / {}".format(background,
      net.evaluate(changed_test_data),len(changed_test_data)))
'''
trainer.evaluate(changed_test_data, background)
for result in trainer.sortResults():
        print("{} : {} / {}".format(result['display'], result['count'], result['sample']))


