#===============================================================================
# #Autor: Rosenio Pinto
# #e-mail: kenio3d@gmail.com
# #
# # This is the template for create custom batch widgets
# #
#===============================================================================
from BatchWidgetEngine import *

WIDGET_NAME     = 'Yeti Cache Import'
WIDGET_TYPE     = 'RENDER'
WIDGET_DESC     = 'Reference the yeti cache scene.'
WIDGET_SETTINGS = {}

#===============================================================================
# #Yeti Pipeline
#===============================================================================
from Tools.YetiPipeline import *

class YetiCacheImport_widget(BatchWidgetEngine):
    name        = "YetiCacheImport"

    def __init__(self, scene_info={}):
        super(YetiCacheImport_widget, self).__init__(scene_info)
        
        self.reference_type_level_on = False
        self.reference_level_on      = True
        
        self.onStart(self.scene_info)
        
    #===========================================================================
    # #The starter function
    #===========================================================================
    def onStart(self, scene_info):

        #===================================================================
        # #On Start level event commands here
        #===================================================================
        # 'CODE HERE'
        #===================================================================
        # #On Start level event commands here
        #===================================================================
        
        return self.run()
    
    #===========================================================================
    # #Run on the scene
    #===========================================================================
    def scene_level_event(self, scene_info):
        '''Scene level event'''

        #===================================================================
        # #Scene level event commands here
        #===================================================================

        #=======================================================================
        # Reference Yeti Scene
        #=======================================================================
        yeti_scene_path = scene_info.project_path+'%s/%s/%s_yeti_cache.ma'%(GROOM_PATH, scene_info.scene_short_name, scene_info.scene_short_name)
        if cmds.file(yeti_scene_path, exists=True, q=True):
            self.ReferenceYeti(yeti_scene_path)

        #===================================================================
        # #Scene level event commands here
        #===================================================================

    #===========================================================================
    # #Run for each reference type
    #===========================================================================
    def reference_type_level_event(self, reference_type):
        '''Reference type event'''
        
        #===================================================================
        # #Reference type level event commands here
        #===================================================================
        #=======================================================================
        # print 'CODE HERE'
        #=======================================================================
        #===================================================================
        # #Reference type level event commands here
        #===================================================================

    #===========================================================================
    # #Run for each reference
    #===========================================================================
    def reference_level_event(self, scene_info, reference_type, reference_name, isCamera):
        '''Reference level event'''
        
        #===================================================================
        # #Reference level event commands here
        #===================================================================
        #=======================================================================
        # print 'CODE HERE'
        #=======================================================================
        #=======================================================================
        # #Handle if reference is of type CAMERA
        #=======================================================================
        if isCamera:
            print 'Camera name: %s'%reference_name
        
        #===================================================================
        # #Reference level event commands here
        #===================================================================

    #===========================================================================
    # #Last function called
    #===========================================================================
    def onEnd(self, scene_info):

        #===================================================================
        # #On end level event commands here
        #===================================================================
        #=======================================================================
        # #Save the file
        #=======================================================================
        cmds.file(save=True, f=True)
        #===================================================================
        # #On end level event commands here
        #===================================================================
        
        return scene_info


    #===========================================================================
    # #This is an extra funcions on the batch widget
    #===========================================================================
    def ReferenceYeti(self, yeti_scene_path='', namespace=''):
        #=======================================================================
        # #Reference the Yeti file
        #=======================================================================

        if not yeti_scene_path in cmds.file(q=True, l=True):
            cmds.file(yeti_scene_path, reference=True, mergeNamespacesOnClash=False, namespace=namespace)
                
        #=======================================================================
        # #Set reference relative path
        #=======================================================================
        uName   = 'cache/'+yeti_scene_path.split('cache/')[-1]
        refNode = cmds.referenceQuery(yeti_scene_path, referenceNode=True)
        
        cmds.file(uName, loadReference=refNode)
        
#===============================================================================
# # The function the return that class from external tools
#===============================================================================
def main(sceneInfo={}):
    return YetiCacheImport_widget(sceneInfo)



