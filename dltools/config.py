from pathlib import Path
from shutil import move

def setConfig(format:str):
    if format in ['coco']:
        formatConfig = coco
    elif format in ['cvat']:
        formatConfig = cvat
    elif format in ['datumaro']:
        formatConfig = datumaro
    elif format in ['image_dir', 'imagenet', 'imagenet_txt']:
        formatConfig = imagenet
    elif format in ['label_me']:
        formatConfig = labelme
    elif format in ['mot_seq', 'mots']:
        formatConfig = mot
    elif format in ['voc']:
        formatConfig = voc
    elif format in ['yolo']:
        formatConfig = yolo
    elif format in ['tf_detection_api']:
        formatConfig = tf
    else:
        raise NotImplementedError
    return formatConfig()

class DefaultConfig:
    def getImgDir(self, subset):
        return getattr(self, 'defaultImgDir')

    def getAnnoDir(self, subset):
        return getattr(self, 'defaultAnnoDir')

class cvat(DefaultConfig):
    def __init__(self) -> None:
        self.imageIdName = 'frame'
        self.defaultSubset = 'default'
        self.defaultImgDir = Path('images')
        self.defaultAnnoDir = Path('')

class datumaro(DefaultConfig):
    def __init__(self) -> None:
        self.imageIdName = 'id'
        self.defaultSubset = 'default'
        self.defaultImgDir = Path('dataset/images')
        self.defaultAnnoDir = Path('dataset/annotations')

class voc(DefaultConfig):
    def __init__(self) -> None:
        self.imageIdName = None
        self.defaultSubset = 'default'
        self.defaultImgDir = Path('JPEGImages')
        self.defaultAnnoDir = Path('Annotations')

class yolo(DefaultConfig):
    def __init__(self) -> None:
        self.imageIdName = None
        self.defaultSubset = 'train'
        self.defaultImgDir = self.setDir(self.defaultSubset)
        self.defaultAnnoDir = self.setDir(self.defaultSubset)
    
    @staticmethod
    def setDir(subset):
        return Path(f'obj_{subset}_data')

    def getImgDir(self, subset):
        return self.setDir(subset)

    def getAnnoDir(self, subset):
        return self.setDir(subset)

class coco(DefaultConfig):
    def __init__(self) -> None:
        self.imageIdName = 'id'
        self.defaultSubset = 'default'
        self.defaultImgDir = Path('images')
        self.defaultAnnoDir = Path('annotations')

class mot(DefaultConfig):
    def __init__(self) -> None:
        self.imageIdName = None
        self.defaultSubset = 'default'
        self.defaultImgDir = Path('img1')
        self.defaultAnnoDir = Path('gt')

class labelme(DefaultConfig):
    def __init__(self) -> None:
        self.imageIdName = None
        self.defaultSubset = 'default'
        self.defaultImgDir = Path('')
        self.defaultAnnoDir = Path('')

class imagenet(DefaultConfig):
    def __init__(self) -> None:
        self.imageIdName = None
        self.defaultSubset = 'default'
        self.defaultImgDir = Path('')
        self.defaultAnnoDir = Path('')

class tf(DefaultConfig):
    def __init__(self) -> None:
        self.imageIdName = None
        self.defaultSubset = ''
        self.defaultImgDir = Path('')
        self.defaultAnnoDir = Path('')
