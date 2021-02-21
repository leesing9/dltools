from dltools.api.api import CommAPI, run_api
from dltools.api.info import ProjectInfo,TaskInfo

from typing import List

class ProjectAPI(CommAPI):
    def __init__(self) -> None:
        super().__init__(ProjectInfo)
        self.target_url = self.get_api_url('projects')

    def get(self, search:str=None, owner:str=None, status:str='annotation', id:int=None, page:int=None, page_size:int=None, **kwd):
        params = {'search':search,
                  'id': id,
                  'status':status,
                  'owner':owner,
                  'page':page,
                  'page_size':page_size}
        params.update(kwd)
        return super().get(**params)

    @run_api
    def get_tasks(self, proj_id:int):
        r = self.session.get(self.target_url+f'/{proj_id}/tasks')
        r.raise_for_status()
        result = r.json()
        result['results'] = [TaskInfo(task) for task in result['results']]
        return result

# if __name__ == '__main__':
