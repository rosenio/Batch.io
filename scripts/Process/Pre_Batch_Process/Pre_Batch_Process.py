from SystemConfig import *
import Batch_Thread as THD
from Batch_io_UI import *
from Utils import *
from StringIO import StringIO

class Pre_Batch_Process(QWidget):
    def __init__(self, parent=None):
        super(Pre_Batch_Process, self).__init__(parent)   
        self.Pre_Batch_Scene_Info  = Pre_Batch_Scene_Info.globalInstance(Pre_Batch_Scene_Info)
        
        self.Pre_Batch_Info        = Pre_Batch_Info.globalInstance(Pre_Batch_Info).Pre_Batch_Info
        self.Pre_Batch_Thread_Info = Pre_Batch_Thread_Info.globalInstance(Pre_Batch_Thread_Info).Pre_Batch_Thread_Info
        self.Pre_Batch_Thread_Pool = QThreadPool()
        
        self.process_file          = os.environ['BATCH_io_SCRIPTS']+'Process/Pre_Batch_Process/Pre_Batch_Maya_Standalone.py'
        
        self.B_UI = Batch_io_UI.globalInstance(Batch_io_UI)
        self.B_UI.pre_batch_Btn.clicked.connect(self.Refresh_Pre_Batch_Data)
        
        self.B_UI.Pre_Batch_Thread_Creation = self.Pre_Batch_Thread_Creation
        
        
        #=======================================================================
        # #Set to anim folder by default
        #=======================================================================
        self.SOURCEFOLDER = Get_SourceFolder().replace('SOURCEFOLDER', 'animation')
        
        #=======================================================================
        # #LOG
        #=======================================================================
        self.LOG          = LOG.globalInstance(LOG).LOG
        
        #=======================================================================
        # #Main thread pool
        #=======================================================================
        self.Pre_Batch_ThreadPool = QThreadPool()
        
    #===============================================================================
    # #Refresh data
    #===============================================================================
    def Refresh_Pre_Batch(self):
        if not self.Pre_Batch_Scene_Info.Scene_List():
            self.Pre_Batch_Thread_Creation()
        else:
            self.B_UI.RefreshUI()
        

    def Refresh_Pre_Batch_Data(self):
        self.SOURCEFOLDER = Get_SourceFolder().replace('SOURCEFOLDER', 'animation')
        self.Pre_Batch_Thread_Creation()

    #===============================================================================
    # #PreBatch functions
    #===============================================================================
    #Main function to create the pre batch scene information
    def Pre_Batch_Thread_Creation(self, scene_short_name_single=None):
        
        if not scene_short_name_single:
            self.Pre_Batch_Scene_Info.Clear()
            
        self.B_UI.CleanSceneWidgetsToBeBatchedUI()
        
        #=======================================================================
        # #The range of the scene list
        #=======================================================================
        source_length = None
        
        #=======================================================================
        # #Get a list of files on the source folder
        #=======================================================================
        self.maya_files = Maya_Files.recursive_glob(self.SOURCEFOLDER, '.mb') + Maya_Files.recursive_glob(self.SOURCEFOLDER, '.ma')

        self.process_count  = 0
        self.process_length = len(self.maya_files[:source_length])
        
        if not self.process_length:
            print 'There is no files on %s'%self.SOURCEFOLDER
            return
        
        
        for scene_full_path in self.maya_files[:source_length]:
            scene_full_path  = scene_full_path.replace('\\', '/')
            scene_short_name = scene_full_path.split('/')[-1].split('.')[0]
            
            self.B_UI.AddSceneWidgetToBeBatchedUI(scene_short_name, False, 'Pre Batching...')
   
            if scene_short_name_single:
                if not scene_short_name_single == scene_short_name:
                    self.B_UI.AddSceneWidgetToBeBatchedUI(scene_short_name, True, 'Ready!')
                    
                    continue

            #===================================================================
            # #Create the Pre Batch Thread with the proper information
            #===================================================================
            Pre_Batch_Thread = THD.Batch_Thread(command = 'mayapy',
                                 processFile = self.process_file, 
                                 args        = {'projectPath':Get_Project(), 
                                                       'scene_full_path':scene_full_path, 
                                                       'scene_short_name':scene_short_name, 
                                                       'preloadOnly':'True',
                                                       'byPassRefs':'False',
                                                       'command_list':[],
                                                       'sceneInfo':{}})
            
            #===================================================================
            # #Thread Sinals connection
            #===================================================================
            Pre_Batch_Thread.signal.Batch_Thread_Started_Signal.connect(self.PreBatchProcessStarted)
            Pre_Batch_Thread.signal.Batch_Thread_Signal.connect(self.PreBatchProcess_Data)
            Pre_Batch_Thread.signal.Batch_Thread_Finished_Signal.connect(self.PreBatchProcessFinished)
            Pre_Batch_Thread.signal.Batch_Thread_Error_Signal.connect(self.PreBatchProcessError)
            Pre_Batch_Thread.signal.Batch_Thread_Status_Signal.connect(self.PreBatchProcessStatus)
            
            #===================================================================
            # #Store the process information for feature use
            #===================================================================
            self.Pre_Batch_Thread_Info[scene_short_name] = {'thread':Pre_Batch_Thread, 'priority':self.B_UI.TH_PRIORITY_LIST[1]}
            
            #===================================================================
            # #Start the process on the thread poo
            #===================================================================
            self.Pre_Batch_ThreadPool.start(Pre_Batch_Thread, 1)

            Pre_Batch_Thread.process_start()

    #===========================================================================
    # #Run on pre batch process estarted
    #===========================================================================
    def PreBatchProcessStarted(self, *args):
        scene_short_name = args[0]
        scene_widget     = self.B_UI.scene_list_widget.assetWidgets[scene_short_name]
        #data             = args[0]['data']
        print 'PreBatch on scene: %s process starting...'%scene_short_name
        
        self.Pre_Batch_Info[scene_short_name] = {}
        
        self.B_UI.AddSceneWidgetToBeBatchedUI(scene_short_name, True, 'PRE BATCH STARTED...')
        scene_widget.SetColor('loading')

    #===========================================================================
    # #Run on pre batch process finished
    #===========================================================================
    def PreBatchProcessFinished(self, *args):
        scene_short_name    = args[0]['scene_short_name']
        data                = args[0]['data']
        self.process_count += 1
        
        #=======================================================================
        # #Update the progress bar
        #=======================================================================
        progress_value = (100.0/self.process_length) * self.process_count
        self.B_UI.SetProgressValue(progress_value)
        

        #===============================================================
        # #Get scene info and scene widdget to update the staus
        #===============================================================
        scene_info = self.Pre_Batch_Info[scene_short_name]
        if scene_info: 
            print "Command: %s on scene: %s finished with status: %s"%(scene_info['command'],
                                                                   scene_short_name, 
                                                                   scene_info['status'])
            

            self.B_UI.AddSceneWidgetToBeBatchedUI(scene_short_name, True, scene_info['status'])
            

        if self.process_count >= self.process_length:
            print 'Pre Batch Finished!'
            
            self.B_UI.RefreshUI()

    #===========================================================================
    # #Run on error got from process
    #===========================================================================
    def PreBatchProcessError(self, *args):


        scene_short_name = args[0]['scene_short_name']
        data             = args[0]['data']

        self.LOG[scene_short_name] = []
            
        for line in data.splitlines():
            if 'WARNING' or 'ERROR' in line:
                #===============================================================
                # #Update batch info 
                #===============================================================
                self.Pre_Batch_Info[scene_short_name] = {'command':'Pre Batch', 'status':'Error'}
                #===============================================================
                # #LOG
                #===============================================================
                self.B_UI.console.AddText(line)

                
                self.LOG[scene_short_name].append(line)

        self.B_UI.AddSceneWidgetToBeBatchedUI(scene_short_name, True, 'Error')

        
        
    #===========================================================================
    # #Pre batch process read output messages
    #===========================================================================
    def PreBatchProcess_Data(self, *args):
        scene_short_name = args[0]['scene_short_name']
        data             = args[0]['data']
        data_ready       = False

        for line in data.splitlines():
            #===================================================================
            # #Get the main data
            #===================================================================
            if data_ready:

                #===============================================================
                # #Read and decompress pre batch data
                #===============================================================
                pre_batch_file = tempfile.gettempdir()+"/pre_batch_data_%s.json"%scene_short_name
                if os.path.isfile(pre_batch_file):
                    with open(pre_batch_file, "r") as pre_batch_data:
                        compressed_data = pre_batch_data.read()
                    outputData = eval(zlib.decompress(base64.b64decode(compressed_data)))
                
                    #Delete the temporary file
                    os.remove(pre_batch_file)
                
                
                    #===============================================================
                    # #If error in pre batch process
                    #===============================================================
                    if 'status' in outputData.keys():
                        print "Command: 'Pre Batch' on scene: %s finished with status: %s \n Erro: %s"%(outputData['scene_short_name'],
                                                                               outputData['status'],
                                                                               outputData['error'])
                        data_ready = False
    
                    
                    self.Pre_Batch_Scene_Info.Set_Scene_Info(outputData)
                
            if 'DATA READY' in line:
                data_ready = True


    #Feed the status
    def PreBatchProcessStatus(self, *args):
        scene_short_name = args[0]['scene_short_name']
        data             = args[0]['data']
        
        started = False
        for line in data.splitlines():
            if started:
                log_line = 'Processing stage on scene %s: %s'%(scene_short_name, (line + '%'))
                self.B_UI.console.AddText(log_line)
                #===============================================================
                # #LOG
                #===============================================================
                
                self.LOG[scene_short_name].append(log_line)

                started = False

            if 'STATUS' in line:
                started = True
                
            if 'STARTED' in line:
                self.B_UI.console.AddText(line)
                self.Pre_Batch_Info[scene_short_name] = {'command':'Pre Batch', 'status':'Started'}
                #===============================================================
                # #LOG
                #===============================================================
                self.LOG[scene_short_name] = []
                self.LOG[scene_short_name].append(line)
            
            if 'FINISHED' in line:
                self.B_UI.console.AddText(line)
                self.B_UI.console.AddText('<>.<>.<><><>.<>.<>')
                
                if self.Pre_Batch_Info[scene_short_name]['status'] == 'Error':
                    self.Pre_Batch_Info[scene_short_name] = {'command':'Pre Batch', 'status': 'Error'}
                else:
                    self.Pre_Batch_Info[scene_short_name] = {'command':'Pre Batch', 'status': 'Ready'}
                #===============================================================
                # #LOG
                #===============================================================
                self.LOG[scene_short_name].append(line)


                
                