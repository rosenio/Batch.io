#===============================================================================
# #Autor: Rosenio Pinto
# #e-mail: kenio3d@gmail.com
# #
# # This is the template for create custom batch widgets
# #
#===============================================================================
from BatchWidgetEngine import *


WIDGET_NAME     = 'Alembic Cache'
WIDGET_TYPE     = 'ANIM'
WIDGET_DESC     = 'Generate Alembic Cache for the references.'
WIDGET_SETTINGS = {'include_extra_global': True, 'mesh_group':'MESH', 'camera_name':CAMERA_NAME, 'id_attr_name':'id', 'use_mesh_group':False}

class AlembicCache_widget(BatchWidgetEngine):
    name        = "AlembicCache"

    def __init__(self, scene_info={}):
        super(AlembicCache_widget, self).__init__(scene_info)
        
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
        self.custom_length     = float(scene_info.end_frame - scene_info.start_frame)+1
        self.abc_commands      = []
        self.reference_list_db = {}
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
        # #Check if the extra cache global group and create the alembic command
        #=======================================================================
        if cmds.objExists('EXTRA_CACHE_GLOBAL') and WIDGET_SETTINGS['include_extra_global']:
            #===================================================================
            # #Feed the alembic information
            #===================================================================
            cache_folder = scene_info.project_path+"%s/%s/%S/EXTRA/"%(CACHE_FOLDER, scene_info.scene_short_name, REF_FOLDER)
            if not os.path.exists(cache_folder):
                os.makedirs(cache_folder)
                
            #===================================================================
            # #Add the scene extra cache command to the list
            #===================================================================
            abc_path    = cache_folder+'EXTRA_CACHE_GLOBAL'+'.abc'
            abc_command = self.Alembic_Command_Gen(root_name_list = ['EXTRA_CACHE_GLOBAL'], abc_path = cache_folder+'EXTRA_CACHE_GLOBAL'+'.abc')
            
            self.abc_commands.append(abc_command)
            #=======================================================================
            # #Data to put on DB
            #=======================================================================
            self.reference_list_db['EXTRA_CACHE_GLOBAL'] = {'root_name':'EXTRA_CACHE_GLOBAL', 'cache_path':abc_path, 'reference_type':'EXTRA'}
        
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

        root_name_list = []
        root_name      = '%s:%s'%(reference_name, WIDGET_SETTINGS['mesh_group'])
        extra_cache    = '%s:EXTRA_CACHE'%reference_name
        

        if isCamera:
            root_name  = '%s:%s'%(reference_name, WIDGET_SETTINGS['camera_name'])
            root_long_name = cmds.ls(root_name, long=True)[0]
            root_name_list.append(root_long_name)

        if cmds.objExists(extra_cache) and WIDGET_SETTINGS['include_extra_global']:
            extra_cache_long_name = cmds.ls(extra_cache, long=True)[0]
            root_name_list.append(extra_cache_long_name)

        #=======================================================================
        # #Chekck if the object to be cached exists
        #=======================================================================

        if WIDGET_SETTINGS['use_mesh_group'] and not isCamera:
            #===============================================================
            # Use MESH group
            #===============================================================
            root_long_name = cmds.ls(root_name, long=True)[0]
            root_name_list.append(root_long_name)
        
        else:

            #===============================================================
            # Use mesh set
            #===============================================================
            root_mesh_set  = '%s:mesh_set'%reference_name
            if cmds.objExists(root_mesh_set):
                root_name_list += cmds.sets(root_mesh_set, q=True)
        
        if root_name_list:
            #===================================================================
            # #Feed the alembic information
            #===================================================================
            cache_folder = scene_info.project_path+"%s/%s/%s/%s/"%(CACHE_FOLDER, scene_info.scene_short_name, REF_FOLDER, reference_type)
            if not os.path.exists(cache_folder):
                os.makedirs(cache_folder)
    
            #===================================================================
            # #Add the reference cache command to the list
            #===================================================================
            abc_path    = cache_folder+reference_name+'.abc'
            abc_command = self.Alembic_Command_Gen(root_name_list = root_name_list, abc_path = abc_path)
    
            self.abc_commands.append(abc_command)
    
            #=======================================================================
            # #Data to put on DB
            #=======================================================================
            self.reference_list_db[reference_name] = {'root_name':root_name, 'cache_path':abc_path, 'reference_type':reference_type}


    def Alembic_Command_Gen(self, root_name_list='', abc_path=''):
        #=======================================================================
        # #Alembic command params
        #=======================================================================

        root_attrs  = ' -root '.join(root_name_list)
        flags       = ' -writeVisibility -uvWrite -writeuvsets -worldSpace -writeColorSets -renderableOnly -eulerFilter -ro -dataFormat ogawa '
        attrs       = ' -a '.join([WIDGET_SETTINGS['id_attr_name'], 'castsShadows', 'receiveShadows', 'displayColorChannel', 'materialBlend'])
        
        #=======================================================================
        # #Return by frame cached command(updates the log an ui)
        #=======================================================================
        progress_factor = 100.0/(self.custom_length)
        frame_callback  = "print('PROGRESS_'+str(#FRAME#*%2f))"%float(progress_factor)

        #=======================================================================
        # #Alembic command for reference
        #=======================================================================
        abc_command =  ""
        abc_command += " -frameRange "             + str(self.scene_info.start_frame) + " " + str(self.scene_info.end_frame)
        abc_command += " -pythonPerFrameCallback " + frame_callback
        abc_command += flags
        abc_command += " -root " + root_attrs
        abc_command += " -a "    + attrs
        abc_command += " -file " + abc_path
        
        return abc_command
    
    
    #===========================================================================
    # #Last function called
    #===========================================================================
    def onEnd(self, scene_info): 

        #===================================================================
        # #On end level event commands here
        #===================================================================
        
        #=======================================================================
        # #Export all caches at once
        #=======================================================================
        cmds.AbcExport( j = self.abc_commands )

        try:
            assetData  = mongo_cache.Asset(scene_short_name=scene_info.scene_short_name, reference_list=self.reference_list_db, start_frame=scene_info.start_frame, end_frame=scene_info.end_frame)
            assetDB    = Set_DB()
            assetQuery = assetDB.query({'scene_short_name':scene_info.scene_short_name}).count()

            if assetQuery:
                assetData.updateAll()
            else:
                assetData.put()

        except Exception, e:
            print e

        #===================================================================
        # #On end level event commands here
        #===================================================================
        return scene_info




#===============================================================================
# # The function the return that class from external tools
#===============================================================================
def main(sceneInfo={}):
    return AlembicCache_widget(sceneInfo)





