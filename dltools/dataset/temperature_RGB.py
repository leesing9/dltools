import numpy as np
import pandas
from pathlib import Path
from PIL import Image

class RGB:
    def __init__(self, r, g, b) -> None:
        self.key = f'{r},{g},{b}'
        self.val = [r,g,b]

    def __repr__(self) -> str:
        return self.key

    def __iter__(self, *args, **kwds):
        return self.val
        
thermal_dic = {}
t = 0
for r in range(256):
    for b in range(256):
        for g in range(256):
            thermal_dic[RGB(r,g,b)] = t
            t+=1

def thermal_matching(image, thermal_dic, outidr, filename):
    for key, val in thermal_dic:
        np.where(image==val,np.tile(key,3), image)
    image.re
    for rowIndex in range(image.shape[0]):

        for columnIndex in range(image.shape[1]):

            image[rowIndex, columnIndex, : ] = rowIndex, rowIndex, rowIndex

    image = image.astype('uint32')

    # 온도 - RGB dictionary 찾고 .csv 저장
    temperature = numpy.empty(shape = (image.shape[0], image.shape[1]))

    for rowIndex in range(image.shape[0]):

        for columnIndex in range(image.shape[1]):

            # rgb = image[rowIndex, columnIndex, : ]

            key = [key for key, value in thermal_dic.items() if value == image[rowIndex, columnIndex, : ].tolist()]
            temperature[rowIndex, columnIndex] = key[0]

    dataFrame = pandas.DataFrame(temperature)

    dataFrame.to_csv(str(Path(outidr)/f'{filename}.csv'), header = False, index = False)


if __name__ == '__main__':
    path = Path('d:\Capture/P0510-0515_D50_AD30_R0-T26.AVI_20210224_152217.936.png')
    outidr = 'd:/'
    filename = path.stem
    img = Image.open(path)
    thermal_matching(img, thermal_dic,outidr, filename)
    
