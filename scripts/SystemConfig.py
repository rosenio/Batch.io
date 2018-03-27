#===============================================================================
# #Autor:  Rosenio Pinto
# #e-mail: kenio3d@gmail.com
#===============================================================================
from functools import partial
from shutil import copyfile
from pprint import pprint
import base64, zlib
import tempfile
import datetime
import time
import glob
import json
import sys
import os

#===============================================================================
# #Add the main paths to the systems path
#===============================================================================
BATCH_io_SCRIPTS           = os.path.dirname(__file__)+'/'
BATCH_io_IMAGES            = BATCH_io_SCRIPTS.replace('scripts', 'images')
os.environ['XBMLANGPATH'] += BATCH_io_IMAGES

if not BATCH_io_SCRIPTS+'Tools' in sys.path:
    sys.path.append(BATCH_io_SCRIPTS+'Tools')
    sys.path.append(BATCH_io_SCRIPTS+'DB')
    sys.path.append(BATCH_io_SCRIPTS+'UI')
    sys.path.append(BATCH_io_SCRIPTS+'Process')
    sys.path.append(BATCH_io_SCRIPTS+'Process/Batch_Process')
    sys.path.append(BATCH_io_SCRIPTS+'Process/Pre_Batch_Process')
    sys.path.append(BATCH_io_SCRIPTS+'Process/Utils')
    sys.path.append(BATCH_io_SCRIPTS+'Tools')
    sys.path.append(BATCH_io_SCRIPTS+'Widgets')



#===============================================================================
# #Pyside Handle
#===============================================================================
from UI.Qt.QtCore import * 
from UI.Qt.QtGui import * 
from UI.Qt.QtWidgets import *
from UI.Qt import __version__
from shiboken2 import wrapInstance 


#===============================================================================
# #The main Rosenio's UI library
#===============================================================================
try:
    import Asset_Widgets as AW
    reload(AW)
except Exception, e:
    print e
    print 'Problems to import Asset_Widgets'
    
#===============================================================================
# If Maya main window if not in batch mode
#===============================================================================
insideMaya = True
try:
    import maya.OpenMaya as api
    import maya.cmds as cmds
    import maya.mel as mel
    from maya import OpenMayaUI as omui 
    
except Exception, e:
    print e
    insideMaya = False
    

#===============================================================================
# Qt function to get the parent main window
#===============================================================================
def get_main_window():
    if insideMaya:
        if not api.MGlobal.mayaState() == api.MGlobal.kLibraryApp:
            mayaMainWindowPtr   = omui.MQtUtil.mainWindow()
            return wrapInstance(long(mayaMainWindowPtr), QWidget) 

        if not api.MGlobal.mayaState() == api.MGlobal.kInteractive: #Batch mode
            return None
    else:
        return None

#===============================================================================
# Handle DB files
#===============================================================================
from DB import *
import DB.Mongo_Cache as mongo_cache

def Set_DB():
    #===============================================================================
    # #DB
    #===============================================================================
    if insideMaya:
        PROJECTPATH = Get_Project()
        DBPATH      = PROJECTPATH+'data/Cache_db/'
    else:
        PATHS       = mongo_cache.Get_Current_DB_Path()
        PROJECTPATH = PATHS['PROJECTPATH']
        DBPATH      = PATHS['DBPATH']
    
    try:
        if not os.path.exists(DBPATH):
            os.makedirs(DBPATH)
            
        if not os.path.exists(PROJECTPATH):
            os.makedirs(PROJECTPATH)
        #===========================================================================
        # #Register the current db path
        #===========================================================================
        mongo_cache.Save_Current_DB_Path(DBPATH, PROJECTPATH)
        AssetDB = mongo_cache.Asset()
    except Exception, e:
        print e
        print "Problems to save data base: %s"%DBPATH
    
    return AssetDB

#===============================================================================
#  Get the folder to be batched
#===============================================================================
def Get_SourceFolder():
    if insideMaya:
        PROJECTPATH = Get_Project()

    Set_DB()
    return PROJECTPATH+'/scenes/SOURCEFOLDER/'


#===============================================================================
# Get the project path
#===============================================================================
def Get_Project():
    if insideMaya:
        return cmds.workspace( q=True, rd=True )
    else:
        PATHS       = mongo_cache.Get_Current_DB_Path()
        PROJECTPATH = PATHS['PROJECTPATH']
        return PROJECTPATH


#===============================================================================
# 
#===============================================================================
#===============================================================================
# Custom global variables
#===============================================================================
#===============================================================================
# 
#===============================================================================
DEBUG_MODE        = True
SOURCEFOLDERLIST  = ['animation', 'render', 'groom', 'ref', 'modeling']
CACHE_FOLDER      = 'cache/abc'
REF_FOLDER        = 'scenes/ref'
CAMERA_NAME       = 'cam_render'
VERSION           = 2.7
TEMP_FOLDER       = 'c:/temp'
LOAD_MENU         = False


