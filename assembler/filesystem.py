from PyQt5.QtCore import QDir, QEvent, QFileSystemWatcher , Qt
from PyQt5.QtWidgets import *
import os


class FileSection(QWidget):

    def __init__(self, parent=None, path=''):
        super(FileSection, self).__init__(parent=parent)
        self.__path = path

        self.setLayout(QHBoxLayout())
        self.__treeView = QTreeView()

        self.__dirModel = QFileSystemModel()
        self.__dirModel.setRootPath(path)
        self.__dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        self.__treeView.setModel(self.__dirModel)
        self.__treeView.setRootIndex(self.__dirModel.index(path))

        self.__treeView.setIndentation(10)
        self.__treeView.setAnimated(True)
        self.__treeView.setAlternatingRowColors(True)
        self.__treeView.setHeaderHidden(True)
        self.__treeView.setColumnHidden(1, True)
        self.__treeView.setColumnHidden(2, True)
        self.__treeView.setColumnHidden(3, True)

        self.layout().addWidget(self.__treeView)
        self.__treeView.doubleClicked.connect(self.connect)
        self.__treeView.installEventFilter(self)

        self.__watchDog = QFileSystemWatcher(self)
        self.__watchDog.addPath(self.__path)
        self.__treeView.expandAll()
        self.__watchDog.directoryChanged.connect(self.update)
        self.__clickEvent = None 
        
    def setClickEvent(self, event):
        self.__clickEvent = event 

    def connect(self, index):
        file = self.__dirModel.fileInfo(index).filePath()
        if self.__clickEvent:
            self.__clickEvent() 

    def update(self):
        directory = self.__watchDog.directories()[0]
        model = QDir(directory)
        self.__treeView.setModel(model)
        self.__treeView.setRootIndex(model.index(directory))


    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.__treeView:

            menu = QMenu()
            menu.addAction('remove')
            menu.addAction('Make Reference')

            action = menu.exec_(event.globalPos())
            if action:
                pass
            return True
        return super().eventFilter(source, event)
