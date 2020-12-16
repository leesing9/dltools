from pathlib import Path
from datumaro.cli.__main__ import main
from tkinter import Tk, filedialog
from tqdm import tqdm
from dltools.args import ImportArg, ExportArg, DrawItemArg
from dltools.args import Arg
from dltools.dataset import customDataset
from sys import exit
from datumaro.components.project import Project, Environment # project-related things
from datumaro.components.operations import IntersectMerge
from shutil import rmtree
from dltools.utils import remove_readonly

class Commands:
    def __init__(self) -> None:
        root = Tk()
        selectedDatasetPathStr = filedialog.askdirectory()
        if not bool(selectedDatasetPathStr):
            exit()
        self.datasetsPath = Path(selectedDatasetPathStr).absolute()
        root.destroy()
        self.projectsPath = (self.datasetsPath/'..'/f'projects').resolve().absolute()
        self.mergeFolderName = f'{self.datasetsPath.name}_merge'

    def importDataset(self, args:Arg):
        self.projectsPath.mkdir(exist_ok=True, parents=True)
        self.projectsPathListFromDataset = [self.projectsPath/path.name for path in self.getSubDirList(self.datasetsPath)]
        datasetPathList = [path for path in self.getSubDirList(self.datasetsPath) if path.is_dir()]
        for datasetPath in datasetPathList:
            projPath = self.projectsPath/datasetPath.name
            projImportArgs = ['project', 'import', '-i', str(datasetPath), '-o', str(projPath), '-f', args['format'].lower(), '--overwrite']
            main(projImportArgs)
        return self

    def mergeDataset(self, args:Arg):
        datasetPaths:list[Path] = self.getSubDirList(self.datasetsPath)
        source_datasets = [Environment().make_importer(args['format'])(str(path)).make_dataset() for path in datasetPaths]

        mergePath = (self.projectsPath/self.mergeFolderName)
        if mergePath.is_dir():
            rmtree(mergePath, onerror=remove_readonly)
        mergePath.mkdir(exist_ok=True, parents=True)
        dst_dir = str(mergePath)

        merger = IntersectMerge(conf=IntersectMerge.Conf())
        merged_dataset = merger(source_datasets)

        merged_project = Project()
        output_dataset = merged_project.make_dataset()
        output_dataset.define_categories(merged_dataset.categories())
        merged_dataset = output_dataset.update(merged_dataset)
        itemIds = [item.id for item in merged_dataset]
        itemIds.sort()
        annoId = 1
        if args['format']=='coco':
            imageIdName = 'id'
        elif args['format']=='cvat':
            imageIdName = 'frame'
        else:
            imageIdName = None
        for subset in merged_dataset.subsets():
            for idx, itemId in enumerate(itemIds):
                if imageIdName is not None:
                    merged_dataset.get(itemId,subset=subset).attributes[imageIdName] = idx+1
                for anno in merged_dataset.get(itemId, subset=subset).annotations:
                    anno.id = annoId
                    annoId += 1
            merged_dataset.save(save_dir=dst_dir, save_images=True)
        return self

    def exportDataset(self, args:Arg, merge=False):
        if merge:
            projectsPathList = [self.projectsPath/self.mergeFolderName]
        else:
            if not hasattr(self, 'projectsPathListFromDataset'):
                importArgs = ImportArg()
                self.importDataset(importArgs)
            projectsPathList = self.projectsPathListFromDataset

        for proj in projectsPathList:
            exportPath = (self.projectsPath/'..'/'export'/f'{proj.name}_{args["format"].lower()}').absolute()
            if exportPath.is_dir():
                rmtree(exportPath, onerror=remove_readonly)
            exportPath.mkdir(exist_ok=True, parents=True)
            export_args = ['project','export','-f',args['format'].lower(),'-o',str(exportPath),'-p',str(proj)]
            main(export_args)
        return self


    @staticmethod
    def getSubDirList(Path:Path):
        return [dir for dir in Path.iterdir() if dir.is_dir()]

    def mergeFunction(self):
        importArgs = ImportArg()
        exportArgs = ExportArg()
        self.mergeDataset(importArgs)
        self.exportDataset(exportArgs, merge=True)
        return self

    def convertFunction(self):
        importArgs = ImportArg()
        exportArgs = ExportArg()
        self.importDataset(importArgs)
        self.exportDataset(exportArgs)
        return self

    def drawItemFuncion(self):
        importArgs = ImportArg()
        drawItemArgs = DrawItemArg()
        self.importDataset(importArgs)
        self.loadDatasetFromProjFolder()
        self.drawItemOfEveryDataset(drawItemArgs)
        return self

    def loadDatasetFromProjFolder(self):
        if not hasattr(self, 'projectsPathListFromDataset'):
            importArgs = ImportArg()
            self.importDataset(importArgs)
        projectFolders = [path for path in self.projectsPathListFromDataset]
        projects = [Project.load(projectFolder) for projectFolder in projectFolders]
        self.datasets = [customDataset(project.make_dataset()) for project in projects]
        return self
    
    def drawItemOfEveryDataset(self, args:Arg):
        if not hasattr(self, 'projectsPathListFromDataset'):
            self.loadDatasetFromProjFolder()
        else:
            pass
        for dataset in tqdm(self.datasets):
            dataset.drawAndExport(args['lineStyle'], args['cornerStyle'])
        return self
