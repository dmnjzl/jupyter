import util
import numpy as np
import imagePrinter

class Train(object):
    def __init__(self, net, mnist_test_data, showImage=True):
        self.net = net
        self.mnist_test_data = mnist_test_data
        self.results = {}
        self.showImage = showImage

    def sortResults(self):
        sortedResults = []
        for key in sorted(self.results.keys()):
            sortedResults.append(self.results[key])
        return sortedResults

    def training(self, mnist_training_data, epochs=5) :
        # need make copy of data
        # because net.SGD make data set empty.
        training_data = (mnist_training_data[0].copy(), mnist_training_data[1].copy())
        test_data = (self.mnist_test_data[0].copy(), self.mnist_test_data[1].copy())
        training_data, test_data = util.change_data_format(training_data, test_data)
        data = list(training_data)
        print("neural network is learning .......")
        count = self.net.SGD(data, epochs, 10, 3.0, test_data=test_data)
        '''
        if(self.showImage):
            result = {'count':count,'display':'MNIST','sample':len(self.mnist_test_data[0])}
            self.results[-1] = result
            printer = imagePrinter.ImagePrinter((1,10), 'MNIST', 1)
            for i in range(10):
                printer.addImagePair(self.mnist_test_data[0][i], self.mnist_test_data[0][i])
            printer.pilSave(printer.imgTest)
        '''
        print("neural network completed learning.")
        

    def evaluate(self, changed_data, background, display):
        # change changed_test_data to the required format for Network object to test
        test_image = [np.reshape(x, (784, 1)) for x in changed_data[0]]
        test_data = zip(test_image, changed_data[1])
        count = self.net.evaluate(test_data)
        result = {'count':count,'display':display,'sample':len(changed_data[0])}
        if(display.lower() == 'revert'):
            self.results[2] = result
        else:
            self.results[background] = result
        if(self.showImage):
            print("background {} : {} / {}".format(background,count,len(changed_data[0])))
            separator = 1
            if(background == 1):
                separator = 0.5
            printer = imagePrinter.ImagePrinter((1,10), display, separator)
            for i in range(10):
                printer.addImagePair(self.mnist_test_data[0][i], changed_data[0][i])
            # display original and changed images
            printer.printHorizontal()
            # save changed image
            printer.pilSave(printer.imgTest)
        