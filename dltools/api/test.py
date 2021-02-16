from enum import Enum, auto

class CreateParams(Enum):
    NAME = auto()
    OWNER = auto()
    LABELS = auto()

print(CreateParams.NAME.value)
CreateParams.NAME.value = 'name'
print(CreateParams.NAME.value)