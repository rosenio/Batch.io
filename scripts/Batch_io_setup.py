#===============================================================================
# Ugly but handy code to create or remove menu and shelf
#
# The menu and shelf was created when the plugin are loaded, and
# removed if plugin is unloaded
#===============================================================================
from SystemConfig import *

os.environ['BATCH_io_SCRIPTS'] = BATCH_io_SCRIPTS

MAYA_VERSION                   = cmds.about(version=1)
batch_io_MenuDict = {'script':'Batch_io_main.py', 
                          'label':'Batch_io', 
                          'command':'import Batch_io_main as B; Batch_ioInst = B.Batch_io_main.globalInstance(B.Batch_io_main).show()', 
                          'icon':'batch_io.png'}

MENUDICTLIST = []



def Batch_io_SetupMenu():
    parent_menu = 'Batch_io_Menu' #Edit this if you want to put the item menu in your custom menu.
    toolLabel   = 'Batch_io'
    
    gMainWindow = mel.eval('$gMW=$gMainWindow')
    if cmds.menu(parent_menu, q=1, ex=1):
        cmds.deleteUI(parent_menu, menu=1)
    
    
    #===========================================================================
    # #Check temp folder
    #===========================================================================
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)
        
    #===========================================================================
    # Delete shelf if exists
    #===========================================================================
    if cmds.shelfLayout(toolLabel, ex=1):
        cmds.deleteUI(toolLabel)
    
    if LOAD_MENU:
        MENUDICTLIST = [batch_io_MenuDict]
    
        #===========================================================================
        # Create the parent menu
        #===========================================================================
        Batch_io_Menu = cmds.menu(parent_menu, p=gMainWindow, to=1, l=toolLabel)
        
        
        #===========================================================================
        # #Create the shelf
        #===========================================================================
        mel.eval('$scriptsShelf = `shelfLayout -cellWidth 33 -cellHeight 33 -p $gShelfTopLevel %s`;'%toolLabel)
        
    
        for menuDict in MENUDICTLIST:
            if os.path.isfile(BATCH_io_SCRIPTS + menuDict['script']):
                #===================================================================
                # Handle menu and shelf for Maya 2017
                #===================================================================
                if MAYA_VERSION != '2017':
                    #===============================================================
                    # Add a menu item
                    #===============================================================
                    cmds.menuItem(parent=parent_menu, 
                                  i=BATCH_io_IMAGES + menuDict['icon'], 
                                  l=menuDict['label'], 
                                  c=menuDict['command']) #MENU ENTRY
                    
                    #===============================================================
                    # Add a shef item
                    #===============================================================
                    cmds.shelfButton(menuDict['script'].replace('.py', ''), 
                                     annotation=menuDict['label'], 
                                     i=BATCH_io_IMAGES + menuDict['icon'], 
                                     c=menuDict['command'], 
                                     p=toolLabel) #SHELF BUTTON
                    
                #===================================================================
                # Other Maya versions
                #===================================================================
                else:
                    #===============================================================
                    # Add a menu item
                    #===============================================================
                    cmds.menuItem(parent=parent_menu, 
                                  i=menuDict['icon'], 
                                  l=menuDict['label'], 
                                  c=menuDict['command']) #MENU ENTRY
                    
                    #===============================================================
                    # Add a shef item
                    #===============================================================
                    cmds.shelfButton(menuDict['script'].replace('.py', ''), 
                                     annotation=menuDict['label'], 
                                     i=BATCH_io_IMAGES + menuDict['icon'], 
                                     c=menuDict['command'], 
                                     p=toolLabel) #SHELF BUTTON
                
                
                #===================================================================
                # Add the menu
                #===================================================================
                cmds.menuItem(parent=parent_menu, d=1)


#===============================================================================
# Setup load
#===============================================================================
def Batch_io_setup_Load():
    Batch_io_SetupMenu()
    print 'Batch_io: >>> Menu Entry and Shelf created!'


#===============================================================================
# Setup Unload
#===============================================================================
def Batch_io_setup_UnLoad():
    if cmds.menu('Batch_io_Menu', q=1, ex=1):
        cmds.deleteUI('Batch_io_Menu', menu=1)
        
    if cmds.shelfLayout("Batch_io", ex=1):
        cmds.deleteUI("Batch_io")
    
    print 'Batch_io: >>> Menu Entry and Shelf removed!'

