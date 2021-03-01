import numpy as np 

from dltools.dataset.commands import Commands
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from pathlib import Path
from PIL import Image

from dltools.dataset.utils import readJson
from dltools.api import AuthAPI, UserAPI, JobAPI
from dltools.dataset.crypto import Crypt
from dltools.dataset.temperature_RGB import thermal_matching, thermal_matching_v2
from dltools.analytics.project import ProjectAnaly


cfg_path = Path(__file__).parent/'../config.json'
cfg = readJson(cfg_path)
crypt = Crypt()

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
ui_path = Path(__file__).parent/"ui2.ui"
form_class = uic.loadUiType(ui_path)[0]

def error_massage(func):
    def wrapper(self, *arg, **kwdargs):
        try:
            func(self, *arg, **kwdargs)
            QMessageBox.information(self, "작업 성공", '요청한 작업을 완료했습니다.')
        except Exception as e:
            QMessageBox.warning(self, "작업 실패", '올바른 인수를 입력했는지 확인하세요.')
    return wrapper

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

        # download frame image
        self.pushButton_3.clicked.connect(lambda :self.single_dir_select(self.lineEdit_3))
        self.pushButton_2.clicked.connect(self.download_frame_image)
        self.download_frame_image_task_id.currentIndexChanged.connet(self.set_frame_id)

        #merge
        self.pushButton_4.clicked.connect(self.merge)
        self.pushButton_11.clicked.connect(lambda:self.single_dir_select(self.lineEdit_6))

        #열화상
        self.pushButton_9.clicked.connect(lambda:self.multi_file_select(self.listWidget_2))
        self.pushButton_5.clicked.connect(lambda:self.file_list_clear(self.listWidget_2,self.thermal_images))
        self.pushButton_6.clicked.connect(lambda:self.single_file_select(self.lineEdit_4))
        self.pushButton_10.clicked.connect(lambda:self.single_dir_select(self.lineEdit_7))
        self.pushButton_7.clicked.connect(self.run_thermal_matching)

        #보고서
        self.pushButton_8.clicked.connect(self.report)
        self.pushButton_12.clicked.connect(lambda:self.single_dir_select(self.lineEdit_8))
        
        #job 할당
        self.pushButton_13.clicked.connect(self.job_assign)
        #job 할당 초기화
        self.pushButton_14.clicked.connect(self.assign_init)

    @error_massage
    def report(self, *a): return ProjectAnaly(int(self.lineEdit_5.text())).export_report(self.lineEdit_8.text())

    def set_frame_id(self,taks_id):
        task = self.info.filter_task('id', taks_id)[0]
        frame_size = task.size
        self.set_combobox(self.download_frame_image_frame_id, range(frame_size))

    def signin(self, *a):
        base_url = self.url.text()
        username = self.id.text()
        password = self.password.text()
        auth = AuthAPI(base_url)
        r = auth.login(username, password)
        self.userinfo = UserAPI().get_id('self')
        if r:
            self.pushButton.setText('성공')
            self.cmd = Commands()
            self.info = ProjectAnaly()
            self.gridTabWidget.setEnabled(True)

            #
            task_ids = self.info.get_task_elem_list('id')
            task_names = self.info.get_task_elem_list('name')
            task_combo_list = [IdName(id, name)() for id in task_ids for name in task_names]
            self.set_combobox(self.download_frame_image_task_id, task_combo_list)

    @error_massage
    def download_frame_image(self, *a):
        task_id = int(self.lineEdit.text())
        frame_id = int(self.lineEdit_2.text())
        outdir = self.lineEdit_3.text()
        self.cmd.download_labeled_image(task_id, frame_id, outdir)

    @staticmethod
    def set_combobox(combobox, list):
        for line in list:
            combobox.addItem(line)

    def single_file_select(self, lineEdit, *a):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '')
        lineEdit.setText(filename[0])
        
    def single_dir_select(self, lineEdit, *a):
        filename = QFileDialog.getExistingDirectory(self)
        lineEdit.setText(filename)

    def multi_file_select(self, listview, *a):
        filenames = QFileDialog.getOpenFileNames(self, 'Open Files', '', "All Files(*);; Images (*.png *.xpm *.jpg *.jpeg);; json (*.json)")
        self.thermal_images = filenames[0]
        for file in filenames[0]:
            listview.addItem(file)

    def file_list_clear(self, listview, *a):
        listview.clear()
        self.thermal_images.clear()

    @error_massage
    def merge(self, *a):
        import_format = 'coco'
        if self.radioButton_10.isChecked():
            import_format = 'coco'
        elif self.radioButton_9.isChecked():
            import_format = 'cvat'
        elif self.radioButton_7.isChecked():
            import_format = 'voc'
        elif self.radioButton_8.isChecked():
            import_format = 'yolo'
        elif self.radioButton_12.isChecked():
            import_format = 'tfrecord'

        export_format = 'coco'
        if self.radioButton_2.isChecked():
            export_format = 'coco'
        elif self.radioButton_3.isChecked():
            export_format = 'cvat'
        elif self.radioButton.isChecked():
            export_format = 'voc'
        elif self.radioButton_4.isChecked():
            export_format = 'yolo'
        elif self.radioButton_6.isChecked():
            export_format = 'tfrecord'
        elif self.radioButton_5.isChecked():
            export_format = 'voc_segmentations'
        
        if self.checkBox.isChecked()==True:
            no_anno_filter = 'y'
        else: no_anno_filter = 'n'

        self.cmd.set_working_dir(self.lineEdit_6.text())
        self.cmd.mergeDataset({'format':import_format}, {'no_anno_filter':no_anno_filter}) 
        self.cmd.exportDataset({'format':export_format}, merge=True)

    @error_massage
    def run_thermal_matching(self, *a):
        thermal_dic = readJson(self.lineEdit_4.text())
        for path in self.thermal_images:
            image = np.array(Image.open(path))
            filename = Path(path).stem
            thermal_matching_v2(image, thermal_dic, self.lineEdit_7.text(), filename)

    @error_massage
    def job_assign(self, *a):
        project_id = int(self.lineEdit_10.text())
        job_count = int(self.lineEdit_9.text())
        user_api = UserAPI()
        job_api = JobAPI()
        user_ids = [user.id for user in user_api.get()['results'] if 'annotator' in user.groups if user['is_active']]
        empty_jobs = [job.id for job in ProjectAnaly(project_id).jobs if (job.status=='annotation') and (job.assignee is None)]
        for user_id, job_id in zip(user_ids*job_count, empty_jobs):
            job_api.patch_id(job_id, assignee_id=user_id)

    @error_massage
    def assign_init(self, *a):
        project_id = int(self.lineEdit_10.text())
        job_api = JobAPI()
        anno_status_jobs = [job.id for job in ProjectAnaly(project_id).jobs if (job.status=='annotation') and (job.assignee is not None)]
        for job_id in anno_status_jobs:
            job_api.patch_id(job_id, assignee_id=None)

    def _get_task_list(self):
        self.
        
class IdName:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    def __call__(self, *args, **kwds) -> str:
        return f'{self.id}: {self.name}'

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()