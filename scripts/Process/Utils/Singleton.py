#===============================================================================
# #Autor:  Rosenio Pinto
# #e-mail: kenio3d@gmail.com
#===============================================================================
#===============================================================================
# #Ensure singleton pattern
#===============================================================================
class Singleton(object):
    @staticmethod
    def globalInstance(the_class):
        #=======================================================================
        # """ Static access method. """
        #=======================================================================
        if the_class._instance == None:
            the_class._instance = the_class()

        return the_class._instance 
    
    def __init__(self, *args, **kwargs):
        super(Singleton, self).__init__(*args, **kwargs)       
        #=======================================================================
        # """ Virtually private constructor. """
        #=======================================================================
        if self._instance != None:
            self.globalInstance()
        else:
            self._instance = self