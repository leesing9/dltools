from dltools.api.user import UserAPI
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from pathlib import Path

from dltools.dataset.utils import readJson
from dltools.api import AuthAPI, TaskAPI, ProjectAPI, JobAPI
from dltools.dataset.crypto import Crypt


cfg_path = Path(__file__).parent/'../config.json'
cfg = readJson(cfg_path)
crypt = Crypt()
project_api = ProjectAPI()

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
ui_path = Path(__file__).parent/"ui.ui"
form_class = uic.loadUiType(ui_path)[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #sign in
        self.url.setText(cfg['base_url'])
        self.id.setText(cfg['username'])
        self.password.setText(crypt.decrypt(cfg['password']))
        self.pushButton.clicked.connect(self.signin)

        #작업화면




    def signin(self):
        base_url = self.url.text()
        username = self.id.text()
        password = self.password.text()
        auth = AuthAPI(base_url)
        ok = auth.login(username, password)
        self.userinfo = UserAPI().get_id('self')
        if not ok:
            QMessageBox.warning(self, "sign in 실패", 'id/password를 확인하세요.')
        else:
            self.pushButton.setText('성공')

        # 탭 활성화
        if ('annotator' in self.userinfo.groups) or ('observer' in self.userinfo.groups):
            self.adminpage.tab.enable = True
        elif ('admin' in self.userinfo.groups) or ('user' in self.userinfo.groups):
            self.adminpage.tab_2.enable = True
            self.adminpage.tab_3.enable = True
        
        project_api.get()
        

    def update_my_status(self):
        pass

    def set_project_list(self):
        project_count = project_api.get().count
        projects = 
        project
        self.worker_board.clear()
        self.worker_board.clear()




if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()