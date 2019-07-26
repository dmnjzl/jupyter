import util
import numpy as np

class Train(object):
    def __init__(self, model):
        self.net = model
        self.results = {}

    def sortResults(self):
        sortedResults = []
        for key in sorted(self.results.keys()):
            sortedResults.append(self.results[key])
        return sortedResults

    def training(self, mnist_training_data, mnist_test_data, epochs=5) :
        # need make copy of data
        # because net.SGD make data set empty.
        training_data = (mnist_training_data[0].copy(), mnist_training_data[1].copy())
        test_data = (mnist_test_data[0].copy(), mnist_test_data[1].copy())
        training_data, test_data = util.change_data_format(training_data, test_data)
        data = list(training_data)
        print("neural network is learning .......")
        count = self.net.SGD(data, epochs, 10, 3.0, test_data=test_data)
        result = {'count':count,'display':'MNIST','sample':len(mnist_test_data[0])}
        self.results[-1] = result
        print("neural network completed learning.")

    def evaluate(self, src_data, background, revert=False):
        display = str(background)
        if(revert):
            display = 'Revert'
        # change changed_test_data to the required format for Network object to test
        test_image = [np.reshape(x, (784, 1)) for x in src_data[0]]
        test_data = zip(test_image, src_data[1])
        count = self.net.evaluate(test_data)
        result = {'count':count,'display':display,'sample':len(src_data[0])}
        if(revert):
            self.results[2] = result
        else:
            self.results[background] = result
        
        print("background {} : {} / {}".format(background,count,len(src_data[0])))

