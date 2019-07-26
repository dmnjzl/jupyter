import sys

for path in sys.path:
    if(path == 'python-lib'):
        import imagePrinter
        printer = imagePrinter.ImagePrinter((10,10),"image.mnist")
