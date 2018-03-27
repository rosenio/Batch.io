#===============================================================================
# #Autor: Rosenio Pinto
# #e-mail: kenio3d@gmail.com
#===============================================================================
from SystemConfig import *
from Widgets import *
import Widgets as BW
import Batch_Widget_Settings_UI as BWS



class Batch_Widget_Handler(QWidget):
    def __init__(self, parent=None):
        super(Batch_Widget_Handler, self).__init__(parent)

        #=======================================================================
        # #Set the object name
        #=======================================================================
        self.setObjectName('Batch_Widget_Handler_uniqueId')        
        self.setWindowTitle('Console')
        self.setGeometry(0, 0, 300, 300) 
        
        
        #=======================================================================
        # #Set some class variables
        #=======================================================================
        self.SceneInfo       = {}
        self.widget_cmd_dict = {}
        self.batch_mode      = 'ANIM'

        
        self.initUI()
        

    #===========================================================================
    # #UI functions
    #===========================================================================
    def initUI(self):
        self.mainLayout      = QVBoxLayout(self)
        self.setLayout       = self.mainLayout
        
        self.centralLayout   = QHBoxLayout()
        self.addRemoveLayout = QVBoxLayout()
        
        self.Batch_Widget_Stack_AWL   = AW.AssetListWidget(tab_title='Batch Widget Stack', isStatic=True)
        self.Batch_Widget_Library_ASW = AW.AssetListWidget()

        self.Batch_Widget_Stack_AWL.SetDroppable(True)

        self.Batch_Widget_Library_ASW.SetTitle('Batch Widget Library')
        self.Batch_Widget_Library_ASW.SetDroppable(True)

        self.centralLayout.addWidget(self.Batch_Widget_Stack_AWL)
        self.centralLayout.addLayout(self.addRemoveLayout)
        self.centralLayout.addWidget(self.Batch_Widget_Library_ASW)
        
        self.Batch_Widget_Stack_AWL.dropEvent        = self.Batch_Widget_Stack_DropEvent
        self.Batch_Widget_Library_ASW.dropEvent      = self.Library_DropEvent
        self.Batch_Widget_Library_ASW.dragEnterEvent = self.Library_DragEnterEvent
        
        self.mainLayout.addLayout(self.centralLayout)
        
        self.Add_Library_Cmd(self.Get_cmd_Library())


    def Clean_Library_UI(self):
        self.Batch_Widget_Library_ASW.CleanAssetWidgets()
        self.Batch_Widget_Library_ASW.clear()
        
        
    def Clean_Batch_Widget_Stack(self):
        self.Batch_Widget_Stack_AWL.CleanAssetWidgets()
    
    
    def Batch_Widget_Stack_DropEvent(self, event):
        sourceWidget = event.source()

        assetName = sourceWidget.objectName()
        
        if not sourceWidget in self.Batch_Widget_Stack_AWL.assetWidgets.values():
            self.Add_Batch_Widget_To_Stack(assetName)


    def Library_DropEvent(self, event):
        sourceWidget = event.source()
        
        if not sourceWidget in self.Batch_Widget_Library_ASW.assetWidgets.values():
            self.Batch_Widget_Stack_AWL.Remove_Widget(sourceWidget)
            
            sourceWidget.animEnd()


    def Library_DragEnterEvent(self, event):
        event.setDropAction(Qt.TargetMoveAction)
        event.accept()


    def RefreshUI(self):
        self.Add_Library_Cmd(self.Get_cmd_Library())
        self.Clean_Batch_Widget_Stack()

    #===========================================================================
    # #System function
    #===========================================================================
    # #=========================================================================
    #===========================================================================
    # # Load all batch widgets registred
    #===========================================================================
    def Get_cmd_Library(self):
        widget_list = BW.__all__
        self.widget_cmd_dict = {}
        for widget in widget_list:
            if widget.endswith('_widget'):
                
                try:
                    widget_run      = getattr(BW, widget)
                    widget_name     = widget_run.WIDGET_NAME
                    widget_label    = widget_run.WIDGET_NAME
                    widget_tip      = widget_run.WIDGET_DESC
                    widget_type     = widget_run.WIDGET_TYPE
                    widget_settings = widget_run.WIDGET_SETTINGS
                    widget_main     = partial(widget_run.main, self.SceneInfo)

                    #===========================================================
                    # #Get only widget of batch mode type
                    #===========================================================
                    self.widget_cmd_dict[widget_name] = {'widget_name':widget_name, 
                                                         'widget_main':widget_main, 
                                                         'widget_tip':widget_tip, 
                                                         'widget_label':widget_label,
                                                         'widget_type':widget_type, 
                                                         'widget_settings':widget_settings}
                except Exception, e:
                    print e
                    print 'Problem to load batch widgets.'

        return self.widget_cmd_dict


    #===========================================================================
    # #Feed the command library
    #===========================================================================
    def Add_Library_Cmd(self, widget_cmd_dict={}):
        self.Clean_Library_UI()
        checked_widget_dict = {}
        
        for widget_name in widget_cmd_dict.keys():
            widget_type = widget_cmd_dict[widget_name]['widget_type']
            
            batch_widget = AW.AssetWidget()
            
            batch_widget.SetAssetIcon(BATCH_io_IMAGES+'batch_io.png')
            batch_widget.SetAssetLabel(self.widget_cmd_dict[widget_name]['widget_label'])
            batch_widget.setToolTip(widget_cmd_dict[widget_name]['widget_tip'])
            batch_widget.setObjectName(widget_name)
            
            batch_widget.SetDraggable(True)
            batch_widget.SetDroppable(True)

            batch_widget.command = widget_cmd_dict[widget_name]['widget_main']
            
            #===================================================================
            # #Feed the pre dictionary
            #===================================================================
            if not widget_type in checked_widget_dict.keys():
                checked_widget_dict[widget_type] = []
            checked_widget_dict[widget_type].append(batch_widget)
        
        checked_type = []
        for widget_type, batch_widget_list in checked_widget_dict.iteritems():
            for batch_widget in batch_widget_list:
                #===================================================================
                # #Check if there is a batch widget type tab, except create one
                #===================================================================
                if not widget_type in checked_type:
                    self.Batch_Widget_Library_ASW.set_tab(tab_title=widget_type)
                    checked_type.append(widget_type)
                
                #===================================================================
                # #Add the batch widget to the proper tab
                #===================================================================
                self.Batch_Widget_Library_ASW.AddAssetWidget(batch_widget, False, widget_type)
                batch_widget.animRefresh()


    #===========================================================================
    # #Get a list of batch widgets on stack to be executed in scenes
    #===========================================================================
    def Get_cmd_ON_Stack(self):
        batch_widget_commands = {'command_ordered_list':[]}
        for batch_widget in self.Batch_Widget_Stack_AWL.Get_sorted_by_index():
            batch_widget_name = batch_widget.GetName()+'_widget'
            
            batch_widget_commands['command_ordered_list'].append(batch_widget_name)
            batch_widget_commands[batch_widget_name] = batch_widget.settings     
            
        return batch_widget_commands


    #===========================================================================
    # #Add command to stack
    #===========================================================================
    def Add_Batch_Widget_To_Stack(self, widget_name=''):
        batch_widget = AW.AssetWidget()
        batch_widget.SetAssetIcon(BATCH_io_IMAGES+'batch_io.png')
        batch_widget.SetAssetLabel(self.widget_cmd_dict[widget_name]['widget_label'])
        batch_widget.setObjectName(self.widget_cmd_dict[widget_name]['widget_name'])
        
        batch_widget.SetAssetBtn('', partial(BWS.Batch_Widget_Settings_UI, batch_widget), True, True, BATCH_io_IMAGES+'settings.png')
        
        batch_widget.setToolTip(self.widget_cmd_dict[widget_name]['widget_tip'])
        
        batch_widget.SetDraggable(True)
        batch_widget.SetDroppable(True)
        
        widget_settings = self.widget_cmd_dict[widget_name]['widget_settings']
        batch_widget.settings = widget_settings

        self.Batch_Widget_Stack_AWL.AddAssetWidget(batch_widget, True)
        
        
         

    #===========================================================================
    # #Set the local scene info from batch class
    #===========================================================================
    def SetPreBatchInfo(self, SceneInfo={}):
        self.SceneInfo = SceneInfo
        
    
       

        