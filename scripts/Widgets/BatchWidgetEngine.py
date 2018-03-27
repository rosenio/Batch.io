#===============================================================================
# #Autor: Rosenio Pinto
# #e-mail: kenio3d@gmail.com
#
# #DON'T MODIFY THIS FILE! ANY CHANGE MAY OCCUR IN BROCKEN THINGS
#
#===============================================================================
#===============================================================================
# # The base class for widgets inheritance
# # It is the beautifull motor
#===============================================================================
from SystemConfig import *


class BatchWidgetEngine(object):
    '''Base Class for Batch Widgets scene iteration'''
    name        = "BachWidget"

    def __init__(self, scene_info):
        
        self.reference_type_level_on = False
        self.reference_level_on      = False
        self.progress                = 0
        
        self.scene_info              = scene_info
        self.custom_length           = False

        
    #===========================================================================
    # #The starter function
    #===========================================================================
    def onStart(self, scene_info):
        return self.run()

    #===========================================================================
    # #Declaration of scene level event function
    #===========================================================================
    def scene_level_event(self, scene_info=None):
        return scene_info
    
    #===========================================================================
    # #Declaration of reference level event function
    #===========================================================================
    def reference_type_level_event(self, reference_type):
        return reference_type

    #===========================================================================
    # #Declaration os reference level function
    #===========================================================================
    def reference_level_event(self, scene_info, reference_type, reference_name=None, isCamera=False):
        return reference


    #===========================================================================
    # #Main loop 
    #===========================================================================
    def run(self):
        #=======================================================================
        # #Firs log on the widget
        #=======================================================================
        print 'STATUS ' + self.name + '_' + self.scene_info.scene_short_name

        #===================================================================
        # #Scene Level Event
        #===================================================================
        print ">> %s << RUNNING on scene: %s"%(self.name, self.scene_info.scene_short_name)
        #Feed the SceneEvent and pass to scene_event_level function
        self.scene_level_event(self.scene_info)

        #===================================================================
        # #Reference Type Level Event
        #===================================================================
        if self.reference_type_level_on:
            for reference_type in self.scene_info.reference_list.keys():
                #===============================================================
                # LOG
                #===============================================================
                print ">> %s << RUNNING on reference type: %s"%(self.name, reference_type)
                
                self.reference_type_level_event(reference_type)
                
                #=======================================================================
                # #Increment the progress value
                #=======================================================================
                self.progress_increment()

        #===============================================================
        # #Reference Level Event
        #===============================================================
        if self.reference_level_on:
            for reference_type in self.scene_info.reference_list.keys():
                #=======================================================================
                # #Increment the progress value
                #=======================================================================
                self.progress_increment()
                
                for reference_name in self.scene_info.reference_list[reference_type]:
        
                    #===========================================================
                    # #LOG
                    #===========================================================
                    #===========================================================
                    # # By pass if the reference was not checked on batch ui
                    #===========================================================
                    if not self.scene_info.Get_Reference_Check_State(reference_type, reference_name):
                        print ">> %s << NOT RUNNING on reference : %s"%(self.name, reference_name)
                        #=======================================================================
                        # #Increment the progress value
                        #=======================================================================
                        self.progress_increment()
                        continue
                    
                    
                    print ">> %s << RUNNING  on reference : %s"%(self.name, reference_name)
                    self.reference_level_event(self.scene_info, reference_type, reference_name, (reference_type == 'camera'))
                    #=======================================================================
                    # #Increment the progress value
                    #=======================================================================
                    self.progress_increment()

        #=======================================================================
        # #Final level
        #=======================================================================
        self.onEnd(self.scene_info)



    def progress_increment(self):
        self.progress += 1
        print self.status()
        
    #===========================================================================
    # #Output all status progress    
    #===========================================================================
    def status(self):
        statusValue = 0
        
        if not self.scene_info.Get_Scene_Check_State():
            print 'STATUS '+'UNCHECKED'+'_'+self.scene_info.scene_short_name
        
            return 100
        
        #=======================================================================
        # #Get the length of processes
        #=======================================================================
        if self.reference_type_level_on:
            statusValue += len(self.scene_info.reference_list.keys())
        
        if self.reference_level_on:
            statusValue += len(self.scene_info.reference_list.keys()) 
            statusValue += sum(map(len, self.scene_info.reference_list.values()))
        
        if self.custom_length:
            statusValue =+ self.custom_length
        
        #=======================================================================
        # #Calculate the proportion of process status
        #=======================================================================
        progress = int((100.0/statusValue) * (self.progress))
        
        if progress >= 100:
            progress = 100
        

        #=======================================================================
        # #Report the progress message
        #=======================================================================
        print 'STATUS '+self.name+'_'+self.scene_info.scene_short_name
        
        
        return 'PROGRESS_'+str(progress)
    
    
    #===========================================================================
    # #Last function called
    #===========================================================================
    def onEnd(self, event):        
        return event






