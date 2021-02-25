import numpy as np
import pandas as pd
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
image = np.ones(shape = (28, 28, 3))

def thermal_matching(image, dictionary, outidr, filename):
    for rowIndex in range(image.shape[0]):

        for columnIndex in range(image.shape[1]):

            image[rowIndex, columnIndex, : ] = rowIndex, rowIndex, rowIndex

    image = image.astype('uint32')

    # 온도 - RGB dictionary 찾고 .csv 저장
    temperature = np.empty(shape = (image.shape[0], image.shape[1]))

    for rowIndex in range(image.shape[0]):

        for columnIndex in range(image.shape[1]):

            # rgb = image[rowIndex, columnIndex, : ]

            key = [float(key) for key, value in dictionary.items() if value == image[rowIndex, columnIndex, : ].tolist()]
            temperature[rowIndex, columnIndex] = key[0]

    dataFrame = pd.DataFrame(temperature)

    dataFrame.to_csv(str(Path(outidr)/f'{filename}.csv'), header = False, index = False)

def thermal_matching_v2(image, thermal_dic, outidr, filename):
    mask = np.zeros((*image.shape[:2],1))
    uniq = np.unique(image.reshape((-1,3)), axis=0)
    for rgb in uniq:
        dic_key = '{},{},{}'.format(*list(rgb))
        position = (image==rgb) & (mask==0)
        image = np.where(position, thermal_dic[dic_key],  image)
        mask = np.where(position, 1, mask)

    image = image[:,:,0].squeeze()
    pd.DataFrame(image).to_csv(str(Path(outidr)/f'{filename}.csv'), header = False, index = False)

