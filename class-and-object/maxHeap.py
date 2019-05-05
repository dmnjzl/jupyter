#MaxHeap class from Lab 3
class MaxHeap(object):
    def __init__(self,data=[]):
        # constructor - empty array
        self.data = data

    def isEmpty(self):
        # return true if maxheaph has zero elements
        return(len(self.data)==0)

    def getSize(self):
        # return number of elements in maxheap
        return(len(self.data))

    def clear(self):
        # remove all elements of maxheap
        self.data=[]

    def printout(self):
        # print elements of maxheap
        print (self.data)

    def getMax(self):
        # return max element of maxHeap
        # check that maxHeaph is non-empty
        if (not self.isEmpty()):
            return(max(self.data))
        else:
            return None

    #helper method for add(newEntry) and removeMax()
    #swap elements so parent node is greater than both its children
    #if swap made, call heapify on swapped child

    def heapify(self, parentIndex):
        #given parentIndex, find left and right child indices
        child1Index = parentIndex*2+1
        child2Index = parentIndex*2+2
        largest=parentIndex

        # check if left child is larger than parent
        if (child1Index < len(self.data)) and (self.data[child1Index] > self.data[parentIndex]):
            largest = child1Index

        # check if right child is larger than the max of left child
        # and parent
        if (child2Index < len(self.data)) and (self.data[child2Index] > self.data[largest]):
            largest = child2Index

        # if either child is greater than parent:
            # swap child with parent
        if (largest != parentIndex):
            self.data[largest], self.data[parentIndex] = self.data[parentIndex], self.data[largest]
            self.heapify(largest)

        # call heapify() on subtree

    def buildHeap(self, A):
        # build maxheap, calling heapify() on each non-leaf node
        self.data = A
        for i in range((len(A)-1)//2, -1, -1):
            self.heapify(i)


    def removeMax(self):
        # remove root node, call heapify() to recreate maxheap
        if (not self.isEmpty()):
            maxVal = self.data[0]

            if (len(self.data)>1):
                self.data[0] = self.data[len(self.data)-1]

                # remove last element
                self.data.pop()
                self.heapify(0)

            else:
                self.data.pop()
            return maxVal
        else:
            return None


