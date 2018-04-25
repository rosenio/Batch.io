from SystemConfig import *

# from maya import cmds
import json
try:
    from pymel import core as pm
except Exception, e:
    pm = cmds
    print e
    print "Problems to import pymel"

# from pprint import pprint
# from datetime import datetime
# import os
# import ast

class ShaderPipeline(object):
    def __init__(self, characterName, characterType, projectPath):
        super(ShaderPipeline, self).__init__()

        self.characterName  = characterName
        self.characterType  = characterType
        self.shaderDict     = {}

        self.projectPath    = projectPath
        self.publishPath    = '{}cache/shader/{}/{}/'.format(self.projectPath,
                                                             self.characterType,
                                                             self.characterName)

        self.setMembers     = self.getSetMembers()

        self.actualDate     = datetime.datetime.now()
        self.date           = '{:0>2}_{:0>2}_{}'.format(self.actualDate.day, self.actualDate.month, self.actualDate.year)
        self.DictUUID       = {}
        self.allShaders     = []

    def getSetMembers(self):
        try:
            meshs = pm.sets('%s:mesh_set' % self.characterName , query=True)
        except:
            mesh = None
        return mesh

    def set_UUID_ShaderGroup_Variable(self, sg, shape, shapeUUID):

        if not self.DictUUID.has_key(sg):
            self.DictUUID[sg] = {shape:shapeUUID}
        else:
            self.DictUUID[sg].update({shape:shapeUUID})

    def jsonVersionCons(self):

        try:
            listFiles = [ jsonFiles for jsonFiles in os.listdir(self.publishPath) if jsonFiles.endswith('.json') ]
            num = []
            versionNumber = '{}{:0>3}'.format('SdrVer', 1)
            if listFiles:
                for f in listFiles:
                    v = f.split('_SdrVer')[-1]
                    v = int(v.split('.json')[0])
                    num.append(v)

                versionNumber = '{}{:0>3}'.format('SdrVer', max(num)+1)
            else:
                versionNumber = '{}{:0>3}'.format('SdrVer', 1)

            fileName = '%s_%s_%s.json' % (self.characterName, self.date, versionNumber )

            return fileName

        except WindowsError as winEr:
            print winEr
            print 'Make new dir...'
            print self.publishPath
            os.makedirs(self.publishPath)
            versionNumber = '{}{:0>3}'.format('SdrVer', 1)
            fileName = '%s_%s_%s.json' % (self.characterName, self.date, versionNumber )

            return fileName

    def DictUUIDConstruct(self):
        if self.DictUUID:
            jsonName = self.jsonVersionCons()
            jsonData = []
            for shaderGrp in self.DictUUID:
                with open(self.publishPath+jsonName, 'w') as jsonFile:
                    entry = {'shaderGroup': shaderGrp.split('.')[0], 'data': self.DictUUID[shaderGrp]}
                    jsonData.append(entry)
                    json.dump(jsonData, jsonFile, indent=4, sort_keys=True)

    def append_shaders(self, shd):
        if shd:
            for s in shd:
                self.allShaders.append(s)
        self.allShaders = list(set(self.allShaders))

    def setUUID(self):
        shaderGrpList = []
        for member in self.setMembers:
            fullPathName = pm.ls(member, long=True)[0]#member.fullPath()
            shape = pm.listRelatives(member, shapes=True, fullPath=True)[0]#.getShape()
            UUID = getShapeUUID(shape)
            connections = pm.listConnections(shape, plugs=True, destination=True, source=False)
            for conn in connections:
                UUIDlist = []
                nodeType = pm.nodeType(conn)
                if nodeType == 'shadingEngine':
                    shaderGrp = conn
                    # acrescenta ao discionario de UUID
                    self.set_UUID_ShaderGroup_Variable(shaderGrp, shape, UUID)
                    shaders = [ s for s in
                                pm.listConnections(shaderGrp, source=True, destination=False)
                                if pm.nodeType(s) !='transform'] # retorna os shaders atrelados ao shape
                    shapeUUID = getShapeUUID(shape) # UUID do shape
                    shaderGrpList.append(shaderGrp)
                    self.append_shaders(shaders)
                    self.append_shaders(getConns(shaders)) # retorna toda a hierarquia de shaders

        self.append_shaders(shaderGrpList)

    def fileVersionCons(self):
        try:
            listFiles = [ mayaFiles for mayaFiles in os.listdir(self.publishPath) if mayaFiles.endswith('.mb') ]
            num = []
            versionNumber = '{}{:0>3}'.format('SdrVer', 1)
            if listFiles:
                for f in listFiles:
                    v = f.split('_SdrVer')[-1]
                    v = int(v.split('.mb')[0])
                    num.append(v)

                versionNumber = '{}{:0>3}'.format('SdrVer', max(num)+1)
            else:
                versionNumber = '{}{:0>3}'.format('SdrVer', 1)

            fileName = '%s_%s_%s.mb' % (self.characterName, self.date, versionNumber )

            return fileName

        except WindowsError as winEr:
            print winEr
            print 'Make new dir...'
            print self.publishPath
            os.makedirs(self.publishPath)
            versionNumber = '{}{:0>3}'.format('SdrVer', 1)
            fileName = '%s_%s_%s.mb' % (self.characterName, self.date, versionNumber )

            return fileName

    def shaderImportApply(self, f, j):
        print 'applying shader to file: '+ f + 'using json file ' + j
        publishPath     =   self.publishPath
        #publishPath     =   'W:/JOBS/WORLD_ANIMAL_PROJETCTION_360/cache/shader/character/pig_baby'
        fullFilePath    =   publishPath+'/'+f
        fullJsonPath    =   publishPath+'/'+j

        jsonData        =   json.load(open(fullJsonPath))
        importPath      =   cmds.file(                        fullFilePath      ,
                                      i                   =   True              ,
                                      type                =   "mayaBinary"      ,
                                      rpr                 =   f.split('.mb')[0] ,
                                      pr                  =   False             ,
                                      loadReferenceDepth  =   'all'              )

        for item in range(len(jsonData)):
            d = jsonData[item]['data']
            s = jsonData[item]['shaderGroup']
            for dt in d:
                shapeuuid = d[dt]
                shapeFullPath = dt
                cmds.sets(cmds.ls(shapeuuid, uuid=True), edit=1, forceElement = s)

    def shaderPublish(self):
        # Query ShaderGroup and UUID
        self.setUUID()
        # Dictionary UUID and Setup
        self.DictUUIDConstruct()

        # File name Constructor
        exportFileName = self.fileVersionCons()

        # Export file
        print self.allShaders, "!!!!!!"
        if self.allShaders:
            pm.select(self.allShaders, replace=True, noExpand=True)
            pm.file(self.publishPath+'/'+exportFileName, type='mayaBinary', es=True)

    def versionVerify(self, fileType):

        if os.path.exists(self.publishPath):
            listFiles = [ files for files in os.listdir(self.publishPath) if files.endswith(fileType) ]
            num = []
            if listFiles:
                for f in listFiles:
                    fl, v = f.split('_SdrVer')
                    v = int(v.split(fileType)[0])
                    num.append(v)
                    m = max(num)
                    recentFile = '{}{}{:0>3}{}'.format(fl,'_SdrVer', m, fileType)

                return recentFile
            else:
                cmds.warning('File not finded')
                return

    def shaderImport(self):
        print 'Importing shaders...'

        mayaFile = self.versionVerify('.mb')
        jsonFile = self.versionVerify('.json')

        if mayaFile and jsonFile:
            self.shaderImportApply(mayaFile, jsonFile)
        else:
            cmds.warning('File not finded')
            return

    def shaderSceneVerify(self):

        jsonFile = self.publishPath+'/'+self.versionVerify('.json')

        if jsonFile:
            data = json.load(open(jsonFile))
            for item in range(len(data)):
                d = data[item]['data']
                s = data[item]['shaderGroup']
                if cmds.objExists(s):
                    shaderNodes = getConns(s)
                    cmds.delete(s, shaderNodes)


def getConns(node):
    # Query list connections
    conns = pm.listConnections(node, destination=False)
    if conns:
        conns = list(set(conns))
        for c in conns:
            newConns = getConns(c)
            if newConns:
                newConns = list(set(newConns))
                conns.extend(newConns)
    return conns

def getShapeUUID(shape):
    # Query shape UUID
    return cmds.ls(shape, uuid=True)[0]
