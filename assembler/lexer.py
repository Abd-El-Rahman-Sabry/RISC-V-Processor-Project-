import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.Qsci import QsciScintilla, QsciLexerCustom
from PyQt5.QtGui import QColor, QFont


class CustomAssemblyLexer(QsciLexerCustom):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Define color styles
        self.styles = {
            'default': 0,
            'keyword': 1,
            'register': 2,
            'comment': 3,
            'number': 4,
            'label': 5,
        }

        # Set up colors and fonts for different styles
        self.setColor(QColor("#000000"), self.styles['default'])  # Default text (black)
        self.setColor(QColor("#0000FF"), self.styles['keyword'])  # Keywords (blue)
        self.setColor(QColor("#FF00FF"), self.styles['register'])  # Registers (magenta)
        self.setColor(QColor("#008000"), self.styles['comment'])  # Comments (green)
        self.setColor(QColor("#FF0000"), self.styles['number'])  # Numbers (red)
        self.setColor(QColor("#8BBB8B"), self.styles['label'])  # Labels (purple)

        fontName = "Consolas"
        # Set default font for each style
        self.setFont(QFont(fontName, 12, weight=QFont.Weight.Normal) , self.styles['default']) 
        self.setFont(QFont(fontName, 12, weight=QFont.Weight.Bold) , self.styles['keyword']) 
        self.setFont(QFont(fontName, 12, weight=QFont.Weight.Medium) , self.styles['register']) 
        self.setFont(QFont(fontName, 12, weight=QFont.Weight.Normal) , self.styles['comment']) 
        self.setFont(QFont(fontName, 12, weight=QFont.Weight.DemiBold) , self.styles['number']) 
        self.setFont(QFont(fontName, 12, weight=QFont.Weight.Bold) , self.styles['label']) 
         
        
        
        # Define keywords, registers, and labels
        one_op = ["NOP" , "HLT" , "SETC" , "NOT" , "INC" , "OUT" , "IN"]
        two_op = ["MOV" , "ADD" , "SUB", "AND" , "IADD"]
        mem_control = ["PUSH" , "POP" , "LDM" , "LDD" , "STD" , ]
        branch_control = ["JZ" , "JN" , "JC" , "JMP" , "CALL" , "RET" , "RTI" , "INT"]
        
        self.keywords = one_op + two_op + mem_control + branch_control 
        
        self.registers = ["R0" ,"R1", "R2", "R3", "R4", "R5" , "R6" , "R7"]

    def language(self):
        return "CustomAssembly"
    
    def description(self, style):
        descriptions = {
            self.styles['default']: "Default",
            self.styles['keyword']: "Keyword",
            self.styles['register']: "Register",
            self.styles['comment']: "Comment",
            self.styles['number']: "Number",
            self.styles['label']: "Label"
        }
        return descriptions.get(style, "")

    def styleText(self, start, end):
        editor = self.editor()
        if editor is None:
            return

        # Get text from the editor
        text = editor.text()[start:end]
        length = len(text)

        # Reset styling
        self.startStyling(start)
        
        i = 0
        while i < length:
            char = text[i]

            # Numbers
            if char.isdigit():
                j = i
                while j < length and text[j].isdigit():
                    j += 1
                self.setStyling(j - i, self.styles['number'])
                i = j

            # Comments (e.g. "//")
            elif text[i:i+1] == "#":
                j = text.find('\n', i)
                if j == -1:
                    j = length
                self.setStyling(j - i, self.styles['comment'])
                i = j

            # Keywords, Registers, and Labels
            elif char.isalpha() or char == '_':
                j = i
                while j < length and (text[j].isalnum() or text[j] == '_'):
                    j += 1
                word = text[i:j].upper() 

                if word in self.keywords:
                    self.setStyling(j - i, self.styles['keyword'])
                elif word in self.registers:
                    self.setStyling(j - i, self.styles['register'])
                elif word.endswith(':'):
                    self.setStyling(j - i, self.styles['label'])
                else:
                    self.setStyling(j - i, self.styles['default'])

                i = j

            # Default style for other characters
            else:
                self.setStyling(1, self.styles['default'])
                i += 1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor = QsciScintilla()
        self.setCentralWidget(self.editor)

        # Apply the custom lexer to the editor
        lexer = CustomAssemblyLexer(self.editor)
        self.editor.setLexer(lexer)

        # Add some example assembly code
        self.editor.setText(
            "MOV R1, 10\n"
            "ADD R2, R1\n"
            "JMP start\n"
            "// This is a comment\n"
            "start:\n"
            "CMP R1, R2\n"
            "SUB R1, 1"
        )


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
