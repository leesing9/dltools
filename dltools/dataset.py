import random as rd
import numpy as np
import cv2

from datumaro.components.project import ProjectDataset # project-related things
from datumaro.components.extractor import DatasetItem, Bbox, Polygon, AnnotationType, LabelCategories
from tqdm import tqdm
from collections import defaultdict
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import Union
from copy import deepcopy


class customDataset:

    def __init__(self, dataset:ProjectDataset) -> None:
        self.dataset = dataset
        categories = dataset.categories()[AnnotationType.label]
        self._imageDatas = (customDataset.ImageData(item, categories) for item in dataset)

    def drawAndExport(self, lineStyle, cornerStyle):
        for imageData in tqdm(self._imageDatas, total=len(self.dataset)):
            imageData.drawItem(lineStyle, cornerStyle).saveImg()

    class ImageData:
        colorMap = defaultdict(lambda :(rd.randint(0,64)*4+3,rd.randint(0,64)*4+3,rd.randint(0,64)*4+3))
        try:
            with open(str(self.root/'labelmap.txt'),'r', encoding='utf-8') as f:
                labelmap = f.readlines()
            labelmap = [line.split(':')[0] for line in labelmap]
            labelmap = dict([(line[0], line[1]) for line in labelmap])
            colorMap.update(labelmap)
            print(colorMap)
        except:
            print('label color를 임의로 생성합니다.')

        def __init__(self, item:DatasetItem, categories:LabelCategories) -> None:
            self.item = item
            self.lineStyles = ['dot', 'solid']
            self.conerStyles = ['sharp', 'round']
            self.categories = categories
            self.img = item.image.data
            self.fontscale = max(self.img.shape[:2]*np.array([30/1080, 30/1620]))
            self.thick = int(max([*list(self.img.shape[:2]*np.array([2/1080, 2/1620])),2]))
            self.root = Path(item.image.path[:item.image.path.rfind(item.id)]).parent

        def saveImg(self):
            img = deepcopy(self.img)
            img = Image.fromarray(img.astype(np.uint8))
            savePath:Path = self.root/'images_draw-label'/Path(self.item.image.path).name
            savePath.parent.mkdir(exist_ok=True, parents=True)
            img.save(savePath)
            return self

        def drawItem(self, lineStyle, cornerStyle):
            for anno in self.item.annotations:
                if isinstance(anno,Bbox):
                    self.drawBbox(anno, lineStyle, cornerStyle).drawLabel(anno)
                elif isinstance(anno,Polygon):
                    self.drawSeg()
            return self

        @staticmethod
        def chgImageOrder(inputImg):
            img = deepcopy(inputImg)
            if len(img.shape) == 3 and img.shape[2] in {3, 4}:
                img[:, :, :3] = img[:, :, 2::-1]

        @staticmethod
        def getColor(anno:Union[Bbox,Polygon]):
            color = customDataset.ImageData.colorMap[anno.label]
            while len(customDataset.ImageData.colorMap) != len(set(customDataset.ImageData.colorMap.values())):
                del customDataset.ImageData.colorMap[anno.label]
                color = customDataset.ImageData.colorMap[anno.label]
            return color

        def drawBbox(self, anno:Bbox, lineStyle, cornerStyle):
            color = self.getColor(anno)
            bbox = [int(i) for i in anno.points]
            if cornerStyle=='round':
                self.roundRectangle(self.img,(bbox[0], bbox[1]), (bbox[2], bbox[3]), color, self.thick, linestyle=lineStyle)
            elif cornerStyle=='sharp':
                self.rectangle(self.img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, self.thick, linestyle=lineStyle)
            else:
                raise AssertionError(f'cornerStyle must be one of {", ".join(self.conerStyles)}')
            return self

        def rectangle(self, img, topleft, bottomright, color, thick, linestyle='solid'):
            if linestyle=='solid':
                cv2.rectangle(img, (topleft[0], topleft[1]), (bottomright[0], bottomright[1]), color, thick)
            elif linestyle=='dot':
                self.dotLine(img, topleft, (bottomright[0], topleft[1]), color, thick)#top
                self.dotLine(img, (topleft[0],bottomright[1]), (bottomright[0], bottomright[1]), color, thick)#bottom
                self.dotLine(img, topleft, (topleft[0], bottomright[1]), color, thick)#left
                self.dotLine(img, (bottomright[0],topleft[1]), (bottomright[0],bottomright[1]), color, thick)#right
            return self
            
        def roundRectangle(self, img, topleft, bottomright, color, thick, linestyle='solid'):
            if linestyle=='solid':
                _line, _ellipsis = cv2.line, cv2.ellipse
            elif linestyle=='dot':
                _line, _ellipsis = self.dotLine, self.dotEllipse
            else:
                raise AssertionError(f'linestyle must be one of {", ".join(self.lineStyles)}')

            border_radius = thick*20
            b_h, b_w = int((bottomright[1]-topleft[1])/2), int((bottomright[0]-topleft[0])/2)
            r_y, r_x = min(border_radius,b_h), min(border_radius,b_w)

            _line(img, topleft, (bottomright[0]-r_x, topleft[1]), color, thick)#top
            _line(img, (topleft[0]+r_x,bottomright[1]), (bottomright[0]-r_x, bottomright[1]), color, thick)#bottom
            _line(img, topleft, (topleft[0], bottomright[1]-r_y), color, thick)#left
            _line(img, (bottomright[0],topleft[1]+r_y), (bottomright[0],bottomright[1]-r_y), color, thick)#right
            _ellipsis(img, (bottomright[0]-r_x, topleft[1]+r_y), (r_x, r_y), 0, 0, -90, color, thick)#top-right
            _ellipsis(img, (topleft[0]+r_x, bottomright[1]-r_y), (r_x, r_y), 0, 90, 180, color, thick)#bottom-left
            _ellipsis(img, (bottomright[0]-r_x, bottomright[1]-r_y), (r_x, r_y), 0, 0, 90, color, thick)#bottom-right
            return self

        @staticmethod
        def dotEllipse(img, center, r, rotation, start, end, color, thick):
            dr = int((end-start)/4.5)

            start1 = start
            while np.sign(end-start1)==np.sign(dr):
                end1 = start1+dr
                if np.abs(end-start1)< np.abs(dr):
                    end1=end
                cv2.ellipse(img, center, r, rotation, start1, end1, color, thick)
                start1 += 2*dr

        @staticmethod
        def dotLine(img, topleft, bottomright, color, thick):
            a = np.sqrt((bottomright[0]-topleft[0])**2+(bottomright[1]-topleft[1])**2)
            if a==0:
                return
            dotgap = thick*10
            b = a/dotgap
            dx = int((bottomright[0]-topleft[0])/b)
            dy = int((bottomright[1]-topleft[1])/b)

            x1, y1 = topleft
            while (np.sign(bottomright[0]-x1)==np.sign(dx)) & (np.sign(bottomright[1]-y1)==np.sign(dy)):
                end_x = x1+dx
                end_y = y1+dy

                if np.abs(bottomright[0]-end_x)<np.abs(dx):
                    end_x = bottomright[0]
                if np.abs(bottomright[1]-end_y)<np.abs(dy):
                    end_y = bottomright[1]
                    
                cv2.line(img, (x1, y1), (end_x, end_y), color, thick)
                x1 += 2*dx
                y1 += 2*dy

        def drawLabel(self, anno:Union[Bbox,Polygon]):
            bbox = list(map(lambda coord: int(np.around(coord)),anno.points))
            label = self.categories[anno.label].name
            color = self.getColor(anno)
            textColor = tuple(np.array([255,255,255]) - np.array(color))
            #draw label
            fontpath = 'NanumGothicBold.ttf'
            font = ImageFont.truetype(fontpath, int(self.fontscale))
            img_label = Image.new('RGB', (int(self.fontscale*100),int(self.fontscale*1.5)),color=color)
            draw = ImageDraw.Draw(img_label)
            draw.text((0, 0), label, font = font, fill = textColor)
            w, h = draw.textsize(label, font=font)
            img_label = img_label.crop((0,0,w,int(h*1.1)))
            text_y = max(bbox[1] - h,0) #label 위치 조정
            img = Image.fromarray(self.img.astype(np.uint8))
            img.paste(img_label,(bbox[0],text_y))
            self.img = np.array(img)

            # label_idx_inImg = (bbox[0], text_y, bbox[0]+w, text_y+h)
            # self.img[label_idx_inImg[1]:label_idx_inImg[3], label_idx_inImg[0]:label_idx_inImg[2]] = img_label
            return self

        def drawSeg(self):
            return