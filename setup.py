from setuptools import setup, find_packages
# from setuptools.command.install import install
from subprocess import check_call
import sys

install_requires = [
        # 'cython',
        'easydict',
        'tqdm',
        'numpy<=1.19.3',
        'opencv-python',
        'pillow',
        'tensorflow',
        "pycocotools @ git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI ;platform_system=='Windows'",
        'datumaro @ git+https://github.com/zmfkzj/datumaro'
    ]

# class PreInstallCommand(install):
#     """Pre-installation for installation mode."""
#     def run(self):
#         check_call([sys.executable, '-m'] + "pip install -r requirements.txt".split())
#         install.run(self)

check_call([sys.executable, '-m'] + "pip install -r requirements.txt".split())
setup(
    name='dltools',
    version='0.0.1',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=install_requires,
    include_package_data = True,
    # cmdclass={
    #     'install':PreInstallCommand,
    # },
    entry_points={
        'console_scripts': [
            'dltools=dltools.DatasetTools:main'
        ]
    }
)