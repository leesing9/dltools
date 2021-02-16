from enum import Enum
from dltools.api.api import CommAPI
from dltools.api.info import ProjectInfo, LabelInfo, TaskInfo, UserInfo

from typing import List

class ProjectAPI(CommAPI):
    def __init__(self) -> None:
        super().__init__(ProjectInfo)
        self.target_url = self.get_api_url('projects')

    @staticmethod
    def get_params(projname:str=None, owner:UserInfo=None, status:str='annotation', id:int=None, page:int=None, page_size:int=None):
        params = {'name':projname,
                  'id': id,
                  'status':status,
                  'owner':owner['username'],
                  'page':page,
                  'page_size':page_size}
        return {key:val for key, val in params.items() if val}

    def create(self, **kwdag):
        '''
        name:str, owner:UserInfo, labels:List[LabelInfo]
        '''
        return super().create(**kwdag)

    def get_tasks(self, id):
        r = self.session.get(self.target_url+f'/{id}/tasks')
        r.raise_for_status()
        result = r.json()
        result['results'] = [TaskInfo(task) for task in result['results']]
        return result

if __name__ == '__main__':
    project_api = ProjectAPI()
    print(project_api.session)
