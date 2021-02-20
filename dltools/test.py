from dltools.api.auth import AuthAPI
from dltools.api.task import TaskAPI
from dltools.api.project import ProjectAPI

base_url = 'http://tmecnc62.iptime.org:12380'
auth = AuthAPI(base_url)

username = 'serveradmin'
password = 'wnrWkd131@Cv'
auth.login(username=username, password=password)

##make project
project = ProjectAPI()
project.get(project.get_params())