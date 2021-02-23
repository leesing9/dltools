import numpy as np

from datumaro.components.dataset import Dataset
from datumaro.components.extractor import Bbox, DatasetItem, Polygon
from dltools.api.job import JobAPI
from time import sleep
from dltools.api.info import JobInfo, LabeledDataInfo, AuthorInfo, LabelInfo, ProjectInfo, TaskInfo, UserInfo, AttributeInfo
from dltools.api import AuthAPI, TaskAPI
from dltools.dataset.dataset import customDataset

from pathlib import Path
from typing import List

base_url = 'http://tmecnc62.iptime.org:12380'
auth = AuthAPI(base_url)

username = 'serveradmin'
password = 'wnrWkd131@Cv'

#login
auth.login(username=username, password=password)
#task api class call
task = TaskAPI()
job = JobAPI()

# rq17 - 라벨 그려진 이미지 다운
def download_labeled_image(task_id:int, frame_id:int, outdir:str):
    filename, img = task.download_frame(task_id, frame_id, outdir, save=False)
    labels = dict([(label.id, label) for label in task.get_id(task_id).labels])
    jobs = task.get_jobs(task_id)
    job_id_with_frame = [job.id for job in jobs if (int(job.start_frame) <= frame_id) & (frame_id <= int(job.stop_frame))]
    job_annos_list = [job.get_annotations(job_id) for job_id in job_id_with_frame]
    annos = [[anno for anno in job_annos.shapes if anno.frame==frame_id][0] for job_annos in job_annos_list]
    categories=[label.name for label in labels.values()]
    items = []
    for anno in annos:
        attriname = dict([ (attr.id, attr.name) for attr in labels[anno.label_id].attributes ])
        attris = dict([ (attriname[attr.spec_id], attr.value) for attr in anno.attributes ])
        if anno.type=='rectangle':
            x,y,x2,y2 = anno.points
            items.append(Bbox(x,y,x2-x, y2-y,attributes=attris, label=categories.index(labels[anno.label_id].name)))
        elif anno.type=='polygon':
            items.append(Polygon(anno.points,attributes=attris, label=categories.index(labels[anno.label_id].name)))

    # image = {'data': np.asarray(img),
    #          'path': str(Path(outdir)/filename)}
    dataset = Dataset.from_iterable([
                    DatasetItem(id=filename, annotations=items, image=np.array(img))],
                    categories=categories)
    customset = customDataset(dataset)
    for image_data in customset._imageDatas:
        image_data.drawItem('s','s').saveImg(Path(outdir)/filename)
                    
# download_labeled_image(45, 0, 'f:')
    
# rq22 - Task 결과 합치기

# rq24 - 데이터셋에서 빈 이미지 제거

# rq28 - 통계기능

# rq29 - 할당 편의성 개선
def job_assign(job_id:int, assignee_id:int):
    job = JobAPI()
    job.patch_id(job_id, assignee_id=assignee_id)

job_assign(18, 7)

# rq33 - 보고서

# rq38 - 열화상 이미지 온도 csv 파일로 출력

#task - get tasks
print('\n#task - get tasks')
print(task.get())

#task - download frame
print('\n#task - download frame')

#change assignee