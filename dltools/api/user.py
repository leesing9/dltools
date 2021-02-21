from dltools.api.api import CommAPI
from dltools.api.info import UserInfo

from typing import Union

class UserAPI(CommAPI):
    def __init__(self) -> None:
        super().__init__(UserInfo)
        self.target_url = self.get_api_url('users')

    def get(self, search:str=None, id:int=None, page:int=None, page_size:int=None, **kwd)->Union[dict,bool]:
        params = {'search':search,
                  'id': id,
                  'page':page,
                  'page_size':page_size}
        params.update(kwd)
        return super().get(**params)

    def create(self):
        raise AttributeError
