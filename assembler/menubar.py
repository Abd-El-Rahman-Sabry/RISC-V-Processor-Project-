
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import json


class AsmMenuBar(QMenuBar):

    def __init__(self, json, parent=None):
        super(AsmMenuBar, self).__init__(parent)
        self.__jsonRef = json
        self.__menuDict = None
        self.__initialization()

    def __initialization(self):
        with open(self.__jsonRef, 'r') as f:
            self.__menuDict = json.loads(f.read())

    def build(self):
        self.__constructFromJson(self.__menuDict)

    def __constructFromJson(self, menus, leaf=None):
        for name, item in menus.items():
            if item['type'] == 'menu':
                menu = QMenu(name, self)
                self.__constructFromJson(item['items'] if 'items' in item.keys() else {}, menu)

                if not (item['icon'] is None):
                    menu.setIcon(QIcon(item['icon']))
                if not (leaf is None):
                    leaf.addMenu(menu)
                else:
                    self.addMenu(menu)

            elif item['type'] == 'action':
                if item['icon'] is None:
                    action = QAction(name, self)
                else:
                    action = QAction(QIcon(item['icon']), name, self)

                if 'checkable' in item.keys():
                    action.setCheckable(item['checkable'])

                if 'slot' in item.keys():
                    action.triggered.connect(item['slot'])
                if leaf is None:
                    self.addAction(action)
                else:
                    leaf.addAction(action)

            elif item['type'] == 'sep':
                if leaf is None:
                    self.addSeparator()
                else:
                    leaf.addSeparator()

    def bindEvent(self, path: str, slot):
        pathItems = path.split('/')
        pathItems = [i.strip().replace(' ' , '%') for i in pathItems]
        pathItems = " items ".join(pathItems).split()
        pathItems = [i.strip().replace('%', ' ') for i in pathItems]

        action = pathItems.pop()
        val = self.__menuDict
        for item in pathItems:
            val = val[item]
        print(val)
        if val[action]['type'] != "action":
            raise Exception("Can't bind an Event to menu it must be an action")

        val[action]['slot'] = slot
