from dltools.api.job import JobAPI
from time import sleep
from dltools.api.info import AuthorInfo, LabelInfo, ProjectInfo, TaskInfo, UserInfo, AttributeInfo
from dltools.api.auth import AuthAPI
from dltools.api.user import UserAPI
from dltools.api.project import ProjectAPI
from dltools.api.task import TaskAPI

from pathlib import Path

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
    img = task.download_frame(task_id, frame_id, outdir)
    jobs = task.get_jobs(task_id)
    job_id_with_frame = [job.id for job in jobs if (int(job.start_frame) <= frame_id) & (frame_id <= int(job.stop_frame))]
    anno_list = [job.get_anno(job_id) for job_id in job_id_with_frame]
    

# rq22 - Task 결과 합치기

# rq24 - 데이터셋에서 빈 이미지 제거

# rq28 - 통계기능

# rq29 - 할당 편의성 개선

# rq33 - 보고서

# rq38 - 열화상 이미지 온도 csv 파일로 출력

#task - get tasks
print('\n#task - get tasks')
print(task.get())

#task - download frame
print('\n#task - download frame')

#change assignee