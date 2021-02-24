from dltools.dataset.menu import Menu
from dltools.dataset.commands import Commands
from dltools.rq_test import download_labeled_image, export_report
from dltools.api import AuthAPI
from dltools.dataset.utils import readJson

from pathlib import Path

cfg_path = Path(__file__).parent/'../config.json'
cfg = readJson(cfg_path)

base_url = cfg
auth = AuthAPI(base_url)


#login
# auth.login(username=username, password=password)

def main():
    command = Commands()
    mainMenu = Menu('Main')\
            .setCommand('directory 재설정', command.selWorkDir, 'dataset directory를 다시 선택합니다. ')\
            .setCommand('dataset 합치기',command.mergeFunction,'여러 데이터셋을 하나로 합칩니다.')\
            .setCommand('dataset 변환', command.convertFunction, '다른 형식의 데이터셋으로 바꿉니다. 예) coco format -> voc format')\
            .setCommand('draw label', command.drawItemFuncion, '이미지에 라벨을 그리기. 각 데이터셋 폴더/images_draw-label 안에 저장됨.')\
            .setCommand('frame download', command.drawItemFuncion, '이미지에 라벨을 그리기. 각 데이터셋 폴더/images_draw-label 안에 저장됨.')

    mainMenu()

if __name__ == "__main__":
    main()