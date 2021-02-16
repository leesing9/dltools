import json
import requests
import pandas as pd

from dltools.crypto import Crypt

from collections import defaultdict
from typing import Union
from pathlib import Path


class Project():
    def __init__(self, session:requests.Session, base_url) -> None:
        self.session = session
        self.base_url = base_url

    def get_proj(self)->dict:
        r = self.session.get(''.join([self.api_url,'projects']))
        r.raise_for_status()
        return r.json()

    def create_proj(self,projName:str, labels_path:Path):
        with open(str(labels_path), 'r') as f:
            labels = json.load(f)
        data ={ "name": projName,
                "labels": labels
                }
        self.session.post(self.api_url, data=data)
    
    def getProjList(self):
        r = requests.get(base_url+'projects')
        r = requests.get(base_url+'projects', params={'page_size': r.json()['count']})
        print('no\tid\tname')
        print('----------------------------')
        print(f'0\t-\tall')
        projrepo = []
        for idx, proj in enumerate(r.json()['results']):
            num = idx +1
            print( f'{num}\t{proj["id"]}\t{proj["name"]}')
            projrepo.append(pd.Series(proj, name=num))
        self.projDf = pd.DataFrame(projrepo)

    def selProj(self):
        self.getProjList()
        print()
        selNum = int(input('no. 선택: '))
        try:
            if selNum == 0:
                self.proj_id = 'all'
            else:
                self.seledProj = self.projDf.loc[int(selNum)]
                self.proj_id = self.seledProj['id']
        except KeyError as e:
            print('잘못된 숫자를 선택했습니다.')
            self.selProj()

    def getTasksInfo(self):
        if self.proj_id == 'all':
            r = self.session.get()
            r = requests.get(base_url+f'tasks', headers=header_gs)
            r = requests.get(base_url+f'tasks', headers=header_gs, params={'page_size':r.json()['count']})
        else:
            r = requests.get(base_url+f'projects/{cfg.projectId}/tasks', headers=header_gs)
            r = requests.get(base_url+f'projects/{cfg.projectId}/tasks', headers=header_gs, params={'page_size':r.json()['count']})
        taskrepo = []
        for task in r.json()['results']:
            taskrepo.append(pd.Series(task))
        self.taskInfo = pd.DataFrame(taskrepo)

    def exportProjTaskTable(self):
        self.getProjList()
        table = self.taskInfo[['id', 'name', 'project']]\
                .rename(columns=dict(zip(['id', 'name', 'project'],['taskId', 'taskName', 'projId'])))
        table['projName'] = table['projId'].map(self.projDf[['id','name']].set_index('id').to_dict()['name'])
        table.to_csv(cfg.projectFile,encoding='euc-kr')

    def readProjTaskTable(self):
        '''
        tabel cols = [taskId, taskName, projId, projName]
        '''
        self.projTaskTable = pd.read_csv(cfg.projectFile)

    def assignProjFromTable(self):
        self.readProjTaskTable()
        for task in self.projTaskTable.itertuples():
            requests.patch(base_url+f'tasks/{task.taskId}', headers=header_gs, data={"project":task.projId})

    def assignProjAllUnassignedTask(self):
        self.selProj()
        unassignedTaskInfo = self.taskInfo.loc[self.taskInfo['project'].isna()]
        if self.proj_id == 'all':
            print('다른 Project를 선택해 주세요')
            self.selProj()
        for info in unassignedTaskInfo.itertuples():
            requests.patch(base_url+f'tasks/{info.taskId}', headers=header_gs, data={"project":self.seledProj})

    @property
    def api_url(self):
        return get_api_url(self.base_url)
if __name__=="__main__":
    cfg_path = './dltools/config.json'
    cfg = readJson(cfg_path)
    session = get_sesstion('tmecnc62.iptime.org:11380', 'serveradmin', 'wnrWkd131@Cv')
    print(session)