from copy import deepcopy
from pathlib import Path, PosixPath
from datumaro.cli.__main__ import main
from tkinter import Tk, filedialog
from datumaro.components.dataset import Dataset
from tqdm import tqdm
from dltools.args import ImportArg, ExportArg, DrawItemArg, NoAnnoFilterArg
from dltools.args import Arg
from dltools.dataset import customDataset
from dltools.config import setConfig
from sys import exit
from datumaro.components.project import Project, Environment, ProjectDataset # project-related things
from datumaro.components.operations import IntersectMerge
from shutil import copy, rmtree, move
from dltools.utils import remove_readonly
from functools import reduce

class Commands:
    def __init__(self) -> None:
        self.selWorkDir()

    def selWorkDir(self):
        root = Tk()
        selectedDatasetPathStr = filedialog.askdirectory()
        if not bool(selectedDatasetPathStr):
            exit()
        root.destroy()
        self.datasetsPath = Path(selectedDatasetPathStr).absolute()
        self.datasetPathList = self.getSubDirList(self.datasetsPath)
        self.projectsPath = (self.datasetsPath/'..'/f'projects').resolve().absolute()
        self.mergeFolderName = f'{self.datasetsPath.name}_merge'

    def importDataset(self, args:Arg):
        self.projectsPath.mkdir(exist_ok=True, parents=True)
        self.projectsPathListFromDataset = [self.projectsPath/path.name for path in self.getSubDirList(self.datasetsPath)]
        for datasetPath in self.datasetPathList:
            projPath = self.projectsPath/datasetPath.name
            projImportArgs = ['project', 'import', '-i', str(datasetPath), '-o', str(projPath), '-f', args['format'].lower(), '--overwrite']
            main(projImportArgs)
        return self

    def mergeDataset(self, import_args:Arg, filter_arg:Arg):
        config = setConfig(import_args['format'])
        source_datasets = dict([(path, Environment().make_importer(import_args['format'])(str(path)).make_dataset()) for path in self.datasetPathList])
        itemIdsAndPath = reduce(lambda x,y: x+y, [[(item.id, path) for item in dataset] for path, dataset in source_datasets.items()])
        # for itemId, path in itemIdsAndPath:
        for path, dataset in source_datasets.items():
            itemIdsInPath = set([itemId for itemId, _path in itemIdsAndPath if _path==path])
            itemIdsOutPath = set([itemId for itemId, _path in itemIdsAndPath if _path!=path])
            if itemIdsInPath & itemIdsOutPath:
                for subsetName, subset in dataset.subsets().items():
                    imgDir:Path = path/config.getImgDir(subsetName)
                    _subset = deepcopy(subset.items)
                    for item in _subset.values():
                        imgFile = Path(item.image.path)
                        relPath = imgFile.relative_to(imgDir)
                        newPath = imgDir/path.name/relPath
                        oldItemId = item.id
                        newItemId = item.id = str(path.name/relPath.parent/relPath.stem).replace('\\', '/')
                        item.image._path = str(newPath)
                        del subset.items[oldItemId]
                        subset.items[newItemId] = item
                        newPath.parent.mkdir(parents=True, exist_ok=True)

                        if item.image.has_data:
                            move(str(imgFile), str(imgDir/path.name/relPath))

        mergePath = (self.projectsPath/self.mergeFolderName)
        if mergePath.is_dir():
            rmtree(mergePath, onerror=remove_readonly)
        mergePath.mkdir(exist_ok=True, parents=True)
        dst_dir = str(mergePath)

        merger = IntersectMerge(conf=IntersectMerge.Conf())
        merged_dataset = merger(list(source_datasets.values()))

        merged_project = Project()
        output_dataset = merged_project.make_dataset()
        output_dataset.define_categories(merged_dataset.categories())
        merged_dataset = output_dataset.update(merged_dataset)
        if filter_arg['no_anno_filter'].lower()=='y':
            filtered_dataset = Project().make_dataset()
            filtered_dataset.define_categories(merged_dataset.categories())
            merged_dataset = filtered_dataset.update(merged_dataset.select(lambda item: len(item.annotations) != 0))
        annoId = 1
        imageIdName = config.imageIdName
        for idx, item in tqdm(enumerate(merged_dataset), desc='datasets'):
            if imageIdName is not None:
                item.attributes[imageIdName] = idx+1
            for anno in item.annotations:
                anno.id = annoId
                annoId += 1
        merged_dataset.save(save_dir=dst_dir, save_images=True)


        # for subsetName, subset in tqdm(merged_dataset.subsets().items(), desc='datasets'):
        #     for idx, itemId in tqdm(enumerate(itemIds), desc='items'):
        #         if imageIdName is not None:
        #             merged_dataset.get(itemId,subset=subsetName).attributes[imageIdName] = idx+1
        #         for anno in merged_dataset.get(itemId, subset=subsetName).annotations:
        #             anno.id = annoId
        #             annoId += 1
        #     merged_dataset.save(save_dir=dst_dir, save_images=True)
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
            export_args = ['project','export','-o',str(exportPath),'-p',str(proj),'-f',args['format'].lower(), '--', '--save-images']
            main(export_args)
        return self


    @staticmethod
    def getSubDirList(Path:Path):
        return [dir for dir in Path.iterdir() if dir.is_dir()]

    def mergeFunction(self):
        importArgs = ImportArg()
        exportArgs = ExportArg()
        no_anno_filter_arg = NoAnnoFilterArg()
        self.mergeDataset(importArgs, no_anno_filter_arg)
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