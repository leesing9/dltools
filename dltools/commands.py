from pathlib import Path
from datumaro.cli.__main__ import main
from tkinter import Tk, filedialog
from tqdm import tqdm
from dltools.args import ImportArg, ExportArg, DrawItemArg
from datumaro.components.project import Project # project-related things
from dltools.args import Arg
from dltools.dataset import customDataset

class Commands:
    def __init__(self) -> None:
        root = Tk()
        self.datasetsPath = Path(filedialog.askdirectory())
        while bool(str(self.datasetsPath)):
            self.datasetsPath = Path(filedialog.askdirectory())
        root.destroy()
        self.projectsPath = (self.datasetsPath/'..'/'projects').resolve().absolute()
        self.mergeFolderName = 'merged'

    def checkDefineVariable(self, var:str):
        try:
            eval(var)
            return True
        except AttributeError:
            return False

    def importDataset(self, args:Arg):
        if args['format'].lower() not in args.supportFormat:
            args['format'] = input('지원하지 않는 format입니다. 다시 입력해주세요.')
        self.projectsPath.mkdir(exist_ok=True, parents=True)
        self.projectsPathListFromDataset = [self.projectsPath/path.name for path in self.getSubDirList(self.datasetsPath)]
        datasetPathList = [path for path in self.getSubDirList(self.datasetsPath) if path.is_dir()]
        for datasetPath in datasetPathList:
            projPath = self.projectsPath/datasetPath.name
            projImportArgs = ['project', 'import', '-i', str(datasetPath), '-o', str(projPath), '-f', args['format'].lower(), '--overwrite']
            main(projImportArgs)
        return self

    def mergeDataset(self):
        if not self.checkDefineVariable('self.projectsPathListFromDataset'):
            importArgs = ImportArg()
            self.importDataset(importArgs)
        projsPathList = [str(dir) for dir in self.projectsPathListFromDataset]
        mergePath = (self.projectsPath/self.mergeFolderName)
        mergePath.mkdir(exist_ok=True)
        merge_args = ['merge', '-o', str(mergePath), '--overwrite', *projsPathList]
        main(merge_args)
        return self

    def exportDataset(self, args:Arg, merge=False):
        if args['format'].lower() not in args.supportFormat:
            args['format'] = input('지원하지 않는 format입니다. 다시 입력해주세요.')

        if merge:
            projectsPathList = [self.projectsPath/self.mergeFolderName]
        else:
            if not self.checkDefineVariable('self.projectsPathListFromDataset'):
                importArgs = ImportArg()
                self.importDataset(importArgs)
            projectsPathList = self.projectsPathListFromDataset

        for proj in projectsPathList:
            exportPath = (self.projectsPath/'export'/args['format'].lower()/proj.name).absolute()
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
        self.importDataset(importArgs)
        self.mergeDataset()
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
        if not self.checkDefineVariable('self.projectsPathListFromDataset'):
            importArgs = ImportArg()
            self.importDataset(importArgs)
        projectFolders = [path for path in self.projectsPathListFromDataset]
        projects = [Project.load(projectFolder) for projectFolder in projectFolders]
        self.datasets = [customDataset(project.make_dataset()) for project in projects]
        return self
    
    def drawItemOfEveryDataset(self, args:Arg):
        if not self.checkDefineVariable('self.datasets'):
            self.loadDatasetFromProjFolder()
        else:
            pass
        for dataset in tqdm(self.datasets):
            dataset.drawAndExport(args['lineStyle'], args['cornerStyle'])
        return self
