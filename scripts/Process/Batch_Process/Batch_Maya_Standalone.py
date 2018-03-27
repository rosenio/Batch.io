
#===============================================================================
## Autor: Rosenio Pinto 
##
## This file is a widget for run in Batch process
##
#===============================================================================

#===============================================================================
# #Required  modules import
#===============================================================================
import sys, os
import base64, zlib
import tempfile

BATCH_io_SCRIPTS = os.environ['BATCH_io_SCRIPTS']
sys.path.append(BATCH_io_SCRIPTS)
sys.path.append(BATCH_io_SCRIPTS+'/Process')


import maya.standalone
import maya.cmds as cmds
import maya.mel as mel


try:
    from Utils import *

    import json
    from Widgets import *
    import Widgets as BW
except Exception, e:
    print e

#===============================================================================
# #Required Parsing args
#===============================================================================
def ParseArgs():
    args = sys.argv[1:]
    
    inputData = {}
    for i in range(0, len(args), 2):
        key   = args[i]
        value = args[i+1]
        inputData[key] = value
    
    return inputData

parsedArgs          = ParseArgs()

MAYA_PROJECT_PATH   = parsedArgs['-projectPath']
SCENE_FULL_PATH     = parsedArgs['-scene_full_path']
COMMAND_LIST        = eval(parsedArgs['-command_list'])
SCENE_SHORT_NAME    = parsedArgs['-scene_short_name']

scene_info_dict      = eval(parsedArgs['-sceneInfo'])

PRE_BATCH_SCENE_INFO = Pre_Batch_Scene_Info.globalInstance(Pre_Batch_Scene_Info)
SCENE_INFO           = PRE_BATCH_SCENE_INFO.Set_Scene_Info(scene_info_dict)


#===============================================================================
# #Custom modules import
# #Example:
# #import datetime
#===============================================================================
from datetime import datetime
import time

#===============================================================================
# #Custom global variables
# #Example:
#===============================================================================

if SCENE_INFO.Get_Scene_Check_State():
    #===============================================================================
    # #Required Maya standalone initialization
    #===============================================================================
    maya.standalone.initialize()
    
    cmds.loadPlugin('AbcImport.mll')
    cmds.loadPlugin('AbcExport.mll')
    
    #===============================================================================
    # #Not required but important Set Maya project
    #===============================================================================
    cmds.workspace( MAYA_PROJECT_PATH, openWorkspace=True )


    #===========================================================================
    # #Open the scene
    #===========================================================================
    cmds.file(SCENE_FULL_PATH, o=True, f=True)


#===============================================================================
# #The main function of batch widget
# #This function is the function the batch process will run
#===============================================================================

        
def main():

    #=======================================================================
    # #Run the command in the scene for eatch reference
    # 
    #=======================================================================
    outputData = {}
    count      = 0
    interrupt  = False
    for batch_widget_name in COMMAND_LIST['command_ordered_list']:
        batch_widget_settings = COMMAND_LIST[batch_widget_name]
        
        batch_widget  = getattr(BW, batch_widget_name)
        
        print 'Command NAME'+str(batch_widget_name)
        print 'Command LABEL'+str(batch_widget.WIDGET_NAME)
        
        #=======================================================================
        # #If scene is unchecked, break
        #=======================================================================
        if not SCENE_INFO.Get_Scene_Check_State():
            print 'UNCHECKED'
            outputData   = {'command':str(count)+'_'+batch_widget_name, 'status':'Unchecked'}
            break
        

        #=======================================================================
        # #Call the widget command
        #=======================================================================
        
        try:
            if not interrupt:
                #===================================================================
                # #Run the widget
                #===================================================================
                batch_widget.WIDGET_SETTINGS = batch_widget_settings
                batch_widget.main(SCENE_INFO)
     
                #=======================================================================
                # #Feed the output data
                #=======================================================================
                outputData = {'command':str(count)+'_'+batch_widget_name, 'status':'Finished'}
    
                time.sleep(1)
            else:
                outputData = {'command':str(count)+'_'+batch_widget_name, 'status':'Not Finished'}
                
        except Exception, e:
            #===================================================================
            # #Get the erro if exception
            #===================================================================
            print 'ERROR_<<<_%s_>>>_%s'%(str(e), SCENE_SHORT_NAME)
            outputData = {'command':str(count)+'_'+batch_widget_name, 'status':'Error'}
            print outputData
            interrupt = True
 

        count += 1
    
    #===========================================================================
    # # Return some information if no batch widgets are added
    #===========================================================================
    if not outputData:
        outputData = {'No_Batch_Wiget':{SCENE_SHORT_NAME:'You need to add a batch wiget on stack list.'}}


    #===========================================================================
    # #Write compressed data to be readed on batch process
    #===========================================================================
    outputData_B64 = base64.b64encode(zlib.compress(str(outputData), 9))

    with open(tempfile.gettempdir()+"/batch_data.json", "w") as batch_data_file:
        batch_data_file.write(str(outputData_B64))

    print 'DATA READY'        
    print outputData

print '\n'
print '### Process: STARTED on scene: >> %s << in | %s | ###'%(SCENE_SHORT_NAME, "{:%d.%m.%Y - %H:%M}".format(datetime.now()))
#===============================================================================
# #Start the main function
#===============================================================================
main()
#===============================================================================
# #End of process
#===============================================================================
print '### Process: FINISHED on scene: >> %s << in | %s | ###'%(SCENE_SHORT_NAME, "{:%d.%m.%Y - %H:%M}\n".format(datetime.now()))









