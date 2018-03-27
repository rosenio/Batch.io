#===============================================================================
# Batch.io Maya Plugin
#
# Description:
#   Load the script that creates the menu and shelf
#===============================================================================
import sys
import os
import imp
import maya.cmds as cmds
import maya.mel as mel

#===============================================================================
# Scripts path folder
#===============================================================================
dirPath = os.path.dirname(cmds.pluginInfo('Batch_io', q=1, path=1))

#===============================================================================
# Add the scripts path to the system paths 
#===============================================================================
if dirPath and os.path.isdir(dirPath):
    scriptsPath = dirPath.replace('Batch_io/plug-ins', 'Batch_io/scripts')

    if not scriptsPath in sys.path:
        sys.path.append(scriptsPath)

else:
    cmds.warning('Batch_io folder not found!')
    cmds.unloadPlugin('Batch_io.py', f=1)
    
    os.environ['Batch_io'] = ' '

    sys.exit()


#===============================================================================
# Plugin initializer
#===============================================================================
def initializePlugin(obj):
    import Batch_io_setup
    reload(Batch_io_setup)
    Batch_io_setup.Batch_io_setup_Load()
    print 'Batch_io: >>> Plug-In successfully loaded!'


#===============================================================================
# Plugin unitializer
#===============================================================================
def uninitializePlugin(obj):
    import Batch_io_setup
    reload(Batch_io_setup)
    Batch_io_setup.Batch_io_setup_UnLoad()
    print "Batch_io: >>> Plug-In unloaded!"



