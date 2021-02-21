from dltools.api.info import UserInfo
from dltools.api.api import API, run_api

class AuthAPI(API):
    def __init__(self, base_url:str) -> None:
        super().__init__(base_url)
        self.target_url = self.get_api_url('auth')

    @run_api
    def register(self, username:str, password:str)->None:
        data = {'username': username,
                'password1': password,
                'password2': password}
        r = self.session.post(self.target_url + '/register', data=data)
        self.r = r
        r.raise_for_status()
        return UserInfo(r.json())
