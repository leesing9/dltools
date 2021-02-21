from easydict import EasyDict
import sys
from typing import Callable
from dltools.utils import consolClear

class Menu:
    prevMunu = None

    def __init__(self, menuName:str) -> None:
        self.menuName = menuName
        self.command = EasyDict()
        if menuName != 'Main':
            self.setCommand('이전메뉴', self.goToPrev)
        self.setCommand('종료', sys.exit)

    def __str__(self) -> str:
        header = 'No\tOption\t\t\tHelp\n-----------------------------------------------------------------'
        opts = [self.menuName, header]
        for no,val in self.command.items():
            line = f'{no}\t{val.opt}\t\t{val.help}'
            opts.append(line)
        return '\n'.join(opts)
    
    def __call__(self):
        self.selectAndRun()

    def selectAndRun(self):
        self.prevMunu = Menu.prevMunu
        Menu.prevMunu = self
        consolClear()
        print(self)
        while True:
            selNum = input('선택 No: ').strip()
            if selNum in self.command.keys():
                break
            else:
                print('입력이 잘못되었습니다. ')
        # try:
        #     self.command[selNum].function()
        # except Exception as e:
        #     print(e)
        #     input('\npress any key...........')
        self.command[selNum].function()
        self.selectAndRun()

    def setCommand(self, opt:str, function:Callable, help='') :
        no = str(len(self.command))
        self.command[no] = {"opt": opt,
                            "function": function, 
                            "help": help}
        return self

    def goToPrev(self):
        self.prevMunu.selectAndRun()