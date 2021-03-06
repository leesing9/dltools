from dltools.api.user import UserAPI
import numpy as np

from dltools.api.job import JobAPI
from dltools.api import AuthAPI, TaskAPI
from dltools.dataset.dataset import customDataset
from dltools.analytics import ProjectAnaly, makeReport

from pathlib import Path
from typing import List
from datumaro.components.dataset import Dataset
from datumaro.components.extractor import Bbox, DatasetItem, Polygon
from time import sleep

# rq17 - 라벨 그려진 이미지 다운
def download_labeled_image(task_api, task_id:int, frame_id:int, outdir:str):
    filename, img = task_api.download_frame(task_id, frame_id, outdir, save=False)
    labels = dict([(label.id, label) for label in task_api.get_id(task_id).labels])
    jobs = task_api.get_jobs(task_id)
    job_id_with_frame = [job.id for job in jobs if (int(job.start_frame) <= frame_id) & (frame_id <= int(job.stop_frame))]
    job_annos_list = [job_api.get_annotations(job_id) for job_id in job_id_with_frame]
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
def job_assign(project_id:int, job_count:int):
    user = UserAPI()
    job = JobAPI()
    user_ids = [user.id for user in user.get() if ]
    empty_jobs = [job.id for job in ProjectAnaly(project_id).jobs]
    for user_id, job_id in zip(user_ids*job_count, empty_jobs):
        job.patch_id(job_id, assignee_id=user_id)

# rq28, 33 - 통계&보고서
def export_report(project_id):
    prjanaly = ProjectAnaly(project_id)
    assignee_table, label_table = prjanaly()
    makeReport(dataFrame1 = assignee_table, dataFrame2 = label_table, saveExcelName = 'Report')

# rq38 - 열화상 이미지 온도 csv 파일로 출력

#task - get tasks
# print('\n#task - get tasks')
# print(task.get())

# #task - download frame
# print('\n#task - download frame')

#change assignee
