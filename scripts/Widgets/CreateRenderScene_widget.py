#===============================================================================
# #Autor: Rosenio Pinto
# #e-mail: kenio3d@gmail.com
# #
# # This is the template for create custom batch widgets
# #
#===============================================================================
from BatchWidgetEngine import *

WIDGET_NAME     = 'Create Render Scene'
WIDGET_TYPE     = 'RENDER'
WIDGET_DESC     = 'Create a render scene based on published caches.\nCaches must be published.'
WIDGET_SETTINGS = {'merge':True, 'include_extra_global':True, 'include_yeti':True, 'offset':True}

class CreateRenderScene_widget(BatchWidgetEngine):
    name        = "CreateRenderScene"
    
    def __init__(self, scene_info={}):
        super(CreateRenderScene_widget, self).__init__(scene_info)
        
        self.reference_type_level_on = False
        self.reference_level_on      = True
        
        self.onStart(scene_info)
        
    #===========================================================================
    # #The starter function
    #===========================================================================
    def onStart(self, scene_info):
        #===================================================================
        # #On Start level event commands here
        #===================================================================
        
        #=======================================================================
        # #File new and load the alembic plugin
        #=======================================================================
        if not WIDGET_SETTINGS['merge']:
            cmds.file(new=True, f=True)
        else:
            if cmds.file(scene_info.scene_full_path.replace('animation', 'render'), ex=True, q=True):
                cmds.file(scene_info.scene_full_path.replace('animation', 'render'), o=True, f=True)
            else:
                cmds.file(new=True, f=True)
                cmds.file(rename=scene_info.scene_full_path.replace('animation', 'render'))
            

        #=======================================================================
        # #Initialize the DB to get the data relative to this scene
        #=======================================================================
        Asset_DB                = Set_DB()
        self.Asset_DB_Query     = Asset_DB.query({'scene_short_name': scene_info.scene_short_name})
        self.reference_list_db  = self.Asset_DB_Query['reference_list']

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
        # #Reference the alembic file relative to this reference
        #=======================================================================
        if WIDGET_SETTINGS['include_extra_global']:
            if 'EXTRA_CACHE_GLOBAL' in self.reference_list_db.keys():
                self.ReferenceAlembic(cache_path = self.reference_list_db['EXTRA_CACHE_GLOBAL']['cache_path'])
        
        
        #=======================================================================
        # Reference Yeti Scene
        #=======================================================================
        if WIDGET_SETTINGS['include_yeti']:
            yeti_scene_path = scene_info.project_path+'cache/fur/%s/%s_yeti_cache.ma'%(scene_info.scene_short_name, scene_info.scene_short_name)
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
         
        #=======================================================================
        # #Reference the alembic file relative to this reference
        #=======================================================================
        self.ReferenceAlembic(cache_path = self.reference_list_db[reference_name]['cache_path'], namespace = reference_name)

        if isCamera:
            #===================================================================
            # #Lock camera
            #===================================================================
            cmds.camera('%s:%s'%(reference_name, CAMERA_NAME), edit=True, lockTransform=True)
        
        if not cmds.objExists(self.reference_list_db[reference_name]['root_name']):
            alembicNode = cmds.ls('%s:*'%reference_name, type='AlembicNode')

            if alembicNode:
                rootNodes   = cmds.listConnections(alembicNode)
            else:
                rootNodes = cmds.ls('%s:*'%reference_name, type='transform')
            try:
                cmds.group(rootNodes, n='%s_MESH'%reference_name)
            except:
                pass
        #=======================================================================
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
        
        if WIDGET_SETTINGS['offset']:
            self.SetOffset()
        else:
            #=======================================================================
            # #Set the time slider of the scene
            #=======================================================================
            start_frame = self.Asset_DB_Query['start_frame']
            end_frame   = self.Asset_DB_Query['end_frame']
            
            self.SetTimeSlider(start_frame, end_frame)


        #=======================================================================
        # #Save the file
        #=======================================================================
        if not WIDGET_SETTINGS['merge']:
            cmds.file(rename=scene_info.scene_full_path.replace('animation', 'render'))
            
        
        cmds.file(save=True, f=True)
        
        #===================================================================
        # #On end level event commands here
        #===================================================================
        return scene_info
        

    
    #===========================================================================
    # #This is an extra funcions on the batch widget
    #===========================================================================
    def ReferenceAlembic(self, cache_path='', namespace=''):
        #=======================================================================
        # #Reference the alembic file
        #=======================================================================

        if not WIDGET_SETTINGS['merge']:
            cache_path = cmds.file(cache_path, reference=True, mergeNamespacesOnClash=False, namespace=namespace)
        else:
            if not cache_path in cmds.file(q=True, l=True):
                cache_path = cmds.file(cache_path, reference=True, mergeNamespacesOnClash=False, namespace=namespace)
                
        #=======================================================================
        # #Set reference relative path
        #=======================================================================
        uName   = cache_path.split(Get_Project())[-1]
        refNode = cmds.referenceQuery(cache_path, referenceNode=True)
        
        cmds.file(uName, loadReference=refNode)
        
        
        
    def ReferenceYeti(self, yeti_scene_path='', namespace=''):
        #=======================================================================
        # #Reference the Yeti file
        #=======================================================================

        if not WIDGET_SETTINGS['merge']:
            cmds.file(yeti_scene_path, reference=True, mergeNamespacesOnClash=False, namespace=namespace)
        else:
            if not yeti_scene_path in cmds.file(q=True, l=True):
                cmds.file(yeti_scene_path, reference=True, mergeNamespacesOnClash=False, namespace=namespace)
                
        #=======================================================================
        # #Set reference relative path
        #=======================================================================
        uName   = 'cache/'+yeti_scene_path.split('cache/')[-1]
        refNode = cmds.referenceQuery(yeti_scene_path, referenceNode=True)
        
        cmds.file(uName, loadReference=refNode)


    #===========================================================================
    # #Set Offset
    #===========================================================================
    def SetOffset(self):
        alembic_nodes = cmds.ls(type='AlembicNode')
        
        for alembic_node in alembic_nodes:
            start_frame = cmds.getAttr(alembic_node+'.startFrame')
            end_frame   = cmds.getAttr(alembic_node+'.endFrame')
            
            offset      = (end_frame - start_frame)+1
            
            cmds.setAttr(alembic_node+'.offset', -(start_frame-1))
        
        if not alembic_nodes:
            offset = (self.scene_info.end_frame -self.scene_info.start_frame)+1
            
        self.SetTimeSlider(1, offset)


    #===========================================================================
    # Set the scene timeslider
    #===========================================================================
    def SetTimeSlider(self, start_frame=0, end_frame=10):
        cmds.playbackOptions(min=start_frame, max=end_frame)
        cmds.playbackOptions(ast=start_frame, aet=end_frame)
        

#===============================================================================
# # The function the return that class from external tools
#===============================================================================
def main(sceneInfo={}):
    return CreateRenderScene_widget(sceneInfo)



