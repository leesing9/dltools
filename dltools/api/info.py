from enum import Enum, auto
from typing import List
from functools import reduce

class _Enum(Enum):
    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return str(self)

class Info(dict):
    class Elems(_Enum):pass
    class CreateParams(_Enum):pass

    def __init__(self):
        super().__init__()
        self.set_elems()

    def set_elems(self):
        for elem in self.Elems.__members__.keys():
            elem = elem.lower()
            try:
                if elem in ['owner', 'assignee']:
                    setattr(self, elem, UserInfo(self[elem]))
                elif elem =='tasks':
                    setattr(self, elem, [TaskInfo(task) for task in self[elem]])
                elif elem =='labels':
                    setattr(self, elem, [LabelInfo(task) for task in self[elem]])
                elif elem =='segments':
                    setattr(self, elem, [SegmentInfo(task) for task in self[elem]])
                elif elem =='attributes':
                    setattr(self, elem, [AttributeInfo(task) for task in self[elem]])
                elif elem =='jobs':
                    setattr(self, elem, [JobInfo(task) for task in self[elem]])
                else:
                    setattr(self, elem, self[elem])
            except KeyError:
                setattr(self, elem, None)

    def update_dict(self):
        for elem in self.Elems.__members__.keys():
            elem = elem.lower()
            if (elem_value:=getattr(self, elem)) is not None:
                self[elem] = elem_value

    def create(self, **kwdag):
        create_params = set([key.lower() for key in self.CreateParams.__members__.keys()])
        if create_params==set([key.lower() for key in kwdag.keys()]):
            for elem, val in kwdag.items():
                setattr(self, elem, val)
            self.update_dict()
            return self
        else:
            print('올바른 인수를 입력하세요.')

class UserInfo(Info):
    Elems = _Enum('Elems', ' '.join(['url', 'id', 'username', 'first_name', 'last_name', 'email', 'groups',
            'is_staff', 'is_superuser', 'is_active']).upper())
    def __init__(self):
        super().__init__(UserInfo.Elems)

class SegmentInfo(Info):
    Elems = _Enum('Elems', ' '.join(['start_frame', 'stop_frame', 'jobs']).upper())

    def __init__(self):
        super().__init__(SegmentInfo.Elems)

class JobInfo(Info):
    Elems = _Enum('Elems', ' '.join(['url', 'id', 'assignee', 'reviewer', 'status']).upper())

    def __init__(self):
        super().__init__(JobInfo.Elems)
        
class AttributeInfo(Info):
    class Elems(_Enum):
        ID = auto()
        NAME = auto()
        MUTABLE = auto()
        INPUT_TYPE = auto()
        DEFAULT_VALUE = auto()
        VALUES = auto()

    class CreateParams(_Enum):
        NAME = auto()
        MUTABLE = auto()
        INPUT_TYPE = auto()
        DEFAULT_VALUE = auto()
        VALUES = auto()

    def __init__(self):
        super().__init__(AttributeInfo.Elems)


    def create(self, name:str, input_type:str, values:List[str], mutable:bool=False, default_value:str=None):
        if default_value is None:
            default_value = values[0]
        create_elems = {'name':name, 
                        'input_type':input_type, 
                        'values':values, 
                        'mutable':mutable, 
                        'default_value':default_value}
        for elem, val in create_elems.items():
            setattr(self, elem, val)
        self.update_dict()

class LabelInfo(Info):
    Elems = _Enum('Elems', ' '.join(['id', 'name', 'color', 'attributes']).upper())

    class CreateParams(_Enum):
        NAME = auto()
        ATTRIBUTES = auto()

    def __init__(self):
        super().__init__(LabelInfo.Elems)

    def create(self, name:str, attributes:List[AttributeInfo]=[]):
        create_elems = {'name':name, 'attributes':attributes}
        for elem, val in create_elems.items():
            setattr(self, elem, val)
        self.update_dict()

class TaskInfo(Info):
    Elems = _Enum('Elems', ' '.join(['url', 'id', 'name', 'project_id', 'mode', 'labels', 'data', 'dimension',
                'owner', 'assignee', 'bug_tracker', 'segments', 'size', 'image_quality',
                'created_data', 'updated_date', 'status', 'overlap', 'segment_size']).upper())

    class CreateParams(_Enum):
        NAME = auto()
        OWNER = auto()
        LABELS = auto()

    # def __init__(self):
    #     super().__init__(TaskInfo.Elems)

    # def create(self, name:str, owner:UserInfo, labels:LabelInfo):
    #     create_elems = {'name':name, 'owner':owner, 'labels':labels}
    #     for elem, val in create_elems.items():
    #         setattr(self, elem, val)
    #     self.update_dict()

class ProjectInfo(Info):
    Elems = _Enum('Elems', ' '.join(['url', 'id', 'name', 'labels', 'tasks', 
                'owner', 'assignee', 'bug_tracker', 
                'created_data', 'updated_date', 'status']).upper())

    class CreateParams(_Enum):
        NAME = auto()
        OWNER = auto()
        LABELS = auto()

    def __init__(self):
        super().__init__(ProjectInfo.Elems)

    def create(self, name:str, owner:UserInfo, labels:LabelInfo=[]):
        create_elems = {'name':name, 'owner':owner, 'labels':labels}
        for elem, val in create_elems.items():
            setattr(self, elem, val)
        self.update_dict()

class DataInfo(Info):
    class Elems(_Enum):
        CHUNK_SIZE = auto()
        SIZE = auto()
        IMAGE_QUALITY= auto()
        START_FRAME = auto()
        STOP_FRAME = auto()
        FRAME_FILTER = auto()
        COMPRESSED_CHUNK_TYPE = auto()
        ORIGINAL_CHUNK_TYPE = auto()
        CLIENT_FILES = auto()
        SERVER_FILES = auto()
        REMOTE_FILES = auto()
        USE_ZIP_CHUNKS = auto()
        USE_CACHE = auto()
        COPY_DATA = auto()

    def __init__(self):
        super().__init__(ProjectInfo.Elems)

    def create(self, image_quality:int, owner:UserInfo, labels:LabelInfo=[]):
        create_elems = {'name':name, 'owner':owner, 'labels':labels}
        for elem, val in create_elems.items():
            setattr(self, elem, val)
        self.update_dict()
        

if __name__ == "__main__":
    params = TaskInfo().create(name='asdf', owner='asdf', labels='qwe')
    print(params)
