from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import json


class AsmToolbar(QToolBar):

    @staticmethod
    def fromJson(name, jsonRef, parent):
        with open(jsonRef, 'r') as f:
            d = json.loads(f.read())
            return AsmToolbar(name, d, parent)

    def __init__(self, name, actions=None, parent=None):
        super(AsmToolbar, self).__init__(name, parent)
        self.setIconSize(QtCore.QSize(18, 18))
        self.setMovable(False)
        self.__items = {} if actions is None else actions

    def appendAction(self, name, slot , icon=None):
        self.__items[name] = {'slot': slot, 'type': 'action'}
        if not (icon is None):
            self.__items[name]['icon'] = icon

    def appendWidget(self, name, widget, ):
        self.__items[name] = {'type': 'widget', 'widget': widget}

    def build(self):
        for name , item in self.__items.items():
            if item['type'] == 'action':
                action = QAction(name , self)
                if 'slot' in item.keys():
                    action.triggered.connect(item['slot'])

                if 'icon' in item.keys():
                    action.setIcon(QIcon(item['icon']))
                self.addAction(action)
            elif item['type'] == 'widget':
                self.addWidget(item['widget'])


