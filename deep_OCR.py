import matplotlib.pyplot as plt
import numpy as np
import keras_ocr
from PIL import Image
import cv2 as cv


def deepOCR(path):
    detector = keras_ocr.detection.Detector()
    recognizer = keras_ocr.recognition.Recognizer()

    image = keras_ocr.tools.read(path)
    read_image = cv.imread(path)
    read_image = cv.rectangle(read_image, (470, 84), (502, 104), (255, 0, 0))
    data_extract = list()
    boxes = detector.detect(images=[image])[0]
    predictions = recognizer.recognize_from_boxes(image=image, boxes=boxes)
    # canvas = keras_ocr.detection.drawBoxes(image, boxes,(255,255,255),10)
    for text, box in predictions:
        read_image = cv.rectangle(read_image, (int(box[0][0]), int(box[0][1])), (int(box[2][0]), int(box[2][1])),
                                  (255, 255, 255), -1)
        # plt.annotate(s=text, xy=box[0])
        data_extract.append(text)
        # print(text,end=" ")

    print(data_extract)
    word_counter = 0
    with open("log.txt", 'w') as filehnadler:
        for i in data_extract:
            if word_counter <= 10:
                filehnadler.write(i)
                filehnadler.write(" ")
                word_counter += 1
            else:
                filehnadler.write("\n")
                word_counter = 0

    cv.imwrite('removed.png', read_image)
    cv.imshow('reax', read_image)
    cv.waitKey(0)
    # plt.imshow(canvas)
    # plt.show()
