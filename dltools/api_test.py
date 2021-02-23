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
print('\nlogin')
auth.login(username=username, password=password)

#auth - user regist
print('\n#auth - user regist')
print(auth.register('api_test', 'tm123456'))

#user api class call
print('\n#user api class call')
user = UserAPI()
print(user)

#user - get users
print('\n#user - get users')
r = user.get('api_test')
print(r)
test_user = r['results'][0]

#user - get user self
print('\n#user - get user self')
print(user.get_id(test_user.id))

#project api class call
print('\n#project api class call')
project = ProjectAPI()

#project - create project
print('\n#project - create project')
attribs = [AttributeInfo().create("Category","radio", ["손상","비손상"]),
          AttributeInfo().create("comment", "text", [""]),
          AttributeInfo().create("Pipe_type", "radio", ["원형관", "박스관"]), 
          AttributeInfo().create("Pipe_material", "radio", ["강성관", "연성관"]),
          AttributeInfo().create("Inspection_view", "radio", ["정면", "측면"]),
          AttributeInfo().create("Inspection_location", "radio", ["관로내부", "관로입구","관로외부", "맨홀"])]
labels = [LabelInfo().create("파손", attribs)]
projname = 'api test project'
params = ProjectInfo().create(projname, labels)
r = project.create(**params)
print(r)

#project - patch project
print('\n#project - patch project')
print(project.patch_id(r.id, owner=AuthorInfo().create(test_user.username)))

#project - get projects
print('\n#project - get projects')
r = project.get(projname)
print(r)
if r:
    test_proj = r['results'][0]
else:
    raise Exception()

#project - get project self
print('\n#project - get project self')
print(project.get_id(test_proj.id))

#project - get project tasks
print('\n#project - get project tasks')
print(project.get_tasks(test_proj.id))

#task api class call
print('\n#task api class call')
task = TaskAPI()
print(task)

#task - create task
print('\n#task - create task')
task_r1 = task.create(**TaskInfo().create('api_test_task1', project_id=test_proj.id))
print(task_r1)

# task_r2 = task.create(**TaskInfo().create('api_test_task2',labels))
# print(task_r2)

#task - patch task
print('\n#task - patch task')
print(task.patch_id(id=task_r1.id, owner=AuthorInfo().create('serveradmin')))
# print(task.patch_id(id=task_r2.id, owner=AuthorInfo().create('serveradmin')))

#task - attach_data
print('\n#task - attach_data')
resources1 = str(Path('f:\\task_20210111_bbox_파손-2021_01_14_14_51_27-coco 1.0/images.7z'))
# resources2 = [str(img) for img in Path('f:\\task_20210111_bbox_파손-2021_01_14_14_51_27-coco 1.0/images/8차20210111/파손/').iterdir()]
print(task.attach_data(task_r1.id, 'local', resources1))
# print(task.attach_data(task_r2.id, 'local', resources2))

#task - get status
print('\n#task - get status')
while True:
    status = task.get_status(task_r1.id)['state']
    sleep(5)
    if status == 'Finished':
        print(status)
        break

# while True:
#     status = task.get_status(task_r2.id)['state']
#     sleep(5)
#     if status == 'Finished':
#         print(status)
#         break

#task - get tasks
print('\n#task - get tasks')
print(task.get())

#task - get task self
print('\n#task - get task self')
print(task.get_id(task_r1.id))

#task - upload_anno
print('\n#task - upload_anno')
print(task.upload_annotations(task_r1.id, 'COCO 1.0', 'f:/task_20210111_bbox_파손-2021_01_14_14_51_27-coco 1.0/annotations/instances_default.json'))

#task - download_anno
print('\n#task - download_anno')
print(task.get_annotations(task_r1.id, 'CVAT for images 1.1', 'download_anno_test.zip', 'f:/', download=True))

#task - del anno
print('\n#task - del anno')
print(task.del_annotations(task_r1.id))

#task - download frame
print('\n#task - download frame')
print(task.download_frame(task_r1.id, 1, "f:"))

#task - get data meta
print('\n#task - get data meta')
print(task.get_data_meta(task_r1.id))

#task - download dataset
print('\n#task - download dataset')
print(task.download_dataset(task_r1.id, 'CVAT for images 1.1', 'download_dataset_test.zip', 'f:/'))

#task - get jobs
print('\n#task - get jobs')
print(task.get_jobs(task_r1.id))

#task - del task
print('\n#task - del task')
print(task.del_id(task_r1.id))

#project - del project
print('\n#project - del project')
print(project.del_id(test_proj.id))

#user - user delete
print('\n#user - user delete')
print(user.del_id(test_user.id))
