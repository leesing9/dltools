from types import FunctionType
import requests

from dltools.utils import saveJson, readJson
from dltools.crypto import Crypt
from dltools.api.info import Info

from typing import Union, Type
from pathlib import Path

class API:
    def __init__(self, base_url:str) -> None:
        API.base_url = base_url

    @classmethod
    def get_api_url(cls, target)->str:
        if cls.base_url.endswith('/'):
            target_url = f'{cls.base_url}api/v1/{target}'
        else:
            target_url = f'{cls.base_url}/api/v1/{target}'

        if cls.base_url.startswith('http://'):
            target_url = cls.base_url
        elif cls.base_url.startswith('https://'):
            target_url = cls.base_url.replace('https://', 'http://')
        else:
            target_url = ''.join(['http://',target_url])

        return target_url

    def login(self, username:str, password:str)->Union[requests.Session,bool]:
        session = requests.session()
        crypto = Crypt()

        cfg_path = Path(__file__).parent/'../config.json'
        cfg = readJson(cfg_path)
        cfg['username'] = username
        cfg['password'] = crypto.encrypt(password)
        cfg['base_url'] = API.base_url
        saveJson(cfg_path, cfg)

        data = {'username': username,
                'password': password}

        r = session.post(self.get_api_url('auth') + '/login', data=data, timeout=3)
        r.raise_for_status()
        if 'csrftoken' in r.cookies:
            session.headers['X-CSRFToken'] = r.cookies['csrftoken']
        API.session = session
        return r.json()
    
    def run_api(func:FunctionType, *aug, **kwdag):
        try:
            return func(*aug, **kwdag)
        except Exception as e:
            print(e)
            return False


class CommAPI(API):
    def __init__(self, info_class) -> None:
        self.InfoClass = info_class
        self.target_url = self.get_api_url('')

    def get(self, **params)->Union[dict,bool]: 
        r = self.session.get(self.target_url, params=params)
        r.raise_for_status()
        result = r.json()
        result['results'] = [self.InfoClass(target) for target in result['results']]
        return result

    def get_id(self, id:Union[int, str])->Union[Type[Info],bool]:
        if isinstance(id, int) or (id=='self'):
            r = self.session.get(self.target_url + f'/{id}')
            r.raise_for_status()
            return self.InfoClass(r.json())
        else:
            print('id가 \"self\"나 \"숫자\"가 아닙니다.')
            return False
    
    def del_id(self, id:int)->bool:
        r = self.session.delete(self.target_url+f'/{id}')
        r.raise_for_status()
        if r.status_code == 204:
            return r.json()
        else:
            return False
    
    def create(self, **kwdag):
        data = self.InfoClass().create(**kwdag)
        r = self.session.post(self.target_url, data=data)
        r.raise_for_status()
        return self.InfoClass(r.json())
