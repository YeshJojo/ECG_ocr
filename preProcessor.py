import cv2 as cv
import numpy as np
from PIL import Image
import phase_Two


def preProcessor(path):
    # primarly using PIL to reduce the DPI of the image
    image = Image.open(path)
    image.save("stepOne-00.png", dpi=(600, 600))

    # reading again to perform the peration and convertio to grayscale image
    image = cv.imread(path)
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Binary Thresholding to remove grid lines
    # performing an histogram analysis
    # from matplotlib import pyplot as plt
    # historam_analysis = cv.calcHist([gray_image],[0],None,[256],[0,256])
    # plt.plot(historam_analysis)
    # plt.show()

    # thresholding block , to remove background gridlines
    # addaptive gausian thresholding
    ths_image = cv.adaptiveThreshold(gray_image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 13, 60)
    cv.imshow('result1', ths_image)
    cv.waitKey(0)

    # median filtering
    median = cv.medianBlur(ths_image, 1)
    # cv.imshow('median',median)
    # cv.waitKey(0)

    # interpolation to connectet the missing points
    # test5 = cv.resize(test4,(1733,257),fx=0,fy=0,interpolation=cv.INTER_LINEAR)
    # interpolation = cv.resize(median,(1733,257),fx=0,fy=0,interpolation=cv.INTER_NEAREST)
    test5 = cv.resize(median, (1733, 257), fx=0, fy=0, interpolation=cv.INTER_NEAREST)
    # cv.imshow('interpolation',test5)
    # cv.waitKey(0)

    # for removing noice
    _, blackAndWhite = cv.threshold(ths_image, 127, 255, cv.THRESH_BINARY_INV)
    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(blackAndWhite, None, None, None, 8, cv.CV_32S)
    sizes = stats[1:, -1]  # get CC_STAT_AREA component
    test3 = np.zeros((labels.shape), np.uint8)

    for i in range(0, nlabels - 1):
        if sizes[i] >= 3:  # filter small dotted regions
            test3[labels == i + 1] = 255

    test4 = cv.bitwise_not(test3)
    # cv.imwrite('testrun.jpg',test4)
    cv.imshow('test4', test4)
    cv.waitKey(0)

    # interpolation to connectet the missing pixel
    # test5 = cv.resize(test4,(1733,257),fx=0,fy=0,interpolation=cv.INTER_LINEAR)
    # test5 = cv.resize(test4,(1733,257),fx=0,fy=0,interpolation=cv.INTER_NEAREST)
    test5 = cv.resize(test4, (1733, 257), fx=0, fy=0, interpolation=cv.INTER_CUBIC)
    # cv.imshow('test5.png',test5)
    cv.imwrite('test5.jpg', test5)
    cv.waitKey(0)
    phase_Two.mainCall(test5)
