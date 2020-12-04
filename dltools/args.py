from easydict import EasyDict
from typing import Dict

class Arg:
    def __init__(self, argsAndType:Dict[str,str]=dict()):
        self.args = EasyDict()
        for name,(type, help) in argsAndType.items():
            inputPrint = f'\n\n{help}\n{name} 입력: '
            val = input(inputPrint)
            arg = eval(f'{type}(\'{val.strip()}\')')
            self.args[name] = arg
    
    def __getitem__(self, name) -> EasyDict: 
        return self.args[name]

class ImportArg(Arg):
    def __init__(self) -> None:
        self.supportFormat = ['coco', 'cvat', 'datumaro', 'image_dir', 'imagenet', 'imagenet_txt', 'label_me', 'mot_seq', 'mots','tf_detection_api', 'voc', 'yolo']
        args = {'format':('str', f'다운로드 한 데이터셋의 형식.\n지원형식: {",".join(self.supportFormat)}')}
        super().__init__(args)

class ExportArg(Arg):
    def __init__(self) -> None:
        self.supportFormat = ['coco', 'cvat', 'datumaro', 'datumaro_project', 'label_me', 'mot_seq_gt', 'mots_png', 'tf_detection_api', 'voc','voc_segmentation', 'yolo']
        args = {'format':('str', f'내보낼 데이터셋의 형식.\n지원형식: {",".join(self.supportFormat)}')}
        super().__init__(args)

class DrawItemArg(Arg):
    def __init__(self) -> None:
        args = {'lineStyle':('str', f'선의 형태. dot(점선), solid(실선)'),
                'cornerStyle':('str', f'상자 모서리의 형태. sharp(직각), round(둥금)')}
        super().__init__(args)