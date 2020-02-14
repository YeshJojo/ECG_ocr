# primary imports

import cv2 as cv
import numpy as np
from PIL import Image

# reading the image form the directory
initial_image = cv.imread("stepOne.jpg")
initial_image.save("stepOne-00.png", dpi=(600, 600))
