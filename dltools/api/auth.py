from dltools.api.api import API

class AuthAPI(API):
    def __init__(self, base_url:str) -> None:
        super().__init__(base_url, 'auth')
        self.target_url = self.get_api_url('auth')

    def register(self, username:str, password:str)->None:
        data = {'username': username,
                'password': password}
        try:
            r = self.session.post(self.target_url + '/register', data=data)
            r.raise_for_status()
        except Exception as e:
            print(e)
