import pandas as pd
import numpy as np

from copy import deepcopy
from functools import reduce
from typing import Any

from dltools.api.info import LabeledDataInfo, SimpleJobInfo
from dltools.api import JobAPI, TaskAPI, ProjectAPI, AuthAPI
from dltools.analytics.Test_WriteReport4 import makeReport


class ProjectAnaly:
    def __init__(self, project_id) -> None:
        self.project_api = ProjectAPI()
        self.task_api = TaskAPI()
        self.raw_task_info = {}
        self.project_info = self.project_api.get_id(project_id)
        self.labels = dict([(label.id, label.name) for label in self.project_info.labels])
        self.attribute_names = dict([(attr['id'], attr['name']) for label in self.project_info.labels for attr in label['attributes']])
        self.tasks =  self.project_info.tasks
        self.jobs = [[[self._process_job(job,task.id) for job in seg.jobs] for seg in task.segments] for task in self.tasks]
        self.jobs = reduce(lambda x, y: x+y, reduce(lambda x, y: x+y, self.jobs))
        self.annos = [self._process_anno(self.task_api.get_annotations(task.id)) for task in self.tasks]
        self.annos =reduce(lambda x, y: x+y, self.annos) 

        self.job_df = pd.DataFrame(self.jobs)
        self.job_df[['assignee', 'reviewer']] = self.job_df[['assignee', 'reviewer']].fillna('@Unallocated')

        self.anno_df = pd.DataFrame(self.annos)

        assignee_table = pd.pivot_table(self.job_df, 'id', 'assignee', 'status', aggfunc='count', fill_value=0)
        self.assignee_table = pd.DataFrame(assignee_table, columns=['annotation','validation','modification','complete']).fillna(0).reset_index()
        self.assignee_table = self.assignee_table.rename(columns={'assignee':'작업자','annotation':'미작업','validation':'검수대기','modification':'수정대기','complete':'완료'})

        label_table = pd.pivot_table(self.anno_df, 'frame', 'label', 'type', aggfunc='count', fill_value=0)
        self.label_table = pd.DataFrame(label_table, columns=['rectangle', 'polygon', 'polyline', 'points', 'cuboid']).fillna(0).reset_index()
        self.label_table = self.label_table.rename(columns={'rectangle':'bounding box'})

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.assignee_table, self.label_table

    @staticmethod
    def _process_job(job:SimpleJobInfo, task_id:int):
        copy_job = deepcopy(job)
        copy_job['task_id'] = task_id

        for auth in ['assignee', 'reviewer']:
            if copy_job[auth] is not None:
                copy_job[auth] = copy_job[auth]['username']

        del copy_job['url']
        return copy_job
        

    def _process_anno(self, annos:LabeledDataInfo):
        annos = deepcopy(annos)

        anno_list = []
        for tag in annos['tags']:
            tag['type'] = 'tag'

            tag['label'] = self.labels[tag['label_id']]
            del tag[key]

            for key in tag:
                if key in ['id', 'group','source']:
                    del tag[key]

            for attr in tag['attributes']:
                tag[self.attribute_names[attr['spec_id']]] = attr['value']
                del tag[key]

            anno_list.append(deepcopy(tag))

        for shape in annos['shapes']:
            shape['label'] = self.labels[shape['label_id']]

            for attr in shape['attributes']:
                shape[self.attribute_names[attr['spec_id']]] = attr['value']

            for key in ['id', 'group','source','points', 'attributes', 'label_id', 'z_order']:
                del shape[key]
            anno_list.append(deepcopy(shape))

        for track in annos['tracks']:
            for shape in track['shapes']:
                shape['label'] = self.labels[track['label_id']]

                for attr in shape['attributes']:
                    shape[self.attribute_names[attr['spec_id']]] = attr['value']

                for key in ['id','points', 'attributes', 'outside', 'z_order']:
                    del shape[key]
                anno_list.append(deepcopy(shape))
        
        return anno_list

    def export_report(self, outdir):
        makeReport(dataFrame1 = self.assignee_table, dataFrame2 = self.label_table, saveExcelName = 'Report', outdir=outdir)
        
if __name__ =='__main__':
    base_url = 'http://tmecnc62.iptime.org:12380'
    auth = AuthAPI(base_url)

    username = 'serveradmin'
    password = 'wnrWkd131@Cv'

    #login
    auth.login(username=username, password=password)
    #task api class call
    task = TaskAPI()
    job = JobAPI()

    prjanaly = ProjectAnaly(62)
    assignee_table, label_table = prjanaly()
    makeReport(dataFrame1 = assignee_table, dataFrame2 = label_table, saveExcelName = 'Report')