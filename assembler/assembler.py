import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from PyQt5.Qsci import * 

from PyQt5.QtGui import *
from PyQt5.Qsci import QsciScintilla, QsciLexerPython , QsciLexerNASM
from PyQt5.QtWidgets import QWidget
from filesystem import FileSection
from menubar import AsmMenuBar
from toolbar import AsmToolbar
from lexer import CustomAssemblyLexer



class RISCVAssemblerEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(RISCVAssemblerEditor, self).__init__(parent)

        self.setWindowTitle("RISC V Assembler")
        
        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))

        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)

        self.markerDefine(QsciScintilla.RightArrow,
            self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ee1111"),
            self.ARROW_MARKER_NUM)

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

        # Set Python lexer
        # Set style for Python comments (style number 1) to a fixed-width
        # courier.
        #
        
        lexer = CustomAssemblyLexer(self)
        
        lexer.setDefaultFont(font)
        self.setLexer(lexer)

        text = bytearray(str.encode("Arial"))
# 32, "Courier New"         
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, text)

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # not too small
        self.setMinimumSize(600, 450)

class MainMenu (QMainWindow): 
    
    def generateSlot(self):
        txt = self.getCurrentEditorWindow().text() 
        asm = Assembler(txt)
        asm.extract_instructions()  
        
    
    def initMenu(self):
        menu = AsmMenuBar("assembler\menu.json",self)
        
        '''
            
            Building the Menu 
            
        '''
        menu.bindEvent("File/New Text File", lambda: print("Hello"))
        menu.bindEvent("File/Exit", lambda: exit())
        
        
        menu.build()         
        self.setMenuBar(menu)
        return menu 
    
    def initTools(self): 
        toolbar = AsmToolbar("Static Toolbar")
        
        '''
            Building the Tool bar 
        
        '''
        toolbar.appendAction("open" , lambda : print("Hello") , "assembler/icons/open-file.png")
        toolbar.appendAction("save" , lambda : print("Hello") , "assembler/icons/save-file.png")
        toolbar.appendAction("new" , lambda :self.addTab("untitled.asm") , "assembler/icons/new-document.png")
        toolbar.appendAction("generate" ,self.generateSlot, "assembler/icons/printer.png")
        
        toolbar.build() 
        self.addToolBar(toolbar) 
        return toolbar 
    
    def initTabView(self):
        tab_view = QTabWidget(self)
        tab_view.setTabsClosable(True) 
        tab_view.tabCloseRequested.connect(lambda i : tab_view.removeTab(i))
        return tab_view; 
    
    def getCurrentEditorWindow(self): 
        current_widget = self.tabview.currentWidget()
        return current_widget
    
    def addTab(self , title):
        editor = RISCVAssemblerEditor() 
        self.tabview.addTab(editor , title)
        
        
    def __init__(self,) -> None:
        super().__init__()
        self.setCentralWidget(QWidget())
        self.setWindowTitle("Sabry and Halim Assembler")
        
        self.layout = QVBoxLayout() 
        
        # Main Parts in the editors 
        self.editor = RISCVAssemblerEditor() 
        self.menu = self.initMenu() 
        self.toolbar = self.initTools() 
        self.tabview = self.initTabView() 
        
        self.layout.addWidget(self.tabview)
        self.addTab("untitled.asm")
        self.centralWidget().setLayout(self.layout)
        
        
        
        # Build The status bar 
        self.status = QStatusBar(self)
        self.setStatusBar(self.status)
        self.status.showMessage("Welcome to the custom assembler" , 3000)
        
        
        # File System 
        
        self.file_system = FileSection(self, os.getcwd())
        self.file_dock = QDockWidget(self)
        self.file_dock.setWindowTitle("explorer")
        self.file_dock.setWidget(self.file_system)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,self.file_dock , ) 
        print(os.getcwd())
        
        

class Assembler: 
    
    
    def __init__(self, src) -> None:
        self.__src = src 
        
    def extract_instructions(self): 
        import re 
        
        pattern  = re.compile(r"^\s*(\w+)\s*([\w()]+)?(?:\s*,\s*([\w()]+))?(?:\s*,\s*([\w()]+))?\s*$" ,flags=re.RegexFlag.MULTILINE)
        matches = re.findall(pattern,self.__src )
        
        print(matches)
        
    
        
        



if __name__ == "__main__": 
    app = QApplication([])
    editor = MainMenu() 
    app.setStyle("Fusion")
    
    editor.show() 
    app.exec_() 
    
    
