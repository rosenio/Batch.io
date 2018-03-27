#===============================================================================
# #Autor:  Rosenio Pinto
# #e-mail: kenoi3d@gmail.com
#===============================================================================
#===============================================================================
# This is the main manager thats holds and manage all other io
#===============================================================================
from SystemConfig import *
from Utils import *
from Pre_Batch_Process import *
from Batch_Process import *
from Batch_io_UI import *
import Import_Cache as IC
import Singleton as Sing

reload(IC)


class Batch_io_main(Sing.Singleton, QWidget):
    _instance = None
    def __init__(self, parent=None):
        super(Batch_io_main, self).__init__(parent)   

        #=======================================================================
        # #Parent widget under Maya main window        
        #=======================================================================
        self.setParent(get_main_window())        
        self.setWindowFlags(Qt.Window)
        self.setWindowIcon(QIcon(QPixmap(BATCH_io_IMAGES+'batch_io_icon.png')))
        #=======================================================================
        # #Set the object name
        #=======================================================================
        self.setObjectName('Batch.io_uniqueId')        
        self.setWindowTitle('Batch.io %s'%VERSION)        
        self.setGeometry(500, 100, 1300, 900)
        
        self.collapsed = False
        
        self.initUI()
        

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.setLayout  = self.mainLayout
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        
        self.header_layout = QHBoxLayout()
        
        detachAction = QAction(QIcon('unparent.png'), '&Unpurent', self)
        detachAction.setShortcut('Ctrl+P')
        detachAction.setStatusTip('Unparent from Maya')
        detachAction.triggered.connect(self.UnParent)

        collapseAction = QAction(QIcon('collapse.png'), '&Collapse', self)
        collapseAction.setShortcut('Ctrl+E')
        collapseAction.setStatusTip('Collapse the UI')

        refreshAction = QAction(QIcon('refresh.png'), '&Reresh', self)
        refreshAction.setShortcut('Ctrl+R')
        refreshAction.setStatusTip('Refresh the UI')

        self.menubar = QMenuBar(self)

        settingsMenu = self.menubar.addMenu('&Settings')
        settingsMenu.addAction(detachAction)
        settingsMenu.addAction(collapseAction)
        settingsMenu.addAction(refreshAction)


        #=======================================================================
        # #Set folder combo box
        #=======================================================================
        self.project_lbl    = QLabel(Get_Project())
        self.project_lbl.setFont(AW.fontSize_H2)
        
        self.folderComboBox = QComboBox()
        self.folderComboBox.setFont(AW.fontSize_H1)
        self.folderComboBox.setFixedWidth(200)
        
        self.folderComboBox.addItems(SOURCEFOLDERLIST)
        self.folderComboBox.currentIndexChanged.connect(self.Folder_ComboBox_Change)
      
        #=======================================================================
        # #Set tab manager
        #=======================================================================
        self.Batch_io_Tabs = QTabWidget(self)
        self.Batch_io_Tabs.setTabPosition(QTabWidget.North)
        #=======================================================================
        # #Add everything to the layout
        #=======================================================================
        self.header_layout.addWidget(self.project_lbl, 1, Qt.AlignRight)
        self.header_layout.addWidget(self.folderComboBox, 0, Qt.AlignRight)
        
        self.mainLayout.addLayout(self.header_layout)
        self.mainLayout.addWidget(self.Batch_io_Tabs)

        #=======================================================================
        # #Open the window
        #=======================================================================
        self.show()
      
        #=======================================================================
        # #Call external io to put in the ui
        #=======================================================================
        self.B_UI      = Batch_io_UI.globalInstance(Batch_io_UI)
        self.impCache  = IC.ImportCache()
        self.P_BP      = Pre_Batch_Process()
        self.BP        = Batch_Process()
        
        
        self.Pre_Batch_Scene_Info = Pre_Batch_Scene_Info.globalInstance(Pre_Batch_Scene_Info)
        
        #=======================================================================
        # #ADD Tab items
        #=======================================================================
        self.Batch_io_Tabs.addTab(self.BP,       'Batch.io')
        self.Batch_io_Tabs.addTab(self.impCache, 'Import')
        self.Batch_io_Tabs.currentChanged.connect(self.OnTabChange)

        #=======================================================================
        # #Make some connections
        #=======================================================================
        self.B_UI.Batch_Process_Creation = self.BP.Batch_Process_Creation
        self.B_UI.project_lbl            = self.project_lbl
        
        collapseAction.triggered.connect(self.collapse)
        refreshAction.triggered.connect(self.B_UI.RefreshUI)
        #=======================================================================
        # #Call the first function pre batch
        #=======================================================================
        self.P_BP.Refresh_Pre_Batch()
        
        #QThreadPool.globalInstance().setMaxThreadCount(4)
        
    
    #===========================================================================
    # #Call on folder dropdown change        
    #===========================================================================
    def Folder_ComboBox_Change(self, *args):
        source_folder          =  SOURCEFOLDERLIST[args[0]]
        self.P_BP.SOURCEFOLDER = Get_SourceFolder().replace('SOURCEFOLDER', source_folder)
        self.B_UI.batch_mode   = source_folder
        self.P_BP.Pre_Batch_Thread_Creation()
    
    
    #===========================================================================
    # #Call on main tab change    
    #===========================================================================
    def OnTabChange(self, i):
        if i == 1:
            self.Batch_io_Tabs.widget(i).RefreshUICmd()
            
            
    #===========================================================================
    # #Call on close window
    #===========================================================================
    def closeEvent(self, event):
        #=======================================================================
        # #Close all running process
        #=======================================================================
        self.B_UI.Stop()


        print "Closing things"
    
    
    #===========================================================================
    # #Collapse window
    #===========================================================================
    def collapse(self):
        self.B_UI.collapse()
        if self.collapsed:
            self.setGeometry(500, 100, 1300, 900)
            self.collapsed = False
        else:
            self.setGeometry(500, 100, 100, 600)
            self.collapsed = True 
        
    
    #===========================================================================
    # #Unparent window from maya
    #===========================================================================
    def UnParent(self, *args, **kwargs):
        if not self.parent():
            self.setParent(get_main_window())
            self.setWindowFlags(Qt.Window)
        else:
            self.setParent(None)
        self.show()
        


        
            
            
        