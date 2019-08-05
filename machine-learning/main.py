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
trainer = train.Train(net, mnist_test_data, False)
trainer.training(mnist_training_data, 5)

# change test data background color
# 0 = black
# 1 = white
background = 1.0
image, label = mnist_test_data
changed_test_image = []
size = len(image)
for i in range(size):
    img = image[i].copy()
    # loop through each point of the image
    for k in range(len(img)):
        if img[k] <= background:
            img[k] = background
    changed_test_image.append(img)
#changed_test_data = (changed_test_image[:100], label[:100])

# print the first 100 images
display = "image-"+str(background)
'''
printer = imagePrinter.ImagePrinter((1,10),display)
for i in range(10):
    printer.addImagePair(test_image[i], changed_test_image[i])
printer.printHorizontal()
'''
'''
# change changed_test_data to the required format for Network object to test
test_inputs = [np.reshape(x, (784, 1)) for x in changed_test_data[0]]
changed_test_data = zip(test_inputs, changed_test_data[1])


changed_test_data = list(changed_test_data)
print("background {} : {} / {}".format(background,
      net.evaluate(changed_test_data),len(changed_test_data)))
'''
size = 1
ok = 0
notOk = 0
cnt = [0,0,0,0,0,0,0,0,0,0]

for k in range(0,10000):
        img = changed_test_image[k*size:k*size+size]
        lbl = label[k*size:k*size+size]
        changed_test_data = (img, lbl)
        trainer.evaluate(changed_test_data, background, display)
        for result in trainer.sortResults():
                if(0 != result['count']):
                        cnt[int(lbl)] += 1
                        ok += 1
                else:
                        notOk += 1
'''
for k in range(0,10000):
        count = -1
        for i in range(0,2):
                img = changed_test_image[k*size:k*size+size]
                lbl = label[k*size:k*size+size]
                changed_test_data = (img, lbl)
                trainer.evaluate(changed_test_data, background, display)
                for result in trainer.sortResults():
                        if (count == -1):
                                #print("**** {} {} {} {}".format(k, i, result['count'], count))
                                count = result['count']
                        else:
                                if(count != result['count']):
                                        print("{}, {}, {} : {} / {}".format(k, i, count, result['count'], result['sample']))
                                else:
                                        if(count == 0):
                                                notOk += 1
                                        else:
                                                print(lbl)
                                                ok += 1
                                                '''
print(cnt)
print("ok:{} notOk:{}".format(ok, notOk))
