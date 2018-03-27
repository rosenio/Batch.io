#===============================================================================
# #Autor: Rosenio Pinto
# #e-mail: kenio3d@gmail.com
# #
# # This is the template for create custom batch widgets
# #
#===============================================================================
from BatchWidgetEngine import *

WIDGET_NAME     = 'WIDGET NAME'
WIDGET_TYPE     = 'WIDGET_TYPE'
WIDGET_DESC     = 'WIDGET DESCRIPTION.'
WIDGET_SETTINGS = {}

class WidgetName_widget(BatchWidgetEngine):
    name        = "WidgetName"
    
    def __init__(self, scene_info={}):
        super(WidgetName_widget, self).__init__(scene_info)
        
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
        # 'CODE HERE'
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
        # 'CODE HERE'
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
        # 'CODE HERE'
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
# # The function that returns the class from external tools
#===============================================================================
def main(sceneInfo={}):
    return WidgetName_widget(sceneInfo)



