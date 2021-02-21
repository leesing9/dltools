from enum import Enum, auto
from typing import List
from typing import Union

class _Enum(Enum):
    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return str(self)

class Info(dict):
    class Elems(_Enum):pass

    def __init__(self,*arg):
        super().__init__(*arg)
        self.set_elems()

    def set_elems(self):
        for elem in self.Elems.__members__.keys():
            elem = elem.lower()
            try:
                if self[elem] is not None:
                    if elem in ['owner', 'assignee', 'reviewer', 'resolver']:
                        setattr(self, elem, AuthorInfo(self[elem]))
                    elif elem =='tasks':
                        setattr(self, elem, [TaskInfo(task) for task in self[elem]])
                    elif elem =='labels':
                        setattr(self, elem, [LabelInfo(label) for label in self[elem]])
                    elif elem =='segments':
                        setattr(self, elem, [SegmentInfo(seg) for seg in self[elem]])
                    elif elem =='attributes':
                        if self.__class__ in [LabeledImageInfo, LabeledShapeInfo, LabeledTrackInfo, TrackedShapeInfo]:
                            setattr(self, elem, [AttributeValInfo(attr) for attr in self[elem]])
                        else:
                            setattr(self, elem, [AttributeInfo(attr) for attr in self[elem]])
                    elif elem =='jobs':
                        if self.__class__ == SegmentInfo:
                            setattr(self, elem, [SimpleJobInfo(i) for i in self[elem]])
                    elif elem =='frames':
                        setattr(self, elem, [FrameMetaInfo(i) for i in self[elem]])
                    elif elem =='shapes':
                        if self.__class__ == LabeledDataInfo:
                            setattr(self, elem, [LabeledShapeInfo(i) for i in self[elem]])
                        elif self.__class__ == LabeledTrackInfo:
                            setattr(self, elem, [TrackedShapeInfo(i) for i in self[elem]])
                        else:
                            raise Exception()
                    elif elem =='comment_set':
                        setattr(self, elem, [CommentInfo(i) for i in self[elem]])
                    else:
                        setattr(self, elem, self[elem])
                else:
                    setattr(self, elem, None)
            except KeyError: pass
            except Exception as e: print(e)

    def update_dict(self):
        for elem in self.Elems.__members__.keys():
            elem = elem.lower()
            if hasattr(self,elem):
                if (elem_value:=getattr(self, elem)) is not None:
                    self[elem] = elem_value

    def create(self, **elems)->Union[dict,None]:
        for elem, val in elems.items():
            setattr(self, elem, val)
        self.update_dict()
        return self

class AuthorInfo(Info):
    class Elems(_Enum):
        URL = auto()
        ID = auto()
        USERNAME = auto()
        FIRST_NAME = auto()
        LAST_NAME = auto()

    def create(self, username:str, **kwd):
        create_elems = {'username':username}
        create_elems.update(kwd)
        return super().create(**create_elems)

class UserInfo(Info):
    Elems = _Enum('Elems', ' '.join(['url', 'id', 'username', 'first_name', 'last_name', 'email', 'groups',
            'is_staff', 'is_superuser', 'is_active']).upper())

class SegmentInfo(Info):
    Elems = _Enum('Elems', ' '.join(['start_frame', 'stop_frame', 'jobs']).upper())

class JobInfo(Info):
    Elems = _Enum('Elems', ' '.join(['url', 'id', 'assignee assignee_id', 
            'reviewer reviewer_id', 'status', 'start_frame stop_frame task_id']).upper())
        
class AttributeInfo(Info):
    class Elems(_Enum):
        ID = auto()
        NAME = auto()
        MUTABLE = auto()
        INPUT_TYPE = auto()
        DEFAULT_VALUE = auto()
        VALUES = auto()

    def create(self, name:str, input_type:str, values:List[str], mutable:bool=False, default_value:str=None, **kwd):
        if default_value is None:
            default_value = values[0]
        create_elems = {'name':name, 
                        'input_type':input_type, 
                        'values':values, 
                        'mutable':mutable, 
                        'default_value':default_value}
        create_elems.update(kwd)
        return super().create(**create_elems)

class LabelInfo(Info):
    Elems = _Enum('Elems', ' '.join(['id', 'name', 'color', 'attributes']).upper())

    def create(self, name:str, attributes:List[AttributeInfo]=[], **kwd):
        create_elems = {'name':name, 'attributes':attributes}
        create_elems.update(kwd)
        return super().create(**create_elems)

class TaskInfo(Info):
    Elems = _Enum('Elems', ' '.join(['url', 'id', 'name', 'project_id', 'mode', 'labels', 'data', 'dimension',
                'owner', 'assignee', 'bug_tracker', 'segments', 'size', 'image_quality',
                'created_data', 'updated_date', 'status', 'overlap', 'segment_size']).upper())

    def create(self, name:str, labels:LabelInfo=None, project_id:int=None, **kwd):
        if (labels is None) ^ (project_id is None):
            create_elems = {'name':name, 'labels':labels, 'project_id':project_id}
            create_elems.update(kwd)
        else:
            raise Exception('labels와 project_id 중 하나만 입력하세요.')
        return super().create(**create_elems)

class ProjectInfo(Info):
    Elems = _Enum('Elems', ' '.join(['url', 'id', 'name', 'labels', 'tasks', 
                'owner', 'assignee', 'bug_tracker', 
                'created_data', 'updated_date', 'status']).upper())

    def create(self, name:str,  labels:LabelInfo=[], **kwd):
        create_elems = {'name':name, 'labels':labels}
        create_elems.update(kwd)
        return super().create(**create_elems)

class DataMetaInfo(Info):
    class Elems(_Enum):
        CHUNK_SIZE = auto()
        SIZE = auto()
        IMAGE_QUALITY= auto()
        START_FRAME = auto()
        STOP_FRAME = auto()
        FRAME_FILTER = auto()
        FRAMES = auto()

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

class FrameMetaInfo(Info):
    class Elems(_Enum):
        WIDTH = auto()
        HEIGHT = auto()
        NAME = auto()

class StatusInfo(Info):
    class Elems(_Enum):
        STATE = auto()
        MESSAGE = auto()

class LabeledDataInfo(Info):
    class Elems(_Enum):
        VERSION = auto()
        TAGS = auto()
        SHAPES = auto()
        TRACKS = auto()

class LabeledImageInfo(Info):
    class Elems(_Enum):
        ID = auto()
        FRAME = auto()
        LABEL_ID = auto()
        GROUP = auto()
        SOURCE = auto()
        ATTRIBUTES = auto()

class LabeledShapeInfo(Info):
    class Elems(_Enum):
        TYPE = auto()
        OCCLUDED = auto()
        Z_ORDER = auto()
        POINTS = auto()
        ID = auto()
        FRAME = auto()
        LABEL_ID = auto()
        GROUP = auto()
        SOURCE = auto()
        ATTRIBUTES = auto()

class LabeledTrackInfo(Info):
    class Elems(_Enum):
        ID = auto()
        FRAME = auto()
        LABEL_ID = auto()
        GROUP = auto()
        SOURCE = auto()
        SHAPES = auto()
        ATTRIBUTES = auto()

class AttributeValInfo(Info):
    class Elems(_Enum):
        SPEC_ID = auto()
        VALUE = auto()

class TrackedShapeInfo(Info):
    class Elems(_Enum):
        TYPE = auto()
        OCCLUDED = auto()
        Z_ORDER = auto()
        POINTS = auto()
        ID = auto()
        FRAME = auto()
        OUTSIDE = auto()
        ATTRIBUTES = auto()

class CombinedIssueInfo(Info):
    class Elems(_Enum):
        ID = auto()
        OWNER = auto()
        OWNER_ID = auto()
        RESOLVER =auto() 
        RESOLVER_ID = auto()
        POSITION = auto()
        COMMENT_SET = auto()
        FRAME = auto()
        CREATED_DATE =auto() 
        RESOLVED_DAATE = auto()
        JOB = auto()
        REVIEW = auto()

class CommentInfo(Info):
    class Elems(_Enum):
        ID = auto()
        AUTHOR = auto()
        AUTHOR_ID = auto()
        MESSAGE = auto()
        CREATED_DATE = auto()
        UPDATED_DATE = auto()
        ISSUE = auto()

class ReviewInfo(Info):
    class Elems(_Enum):
        ASSIGNEE = auto()
        ASSIGNEE_ID = auto()
        REVIEWER = auto()
        REVIEWER_ID = auto()
        ESTIMATED_QUALITY = auto()
        STATUS = auto()
        JOB = auto()

class SimpleJobInfo(Info):
    Elems = _Enum('Elems', ' '.join(['url', 'id', 'assignee assignee_id', 
            'reviewer reviewer_id', 'status']).upper())


if __name__ == "__main__":
    params = TaskInfo().create(name='asdf', owner='asdf', labels='qwe')
    print(params)
