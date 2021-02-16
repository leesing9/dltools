from dltools.api.api import CommAPI
from dltools.api.info import UserInfo

from typing import Union

class UserAPI(CommAPI):
    def __init__(self) -> None:
        super().__init__(UserInfo)
        self.target_url = self.get_api_url('users')

    @staticmethod
    def get_params(username:str=None, id:int=None, page:int=None, page_size:int=None)->Union[dict,bool]:
        params = {'username':username,
                  'id': id,
                  'page':page,
                  'page_size':page_size}
        return {key:val for key, val in params.items() if val}

    def create(self):
        raise AttributeError