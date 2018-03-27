#===============================================================================
# #Autor:  Rosenio Pinto
# #e-mail: kenoi3d@gmail.com
#===============================================================================
from Scene_Info import *
import Singleton as Sing

class Pre_Batch_Scene_Info(Sing.Singleton, object):
    _instance      = None
    Pre_Batch_Info = {}

    def __init__(self):
        super(Pre_Batch_Scene_Info, self).__init__()


    #===========================================================================
    # #Put the scene info
    #===========================================================================
    def Set_Scene_Info(self, outputData={}, temp=False):
        scene_short_name = outputData['scene_short_name']
        scene_info       = Scene_Info(outputData['Scene_CheckState_Info'], 
                                      outputData['Reference_CheckState_Info'],
                                      outputData['Reference_Full_Path'],
                                      outputData['scene_short_name'], 
                                      outputData['scene_full_path'], 
                                      outputData['Project_Path'],
                                      outputData['reference_list'],
                                      outputData['start_frame'],
                                      outputData['end_frame']
                                      )
        
        if not temp:
            self.Pre_Batch_Info[scene_short_name] = scene_info
            
        return scene_info
        
    #===========================================================================
    # #Get the scene info
    #===========================================================================
    def Get_Scene_Info(self, scene_short_name):
        if scene_short_name in self.Pre_Batch_Info.keys():
            return self.Pre_Batch_Info[scene_short_name]


    #===========================================================================
    # #Get all scene_info
    #===========================================================================
    def All_Scene_Info(self):
        return self.Pre_Batch_Info.values()
    
    
    #===========================================================================
    # #Get all scene short name list
    #===========================================================================
    def Scene_List(self):
        return self.Pre_Batch_Info.keys()
    

    def Clear(self):
        self.Pre_Batch_Info.clear()
        
        
    def All_References(self):
        all_ref_list = []
        for scene_info in self.All_Scene_Info():
            for ref_list in scene_info.reference_list.values():
                all_ref_list += ref_list
        all_ref_list += self.All_TYPES()
            
        return all_ref_list
        
    def All_TYPES(self):
        all_ref_type_list = []
        for scene_info in self.All_Scene_Info():
            all_ref_type_list += scene_info.reference_list.keys()
            
        return list(set(all_ref_type_list))
        
        
        
           
        
    