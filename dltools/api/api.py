import requests

from dltools.dataset.utils import saveJson, readJson
from dltools.dataset.crypto import Crypt
from dltools.api.info import Info

from typing import Union, Type
from pathlib import Path
from types import FunctionType
from easydict import EasyDict

def run_api(func:FunctionType):
    def wrapper(self, *arg, **kwdargs):
        try:
            return func(self, *arg, **kwdargs)
        except Exception as e:
            print(e)
            print(self.r.text)
            return False
    return wrapper

        
class API:
    def __init__(self, base_url:str='') -> None:
        API.base_url = base_url
        self.r = EasyDict({'text':''})

    @classmethod
    def get_api_url(cls, target)->str:
        if cls.base_url.endswith('/'):
            target_url = f'{cls.base_url}api/v1/{target}'
        else:
            target_url = f'{cls.base_url}/api/v1/{target}'

        if cls.base_url.startswith('http://'):
            return target_url
        elif cls.base_url.startswith('https://'):
            target_url = target_url.replace('https://', 'http://')
        else:
            target_url = ''.join(['http://',target_url])

        return target_url

    @run_api
    def login(self, username:str=None, password:str=None)->Union[requests.Session,bool]:
        session = requests.session()

        data = {'username': username,
                'password': password}

        r = session.post(self.get_api_url('auth') + '/login', data=data, timeout=3)
        self.r = r
        r.raise_for_status()
        if 'csrftoken' in r.cookies:
            session.headers['X-CSRFToken'] = r.cookies['csrftoken']
        API.session = session

        crypto = Crypt()
        cfg_path = Path(__file__).parent/'../config.json'
        cfg = readJson(cfg_path)
        cfg['username'] = username
        cfg['password'] = crypto.encrypt(password)
        cfg['base_url'] = API.base_url
        saveJson(cfg_path, cfg)

        return r.json()
    


class CommAPI(API):
    def __init__(self, info_class) -> None:
        self.InfoClass = info_class
        self.target_url = self.get_api_url('')
        self.r = EasyDict({'text':''})

    @run_api
    def get(self, **params)->Union[dict,bool]: 
        params = {key:val for key, val in params.items() if val}
        r = self.session.get(self.target_url, params=params)
        self.r = r
        r.raise_for_status()
        result = r.json()
        result['results'] = [self.InfoClass(target) for target in result['results']]
        return result

    @run_api
    def get_id(self, id:Union[int, str])->Union[Type[Info],bool]:
        if isinstance(id, int) or (id=='self'):
            r = self.session.get(self.target_url + f'/{id}')
            self.r = r
            r.raise_for_status()
            if id=='self':
                return [self.InfoClass(target) for target in r.json()['results']][0]
            return self.InfoClass(r.json())
        else:
            print('id가 \"self\"나 \"숫자\"가 아닙니다.')
            return False
    
    @run_api
    def del_id(self, id:int)->bool:
        r = self.session.delete(self.target_url+f'/{id}')
        self.r = r
        r.raise_for_status()
        if r.status_code == 204:
            return True
        else:
            return False
            
    @run_api
    def patch_id(self, id, **kwd):
        r = self.session.patch(self.target_url + f'/{id}', json=kwd)
        self.r = r
        r.raise_for_status()
        return self.InfoClass(r.json())
    
    @run_api
    def create(self, **kwd):
        data = self.InfoClass().create(**kwd)
        r = self.session.post(self.target_url, json=data)
        self.r = r
        r.raise_for_status()
        return self.InfoClass(r.json())
