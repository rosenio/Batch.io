#===============================================================================
## Autor: Rosenio Pinto 
##
## This file is a widget for run in Batch process
##
#===============================================================================

#===============================================================================
# #Required  modules import
#===============================================================================
import maya.standalone
import maya.cmds as cmds
import json
import sys
import base64, zlib
import tempfile

#===============================================================================
# #Required Parsing argument pairs
#===============================================================================
def ParseArgs():
    args = sys.argv[1:]

    inputData = {}
    for i in range(0, len(args), 2):
        key   = args[i]
        value = args[i+1]
        inputData[key] = value
    
    return inputData

parsedArgs = ParseArgs()

MAYA_PROJECT_PATH = parsedArgs['-projectPath']
SCENE_FULL_PATH   = parsedArgs['-scene_full_path']
SCENE_SHORT_NAME  = parsedArgs['-scene_short_name']
COMMAND_LIST      = parsedArgs['-command_list']
SCENE_INFO        = parsedArgs['-sceneInfo']


#===============================================================================
# #Custom modules import
# #Example:
# #import datetime
#===============================================================================
from datetime import datetime
import time

#===============================================================================
# #Required global variables
#===============================================================================
REFFOLDER   = 'ref'


#===============================================================================
# #Required Maya standalone initialization
#===============================================================================
maya = maya.standalone.initialize()

#===============================================================================
# #Not required but important Set Maya project
#===============================================================================
cmds.workspace( MAYA_PROJECT_PATH, openWorkspace=True )


#===========================================================================
# #Open the scene
#===========================================================================
cmds.file(SCENE_FULL_PATH, loadReferenceDepth='none', o=True)


#===========================================================================
# #Read the scene references
#===========================================================================
REFERENCELIST = cmds.ls(type='reference')

sharedNodes = cmds.ls('*sharedReferenceNode*', '*:sharedReferenceNode*')
if sharedNodes:
    for sharedNode in sharedNodes:
        index = REFERENCELIST.index(sharedNode)
        REFERENCELIST.pop(index)


#===========================================================================
# #Read the scene reference count
#===========================================================================
REFCOUNT = len(REFERENCELIST)


#===============================================================================
# #Read the process stage
#===============================================================================
def ProcessStage(step=0):
    processStage = (100/(REFCOUNT)) * (step+1)  
    output       = str(processStage)
    
    return output


#===============================================================================
# #The main function of batch widget
# #This function is the function the batch process will run
#===============================================================================

def main():
    outputData = {}
    outputData['scene_short_name']          = SCENE_SHORT_NAME
    outputData['scene_full_path']           = SCENE_FULL_PATH
    outputData['reference_list']            = {}
    outputData['Scene_CheckState_Info']     = {}
    outputData['Reference_CheckState_Info'] = {}
    outputData['Reference_Full_Path']       = {}
    outputData['Project_Path']              = MAYA_PROJECT_PATH
    outputData['start_frame']               = cmds.playbackOptions(min=True, q=True)
    outputData['end_frame']                 = cmds.playbackOptions(max=True, q=True)
    #===========================================================================
    # #Main references iteration
    #===========================================================================
    for reference_index in range(REFCOUNT):
        try:
            #=======================================================================
            # #Get some ref info
            #=======================================================================
            reference_node      = REFERENCELIST[reference_index]
            reference_path      = cmds.referenceQuery(reference_node, filename=True)
            reference_namespace = cmds.file(reference_path, q=True, namespace=True)
            reference_type      = reference_path.split(REFFOLDER)[-1].split('/')[1]
            #=======================================================================
            # #Feed the output data
            #=======================================================================
            if not reference_type in outputData['reference_list'].keys():
                outputData['reference_list'][reference_type] = []

            #===================================================================
            # #Store the references
            #===================================================================
            outputData['reference_list'][reference_type].append(reference_namespace)
            
            outputData['Reference_Full_Path'][reference_namespace] = reference_path.split('scenes/ref/')[-1]
            #===================================================================
            # #Feed the scene check state for future use
            #===================================================================
            outputData['Scene_CheckState_Info'][SCENE_SHORT_NAME] = True
            
            if not reference_type in outputData['Reference_CheckState_Info'].keys():
                outputData['Reference_CheckState_Info'][reference_type] = {}

            #===================================================================
            # #Feed the reference check state for future use
            #===================================================================
            outputData['Reference_CheckState_Info'][reference_type][reference_namespace] = True
     
            
        except Exception, e:
            outputData['status']                                  = 'Error'
            outputData['error']                                   = str(e)
            outputData['Scene_CheckState_Info'][SCENE_SHORT_NAME] = False
            
            print 'ERROR_%s_%s'%(e, SCENE_SHORT_NAME)
            print outputData


        print 'STATUS'
        print ProcessStage(reference_index)
    
    if not REFCOUNT:
        e = 'Scene has no reference.'
        outputData['status']                                  = 'Error'
        outputData['error']                                   = str(e)
        outputData['Scene_CheckState_Info'][SCENE_SHORT_NAME] = False
        
        print 'ERROR_%s_%s'%(e, SCENE_SHORT_NAME)
        print outputData

        print 'STATUS'
        print 1
        
    #===========================================================================
    # #Write compressed data to be readed on pre batch process
    #===========================================================================
    outputD_b64 =  base64.b64encode(zlib.compress(str(outputData), 9))
    
    time.sleep(2)
    with open(tempfile.gettempdir()+"/pre_batch_data_%s.json"%SCENE_SHORT_NAME, "w") as pre_batch_file:
        pre_batch_file.write(str(outputD_b64))

    
    print 'DATA READY'
    print outputData

print 'Pre Batch: %s STARTED to run on scene: %s in %s'%('', SCENE_SHORT_NAME, "{:%d.%m.%Y - %H:%M}".format(datetime.now()))
#===============================================================================
# #Start the main function
#===============================================================================

main()

#===============================================================================
# #End of process
#===============================================================================
print 'Pre Batch: %s FINISHED on scene: %s in %s'%('', SCENE_SHORT_NAME, "{:%d.%m.%Y - %H:%M}".format(datetime.now()))











