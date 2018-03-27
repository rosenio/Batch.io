#===============================================================================
# #Autor:  Rosenio Pinto
# #e-mail: kenoi3d@gmail.com
#===============================================================================
import Singleton as Sing

class LOG(Sing.Singleton, object):
    _instance = None
    LOG       = {}

    def __init__(self):
        super(LOG, self).__init__()