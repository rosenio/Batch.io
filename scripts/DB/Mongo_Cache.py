import os
import json
import tinymongo as tm

reload(tm)


class Mongo_Cache():
    def __init__(self, type, scene_short_name, reference_list, start_frame, end_frame):
        self.type              = type
        self.scene_short_name  = scene_short_name
        self.reference_list    = reference_list
        self.start_frame       = start_frame 
        self.end_frame         = end_frame
        
        DBPATH                 = Get_Current_DB_Path()['DBPATH']
        
        
        self.db = tm.TinyMongoDatabase(self.type, DBPATH, tm.TinyDB.DEFAULT_STORAGE)
        
        self.id = self.get_id()
    
    def get_id(self):
        query = self.db[self.type].find({'scene_short_name':self.scene_short_name})
        id = None
        if query:
            for item in query:
                id = item['_id']
        return id

    def get_by_id(self, id):
        result = self.db[self.type].find({'_id':id})
        return result

    def put(self):
        self.id = self.db[self.type].insert({'scene_short_name':self.scene_short_name, 
                                             'reference_list':self.reference_list, 
                                             'start_frame':self.start_frame, 
                                             'end_frame':self.end_frame}).inserted_id
        
    def update(self, id='', entry='', value=''):
        self.db[self.type].update({'_id':id}, {'$set':{entry:value}})

    def updateAll(self):
        self.db[self.type].update({'_id':self.id}, {'$set':{'scene_short_name':self.scene_short_name}})
        self.db[self.type].update({'_id':self.id}, {'$set':{'reference_list':self.get_reference_list()}})
        self.db[self.type].update({'_id':self.id}, {'$set':{'start_frame':self.start_frame}})
        self.db[self.type].update({'_id':self.id}, {'$set':{'end_frame':self.end_frame}})

    #Because the reference_list is a dictionary, we need to update him, end not replace
    def get_reference_list(self):
        query = self.db[self.type].find({'_id':self.id})

        if query:
            for item in query:
                reference_list = item['reference_list']
                if reference_list:
                    self.reference_list.update(reference_list)

        return self.reference_list


    def cleanAll(self, id=None):
        if id:
            self.db[self.type].remove({'_id':id})
        else:
            self.db[self.type].remove({})

    def query(self, itemToFind=None):
        if not itemToFind:
            return self.db[self.type].find()
        else:
            return self.db[self.type].find(filter=itemToFind)


class Asset(Mongo_Cache):
    def __init__(self, scene_short_name='', reference_list='', start_frame=0, end_frame=10):
        Mongo_Cache.__init__(self, 'asset', scene_short_name, reference_list, start_frame, end_frame)


def Save_Current_DB_Path(DBPATH='', PROJECTPATH=''):
    with open('c:/temp/db_path.json', 'w') as db_path:
        paths = {'DBPATH':DBPATH, 'PROJECTPATH':PROJECTPATH}
        json.dump(paths, db_path)
        
    return paths
    
def Get_Current_DB_Path():    
    if os.path.isfile('c:/temp/db_path.json'):
        with open('c:/temp/db_path.json') as db_path:
            data = json.load(db_path)

            return data
    else:
        return None
    
    
    
    
    
    
    
    
    