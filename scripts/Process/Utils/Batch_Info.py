#===============================================================================
# #Autor:  Rosenio Pinto
# #e-mail: kenoi3d@gmail.com
#===============================================================================
import Singleton as Sing

class Batch_Info(Sing.Singleton, object):
    _instance        = None
    Batch_Info = {}

    def __init__(self):
        super(Batch_Info, self).__init__()