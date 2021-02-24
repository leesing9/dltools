import numpy
import pandas
from pathlib import Path

dictionary = {0 : [0, 0, 0],
              1 : [1, 1, 1],
              2: [2, 2, 2],
              3 : [3, 3, 3],
              4 : [4, 4, 4],
              5 : [5, 5, 5],
              6 : [6, 6, 6],
              7 : [7, 7, 7],
              8 : [8, 8, 8],
              9 : [9, 9, 9],
              10 : [10, 10, 10],
              11 : [11, 11, 11],
              12 : [12, 12, 12],
              13 : [13, 13, 13],
              14 : [14, 14, 14],
              15 : [15, 15, 15],
              16 : [16, 16, 16],
              17 : [17, 17, 17],
              18 : [18, 18, 18],
              19 : [19, 19, 19],
              20 : [20, 20, 20],
              21 : [21, 21, 21],
              22 : [22, 22, 22],
              23 : [23, 23, 23],
              24 : [24, 24, 24],
              25 : [25, 25, 25],
              26 : [26, 26, 26],
              27 : [27, 27, 27],
}
image = numpy.ones(shape = (28, 28, 3))

def thermal_matching(image, dictionary, outidr, filename):
    for rowIndex in range(image.shape[0]):

        for columnIndex in range(image.shape[1]):

            image[rowIndex, columnIndex, : ] = rowIndex, rowIndex, rowIndex

    image = image.astype('uint32')

    # 온도 - RGB dictionary 찾고 .csv 저장
    temperature = numpy.empty(shape = (image.shape[0], image.shape[1]))

    for rowIndex in range(image.shape[0]):

        for columnIndex in range(image.shape[1]):

            # rgb = image[rowIndex, columnIndex, : ]

            key = [key for key, value in dictionary.items() if value == image[rowIndex, columnIndex, : ].tolist()]
            temperature[rowIndex, columnIndex] = key[0]

    dataFrame = pandas.DataFrame(temperature)

    dataFrame.to_csv(str(Path(outidr)/f'{filename}.csv'), header = False, index = False)