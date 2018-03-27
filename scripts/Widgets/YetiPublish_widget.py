#===============================================================================
# #Autor: Rosenio Pinto
# #e-mail: kenio3d@gmail.com
# #
# # This is the template for create custom batch widgets
# #
#===============================================================================
from BatchWidgetEngine import *

WIDGET_NAME     = 'Yeti Publish'
WIDGET_TYPE     = 'GROOM'
WIDGET_DESC     = 'Publish Yeti to be imported.'
WIDGET_SETTINGS = {}

#===============================================================================
# #Yeti Pipeline
#===============================================================================
from Tools.YetiPipeline import *

class YetiPublish_widget(BatchWidgetEngine):
    name        = "YetiPublish"

    def __init__(self, scene_info={}):
        super(YetiPublish_widget, self).__init__(scene_info)
        
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
        self.YetiPipelineInst = YetiPipeline.YetiPipeline()

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
        #=======================================================================
        # #Import published Yeti
        #=======================================================================
        self.YetiPipelineInst.RenameAllGrooms(reference_name)
        self.YetiPipelineInst.RenameAllFaceSets(reference_name)
        self.YetiPipelineInst.RenameAllYetiNodes(reference_name)
        self.YetiPipelineInst.RenameAllYetiFeatherNodes(reference_name)
        
        self.YetiPipelineInst.YetiPublish(reference_name)
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
        # #Save scene
        #=======================================================================
        cmds.file(save=True, f=True)
        
        #===================================================================
        # #On end level event commands here
        #===================================================================
        
        return scene_info
    
    

#===============================================================================
# # The function the return that class from external tools
#===============================================================================
def main(sceneInfo={}):
    return YetiPublish_widget(sceneInfo)



