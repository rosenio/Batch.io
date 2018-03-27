#===============================================================================
# Autor : Rosenio Pinto
# e-mail: kenio3d@gmail.com
#===============================================================================

class Scene_Info(object):
    def __init__(self, scene_check_state     = {}, 
                        reference_check_state = {},
                        reference_full_path   = {},
                        scene_short_name      = '', 
                        scene_full_path       = '',
                        project_path          = '', 
                        reference_list        = {},
                        start_frame           = 0,
                        end_frame             = 1):
        
        object.__init__(scene_check_state, 
                        reference_check_state, 
                        reference_full_path,
                        scene_short_name, 
                        scene_full_path,
                        project_path, 
                        reference_list,
                        start_frame,
                        end_frame)
        
        #=======================================================================
        # Class parameters
        #=======================================================================
        self.scene_check_state      = scene_check_state
        self.reference_check_state  = reference_check_state
        self.reference_full_path    = reference_full_path 
        self.scene_short_name       = scene_short_name
        self.scene_full_path        = scene_full_path
        self.project_path           = project_path 
        self.reference_list         = reference_list
        self.start_frame            = start_frame
        self.end_frame              = end_frame
        
    
    #===========================================================================
    # Set the scene check state
    #===========================================================================
    def Set_Scene_Check_State(self, value):
        self.scene_check_state[self.scene_short_name] = value
        self.Set_All_Reference_Check_State(value)
    
    #===========================================================================
    # Set the reference check state
    #===========================================================================
    def Set_Reference_Check_State(self, reference_type, reference_name, value):
        self.reference_check_state[reference_type][reference_name] = value
        
    #===========================================================================
    # Get the scene check state
    #===========================================================================
    def Get_Scene_Check_State(self):
        return self.scene_check_state[self.scene_short_name]
    
    #===========================================================================
    # Get the reference check state
    #===========================================================================
    def Get_Reference_Check_State(self, reference_type, reference_name):
        return self.reference_check_state[reference_type][reference_name]
    
    #===========================================================================
    # Set all the scene check state
    #===========================================================================
    def Set_All_Reference_Check_State(self, value):
        for reference_type, reference_list in self.reference_list.iteritems():
            for reference_name in reference_list:
                self.Set_Reference_Check_State(reference_type, reference_name, value)
                
    #===========================================================================
    # Return all data as dict format
    #===========================================================================
    def As_Dict(self):
        return {
                'Scene_CheckState_Info'     :self.scene_check_state,
                'Reference_CheckState_Info' :self.reference_check_state,
                'Reference_Full_Path'       :self.reference_full_path,
                'reference_list'            :self.reference_list,
                'scene_short_name'          :self.scene_short_name,
                'scene_full_path'           :self.scene_full_path,
                'Project_Path'              :self.project_path,
                'start_frame'               :self.start_frame,
                'end_frame'                 :self.end_frame
                }
    
                
                
                
                