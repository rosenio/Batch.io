#===============================================================================
# #Autor: Rosenio Pinto
# #e-mail: kenio3d@gmail.com
#===============================================================================
#===============================================================================
# #Simple console dialog
#===============================================================================
from SystemConfig import *

class Console(QDialog):
    def __init__(self, parent=None):
        super(Console, self).__init__(parent)
        #=======================================================================
        # #Parent widget under Maya main window        
        #=======================================================================
        self.setWindowFlags(Qt.Tool)

        #=======================================================================
        # #Set the object name
        #=======================================================================
        self.setObjectName('Console_uniqueId')        
        self.setWindowTitle('Console')
        
        self.setGeometry(500, 200, 500, 600) 
        
        self.setFont(AW.fontSize_H2)
        
        self.initUI()


    def initUI(self):
        self.mainLayout      = QVBoxLayout(self)
        self.setLayout       = self.mainLayout
        
        self.textBrowser     = QTextBrowser()
        self.textBrowser.setFont(AW.fontSize_H3)

        self.mainLayout.addWidget(self.textBrowser)
        self.SetFont()


    def mousePressEvent(self, event):
        menu = self.textBrowser.createStandardContextMenu()
        clearAct =  QAction(QIcon(":/images/open.png"), "&Clear...", self)
        clearAct.triggered.connect(self.Clear)
        
        menu.addAction(clearAct)
        menu.setContextMenuPolicy(Qt.CustomContextMenu)
        menu.exec_(QCursor.pos())


    def AddText(self, msg):
        self.textBrowser.append(msg)


    def SetFont(self, size=10, bold=False):
        font = self.textBrowser.font()
        font.setPointSize(size)
        font.setBold(bold)
        self.textBrowser.setFont(font)
    
    
    def Clear(self):
        self.textBrowser.clear()
        
        
        
