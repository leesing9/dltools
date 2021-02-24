from easydict import EasyDict
from typing import Any, Dict

class Arg:
    limit = dict()
    def __init__(self, argsAndType:Dict[str,str]):
        self.args = EasyDict()
        for name,(type, help) in argsAndType.items():
            arg = None
            while not self.checkArg(name,arg):
                inputPrint = f'\n\n{help}\n{name} 입력: '
                val = input(inputPrint)
                arg = eval(f'{type}(\'{val.strip()}\')')
            self.args[name] = arg
    
    def __getitem__(self, name) -> EasyDict: 
        return self.args[name]

    @classmethod
    def checkArg(cls, name:str, arg)->bool:
        if arg is None:
            return False
        else:
            if arg in cls.limit[name]:
                return True
            else:
                print('잘못된 값입니다. 다시 입력해주세요.')
                return False

class ImportArg(Arg):
    supportFormat = ['coco', 'cvat', 'datumaro', 'image_dir', 'imagenet', 'imagenet_txt', 'label_me', 'mot_seq', 'mots','tf_detection_api', 'voc', 'yolo']
    args = {'format':('str', f'다운로드 한 데이터셋의 형식.\n지원형식: {", ".join(supportFormat)}')}
    limit = {'format': supportFormat}
    def __init__(self) -> None:
        super().__init__(ImportArg.args)

class ExportArg(Arg):
    supportFormat = ['coco', 'cvat', 'datumaro', 'datumaro_project', 'label_me', 'mot_seq_gt', 'mots_png', 'tf_detection_api', 'voc','voc_segmentation', 'yolo']
    args = {'format':('str', f'내보낼 데이터셋의 형식.\n지원형식: {", ".join(supportFormat)}')}
    limit = {'format': supportFormat}
    def __init__(self) -> None:
        super().__init__(ExportArg.args)

class DrawItemArg(Arg):
    args = {'lineStyle':('str', f'선의 형태. (d)ot(점선), (s)olid(실선)'),
            'cornerStyle':('str', f'상자 모서리의 형태. (s)harp(직각), (r)ound(둥금)')}
    limit = {'lineStyle': ['d', 's'],
             'cornerStyle':[ 's', 'r' ]}
    def __init__(self) -> None:
        super().__init__(DrawItemArg.args)

class NoAnnoFilterArg(Arg):
    supportFormat = ['y', 'n']
    args = {'no_anno_filter':('str', f'annotation이 없는 이미지를 제외하시겠습니까? y/n')}
    limit = {'no_anno_filter': supportFormat}
    def __init__(self) -> None:
        super().__init__(NoAnnoFilterArg.args)

if __name__ == "__main__":
    a = ImportArg()
    