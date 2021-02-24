from dltools.dataset.args import ImportArg, ExportArg, DrawItemArg, Arg
from dltools.dataset.dataset import customDataset
from dltools.dataset.config import setConfig
from dltools.dataset.utils import remove_readonly

from datumaro.cli.__main__ import main
from datumaro.components.project import Project, Environment # project-related things
from datumaro.components.operations import IntersectMerge
from datumaro.components.dataset import Dataset
from datumaro.components.extractor import Bbox, DatasetItem, Polygon

from copy import deepcopy
from pathlib import Path, PosixPath
from tkinter import Tk, filedialog
from tqdm import tqdm
from sys import exit
from shutil import rmtree, move
from functools import reduce
import numpy as np

from dltools.api import JobAPI, TaskAPI
from dltools.analytics import ProjectAnaly, makeReport

class Commands:
    def __init__(self) -> None:
        # self.selWorkDir()
        self.task = TaskAPI()
        self.job = JobAPI()

    def selWorkDir(self):
        root = Tk()
        selectedDatasetPathStr = filedialog.askdirectory()
        if not bool(selectedDatasetPathStr):
            exit()
        root.destroy()
        return selectedDatasetPathStr

    def set_working_dir(self, selectedDatasetPathStr):
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

    def mergeDataset(self, args:Arg):
        config = setConfig(args['format'])
        source_datasets = dict([(path, Environment().make_importer(args['format'])(str(path)).make_dataset()) for path in self.datasetPathList])
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
                        if item.image.has_data:
                            imgFile = Path(item.image.path)
                            relPath = imgFile.relative_to(imgDir)
                            newPath = imgDir/path.name/relPath
                            oldItemId = item.id
                            newItemId = item.id = str(path.name/relPath.parent/relPath.stem).replace('\\', '/')
                            item.image._path = str(newPath)
                            del subset.items[oldItemId]
                            subset.items[newItemId] = item

                            newPath.parent.mkdir(parents=True, exist_ok=True)
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
        itemIds = [item.id for item in merged_dataset]
        annoId = 1
        imageIdName = config.imageIdName
        for subsetName in tqdm(merged_dataset.subsets(), desc='datasets'):
            for idx, itemId in tqdm(enumerate(itemIds), desc='items'):
                if imageIdName is not None:
                    merged_dataset.get(itemId,subset=subsetName).attributes[imageIdName] = idx+1
                for anno in merged_dataset.get(itemId, subset=subsetName).annotations:
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
            export_args = ['project','export','-o',str(exportPath),'-p',str(proj),'-f',args['format'].lower(), '--', '--save-images']
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
        
    def job_assign(self, job_id:int, assignee_id:int):
        self.job.patch_id(job_id, assignee_id=assignee_id)

    @staticmethod
    def export_report(project_id):
        prjanaly = ProjectAnaly(project_id)
        assignee_table, label_table = prjanaly()
        makeReport(dataFrame1 = assignee_table, dataFrame2 = label_table, saveExcelName = 'Report')

    def download_labeled_image(self, task_id:int, frame_id:int, outdir:str):
        filename, img = self.task.download_frame(task_id, frame_id, outdir, save=False)
        labels = dict([(label.id, label) for label in self.task.get_id(task_id).labels])
        jobs = self.task.get_jobs(task_id)
        job_id_with_frame = [job.id for job in jobs if (int(job.start_frame) <= frame_id) & (frame_id <= int(job.stop_frame))]
        job_annos_list = [self.job.get_annotations(job_id) for job_id in job_id_with_frame]
        annos = [[anno for anno in job_annos.shapes if anno.frame==frame_id][0] for job_annos in job_annos_list]
        categories=[label.name for label in labels.values()]
        items = []
        for anno in annos:
            attriname = dict([ (attr.id, attr.name) for attr in labels[anno.label_id].attributes ])
            attris = dict([ (attriname[attr.spec_id], attr.value) for attr in anno.attributes ])
            if anno.type=='rectangle':
                x,y,x2,y2 = anno.points
                items.append(Bbox(x,y,x2-x, y2-y,attributes=attris, label=categories.index(labels[anno.label_id].name)))
            elif anno.type=='polygon':
                items.append(Polygon(anno.points,attributes=attris, label=categories.index(labels[anno.label_id].name)))

        # image = {'data': np.asarray(img),
        #          'path': str(Path(outdir)/filename)}
        dataset = Dataset.from_iterable([
                        DatasetItem(id=filename, annotations=items, image=np.array(img))],
                        categories=categories)
        customset = customDataset(dataset)
        for image_data in customset._imageDatas:
            image_data.drawItem('s','s').saveImg(Path(outdir)/filename)