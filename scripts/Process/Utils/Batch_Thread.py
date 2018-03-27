#===============================================================================
# # Autor: Rosenio Pinto
# # e-mail: kenio3d@Gmail.com
#===============================================================================
from SystemConfig import *

#===============================================================================
# #Create some signal slots
#===============================================================================
class OutPutSignal(QObject):
        Batch_Thread_Started_Signal  = Signal(dict)
        Batch_Thread_Signal          = Signal(dict)
        Batch_Thread_Error_Signal    = Signal(dict)
        Batch_Thread_Finished_Signal = Signal(dict)
        Batch_Thread_Status_Signal   = Signal(dict)


#===============================================================================
# #The main Thread for handle the batch processes
#===============================================================================
class Batch_Thread(QRunnable):
    def __init__(self, command='mayapy', processFile=None, isPreBatch=True, args={}, scene_widget=None):
        super(Batch_Thread, self).__init__() 
        self.signal       = OutPutSignal()

        self.process      = QProcess()

        self.command_name = command
        self.processFile  = r''+processFile
        self.isPreBatch   = isPreBatch
        self.args         = args
        self.scene_widget = scene_widget
        #=======================================================================
        # #Batch process args
        #=======================================================================
        if not self.isPreBatch:
            arg_list=['-projectPath', 
                   self.args['projectPath'],
                    '-scene_full_path', 
                    self.args['scene_full_path'], 
                    '-scene_short_name', 
                    self.args['scene_short_name'], 
                   '-command_list',
                   self.args['command_list'],
                   '-sceneInfo',
                   self.args['sceneInfo']
                   ]

 
        if self.isPreBatch:
            #=======================================================================
            # #Pre Batch process args
            #=======================================================================
            arg_list=['-projectPath',
                    self.args['projectPath'], 
                    '-scene_full_path', 
                    self.args['scene_full_path'], 
                    '-scene_short_name', 
                    self.args['scene_short_name'], 
                    '-preloadOnly', 
                    self.args['preloadOnly'], 
                    '-byPassRefs', 
                    self.args['byPassRefs'],
                    '-command_list',
                    self.args['command_list'],
                    '-sceneInfo',
                    self.args['sceneInfo']
                    ]
        
        self.arg_list = [self.processFile] + arg_list
    

    #===========================================================================
    # #Process that runs the command  
    #===========================================================================
    def process_start(self):
        #=======================================================================
        # # Connect the signal readyReadStandardOutput to the slot of the widget
        #=======================================================================
        
        self.process.started.connect(partial(self.signal.Batch_Thread_Started_Signal.emit, self.args['scene_short_name']))
        self.process.readyReadStandardOutput.connect(partial(self.ReadStdOutput, self.args['scene_short_name']))
        self.process.finished.connect(partial(self.ProcessFinished, self.args['scene_short_name']))
        self.process.errorOccurred.connect(partial(self.ProcessError, self.args['scene_short_name']))

        #=======================================================================
        # #Start the process
        #=======================================================================
        self.process.start(self.command_name, self.arg_list)
        
        if DEBUG_MODE:
            pprint(eval(str(self.args['command_list'])))


    @Slot()
    def ReadStdOutput(self, scene_short_name='', *args):
        
        data        = str(self.process.readAllStandardOutput())
        output_data = {'scene_short_name':scene_short_name, 'data':data}
        
        self.signal.Batch_Thread_Signal.emit(output_data)
        self.signal.Batch_Thread_Status_Signal.emit(output_data)
        
        
        #=======================================================================
        # #debug mode
        #=======================================================================
        if DEBUG_MODE:
            print data
            
        #=======================================================================
        # #UI related
        #=======================================================================
        if self.scene_widget:
            for line in data.splitlines():
                if 'Command LABEL' in line:
                    self.process_label = line.replace('Command LABEL', '').split('_')[0]
                    
                if 'PROGRESS_' in line:
                    #===============================================================
                    # #Update the progressbar of scene widget
                    #===============================================================
                    try:
                        progress = float(line.split('_')[-1])
     
                        self.scene_widget.SetProgressValue(progress)
                        
                    except:
                        pass
                    
                if 'RUNNING' in line:
                    self.scene_widget.SetStatusLabel('Running [ %s ] command...'%self.process_label)
             
        #=======================================================================
        # #UI related
        #=======================================================================


    @Slot()
    def ProcessFinished(self, scene_short_name='', *args):
        data        = str(self.process.readAllStandardOutput())
        output_data = {'scene_short_name':scene_short_name, 'data':data}
        
        self.signal.Batch_Thread_Finished_Signal.emit(output_data)
        
    @Slot()
    def ProcessError(self, scene_short_name='', *args):
        data = str(self.process.readAllStandardError())
        output_data = {'scene_short_name':scene_short_name, 'data':data}
        self.signal.Batch_Thread_Error_Signal.emit(output_data)
        
    

    def stop(self):
        self.quit()


        
        
        
        