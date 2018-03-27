#===============================================================================
# #Autor: Rosenio Pinto
# #e-mail: kenio3d@gmail.com
#===============================================================================
from SystemConfig import *
from Utils import *

import Batch_Widget_Handler as BWH
import Console as Console
import Singleton as Sing



class Batch_io_UI(Sing.Singleton, QWidget):
    _instance = None
    def __init__(self, parent=None):
        super(Batch_io_UI, self).__init__(parent)    
        
 
        #=======================================================================
        # #Set the object name
        #=======================================================================
        self.setObjectName('Batch_io_UI_uniqueId')        
        self.setWindowTitle('Batch_io')
        #=======================================================================
        # #Main info of batch process
        #=======================================================================
        self.Pre_Batch_Scene_Info = Pre_Batch_Scene_Info.globalInstance(Pre_Batch_Scene_Info)
        
        self.Batch_Info        = Batch_Info.globalInstance(Batch_Info).Batch_Info
        
        self.Batch_Thread_Info = Batch_Thread_Info.globalInstance(Batch_Thread_Info).Batch_Thread_Info
        self.TH_PRIORITY_LIST  = ['IdlePriority', 
                                     'NormalPriority', 
                                     'HighPriority', 
                                     'TimeCriticalPriority']

        
        #=======================================================================
        # #For future use
        #=======================================================================
        self.refresh            = True
        self.is_collapsed       = False
        self.batch_mode         = 'ANIM'
        
        #=======================================================================
        # #LOG
        #=======================================================================
        self.LOG                = LOG.globalInstance(LOG).LOG
        
        #=======================================================================
        # #Preserve current refernce category tab
        #=======================================================================
        self.current_category_tab = 0

        #Init the UI
        self.initUI()


    def initUI(self):
        self.mainLayout      = QVBoxLayout(self)
        self.setLayout       = self.mainLayout

        self.centralLayout   = QHBoxLayout(self)
        self.optionBtnLayout = QHBoxLayout(self)
        self.mainLayout.addLayout(self.centralLayout)
        
        self.setGeometry(0, 0, 300, 300) 
        
        #=======================================================================
        # #Scenes stuff
        #=======================================================================
        self.scene_grp_widget   = QWidget()
        self.scene_list_widget  = AW.AssetListWidget(self, tab_title='Scenes', isStatic=True)
        self.scene_list_widget.SetColor()

        self.scene_grp_widget_layout = QVBoxLayout()
        self.scene_grp_widget_layout.addWidget(self.Add_Scene_Widget_HeaderUI())
        self.scene_grp_widget_layout.addWidget(self.scene_list_widget)
        self.scene_grp_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.scene_grp_widget.setLayout(self.scene_grp_widget_layout)
        
        #=======================================================================
        # #Reference stuff
        #=======================================================================
        self.AssetsToBeBatchedTabs = AW.AssetListWidget()
        
        
        self.reference_grp_widget  = QWidget()
        self.reference_grp_widget_layout = QVBoxLayout()
        self.reference_grp_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.reference_grp_widget.setLayout(self.reference_grp_widget_layout)
        self.reference_grp_widget_layout.addWidget(self.Add_Reference_Widget_HeaderUI())
        self.reference_grp_widget_layout.addWidget(self.AssetsToBeBatchedTabs)

        #=======================================================================
        #=======================================================================
        # # #Footer stuff
        #=======================================================================
        #=======================================================================
        self.Batch_Widget_Handler = BWH.Batch_Widget_Handler(self)
        
        self.OptionTabs = QTabWidget(self)
        self.OptionTabs.setTabPosition(QTabWidget.South)


        self.console        = Console.Console(self)

        self.batchBtn       = QPushButton('Batch!')
        self.stopBtn        = QPushButton('Stop')
        self.refreshUIBtn   = QPushButton('Refresh UI')
        self.pre_batch_Btn  = QPushButton('Pre Batch')
        
        self.optionBtnLayout.addWidget(self.batchBtn)
        self.optionBtnLayout.addWidget(self.refreshUIBtn)
        self.optionBtnLayout.addWidget(self.pre_batch_Btn)
        self.optionBtnLayout.addWidget(self.stopBtn)
        
        self.OptionTabs.addTab(self.Batch_Widget_Handler, 'Batch.io')
        self.OptionTabs.addTab(self.console, 'Console')
        #self.mainLayout.addLayout(self.optionBtnLayout)
        
        #=======================================================================
        # #Connect the buttons        
        #=======================================================================
        self.refreshUIBtn.clicked.connect(self.RefreshUI)
        self.stopBtn.clicked.connect(self.Stop)
    
        #=======================================================================
        # #Context menu
        #=======================================================================
        self.context_menu_console = Console.Console(self)
        self.context_menu_console.setWindowTitle('Log')
        
        #=======================================================================
        # #Set the splitters
        #=======================================================================
        self.centralWidgetSplitter = QSplitter(Qt.Horizontal)
        self.centralWidgetSplitter.addWidget(self.scene_grp_widget)
        self.centralWidgetSplitter.addWidget(self.reference_grp_widget)
        self.centralWidgetSplitter.setSizes([400, 200])
        self.centralWidgetSplitter.setStyleSheet("QSplitter:handle{height: 16px; image: url(%sverticalHandle.png);}"%BATCH_io_IMAGES)

        self.footerWidgetSplitter = QSplitter(Qt.Vertical)
        self.footerWidgetSplitter.addWidget(self.centralWidgetSplitter)
        self.footerWidgetSplitter.addWidget(self.OptionTabs)
        self.footerWidgetSplitter.setSizes([600, 250])
        self.footerWidgetSplitter.setStyleSheet("QSplitter:handle{height: 16px; image: url(%shorizontalHandle.png);}"%BATCH_io_IMAGES)

        self.centralLayout.addWidget(self.footerWidgetSplitter)

        

    def RefreshUI(self):
        #=======================================================================
        # #Delete the widgets on the list
        #=======================================================================
        self.CleanAssetWidgetsToBeBatchedUI()
        self.CleanSceneWidgetsToBeBatchedUI()
        
        #=======================================================================
        # #Add the new scene items on the list
        #=======================================================================
        if self.Pre_Batch_Scene_Info.Scene_List():
            for scene_short_name in self.Pre_Batch_Scene_Info.Scene_List():
                if self.Pre_Batch_Scene_Info.Pre_Batch_Info[scene_short_name].scene_check_state[scene_short_name]:
                    self.AddSceneWidgetToBeBatchedUI(scene_short_name, False, 'Ready')
                else:
                    self.AddSceneWidgetToBeBatchedUI(scene_short_name, False, 'Error')
        #=======================================================================
        # #Sort the items and add the reference items related to the first item
        #=======================================================================
        sceneList =  sorted(self.Pre_Batch_Scene_Info.Scene_List())
        sceneList = list(sceneList)
        if sceneList:
            self.scene_list_widget.SortByName(sceneList)
            
            self.AddAssetsToBeBatchedUI(sceneList[0])
        
        #=======================================================================
        # #Update the Batch widget handler
        #=======================================================================
        self.Batch_Widget_Handler.batch_mode = self.batch_mode            
        self.Batch_Widget_Handler.RefreshUI()
        
        #=======================================================================
        # Update the project label
        #=======================================================================
        self.project_lbl.setText('Project: %s'%Get_Project().split('/')[-2])
        #=======================================================================
        # #Finally reset the progress bar
        #=======================================================================
        self.SetProgressValue()
        self.refresh = True
    
    
    def Add_Scene_Widget_HeaderUI(self):
            #===================================================================
            # #Add header scene widgets
            #===================================================================
            self.header_widget = AW.AssetWidget()
            
            self.header_widget.SetCheckBox(True)
            self.header_widget.SetAssetLabel('scene name')
            self.header_widget.SetStatusLabel('status')
            self.header_widget.SetRadioButton(['Idle', 'Normal', 'High', 'Ultra'], 'priority', 1, self.Set_All_Thread_Priority, 'None')
            self.header_widget.Set_Radio_Label()

            self.header_widget.SetAssetBtn(assetButtonLabel="", 
                                           command=self.Batch_Run_Btn_Cmd, 
                                           isSquare=True, 
                                           isVisible=True, 
                                           icon=BATCH_io_IMAGES+'play.png')
            
            self.header_widget.SetAssetBtn("", self.Stop, True, True, BATCH_io_IMAGES+'stop.png')
            
            self.header_widget.SetAssetBtn(assetButtonLabel="", 
                                     command=self.Pre_Batch_Run_Btn_Cmd, 
                                     isSquare=True, 
                                     isVisible=True, 
                                     icon=BATCH_io_IMAGES+'pre_batch.png')
            
            self.header_widget.isTrigger    = False
            self.header_widget.isInterative = False
            
            
            checkbox_slot = self.Set_All_Scene_CheckState
            self.header_widget.SetCheckBoxChangeCmd(checkbox_slot)
            
            return self.header_widget
    
    def print_none(self):
        print 'None'
        
    #===========================================================================
    # #Add scene widgets
    #===========================================================================
    def AddSceneWidgetToBeBatchedUI(self, scene_short_name='', update=False, status=''):
        #=======================================================================
        # #Only update the scene widgets
        #=======================================================================
        if update:
            scene_widget = self.scene_list_widget.assetWidgets[scene_short_name]
            scene_widget.animRefresh()
            scene_widget.SetStatusLabel(status)
            scene_widget.SetProgressValue()

 
        else:
            #===================================================================
            # #Add scene widgets
            #===================================================================
            scene_widget = AW.AssetWidget()
        
            scene_short_name = scene_short_name
            
            scene_widget.SetProgress()
            scene_widget.SetCheckBox(True)
            scene_widget.SetAssetIcon(BATCH_io_IMAGES+'maya-icon.png')
            scene_widget.SetAssetLabel(scene_short_name)
            scene_widget.SetStatusLabel(status)
            scene_widget.SetRadioButton(['Idle', 'Normal', 'High', 'Ultra'], 'Priority', 1, self.Set_Thread_Priority, scene_short_name)
            
            scene_widget.SetAssetBtn(assetButtonLabel="", 
                                     command=partial(self.Batch_Run_Btn_Cmd, scene_short_name), 
                                     isSquare=True, 
                                     isVisible=True, 
                                     icon=BATCH_io_IMAGES+'play.png')
            
            scene_widget.SetAssetBtn(assetButtonLabel="", 
                                     command=partial(self.Stop_Batch_Process, scene_short_name), 
                                     isSquare=True, 
                                     isVisible=True, 
                                     icon=BATCH_io_IMAGES+'stop.png')
            
            
            scene_widget.SetAssetBtn(assetButtonLabel="", 
                                     command=partial(self.Pre_Batch_Run_Btn_Cmd, scene_short_name), 
                                     isSquare=True, 
                                     isVisible=True, 
                                     icon=BATCH_io_IMAGES+'pre_batch.png')
            
            
            scene_widget.SetAssetBtn(assetButtonLabel=u"\u2699", 
                                     command=partial(self.AddAssetsToBeBatchedUI, scene_short_name), 
                                     isSquare=True, 
                                     isVisible=False, 
                                     icon=None)
            
            
            scene_widget.isTrigger = True
            scene_widget.SetContextMenu(self.Set_Context_Menu('scene'))
            


            scene_widget.animRefresh()
                 
            self.scene_list_widget.AddAssetWidget(scene_widget, False, 'Scenes')
            
        
        scene_info = self.Pre_Batch_Scene_Info.Get_Scene_Info(scene_short_name)
        if scene_info:
            scene_widget.setToolTip(scene_info.scene_full_path.split('//')[-1])
            
        checkbox_slot = partial(self.Set_Scene_CheckState, scene_widget)
        scene_widget.SetCheckBoxChangeCmd(checkbox_slot)
        
        #===============================================================
        # # Finished
        #===============================================================
        if status == 'Finished':
            scene_widget.SetColor('ready')
            scene_widget.SetStatusLabel('FINISHED')
            scene_widget.animRefresh()
            
        #===============================================================
        # # Ready
        #===============================================================
        if status == 'Ready':
            scene_widget.SetColor('ready')
            scene_widget.SetStatusLabel('READY!')
            scene_widget.animRefresh()
            
        #===============================================================
        # # Stoped
        #===============================================================
        if status == 'Stoped':
            scene_widget.SetColor('stoped')
            scene_widget.SetStatusLabel('STOPED')
            
        #===============================================================
        # # Unchecked
        #===============================================================
        if status == 'Unchecked':
            scene_widget.SetColor('disabled')
            scene_widget.SetStatusLabel('UNCHECKED')
            self.Set_Scene_CheckState(scene_widget, False)

        
        #===============================================================
        # # Not Finished
        #===============================================================
        if status == 'Not Finished':
            scene_widget.SetColor('stoped')
            scene_widget.SetStatusLabel('FAILED')

        
        #=======================================================================
        # # Set the color if not finished with error
        #=======================================================================
        if status == 'Error':
            scene_widget.SetColor('stoped')
            scene_widget.SetStatusLabel('ERRO')

            
        #=======================================================================
        # # Dont changet the color
        #=======================================================================
        if status == 'Current':
            scene_widget.SetColor('current')

    #===========================================================================
    # #The Play button command of scene widgets
    #===========================================================================
    def Batch_Run_Btn_Cmd(self, scene_short_name=''):
        if not scene_short_name:
            self.Batch_Process_Creation()
        else:
            self.Batch_Process_Creation([self.Pre_Batch_Scene_Info.Get_Scene_Info(scene_short_name)])
            self.scene_list_widget.SetAssetUnselected(scene_short_name)

    #===========================================================================
    # #The pre batch refresh button command of scene widgets
    #===========================================================================
    def Pre_Batch_Run_Btn_Cmd(self, scene_short_name=''):
        self.Pre_Batch_Thread_Creation(scene_short_name)


    #===================================================================
    # #Add reference header widgets
    #===================================================================
    def Add_Reference_Widget_HeaderUI(self):
            self.header_ref_widget = AW.AssetWidget()

            self.header_ref_widget.SetSearch(self.Pre_Batch_Scene_Info.All_References(), self.Enter_Searching_Mode_Cmd, False, 'References')
            self.header_ref_widget.SetAssetBtn(assetButtonLabel="", 
                                     command=self.Batch_Run_on_Filetered_Reference_Cmd, 
                                     isSquare=True, 
                                     isVisible=True, 
                                     icon=BATCH_io_IMAGES+'play.png')

            self.header_ref_widget.isTrigger    = False
            self.header_ref_widget.isInterative = False
            self.header_ref_widget.isHeader     = True

            self.search_mode = False
            return self.header_ref_widget


    #===========================================================================
    # #Run the command only on filtered references
    #===========================================================================
    def Batch_Run_on_Filetered_Reference_Cmd(self):
        for reference_widget in self.result_search:
            reference_widget.asset_btn_list[0].clicked.emit()
    
        
    #===========================================================================
    # #Search engine command
    #===========================================================================
    def Enter_Searching_Mode_Cmd(self, found_reference='rosenio'):
        if not self.search_mode:
            self.CleanAssetWidgetsToBeBatchedUI()
            for scene_short_name in self.Pre_Batch_Scene_Info.Scene_List():
                self.AddAssetsToBeBatchedUI(scene_short_name, True)
            
            self.search_mode = True    
            
        self.result_search = []
        for reference_widget in self.AssetsToBeBatchedTabs.assetWidgets.values():
            reference_name = reference_widget.GetLabel()

            if (found_reference in reference_name) or (found_reference in reference_widget.asset_type):
                reference_widget.show()
                self.result_search.append(reference_widget)
            else:
                reference_widget.hide()
                

    #===========================================================================
    # #Add assets on scene to be Batched
    #===========================================================================
    def AddAssetsToBeBatchedUI(self, scene_short_name='', searching=None):
        if not searching:
            self.CleanAssetWidgetsToBeBatchedUI()
            self.search_mode = False  
        
        scene_info = self.Pre_Batch_Scene_Info.Get_Scene_Info(scene_short_name)
        
        if scene_info:
            #===================================================================
            # #Set the color of selection
            #===================================================================
            self.scene_list_widget.SetAssetUnselected(scene_short_name)
            self.header_ref_widget.SetSearch(self.Pre_Batch_Scene_Info.All_References(), self.Enter_Searching_Mode_Cmd, True)
            reference_list = scene_info.reference_list

            for reference_type in reference_list.keys():

                if searching and not self.search_mode:

                    #===============================================================
                    # #Add a tab for a reference search
                    #===============================================================
                    self.AssetsToBeBatchedTabs.set_tab('Searching...')
                    self.search_mode = True 
                    
                if not searching:
                    #===============================================================
                    # #Add a tab for a reference type if not in searching mode
                    #===============================================================
                    self.AssetsToBeBatchedTabs.set_tab(reference_type)
                    
                    
                for reference_name in reference_list[reference_type]:
                    reference_widget = AW.AssetWidget()
                    reference_widget.SetProgress()
                    reference_widget.SetCheckBox(scene_info.Get_Reference_Check_State(reference_type, reference_name))
                    reference_widget.SetAssetLabel(reference_name.split(':')[0])
                    
                    #===========================================================
                    # #Handle the reference level action
                    # #Wil improve on the feature
                    #===========================================================

                    scene_full_path     = scene_info.scene_full_path
                    reference_full_path = REF_FOLDER+'/'+scene_info.reference_full_path[reference_name]
                    
                    reference_data = {'reference_list':        {reference_type: [reference_name]}, 
                                  'Reference_CheckState_Info': {reference_type: {reference_name: True}}, 
                                  'Reference_Full_Path':       {reference_name: reference_full_path}, 
                                  'scene_short_name':          scene_short_name, 
                                  'Scene_CheckState_Info':     {scene_short_name: True}, 
                                  'scene_full_path':           scene_full_path,
                                  'Project_Path':              scene_info.project_path,
                                  'start_frame':               0,
                                  'end_frame':                 1
                                }
                    
                    #===========================================================
                    # #Toggle the ref on scene info
                    #===========================================================
                    reference_scene_info = self.Pre_Batch_Scene_Info.Set_Scene_Info(outputData=reference_data, temp=True)
                    
                    reference_widget.SetAssetBtn("", partial(self.Batch_Process_Creation, [reference_scene_info]), True, True, BATCH_io_IMAGES+'play.png')
                    reference_widget.SetAssetBtn("", partial(self.toggle_checked, reference_widget), True, False)
                    reference_widget.SetAssetType(reference_type)
                    reference_widget.SetContextMenu(self.Set_Context_Menu('reference', reference_scene_info))
                    
                    #===========================================================
                    # #Reference widget ToolTip
                    #===========================================================
                    
                    if not 'scenes' in reference_full_path:
                        reference_full_path = reference_full_path
                    
                    reference_widget.setToolTip('Scene___________'+scene_short_name+'\n'+
                                                'Path____________'+reference_full_path+'\n'+
                                                'Namespace_____'+reference_name+'\n'+
                                                'Type:___________'+reference_type
                                                )
                    
                    reference_widget.isTrigger = False
                    reference_widget.setParent(self)
                    
                    if self.search_mode:
                        self.AssetsToBeBatchedTabs.AddAssetWidget(reference_widget, True, 'Searching...')
                    else:
                        self.AssetsToBeBatchedTabs.AddAssetWidget(reference_widget, True, reference_type)

                    #===========================================================
                    # #Set the checkbox change state function
                    #===========================================================
                    checkboxslot = partial(self.Set_Reference_CheckState, scene_short_name, reference_type, reference_name)
                    reference_widget.SetCheckBoxChangeCmd(checkboxslot)
        

        self.AssetsToBeBatchedTabs.setCurrentIndex(self.current_category_tab)


    def toggle_checked(self, reference_widget):
        reference_widget.Set_CheckState_Value()
        print reference_widget
    
    
    def CleanSceneWidgetsToBeBatchedUI(self):
        self.scene_list_widget.CleanAssetWidgets()
            

    def CleanAssetWidgetsToBeBatchedUI(self):
        self.current_category_tab = self.AssetsToBeBatchedTabs.currentIndex()
        self.AssetsToBeBatchedTabs.CleanAssetWidgets()
        self.AssetsToBeBatchedTabs.clear()


    def SetProgressValue(self, value=0.0):
        self.header_widget.SetProgressValue(value)


    def resizeEvent(self, event):
        self.SetProgressValue()
        
        
    def collapse(self):
        if not self.is_collapsed:
            
            self.centralWidgetSplitter.setSizes([0, 0])
            self.footerWidgetSplitter.setSizes([0, 0])
            self.parent().setGeometry(500, 100, 0, 0)
            self.is_collapsed = True
            
        else:
            self.centralWidgetSplitter.setSizes([400, 200])
            self.footerWidgetSplitter.setSizes([600, 250])
            self.parent().setGeometry(500, 200, 0, 0)
            self.parent().setGeometry(500, 100, 1300, 900)
            self.is_collapsed = False
    

    #===========================================================================
    # Thread Manager functions   
    #===========================================================================
    #===========================================================================
    # #Stop all
    #===========================================================================
    def Stop(self):
        self.Stop_Pre_Batch_Process()
        self.Stop_Batch_Process()
        

    #===========================================================================
    # #Stop Pre Batch Process
    #===========================================================================
    def Stop_Pre_Batch_Process(self):
        self.Pre_Batch_Thread_Info  = Pre_Batch_Thread_Info.globalInstance(Pre_Batch_Thread_Info).Pre_Batch_Thread_Info

        #=======================================================================
        # #Kill the pre batch process
        #=======================================================================
        for scene_short_name in self.Pre_Batch_Thread_Info.keys():
            pre_batch_thread = self.Pre_Batch_Thread_Info[scene_short_name]['thread']
            
            try:
                pre_batch_thread.process.kill()
            except Exception, e:
                print e

        print 'Pre Batch stoped.'
        print 'All process deleted'

        
    #===========================================================================
    # #Stop Batch Process
    #===========================================================================
    def Stop_Batch_Process(self, scene_short_name=None):
        if not self.Batch_Thread_Info:
            return
        
        batch_thread_info = self.Batch_Thread_Info
        
        #=======================================================================
        # #Handle for single scene process stopping
        #=======================================================================
        if scene_short_name:
            batch_thread_info = {scene_short_name:{'thread':self.Batch_Thread_Info[scene_short_name]['thread']}}
        
        #=======================================================================
        # #Kill the batch process
        #=======================================================================
        for scene_short_name in batch_thread_info.keys():
            batch_thread = batch_thread_info[scene_short_name]['thread']
            if batch_thread:
                batch_thread.process.kill()

            if scene_short_name in self.Batch_Info.keys():
                #===================================================================
                # #Feed the scene status
                #===================================================================
                self.Batch_Info[scene_short_name]['status']  = 'Stoped'
                self.Batch_Info[scene_short_name]['command'] = 'Whatever'
    
                #===================================================================
                # #Log 
                #===================================================================
                log_line                   = 'Command: >> %s << : STOPED to run on scene %s by user.'%('Who cares', scene_short_name)
                self.LOG[scene_short_name] = [log_line]
                
                
                print "Batch process for the scene: %s Stoped"%scene_short_name

        print 'All process deleted'
            
    #===========================================================================
    # # Set thread priority
    #===========================================================================
    def Set_Thread_Priority(self, priority=1, scene_short_name=''):
        priority_name = self.TH_PRIORITY_LIST[priority]
        
        if scene_short_name in self.Batch_Thread_Info.keys():
            self.Batch_Thread_Info[scene_short_name]['priority'] = priority_name
  
            
    def Set_All_Thread_Priority(self, priority=1, *args):
        for scene_widget in  self.scene_list_widget.assetWidgets.values():
            radio_btn = scene_widget.radio_grp.radio_btn_list[priority]
            radio_btn.setChecked(True)
            radio_btn.clicked.emit()
            

    def Set_Scene_CheckState(self, *args):
        scene_widget     = args[0]
        scene_short_name = scene_widget.GetName()
        checkState       = True
        if not args[1]:
            checkState = False

        
        self.scene_list_widget.SetAssetUnselected(scene_widget.GetName())
        self.Pre_Batch_Scene_Info.Get_Scene_Info(scene_short_name).Set_Scene_Check_State(checkState)
        if self.refresh:
            self.AddAssetsToBeBatchedUI(scene_short_name)
        scene_widget.animRefresh()


    def Set_All_Scene_CheckState(self):
        self.refresh = False
        self.scene_list_widget.Set_CheckState_Toggle()

        
    def Set_Reference_CheckState(self, *args):
        scene_short_name  = args[0]
        reference_type    = args[1]
        reference         = args[2]
        checkState        = args[3]
        if checkState == 0:
            checkState = False
            
        if not checkState:
            print scene_short_name, reference_type, reference, "Will not be considered on the batch process."
        
        self.Pre_Batch_Scene_Info.Get_Scene_Info(scene_short_name).Set_Reference_Check_State(reference_type, reference, checkState)
        

    #===========================================================================
    # #Context menu for the widgets
    #===========================================================================
    def Set_Context_Menu(self, type, *args):
        self.context_menu_dict = {}
        
        if type=='scene':
            
            self.context_menu_dict['Log']        = self.log_ctx_mnu
            self.context_menu_dict['Open Scene'] = self.openScene_ctx_mnu
            
            return self.context_menu_dict
        
        if type=='reference':
            self.context_menu_dict['Reference File'] = partial(self.reference_ctx_mnu, *args)
            self.context_menu_dict['Open Scene']     = partial(self.reference_open_ctx_mnu, *args)
            
            return self.context_menu_dict
        
    #===========================================================================
    # #LOG context menu action
    #===========================================================================
    def log_ctx_mnu(self, scene_short_name='', *args):
        if scene_short_name in self.LOG.keys():
            self.context_menu_console.textBrowser.clear()
            
            for line in self.LOG[scene_short_name]:
                self.context_menu_console.AddText(line)
                
            self.context_menu_console.show()

    
    #===========================================================================
    # #Open Scene context menu action
    #===========================================================================
    def openScene_ctx_mnu(self, scene_short_name='', *args):
        if scene_short_name in self.Pre_Batch_Scene_Info.Scene_List():
            scene_full_path = self.Pre_Batch_Scene_Info.Get_Scene_Info(scene_short_name).scene_full_path
            cmds.file(scene_full_path, o=True, f=True)

    
    #===========================================================================
    # #Reference file context menu action        
    #===========================================================================
    def reference_ctx_mnu(self, reference_scene_info='', *args):
        namespace           = args[0]
        reference_full_path = reference_scene_info.reference_full_path[namespace]
        
        cmds.file(reference_full_path, reference=True, mergeNamespacesOnClash=False, namespace=namespace)
        #=======================================================================
        # #Set reference relative path
        #=======================================================================
        refNode = cmds.referenceQuery(reference_full_path, referenceNode=True)
        
        cmds.file(reference_full_path, loadReference=refNode)
        
    #===========================================================================
    # #Reference file context menu action        
    #===========================================================================
    def reference_open_ctx_mnu(self, reference_scene_info='', *args):
        namespace           = args[0]
        reference_full_path = reference_scene_info.reference_full_path[namespace]
        
        cmds.file(reference_full_path, o=True, f=True)

        