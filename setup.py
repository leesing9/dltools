from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_call

install_requires = [
        'cython',
        'easydict',
        'tqdm',
        'numpy<=1.19.3',
        'opencv-python',
        'pillow',
        'tensorflow',
        "pycocotools @ git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI ;platform_system=='Windows'",
        'datumaro @ git+https://github.com/zmfkzj/datumaro'
    ]

class PreInstallCommand(install):
    """Pre-installation for installation mode."""
    def run(self):
        check_call("apt-get install -r requirment.txt".split())
        install.run(self)

setup(
    name='dltools',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=install_requires,
    include_package_data = True,
    cmdclass={
        'install':PreInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'dltools=dltools.DatasetTools:main'
        ]
    }
)