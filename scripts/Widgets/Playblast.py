#===============================================================================
# #Autor: Rosenio Pinto
# #e-mail: kenio3d@gmail.com
# #
# #
#===============================================================================
from BatchWidgetEngine import *

WIDGET_NAME     = 'Playblast'
WIDGET_TYPE     = 'RENDER'
WIDGET_DESC     = 'Generate playblast from the animation scenes.'
WIDGET_SETTINGS = {'res_x': 1920, 'res_y':1080, 'custom_camera':'cam_render'}

class Playblast_widget(BatchWidgetEngine):
    name        = "Playblast"
    
    def __init__(self, scene_info):
        super(Playblast_widget, self).__init__(scene_info)
        
        self.reference_type_level_on = False
        self.reference_level_on      = True

        #=======================================================================
        # #Playblast variables
        #=======================================================================
        self.qimage                  = QImage(1, 1, QImage.Format_RGB32)
        self.image_size              = [WIDGET_SETTINGS['res_x'], WIDGET_SETTINGS['res_y']]
        self.image_prefix            = scene_info.scene_short_name+'/'+scene_info.scene_short_name
        self.camera_name             = scene_info.reference_list['camera'][0]
        
        #=======================================================================
        # #Get the custom camera variable if seted
        #=======================================================================
        if WIDGET_SETTINGS['custom_camera']:
            self.camera_name = WIDGET_SETTINGS['custom_camera']
                                        
        self.onStart(self.scene_info)
        
    #===========================================================================
    # #The starter function
    #===========================================================================
    def onStart(self, scene_info):
        #===================================================================
        # #On Start level event commands here
        #===================================================================
        
        #=======================================================================
        # #Set the custom length value to handle progress log
        #=======================================================================
        self.custom_length = float(scene_info.end_frame - scene_info.start_frame)+1
        
        
        #=======================================================================
        # #Set the render settings for playblast output
        #=======================================================================
        cmds.setAttr('defaultRenderGlobals.imageFormat',                32)
        cmds.setAttr('defaultRenderGlobals.startFrame',                 scene_info.start_frame)
        cmds.setAttr('defaultRenderGlobals.endFrame',                   scene_info.end_frame)
        
        cmds.setAttr('defaultRenderGlobals.animation',                  True)
        cmds.setAttr('defaultRenderGlobals.putFrameBeforeExt ',         True)
        cmds.setAttr('defaultRenderGlobals.useMayaFileName',            True)
        cmds.setAttr('defaultRenderGlobals.useFrameExt',                True)
        cmds.setAttr('defaultRenderGlobals.extensionPadding',           4)
        cmds.setAttr('defaultRenderGlobals.imageFilePrefix',            self.image_prefix, type='string')
        cmds.setAttr('defaultRenderGlobals.outFormatExt',              'png',              type='string')
        cmds.setAttr('defaultRenderGlobals.ren',                       'mayaHardware2',    type='string')

        cmds.setAttr("hardwareRenderingGlobals.lineAAEnable",           True)
        cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable",      True)
        cmds.setAttr('hardwareRenderingGlobals.floatingPointRTEnable',  True)
        cmds.setAttr("hardwareRenderingGlobals.gammaCorrectionEnable",  True)
        cmds.setAttr("hardwareRenderingGlobals.singleSidedLighting",    True)
        cmds.setAttr('hardwareRenderingGlobals.renderMode',             4)
        cmds.setAttr("hardwareRenderingGlobals.ssaoEnable",             1)
        cmds.setAttr("hardwareRenderingGlobals.multiSampleCount",       2)
        cmds.setAttr("hardwareRenderingGlobals.floatingPointRTFormat",  1)
        cmds.setAttr('hardwareRenderingGlobals.holdOutMode',            0)
        cmds.setAttr("hardwareRenderingGlobals.gammaValue",             2.2)
        
        cmds.setAttr('defaultResolution.width',                         self.image_size[0])
        cmds.setAttr('defaultResolution.height',                        self.image_size[1])
        
        #=======================================================================
        # #Aplly color correction
        #=======================================================================
        cmds.colorManagementPrefs(e=True, outputTransformEnabled=True)


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
        for i in range(int(scene_info.start_frame), int(scene_info.end_frame+1)):
            image_file = cmds.ogsRender(camera='%s:%s'% (self.camera_name, self.camera_name), frame=i, noRenderView=True, layer='defaultRenderLayer')
            
            QApplication.processEvents()
            self.insert_hud(image_file, 'Scene: %s\nFrame: %s\ncamera: %s'%(scene_info.scene_short_name, i, self.camera_name))
            #===================================================================
            # #Update the log and ui
            #===================================================================
            self.progress_increment()

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
        #print 'CODE HERE'
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
        #print 'CODE HERE'
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
        # 'CODE HERE'
        #===================================================================
        # #On end level event commands here
        #===================================================================
        
        return scene_info
    
    
    #===========================================================================
    # #Custom function to put the info on the images
    #===========================================================================
    def insert_hud(self, image_file, text=''):
        try:
            self.qimage.load(image_file)
            
            painter = QPainter(self.qimage)
            painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
            painter.setPen(QPen(Qt.white))
            painter.drawText(QRect(10, self.image_size[1]-(25*len(text.splitlines())), 200, 100), text)
           
            self.qimage.save(image_file, 'png', 70)
    
        except Exception, e:
            print e
            print 'Problems saving the file: %s'%image_file


    
    
#===============================================================================
# # The function the return that class from external tools
#===============================================================================
def main(sceneInfo):
    return Playblast_widget(sceneInfo)



