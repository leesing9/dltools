from setuptools import setup, find_packages
from subprocess import check_call
import sys

install_requires = [
        'easydict',
        'tqdm',
        'opencv-python',
        'pillow',
        'tensorflow',
        'requests',
        'cryptography',
        "pycocotools @ git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI ;platform_system=='Windows'",
        'datumaro @ git+https://github.com/zmfkzj/datumaro'
    ]

check_call([sys.executable, '-m'] + "pip install -r requirements.txt".split())
setup(
    name='dltools',
    version='1.0.0',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=install_requires,
    include_package_data = True,
    entry_points={
        'console_scripts': [
            'dltools=dltools.DatasetTools:main'
        ]
    }
)