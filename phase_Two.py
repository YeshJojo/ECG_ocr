#!/usr/bin/env python


import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')
# get_ipython().run_line_magic('pylab', 'inline')
# get_ipython().run_line_magic('config', "InlineBackend.figure_formats = ['retina']")
from imutils import paths
import time  # time1 = time.time(); print('Time taken: {:.1f} sec'.format(time.time() - time1))

SEED = 71
import cv2
import pickle
import warnings

warnings.filterwarnings("ignore")
from statistics import mean, median
import xlsxwriter


## to plot graph using x_list and y_list
def show_graph(x_list, y_list, width, height):
    """ x_list, y_list = x- & y-coordinates to plot
        width, height = size of plot
    """
    plt.figure(figsize=[width, height])  # [width, height]
    plt.scatter(x_list, y_list, marker='.', s=5)
    plt.show()
    return


def extract_feat(image, begin, end):
    """ image = image to read pixel
        begin = start index (include) of x-coordinate 
        end = end+1 index (exclude) of x-coordinate
        returns a list of y-coordinates & summary statistics 
    """
    # (i) to extract y-coordinates
    x_list, y_list = [], [350]  # boundary condition for y_list, padding average value 350
    for x in np.arange(begin, end, 1):
        # x_list.append(x-begin)   # output x will range from 0 to 159
        for y in np.arange(0, 750, 1):
            if np.all(image[y][x] == (0, 0, 0)):  # look for black dot
                y_list.append(750 - y)  # invert the graph, so the origin becomes bottom left
                break
            if y == 749:  # if there is no black dot in the column, append previous point
                y_list.append(y_list[x - begin])
    y_list.pop(0)  # remove boundary condition for y_list, index 0 (ie, 350)
    # show_graph(x_list, y_list, 2, 2)   #need x_list

    # (ii) to extract summary statistics, ie, min, mean, median, max
    y_list.extend(find_stats(y_list, 0, 40))  # quardrant 1
    y_list.extend(find_stats(y_list, 40, 80))  # quardrant 2
    y_list.extend(find_stats(y_list, 80, 120))  # quardrant 3
    y_list.extend(find_stats(y_list, 120, 160))  # quardrant 4
    y_list.extend(find_stats(y_list, 0, 80))  # segment 1 (quardrant 1&2)
    y_list.extend(find_stats(y_list, 40, 120))  # segment 2 (quardrant 2&3)
    y_list.extend(find_stats(y_list, 80, 160))  # segment 3 (quardrant 3&4)

    return y_list


## to extract summary statistics from y-coordinates in given range, ie, min, mean, median, max
def find_stats(y_list, begin, end):
    """ y_list = given list to look for statistics
        begin = start index (include) of list
        end = end index+1 (exclude) of list
        returns a list [min, mean, median, max]
    """
    temp_list = []
    for i in np.arange(begin, end, 1):
        temp_list.append(y_list[i])
    return [min(temp_list), mean(temp_list), median(temp_list), max(temp_list)]


def mainCall(image):
    # to extract black pixel from the entire image
    # image = cv2.imread()
    time1 = time.time()
    x_list, y_list = [], []
    x_list_rev, y_list_rev = [], []

    for x in np.arange(0, 1733, 1):
        for y in np.arange(0, 257, 1):
            if np.all(image[y][x] == (0, 0, 0)):  # black
                x_list.append(x)
                y_list.append(257 - y)
                break

    for x in np.arange(0, 1733, 1):
        for y in np.arange(0, 257, 1):
            if np.all(image[y][x] == (0, 0, 0)):
                if np.all(image[y + 1][x] != (0, 0, 0)):  # black
                    x_list_rev.append(x)
                    y_list_rev.append(257 - y)

    print('Time taken: {:.1f} sec'.format(time.time() - time1))
    show_graph(x_list, y_list, 18, 3)
    show_graph(x_list_rev, y_list_rev, 18, 3)

    x_list_mean, y_list_mean = [], []
    import statistics
    for (i, j, q, r) in zip(x_list, y_list, x_list_rev, y_list_rev):
        x_list_mean.append(statistics.mean([i, q]))
        y_list_mean.append(statistics.mean([j, r]))

    # show_graph(x_list_mean, y_list_mean, 18, 3)
    workbook = xlsxwriter.Workbook("datasave.xlsx")
    worksheet = workbook.add_worksheet("ECG_data")
    row = 1
    col = 0
    worksheet.write(0, 0, 'x')
    worksheet.write(0, 1, 'y')
    for elementx in x_list_rev:
        worksheet.write(row, col, elementx)
        row += 1

    row = 1
    for elementy in y_list_rev:
        worksheet.write(row, col + 1, elementy)
        row += 1

    workbook.close()
