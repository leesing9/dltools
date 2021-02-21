from io import BytesIO
from pathlib import Path
from PIL import Image
from enum import Enum

from dltools.api.api import CommAPI, run_api
from dltools.api.info import DataMetaInfo, JobInfo,StatusInfo, TaskInfo

class TaskAPI(CommAPI):
    def __init__(self) -> None:
        super().__init__(TaskInfo)
        self.target_url = self.get_api_url('tasks')

    def get(self, search:str=None, owner:str=None, mode:str=None, assignee:str=None, status:str=None, id:int=None, page:int=None, page_size:int=None, **kwd):
        params = {'search':search,
                  'id': id,
                  'status':status,
                  'owner':owner,
                  'mode':mode,
                  'assignee':assignee,
                  'page':page,
                  'page_size':page_size}
        params.update(kwd)
        return super().get(**params)

    @run_api
    def download_anno(self, id, format, filename, outdir):
        '''            
            'COCO 1.0',
            'CVAT 1.1',
            'LabelMe 3.0',
            'MOT 1.1',
            'MOTS PNG 1.0',
            'PASCAL VOC 1.1',
            'Segmentation mask 1.1',
            'TFRecord 1.0',
            'YOLO 1.1',
            'ImageNet 1.0'
        '''
        url = self.target_url+f'/{id}/annotations?format={format}&filename={filename}'
        while True:
            r = self.session.get(url)
            self.r = r
            r.raise_for_status()
            if r.status_code == 201:
                break

        r = self.session.get(url + '&action=download')
        self.r = r
        r.raise_for_status()

        with open(str(Path(outdir)/filename), 'wb') as fp:
            fp.write(r.content)
        return r.ok
    
    @run_api
    def upload_anno(self, id:int, format:str, filename:Path):
        '''            
            'COCO 1.0',
            'CVAT 1.1',
            'LabelMe 3.0',
            'MOT 1.1',
            'MOTS PNG 1.0',
            'PASCAL VOC 1.1',
            'Segmentation mask 1.1',
            'TFRecord 1.0',
            'YOLO 1.1',
            'ImageNet 1.0'
        '''
        url = self.target_url+f'/{id}/annotations?format={format}'
        files={'annotation_file': open(str(filename), 'rb')}
        while True:
            r = self.session.put(url, files=files)
            self.r = r
            r.raise_for_status()
            if r.status_code == 201:
                break

        return r.ok

    @run_api
    def del_anno(self, id:int):
        r = self.session.delete(self.target_url+f'/{id}/annotations')
        self.r = r
        r.raise_for_status()
        return r.ok

    @run_api
    def download_frame(self, id:int, frame_id:int, outdir:str):
        url = self.target_url + f'/{id}/data?type=frame&number={frame_id}&quality=original'
        r = self.session.get(url)
        self.r = r
        r.raise_for_status()
        img = Image.open(BytesIO(r.content))
        # mime_type = img.get_format_mimetype() or 'image/jpg'
        # im_ext = mimetypes.guess_extension(mime_type)
        meta = self.get_data_meta(id)
        filename = Path(meta.frames[frame_id].name).name
        img.save(str(Path(outdir)/filename))
        return img

    @run_api
    def attach_data(self, id:int, resource_type:str, resources:list, image_quality:int=100):
        """ Add local, remote, or shared files to an existing task. """
        url = self.target_url + f'/{id}/data'
        data = {}
        files = None
        if not isinstance(resources, list):
            resources = [resources]
        resources.sort()
        resource_type = ResourceType[resource_type.upper()]
        if resource_type == ResourceType.LOCAL:
            files = {'client_files[{}]'.format(i): open(f, 'rb') for i, f in enumerate(resources)}
        elif resource_type == ResourceType.REMOTE:
            data = {'remote_files[{}]'.format(i): f for i, f in enumerate(resources)}
        elif resource_type == ResourceType.SHARE:
            data = {'server_files[{}]'.format(i): f for i, f in enumerate(resources)}
        data['image_quality'] = image_quality
        r = self.session.post(url, data=data, files=files)
        self.r = r
        r.raise_for_status()
        return r.ok

    @run_api
    def get_data_meta(self, id):
        url = self.target_url + f'/{id}/data/meta'
        r = self.session.get(url)
        self.r = r
        r.raise_for_status()
        return DataMetaInfo(r.json())

    @run_api
    def download_dataset(self, id:int, format:str, filename:str, outdir:Path):
        url = self.target_url+f'/{id}/dataset?format={format}&filename={filename}'
        while True:
            r = self.session.get(url)
            self.r = r
            r.raise_for_status()
            if r.status_code == 201:
                break

        r = self.session.get(url + '&action=download')
        self.r = r
        r.raise_for_status()

        filename = Path(filename)
        if filename.suffix != '.zip':
            filename = filename.with_suffix('.zip')
        with open(str(Path(outdir)/filename), 'wb') as fp:
            fp.write(r.content)
        return r.ok

    @run_api
    def get_jobs(self, id:int):
        url = self.target_url + f'/{id}/jobs'
        r = self.session.get(url)
        self.r = r
        r.raise_for_status()
        return [JobInfo(job) for job in r.json()]

    @run_api
    def get_status(self, id:int):
        url = self.target_url + f'/{id}/status'
        r = self.session.get(url)
        self.r = r
        r.raise_for_status()
        return StatusInfo(r.json())

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