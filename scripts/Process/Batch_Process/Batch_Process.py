#===============================================================================
# #Autor: Rosenio Pinto
# #e-mail: kenio3d@gmail.com
#===============================================================================
from SystemConfig import *
from Batch_io_UI import *
from Utils import *


class Batch_Process(QWidget):
    def __init__(self, parent=None):
        super(Batch_Process, self).__init__(parent)           
        
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)
        #=======================================================================
        # #Main info of batch process
        #=======================================================================

        self.Batch_Info        = Batch_Info.globalInstance(Batch_Info).Batch_Info
        self.Batch_Thread_Info = Batch_Thread_Info.globalInstance(Batch_Thread_Info).Batch_Thread_Info
        self.process_file      = os.environ['BATCH_io_SCRIPTS']+'Process/Batch_Process/Batch_Maya_Standalone.py'
        
        self.Pre_Batch_Scene_Info = Pre_Batch_Scene_Info.globalInstance(Pre_Batch_Scene_Info)
        #=======================================================================
        # #Connect to the UI
        #=======================================================================
        self.B_UI                          = Batch_io_UI.globalInstance(Batch_io_UI)
        self.B_UI.Batch_Process_Creation   = self.Batch_Process_Creation
        self.B_UI.batchBtn.clicked.connect(self.Batch_Process_Creation)
        #=======================================================================
        # #Main thread pool
        #=======================================================================
        self.Batch_ThreadPool = QThreadPool()
        
        #=======================================================================
        # #Log
        #=======================================================================
        self.LOG     = LOG.globalInstance(LOG).LOG


        self.mainLayout.addWidget(self.B_UI)
        

    #===============================================================================
    # #Batch functions
    #===============================================================================
    #===========================================================================
    # 
    #===========================================================================
    #===========================================================================
    # #The main batch function
    #===========================================================================
    def Batch_Process_Creation(self, scene_info=None):
        self.B_UI.console.Clear()
        

        for scene_short_name in self.Pre_Batch_Scene_Info.Scene_List():
            self.Batch_Thread_Info[scene_short_name] = {'thread':None, 'priority':'NormalPriority'}
        #=======================================================================
        # #Get the bathc widget list. Return if empty list
        #=======================================================================
        
        self.B_UI.SetProgressValue()

        self.batch_widget_list   = self.B_UI.Batch_Widget_Handler.Get_cmd_ON_Stack()

        #=======================================================================
        # #If nothing on stack commands get out
        #=======================================================================
        if not self.batch_widget_list['command_ordered_list']:
            cmds.warning('You need to add some batch widgets to be runned on the scenes.')
            return
        
        #=======================================================================
        # #On Run button click
        #=======================================================================
        if not scene_info:
            scene_info = sorted(self.Pre_Batch_Scene_Info.All_Scene_Info())

        self.overall_process_count = 0
        self.process_length        = len(scene_info)
        
        #=======================================================================
        # #For eatch scene create an process
        #=======================================================================
        for SceneInfo in scene_info:
            scene_short_name = SceneInfo.scene_short_name
            scene_widget = self.B_UI.scene_list_widget.assetWidgets[scene_short_name]
            #===================================================================
            # #Create the Batch Processes
            #===================================================================
            BT = Batch_Thread(command    = 'mayapy',
                             processFile = self.process_file,
                             isPreBatch  = False, 
                             args={'projectPath':Get_Project(),
                                    'scene_full_path':SceneInfo.scene_full_path, 
                                    'scene_short_name':scene_short_name,
                                    'command_list':str(self.batch_widget_list),
                                    'sceneInfo':str(SceneInfo.As_Dict())
                                    }, scene_widget=scene_widget)
                                         

            #===================================================================
            # #Thread Sinals Connection
            #===================================================================
            BT.signal.Batch_Thread_Started_Signal.connect(self.BatchProcess_Started)
            BT.signal.Batch_Thread_Signal.connect(self.BatchProcess_Data)
            BT.signal.Batch_Thread_Finished_Signal.connect(self.BatchProcess_Finished)
            BT.signal.Batch_Thread_Error_Signal.connect(self.BatchProcess_Error)
            BT.signal.Batch_Thread_Status_Signal.connect(self.BatchProcess_Status)
            
            #===================================================================
            # #Set the priority of the thread
            #===================================================================
            priority_name  = self.Batch_Thread_Info[scene_short_name]['priority'] 
            
            self.Batch_Thread_Info[scene_short_name]['thread']   = BT
            self.Batch_Thread_Info[scene_short_name]['priority'] = priority_name
            priority_index                                       = self.B_UI.TH_PRIORITY_LIST.index(priority_name)
            
            #===================================================================
            # #Start the main threadPool
            #===================================================================
            self.Batch_ThreadPool.start(BT, priority_index)
            
            #===================================================================
            # #Start the thread
            #===================================================================
            BT.process_start()
            
            
      
    #===========================================================================
    # #Start all Batch Thread on thread pool
    #===========================================================================
    def Start_Batch_Main_Thread(self):
        for scene_short_name, Batch_Thread in self.Batch_Thread_Info.iteritems():
            Batch_Thread['thread'].process_run()

    
    #===========================================================================
    # #Slots Callbatcks
    #===========================================================================
    # #BatchProcess_Started:  Will handle the start of the process
    #
    # #BatchProcess_Finished: Will handle the finish of the process
    #
    # #BatchProcess_Data:     Will handle the data that comes form process
    #
    # #BatchProcess_Status:   Will handle the progress status of the process
    #===========================================================================
    # #===========================================================================
    #===========================================================================
    # #===========================================================================
    #===========================================================================
    
    
    #===========================================================================
    # #Run on process started
    #===========================================================================
    def BatchProcess_Started(self, scene_short_name='', *args):
        scene_widget = self.B_UI.scene_list_widget.assetWidgets[scene_short_name]
        
        self.Batch_Info[scene_short_name] = {}
        
        print 'Batch on scene: %s process starting...'%scene_short_name
        self.commandCount = len(self.B_UI.Batch_Widget_Handler.Get_cmd_ON_Stack())
        
        self.B_UI.AddSceneWidgetToBeBatchedUI(scene_short_name, True, 'STARTED...')
        scene_widget.SetColor('loading')


    #===========================================================================
    # #Run on process finished
    #===========================================================================
    def BatchProcess_Finished(self, *args):
        scene_short_name = args[0]['scene_short_name']
        
        self.overall_process_count += 1
        
        self.B_UI.LOG = self.LOG
        self.B_UI.SetProgressValue((100.0/self.process_length) * self.overall_process_count)
        
        #===============================================================
        # #Get scene info and scene widdget to update the staus
        #===============================================================
        scene_info = self.Batch_Info[scene_short_name]
        if scene_info:
            print "Command: %s on scene: %s finished with status: %s"%(scene_info['command'],
                                                                   scene_short_name, 
                                                                   scene_info['status'])
            

            self.B_UI.AddSceneWidgetToBeBatchedUI(scene_short_name, True, scene_info['status'])
        
        
    #===========================================================================
    # #Run on error got from process
    #===========================================================================
    def BatchProcess_Error(self, *args):
        scene_short_name = args[0]['scene_short_name']
        data             = args[0]['data']
        
        for line in data.splitlines():
            if 'ERROR_' in line:
                #===============================================================
                # #Update batch info 
                #===============================================================
                self.Batch_Info[scene_short_name] = {'command':'None', 'status':'Error'}
                #===============================================================
                # #LOG
                #===============================================================
                self.B_UI.console.AddText(line)
                self.LOG[scene_short_name].append(line)



    def BatchProcess_Data(self, *args):
        #=======================================================================
        # # Read the output messages
        #=======================================================================
        scene_short_name  = args[0]['scene_short_name']
        
        data              = args[0]['data']
        data_ready        = False
        
        for line in data.splitlines():
            #===================================================================
            # #Get the Batch info
            #===================================================================
            if data_ready:
                #===============================================================
                # #Read and decompress pre batch data
                #===============================================================
                with open(tempfile.gettempdir()+"/batch_data.json", "r") as batch_file:
                    compressed_data = batch_file.read()
                outputData = eval(zlib.decompress(base64.b64decode(compressed_data)))

                if outputData:
                    self.Batch_Info[scene_short_name] = outputData
                    data_ready = False  


            #===================================================================
            # #Get the data from next received line
            #===================================================================
            if 'DATA READY' in line:
                data_ready = True
 
 
    #===========================================================================
    # #Feed the status
    #===========================================================================
    def BatchProcess_Status(self, *args):
        #=======================================================================
        # # Read the output messages
        #=======================================================================
        scene_short_name = args[0]['scene_short_name']
        scene_widget     = self.B_UI.scene_list_widget.assetWidgets[scene_short_name]
        
        data             = args[0]['data']
        
        #===============================================================
        # #Set to do not get the data on the first iteration
        #===============================================================

        for line in data.splitlines():
            scene_info = self.Batch_Info[scene_short_name]
            
            #===================================================================
            # #Get the status
            #===================================================================
            if 'Command NAME' in line:
                self.processName = line.replace('Command NAME', '').split('_')[0]
                #===================================================================
                # #Update the progress label on ui
                #===================================================================
                if not self.processName == 'UNCHECKED':
                    self.process_count = self.batch_widget_list['command_ordered_list'].index(self.processName+'_widget')


            #===================================================================
            # #Get the first message from the batch widget running on scene level
            #===================================================================
            if 'RUNNING' in line:
                #===============================================================
                # #LOG
                #===============================================================
                self.LOG[scene_short_name].append(line)
            

            if 'PROGRESS_' in line:
                #===============================================================
                # #Update the progressbar of scene widget
                #===============================================================
                try:
                    progress = float(line.split('_')[-1])
                    #===============================================================
                    # #LOG
                    #===============================================================
                    log_line = '>> %s << Progress: [ %s]'%(self.processName, str(int(progress)) +'%')
                    self.LOG[scene_short_name].append(log_line)
                except:
                    pass
                
            
            
            #===================================================================
            # #Unchecked case
            #===================================================================
            if 'UNCHECKED' in line:
                self.Batch_Info[scene_short_name] = {'command':self.processName, 'status':'Unchecked'}
                

            #===================================================================
            # #Log if receive a STARTED message
            #===================================================================
            if 'STARTED' in line:
                #self.console.AddText(line)
                self.Batch_Info[scene_short_name] = {'command':'Batch', 'status':'Started'}
                #===============================================================
                # #LOG
                #===============================================================
                self.LOG[scene_short_name] = []
                self.LOG[scene_short_name].append(line)


            #===================================================================
            # #Log if receive a FINISHED message and update the UI
            #===================================================================
            if 'FINISHED' in line:
                
                if 'status' in self.Batch_Info[scene_short_name].keys():
                    status = self.Batch_Info[scene_short_name]['status']
                    if status == 'Started':
                        status = 'Finished'
                    


                    self.Batch_Info[scene_short_name] = {'command':self.processName, 'status': status}
    
                    #===============================================================
                    # #LOG
                    #===============================================================
                    self.LOG[scene_short_name].append(line)
    
                    for log_line in self.LOG[scene_short_name]:
                        self.B_UI.console.AddText(log_line)
                    self.B_UI.console.AddText('\n#<><><><><><><><><><:><:><:><:><:><><><><><><><><><><>#\n')
                    
                    status_data_ready = False
                
            
            if 'ERROR_' in line:
                #===============================================================
                # #Update batch info 
                #===============================================================
                self.Batch_Info[scene_short_name] = {'command':'None', 'status':'Error'}
                #===============================================================
                # #LOG
                #===============================================================
                self.B_UI.console.AddText(line)
                self.LOG[scene_short_name].append(line)
                
        