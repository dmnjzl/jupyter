import imagePrinter
import numpy as np
import mnist

'''
Prepare data for network training and image display
'''
def prepare_data(mnist_training_data, mnist_test_data) :
    # change MNIST data to the required format for Network object to use
    training_data, test_data = change_data_format(
        mnist_training_data, mnist_test_data)
    return (training_data, test_data)

'''
Print and save the first 100 images
'''
def print_first_100_images(training_data, test_data, background):
    printer = imagePrinter.ImagePrinter((10,10),"image-"+str(background))
    training_images, training_labels = training_data
    test_images, test_labels = test_data
    for i in range(100):
        printer.addImagePair(training_images[i], test_images[i])
    printer.printHorizontal('original and test data')

def select_image(src, nmbr):

    x, y = src
    x1 = []
    size = len(x)
    cnt = 0
    for i in range(size):
        if y[i] == nmbr and cnt < 100:
            img = x[i].copy()
            cnt += 1
            x1.append(img)
    return x1

"""
Revert the grayscale of an image
Used for creating test data
src: (images, labels)
"""
def revertSample(src):
    x, y = src
    x1 = revertData(x)
    return (x1,y)

"""
Used for creating test data and print image
"""
def revertData(x):
    x1 = np.array(x)
    # y is an element based on the first dimention of X1
    x2 = [1 - y for y in x1]
    return x2

"""
Change image background color
Used for creating test data
src: (images, labels)
"""
def changeBackgroundSample(src, background):
    if(background == 1):
        return revertSample(src)
    x, y = src
    x1 = changeBackgroundData(x, background)
    return (x1,y)

"""
Used for creating test data and print image
"""
def changeBackgroundData(x,background):
    if(background == 1):
        return revertData(x)
    x1 = []
    size = len(x)

    for i in range(size):
        img = x[i].copy()
        # loop through each point of the image
        for k in range(len(img)):
            if img[k] < background:
                img[k] = background
#            img[k] = 1 - img[k]
        x1.append(img)
    return x1

"""
Randomly select image pair using image.ImagePrinter:
one from origin and one from modified based on index

Requirement: origin and modified must have the same size and the same order
For example, if origin[index] represents 6, then modified[index] must also represnet 6
"""
def extractImage(origin, modified, file="image"):
    printer = imagePrinter.ImagePrinter((10,10),0.5,file)
    imgSrc = origin
    imgTest = modified
    size = len(imgSrc)
    print("sample size = %d"%size)
    display_index = printer.displayIndexes(size)
    cnt = 0
    for i in range(size):
#        assert(labelSrc[i] != labelSrc[i]), "labelSrc=%d, labelTest=%d" % (labelSrc[i],labelTest[i])
        if display_index[i] > 0:
            cnt += 1
            printer.addImagePair(imgSrc[i], imgTest[i])
    print("select images = %d" % (cnt))
    printer.printImg()

"""
Select subarray of size from MNIST images and labels
Convert them from 3D to 2D for nueral networks machine learning using "sklearn" package
"""
def mnistConv(src_images, src_labels):
    size = src_labels.size
    #imgs = np.zeros((size, 28*28), np.float)
    imgs = np.reshape(src_images[0:size,:,:],(size,28*28))
    #for i in range(size):
    #    imgs[i,:] = _imgs[i,:]/255
    imgs = imgs/255
    return (imgs, src_labels)

def subSample(src_images, src_labels, size):
    if(size > src_labels.size):
        size = src_labels.size

    # select the first 'size' elements according to the first dimention
    labels = src_labels[0:size]
    images = src_images[0:size]
    
    return(images, labels)
    
def load_mnist():
    """ divide MNIST training data (60000) into training data (50000) and validation data (10000)"""
    trn_images = mnist.train_images()
    trn_labels = mnist.train_labels()
    tst_images = mnist.test_images()
    tst_labels = mnist.test_labels()
    #print("training data shape: (%d, %d, %d)" % trn_images.shape)
    #print("training label shape: (%d, )" % trn_labels.shape)
    #print("test data shape: (%d, %d, %d)" % tst_images.shape)
    #print("test label shape: (%d, )" % tst_labels.shape)

    trn_images, trn_labels = mnistConv(trn_images, trn_labels)
    tst_images, tst_labels = mnistConv(tst_images, tst_labels)
    val_images = trn_images[50000:,:]
    val_labels = trn_labels[50000:]
    trn_images = trn_images[0:50000,:]
    trn_labels = trn_labels[0:50000]
    
    print("MNIST data loading completed.")
    return ((trn_images, trn_labels), (val_images, val_labels), (tst_images, tst_labels))

def load_data():
    """Return a tuple containing ``(training_data, validation_data,
    test_data)``. Based on ``load_data``, but the format is more
    convenient for use in our implementation of neural networks.
    In particular, ``training_data`` is a list containing 50,000
    2-tuples ``(x, y)``.  ``x`` is a 784-dimensional numpy.ndarray
    containing the input image.  ``y`` is a 10-dimensional
    numpy.ndarray representing the unit vector corresponding to the
    correct digit for ``x``.
    ``validation_data`` and ``test_data`` are lists containing 10,000
    2-tuples ``(x, y)``.  In each case, ``x`` is a 784-dimensional
    numpy.ndarry containing the input image, and ``y`` is the
    corresponding classification, i.e., the digit values (integers)
    corresponding to ``x``.
    Obviously, this means we're using slightly different formats for
    the training data and the validation / test data.  These formats
    turn out to be the most convenient for use in our neural network
    code."""
    tr_d, va_d, te_d = load_mnist()
    """ tr_d, va_d and te_d are tuples in format (images, labels)
        where 
            images is an array of [images][bytesPerImage]
            labels is an array of [labels]
        and images and labels have the same size
    """
    # The next line of code converts a numpy.ndarray (50000, 784)
    # to a python list (50000) with each element is a numpy.ndarray (784,1)
    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    # The next line of code converts a numpy.ndarray (50000,)
    # to a python list (50000) with each element is a numpy.ndarray (10,1)
    training_results = [vectorized_result(y) for y in tr_d[1]]
    # zip to two lists 
    training_data = zip(training_inputs, training_results)
    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_data = zip(validation_inputs, va_d[1])
    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = zip(test_inputs, te_d[1])
    return (training_data, validation_data, test_data)

'''
This function does the same work as load_data. 
But instead of using load_mnist() to get mnist data
they are passed in as parameters
'''
def change_data_format(tr_d, te_d ):
    """ tr_d, va_d and te_d are tuples in format (images, labels)
        where 
            images is an array of [images][bytesPerImage]
            labels is an array of [labels]
        and images and labels have the same size
    """
    # The next line of code converts a numpy.ndarray (50000, 784)
    # to a python list (50000) with each element is a numpy.ndarray (784,1)
    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    # The next line of code converts a numpy.ndarray (50000,)
    # to a python list (50000) with each element is a numpy.ndarray (10,1)
    # NOTE: Training label format changed: from a number to an array of 10
    training_results = [vectorized_result(y) for y in tr_d[1]]
    # zip to two lists 
    training_data = zip(training_inputs, training_results)

    #validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    #validation_data = zip(validation_inputs, va_d[1])

    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = zip(test_inputs, te_d[1])
    return (training_data, test_data)

def vectorized_result(j):
    """Return a 10-dimensional unit vector with a 1.0 in the jth
    position and zeroes elsewhere.  This is used to convert a digit
    (0...9) into a corresponding desired output from the neural
    network."""
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e
    