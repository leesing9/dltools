from dltools.menu import Menu
from dltools.commands import Commands

def main():
    command = Commands()
    mainMenu = Menu('Main').setCommand('dataset 합치기',command.mergeFunction,'여러 데이터셋을 하나로 합칩니다.')\
                        .setCommand('dataset 변환', command.convertFunction, '다른 형식의 데이터셋으로 바꿉니다. 예) coco format -> voc format')\
                        .setCommand('draw label', command.drawItemFuncion, '이미지에 라벨을 그리기. 각 데이터셋 폴더/images_draw-label 안에 저장됨.')

    mainMenu()