#===============================================================================
# #Autor:  Rosenio Pinto
# #e-mail: kenoi3d@gmail.com
#===============================================================================
import Singleton as Sing

class Pre_Batch_Thread_Info(Sing.Singleton, object):
    _instance             = None
    Pre_Batch_Thread_Info = {}

    def __init__(self):
        super(Pre_Batch_Thread_Info, self).__init__()