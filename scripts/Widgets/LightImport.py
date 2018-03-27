#===============================================================================
# #Autor: Rosenio Pinto
# #e-mail: kenio3d@gmail.com
# #
# # This is a batch widget example used for tutorial purpose
# #
#===============================================================================
from BatchWidgetEngine import *

WIDGET_NAME     = 'Light Import'
WIDGET_TYPE     = 'RENDER'
WIDGET_DESC     = 'Import the lights on the scene.'
WIDGET_SETTINGS = {'custom_list':[], 'custom_vale':''}

class LightImport_widget(BatchWidgetEngine):
    name        = "LightImport"
    
    def __init__(self, scene_info={}):
        super(LightImport_widget, self).__init__(scene_info)
        
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
        
        #=======================================================================
        # #Reference the light
        #=======================================================================
        cmds.file('scenes/%s/LOOKDEV/light_SHOT.mb'%REF_FOLDER, reference=True, namespace='')
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
        # #Parent a character light to the null on the extra cache global group
        #=======================================================================
        if cmds.objExists('EXTRA_CACHE_GLOBAL:NULL_loc'):
            char_light = cmds.duplicate('*:character_light')[0]
            cmds.parentConstraint('EXTRA_CACHE_GLOBAL:NULL_loc', char_light)
            cmds.setAttr(char_light+'.color', 0.0, 0.1, 0.7, type='double3')
            cmds.setAttr(char_light+'.intensity', 100)
            cmds.setAttr(char_light+'.visibility', True)
            
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
        
        #=======================================================================
        # #Handle if reference is of type CAMERA
        #=======================================================================
        if isCamera:
            print 'Camera name: %s'%reference_name
        

        #=======================================================================
        # #Parent constrain the light if the refs are the custom_list
        #=======================================================================
        if reference_name in WIDGET_SETTINGS['custom_list']:
            char_light = cmds.duplicate('*:character_light')[0]
            cmds.parentConstraint(reference_name+':move_all_loc', char_light)
            cmds.setAttr(char_light+'.visibility', True)
        
        #=======================================================================
        # #Parent the point light to the prop sphere
        #=======================================================================
        if WIDGET_SETTINGS['custom_value']:
            if (reference_type == 'PROP') and (reference_name == WIDGET_SETTINGS['custom_value']):
                cmds.parentConstraint(reference_name+':move_all_loc', '*:point_light')

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
        # #Save the scene
        #=======================================================================
        cmds.file(save=True, f=True)
        

        #===================================================================
        # #On end level event commands here
        #===================================================================
        return scene_info
        
    
    
    
#===============================================================================
# # The function that returns the class from external tools
#===============================================================================
def main(sceneInfo={}):
    return LightImport_widget(sceneInfo)



