#===============================================================================
# #Autor: Rosenio Pinto
# #e-mail: kenio3d@gmail.com
# #
# # This is the template for create custom batch widgets
# #
#===============================================================================
from BatchWidgetEngine import *

WIDGET_NAME     = 'Shader Export'
WIDGET_TYPE     = 'LOOKDEV'
WIDGET_DESC     = 'Export published shaders for the references.'
WIDGET_SETTINGS = {}

#===============================================================================
# #Shader Pipeline
#===============================================================================
from Tools.ShaderPipeline import *

class ShaderExport_widget(BatchWidgetEngine):
    name        = "ShaderExport"
    
    def __init__(self, scene_info):
        super(ShaderExport_widget, self).__init__(scene_info)
        
        self.reference_type_level_on = False
        self.reference_level_on      = True

        self.CurrentProject = Get_Project()
        
        self.onStart(self.scene_info)
        
    #===========================================================================
    # #The starter function
    #===========================================================================
    def onStart(self, scene_info):
        return self.run()
    
    #===========================================================================
    # #Run on the scene
    #===========================================================================
    def scene_level_event(self, scene_info):
        '''Scene level event'''

        #===================================================================
        # #Scene level event commands here
        #===================================================================
        
        print 'CODE HERE'
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
        print 'CODE HERE'
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
        print 'CODE HERE'

        #=======================================================================
        # #Handle if reference is of type CAMERA
        #=======================================================================
        if not isCamera:
            print 'Camera name: %s'%reference_name
            shaderPipelineClass = ShaderPipeline.ShaderPipeline(characterName   =   reference_name, 
                                                                characterType   =   reference_type, 
                                                                projectPath     =   self.CurrentProject)
            shaderPipelineClass.shaderPublish()
            self.progress_increment()
            
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
        # 'CODE HERE'
        #===================================================================
        # #On end level event commands here
        #===================================================================
        
        return scene_info
    
    
    
#===============================================================================
# # The function the return that class from external tools
#===============================================================================
def main(sceneInfo):
    return ShaderExport_widget(sceneInfo)



