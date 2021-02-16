import os 
import mimetypes

from io import BytesIO
from pathlib import Path
from PIL import Image
from dltools.api.api import CommAPI
from dltools.api.info import JobInfo, LabelInfo, TaskInfo, UserInfo

from enum import Enum
from time import sleep

class TaskAPI(CommAPI):
    def __init__(self) -> None:
        super().__init__(TaskInfo)
        self.target_url = self.get_api_url('projects')

    @staticmethod
    def get_targets_params(name:str=None, owner:UserInfo=None, mode:str=None, assignee:str=None, status:str='annotation', id:int=None, page:int=None, page_size:int=None):
        params = {'name':name,
                  'id': id,
                  'status':status,
                  'owner':owner['username'],
                  'mode':mode,
                  'assignee':assignee,
                  'page':page,
                  'page_size':page_size}
        return {key:val for key, val in params.items() if val}

    def create(self, **kwdag):
        '''
        name:str, owner:UserInfo, labels:List[LabelInfo],
        resource_type:str= local, share, remote
        resources:str
        '''
        return super().create(**kwdag)

    def download_anno(self, id, format, filename):
        url = self.target_url+f'/{id}/annotations?format={format}&filename={filename}'
        while True:
            r = self.session.get(url)
            r.raise_for_status()
            if r.status_code == 201:
                break

        r = self.session.get(url + '&action=download')
        r.raise_for_status()

        with open(filename, 'wb') as fp:
            fp.write(r.content)
        result = r.json()
        return result
    
    def upload_anno(self, id:int, format:str, filename:Path):
        url = self.target_url+f'/{id}/annotations?format={format}'
        files={'annotation_file': open(str(filename), 'rb')}
        while True:
            r = self.session.put(url, files=files)
            r.raise_for_status()
            if r.status_code == 201:
                break
        result = r.json()
        return result

    def del_anno(self, id:int):
        r = self.session.delete(self.target_url+f'/{id}/annotations')
        r.raise_for_status()
        if r.status_code == 204:
            return r.json()
        else:
            return False

    def download_frame(self, id:int, frame_id:int, outdir:Path):
        url = self.target_url + f'/{id}/data?type=frame&number={frame_id}&quality=original'
        r = self.session.get(url)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content))
        mime_type = img.get_format_mimetype() or 'image/jpg'
        im_ext = mimetypes.guess_extension(mime_type)
        if im_ext == '.jpe' or '.jpeg' or None:
            im_ext = '.jpg'
        outfile = 'task_{}_frame_{:06d}{}'.format(id, frame_id, im_ext)
        img.save(str(outdir/outfile))
        return TaskInfo(r.json())

    def attach_data(self, id:int, resource_type:str, resources:list):
        """ Add local, remote, or shared files to an existing task. """
        url = self.api.tasks_id_data(id)
        data = {}
        files = None
        resources.sort()
        if resource_type == ResourceType.LOCAL:
            files = {'client_files[{}]'.format(i): open(f, 'rb') for i, f in enumerate(resources)}
        elif resource_type == ResourceType.REMOTE:
            data = {'remote_files[{}]'.format(i): f for i, f in enumerate(resources)}
        elif resource_type == ResourceType.SHARE:
            data = {'server_files[{}]'.format(i): f for i, f in enumerate(resources)}
        data['image_quality'] = 100
        r = self.session.post(url, data=data, files=files)
        r.raise_for_status()
        return r.json()

    def get_data_meta(self, id):
        url = self.target_url + f'/{id}/data/meta'
        r = self.session.get(url)
        r.raise_for_status()
        return r.json()

    def download_dataset(self, id:int, format:str, filename:Path):
        url = self.target_url+f'/{id}/dataset?format={format}&filename={filename}'
        while True:
            r = self.session.get(url)
            r.raise_for_status()
            if r.status_code == 201:
                break

        r = self.session.get(url + '&action=download')
        r.raise_for_status()

        if filename.suffix != '.zip':
            filename = filename.with_suffix('.zip')
        with open(str(filename), 'wb') as fp:
            fp.write(r.content)
        result = r.json()
        return result

    def get_jobs(self, id:int):
        url = self.target_url + f'/{id}/jobs'
        r = self.session.get(url)
        r.raise_for_status()
        return [JobInfo(job) for job in r.json()]

    def get_status(self, id:int):
        url = self.target_url + f'/{id}/status'
        r = self.session.get(url)
        r.raise_for_status()
        return r.json()

class ResourceType(Enum):

    LOCAL = 0
    SHARE = 1
    REMOTE = 2

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return str(self)

    @staticmethod
    def argparse(s):
        try:
            return ResourceType[s.upper()]
        except KeyError:
            return s