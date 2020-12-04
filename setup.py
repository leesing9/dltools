from setuptools import setup, find_packages, dist
import os

install_requires = [
        'cython',
        'easydict',
        'tqdm',
        'numpy<=1.19.3',
        'opencv-python',
        'pillow',
        "pycocotools @ git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI ;platform_system=='Windows'",
        'datumaro @ git+https://github.com/zmfkzj/datumaro'
    ]

# osName = os.name
# if osName =='nt':
#     pycocotoolsUrl = 'pycocotools @ git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI'
#     install_requires.insert(1,pycocotoolsUrl)

# dist.Distribution().fetch_build_eggs([
#     'Cython>=0.27.3' # required for pycocotools and others, if need to compile
# ])

setup(
    name='dltools',
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