from SystemConfig import *


class YetiPipeline(object):
    def __init__(self, displayYeti=False):
        super(YetiPipeline, self).__init__()

        self.displayYeti        = displayYeti
        self.cache_selected     = False

        self.toggleYetiDisplay  = False
        self.toggleGroomDisplay = True
        
        self.characterName = 'Character Name'
        self.groomDict     = {}
        
        self.GetCharacterSelection = True
        
        self.publishPath = cmds.workspace( q=True, rd=True )+'cache/groom/'
        
        loadYetiPlugin()
    #===========================================================================
    # #Publish Yeti
    #===========================================================================
    def YetiPublishCall(self):
        self.YetiPublish(self.characterName, self.getUUIDCB.isChecked())
        print "Publishing Yeti"
    
    
    #===========================================================================
    # #Browse the folder with json and groom files
    #===========================================================================
    def BrowseAndSet(self, folderPath = None):
        if not folderPath:
            folderPath = self.Browse()
        if folderPath:
            self.folderPath = folderPath
            os.chdir(self.folderPath)


    #===========================================================================
    # #Simple browse folder
    #===========================================================================
    def Browse(self):
        return QFileDialog.getExistingDirectory().replace("\\", "/")
    
    #===========================================================================
    # #Call all main functions as pass the yeti data
    #===========================================================================
    def ImportYetiMain(self):
        self.importedGrooms          = []
        self.importedFeatherFileList = []
        for yetiDataFilePath in glob.glob("*.json"):
            with open(yetiDataFilePath) as data_file:    
                self.yetiData = json.load(data_file)

            self.getUUID                 = self.yetiData['getUUID']

            self.HandleSets(self.yetiData)
            self.HandleFeathers(self.yetiData)
            self.HandleGrooms(self.yetiData, yetiDataFilePath)


    def ImportAllYeti(self):
        dirList           = os.listdir(self.publishPath)
        importAllJsonDict = {}
        

        for charFolder in dirList:
            os.chdir(self.publishPath+'/'+charFolder)
            if charFolder in importAllJsonDict.keys():
                pass
            else:
                for yetiDataFilePath in glob.glob("*.json"):
                    with open(yetiDataFilePath) as data_file:    
                        yetiData     = json.load(data_file)
                        inputGeoList = yetiData['inputGeo']['inputGeoList']
                        getUUID      = yetiData['getUUID']
                        
                        for inputGeo in inputGeoList:
                            characterRefs = None
                            faceSetDict  = inputGeo['faceSetDict']
                            objectName   = inputGeo['object']
                            objectId     = inputGeo['objectId']
    
                            #Check for characters in the scene
                            
                            characterRefs = self.GetCharacterRefs(objectId, getUUID)
    
                    if characterRefs and not charFolder in importAllJsonDict.keys():
                        importAllJsonDict[charFolder] = self.publishPath+'/'+charFolder

                        print '### Searching for characters: %s was found in the scene!'%charFolder.upper()


            
        for charName in importAllJsonDict.keys():
            os.chdir(importAllJsonDict[charName])
            self.characterName = charName
            self.ImportYetiMain()


    def GetCharacterRefs(self, objectId=None, getUUID=False, uuid_from_db=False):
        
        #Get all objects with the main ID
        if getUUID:
            characterRefs = cmds.ls(objectId)
            
        else:
            characterRefs = cmds.ls('*.id', r=True)
            characterRefs = sorted(list(set([obj.replace('.id', '') for obj in characterRefs if (cmds.objectType(obj) == 'mesh') and (cmds.getAttr(obj) == objectId)])))
        
        return characterRefs


    #===============================================================================
    # #Handle Selection Sets
    #===============================================================================
    def HandleSets(self, yetiData={}):
        print 'Handling Face Sets!'
        
        inputGeoList = yetiData['inputGeo']['inputGeoList']
        getUUID      = yetiData['getUUID']
        for inputGeo in inputGeoList:
            faceSetDict  = inputGeo['faceSetDict']
            objectName   = inputGeo['object']
            objectId     = inputGeo['objectId']

            characterRefs = self.GetCharacterRefs(objectId, getUUID)

            if faceSetDict:
                for faceSet in faceSetDict.keys():
                    newFaceList = []
                    if not cmds.objExists(faceSet):
                        for faceList in faceSetDict[faceSet]:
                            for characterRef in characterRefs:
                                    newFaceList.append(characterRef+faceList)

                        newSet = cmds.sets(newFaceList, n=faceSet)
                        print newSet
                        cmds.addAttr(newSet, ln='yeti_im_set', dt='string')


    #===========================================================================
    # #Handle feather files
    #===========================================================================
    def HandleFeathers(self, yetiData={}):
        print 'Handling Feathers!'

        #Check if this node has feathers objects
        self.hasFeather  = yetiData['hasFeather']

        if self.hasFeather:
            featherObject = yetiData['featherObject'][0]
            
            for inputGeo in yetiData['inputGeo']['inputGeoList']:
                feathersFile = yetiData['inputGeo']['feathers']
                
                #Import feather file
                if feathersFile and not (featherObject.split('|')[-1] in self.importedFeatherFileList):
                    if os.path.exists(feathersFile):
                        cmds.file(feathersFile, i=True)
                        self.importedFeatherFileList.append(featherObject.split('|')[-1])
                
                    if cmds.objExists(featherObject):
                        cmds.addAttr(featherObject, ln='yeti_im_feather', dt='string')


    #===========================================================================
    # #Handle Grooms
    #===========================================================================
    def HandleGrooms(self, yetiData={}, yetiDataFilePath=''):
        print 'Handling Grooms!'
        
        yetiOutputPath      = yetiData['yetiOutputPath']
        yetiNodeName        = yetiData['yetiNode']
        grooms              = yetiData['grooms']
        getUUID             = yetiData['getUUID']

        self.yetiNodeList = []

        inputGeoList = yetiData['inputGeo']['inputGeoList']
        length       = len(yetiData['inputGeo']['inputGeoList'])+1

        yetiNodeNamespaceList = []
        #Create yeti nodes
        #Create and connect grooms
        #Connect feathers
        for inputGeo in yetiData['inputGeo']['inputGeoList']:
            objectId       = inputGeo['objectId']
            objectName     = inputGeo['object']
            isFeather      = inputGeo['isFeather']

            characterRefs = self.GetCharacterRefs(objectId, getUUID)
            #Iterate through all references based on your ID
            yetiNodeShape = None
            if characterRefs:
                for characterRef in characterRefs:
                    groomFile     = yetiDataFilePath.replace('.json', '.grm')
                    namespaceName = characterRef.rsplit(':', 1)[0]
                    
                    yetiNodeNamespaceList.append(namespaceName)
                    
                    if not cmds.objExists(namespaceName+"_"+yetiNodeName):
                        #Create a new yetiNode
                        newNodeShape = mel.eval('pgYetiCreate();')
                        
                        #Get the transform of yeti node
                        yetiNode     = cmds.listRelatives(newNodeShape, parent=True)[0]
                    
                        #Check if there is a namespace
                        if ':' in characterRef:
                            yetiNode = cmds.rename(yetiNode, namespaceName+"_"+yetiNodeName)
                        else:
                            yetiNode = cmds.rename(yetiNode, namespaceName+"_"+yetiNodeName)
    
                        #Get the shape of yeti node
                        yetiNodeShape = cmds.listRelatives(yetiNode, shapes=True)[0]


                        if not self.displayYeti:
                            cmds.setAttr(yetiNodeShape + '.displayOutput', 0)
                        
                        #Set the groom path on the new yetiNode
                        cmds.setAttr(yetiNode+'.cacheFileName', yetiOutputPath + groomFile, type='string')
        
                        #Set the file mode to Cache
                        cmds.setAttr(yetiNode+'.fileMode', 1)                

                        
                    if not isFeather and yetiNodeShape:
                        #Get yeti connections to check groom connection later
                        yetiConns  = cmds.listConnections(yetiNodeShape)
                        
                        #Import grooms
                        if grooms:
                            for groom in grooms:
                                
                                #Import the groom if not imported
                                if not groom in self.importedGrooms:
                                    mel.eval('pgYetiExtractGroomFromNode("' + groom + '", "' + yetiNodeShape + '", "' + '' + '")')
                                    #Populate the imported groom list
                                else:
                                    #If already imported, add the existent groom
                                    try:
                                        groomTrans = cmds.listRelatives(groom, parent=True)[0]
                                        if not groomTrans in yetiConns:
                                            #mel.eval('pgYetiAddGroom("' + groom + '", "' + yetiNodeShape + '");')
                                            mel.eval('pgYetiAddGroom("' + groom + '", "' + yetiNodeShape + '");')
                                    except Exception, e:
                                        print e
            
                                self.importedGrooms.append(groom)
                        
                        #Create the custom variables if exists
                        self.HandleCustomVecVariables(yetiNodeShape, yetiData['CusVarVec'])
                        self.HandleCutomFloatVariables(yetiNodeShape, yetiData['CusVarFlt'])
                        
                        
                        #Add and set .id attribute
                        if not cmds.objExists(yetiNodeShape+'.id'):
                            cmds.addAttr(yetiNodeShape, ln='id', dt='string')
                        
                        #Load all attributs published
                        self.LoadYetiAttributes(yetiNodeName, yetiNodeShape)
                    
                    #Add feather object to the new yetiNode
                    if self.hasFeather:
                        for featherObject in yetiData['featherObject']:
                            mel.eval('pgYetiAddGeometry("' + featherObject + '", "' + yetiNode + '")')
                

        #Add the proper geometry to the new yetiNode
        for inputGeo in yetiData['inputGeo']['inputGeoList']:
            objectId       = inputGeo['objectId']
            objectName     = inputGeo['object']
            isFeather      = inputGeo['isFeather']     
            
            if not isFeather:
                for namespaceName in list(set(yetiNodeNamespaceList)):
                    if ':' in objectName:
                        characterRef = namespaceName+':'+objectName.split(':')[-1]
                    else:
                        characterRef = objectName
                        
                    self.HandleSubdvAttrs(characterRef)
                    
                    yetiNode = namespaceName+'_'+yetiNodeName
                    yetiNodeShape = cmds.listRelatives(yetiNode, shapes=True)[0]

                    #mel.eval('pgYetiAddGeometry("' + characterRef + '", "' + yetiNodeShape + '");')
                    conns = cmds.listConnections(yetiNodeShape)
                    
                    if not cmds.listRelatives(characterRef, parent=True)[0] in conns:
                        mel.eval('pgYetiAddGeometry("%s", "%s");'%(characterRef, yetiNodeShape))

        self.SetAllToCache()


    #===========================================================================
    # #Add Custom Vector variables
    #===========================================================================
    def HandleCustomVecVariables(self, yetiNodeShape=None, customVarList=[]):
        if customVarList:
            for cusVar in customVarList:
                try:
                    cmds.addAttr(yetiNodeShape, ln=customVar, keyable=True, at='double3', p=cusVar)
                except:
                    pass
    
    
    #===========================================================================
    # #Add subdivision attrs
    #===========================================================================
    def HandleSubdvAttrs(self, objShapeNode=None):
        if not 'yetiSubdivision' in cmds.listAttr(objShapeNode):
            cmds.addAttr(objShapeNode, ln='yetiSubdivision', at='bool', k=0)
        if not 'yetiSubdivisionIterations' in cmds.listAttr(objShapeNode):
            cmds.addAttr(objShapeNode, ln='yetiSubdivisionIterations', at='long', k=0)
    
    
    #===========================================================================
    # #Add Custom Float variables    
    #===========================================================================
    def HandleCutomFloatVariables(self, yetiNodeShape=None, customVarList=[]):
        if customVarList:
            for cusVar in customVarList:
                try:
                    cmds.addAttr(yetiNodeShape, ln=cusVar, keyable=True, at='double', dv=0.0, softMinValue=0.0, softMaxValue=100.0)
                except:
                    pass


    #===========================================================================
    # #Update character name callback
    #===========================================================================
    def UpdateCharacterName(self):
        projectPath = cmds.workspace( q=True, rd=True )
        publishPath = projectPath+'cache/groom/'+self.charNameLE.text()
        self.characterName = self.charNameLE.text()
        self.importFolderLE.setText(publishPath)
        self.publishPathLbl.setText(publishPath+'/*.grm')
        if os.path.isdir(publishPath):
            os.chdir(publishPath)


    #===========================================================================
    # #Generate the cache
    #===========================================================================
    def WriteYetiCache(self, cachePath=None, MB=1, loadCache=True, generateYetiCacheFile=False, characterName=None, set_offset=True):
        self.SetAllToNone()
        sceneName = cmds.file(query=True, sn=True, shortName=True).split('.')[0]
        
        if not cachePath:
            projectPath = cmds.workspace( q=True, rd=True )
            cachePath   = yetiOutputPath =  projectPath+"/cache/fur/%s/fur/"%sceneName
        
        #Generate cache for only selected meshes
        if self.cache_selected:
            selObjects       = cmds.ls(sl=True)
            connYetiNodeList = []
            
            if selObjects:
                for obj in selObjects:
                    connYetiNodes = cmds.listConnections(cmds.listRelatives(obj, shapes=True, fullPath=True), type='pgYetiMaya')
                    if connYetiNodes:
                        for yetiNode in connYetiNodes:
                            yetiNodeShape = cmds.listRelatives(yetiNode, shapes=True)[0]
                            if not yetiNodeShape in connYetiNodeList:
                                connYetiNodeList.append(yetiNodeShape)
                if connYetiNodeList:
                    cmds.select(connYetiNodeList, r=True)
            else:
                cmds.warning('You need to select a mesh connected to the YetiNode!')
                return
        else:
        
            #Generate cache for all yeti nodes
            cmds.select(cmds.ls(type='pgYetiMaya'), r=True)
        

        try:
            if not os.path.exists(cachePath):
                os.makedirs(cachePath)
            
            start_frame = cmds.playbackOptions( minTime=True, q=True )
            end_frame   = cmds.playbackOptions( maxTime=True, q=True )
            frameRangeSize = end_frame-start_frame
            
            mel.eval('pgYetiRenderCommand();')
            
            cacheCommand = 'pgYetiCommand -writeCache "' + cachePath + '<NAME>' + '.%04d.fur' +'" -range ' + str(start_frame) + ' ' + str(end_frame) + ' -updateViewport false'
            if MB == 1:
                sample = 1
            else:
                sample = (1/MB)+1
            cacheCommand += ' -samples ' + str(sample)
            print mel.eval(cacheCommand)
            
            if loadCache:
                self.LoadCacheForExistingNodes(cacheFolder=cachePath)

            if set_offset:
                self.SetOffset(start_frame=start_frame, end_frame=end_frame)

            if generateYetiCacheFile:
                self.GenerateYetiCacheScene()
            


        except Exception, e:
            raise SyntaxError(e)


        
        mel.eval('pgYetiRenderCommand();')


    #===========================================================================
    # #Create an maya file with yeti nodes
    #===========================================================================
    def GenerateYetiCacheScene(self, cachePath=None, characterName=None):
        
        sceneName = cmds.file(query=True, sn=True, shortName=True).split('.')[0]

        if not cachePath:
            projectPath = cmds.workspace( q=True, rd=True )
            cachePath   = projectPath+"cache/fur/%s/"%sceneName
            
        #Export yeti nodes and feathers
        yetiNodeList    = [cmds.listRelatives(yetiNode,    parent=True, fullPath=True)[0] for yetiNode    in cmds.ls(type='pgYetiMaya',        long=True)]
        featherNodeList = [cmds.listRelatives(featherNode, parent=True, fullPath=True)[0] for featherNode in cmds.ls(type='pgYetiMayaFeather', long=True)]

        #Delete unknown nodes
        for unknownNode in cmds.ls(type='unknown'):
            if unknownNode == 'rmanFinalGlobals':
                continue
            if cmds.objExists(unknownNode):
                cmds.lockNode(unknownNode, l=False)
                cmds.delete(unknownNode)
        
        #Delete references
        refNodes = cmds.ls(type='reference')
        for refNode in refNodes: 
            try:
                cmds.file(referenceNode=refNode, removeReference=True)
            except:
                pass
            
        self.DeleteAllGrooms()
        
        cmds.select(yetiNodeList, featherNodeList, r=True)
        cmds.refresh()
        
        self.SetAllToCache()
        if yetiNodeList:
            fileName = cmds.file(cachePath + sceneName + '_yeti_cache.ma', type='mayaAscii', es=True, force=True)


    #===========================================================================
    # #Set the fur files in the existing nodes
    #===========================================================================
    def LoadCacheForExistingNodes(self, cacheFolder=None, characterName=None):
        sceneName = cmds.file(query=True, sn=True, shortName=True).split('.')[0]
        
        if not cacheFolder:
            projectPath = cmds.workspace( q=True, rd=True )
            cacheFolder = projectPath+"cache/fur/%s/"%sceneName
            
        for yetiNode in cmds.ls(type='pgYetiMaya'):
            cmds.setAttr(yetiNode+'.cacheFileName', cacheFolder+yetiNode.replace(':', '_')+'.%04d.fur', type='string')
            cmds.setAttr(yetiNode+'.fileMode', 1)
            
            print 'Loading Cache:  %s'%cacheFolder + yetiNode+'.%04d.fur'
        
        
    
    #===========================================================================
    # #Create the yeti nodes in an empty scene and load the fur files
    #===========================================================================
    def LoadCacheFromFiles(self):
        #TODO
        return None


    #===========================================================================
    # #Set all yeti nodes to None on file mode to stop reading the groom file
    #===========================================================================
    def SetAllToNone(self):
        self.SetAllToCache()
        for yetiNode in cmds.ls(type='pgYetiMaya'):
            cmds.setAttr(yetiNode+'.fileMode', 0)
        print "All Yeti nodes are seted to NONE in file mode!"


    #===========================================================================
    # #Set all yeti nodes to Cache on file mode to start reading the groom or cache file
    #===========================================================================
    def SetAllToCache(self):        
        for yetiNode in cmds.ls(type='pgYetiMaya'):
            cmds.setAttr(yetiNode+'.fileMode', 1)
        print "All Yeti nodes are seted to CACHE in file mode!"


    #===========================================================================
    # #Delete All Grooms
    #===========================================================================
    def DeleteAllGrooms(self):
        for groom in cmds.ls(type='pgYetiGroom'):
            cmds.delete(cmds.listRelatives(groom, parent=True)[0])


   
    #===========================================================================
    # #Set Offset
    #===========================================================================
    def SetOffset(self, start_frame=0, end_frame=10):  
        for yetiNode in cmds.ls(type='pgYetiMaya'):
            offset = (end_frame - start_frame)+1
            cmds.disconnectAttr('time1.outTime', yetiNode+'.currentTime')
            cmds.expression(s=yetiNode+'.currentTime = frame+(%s-1)'%start_frame)

        

    #===============================================================================
    #===============================================================================
    # # YetiPublish
    # # Developer: Rosenio Pinto
    # # e-mail:    kenio3d@gmail.com
    #===============================================================================
    # #Usage:
    # 
    # #Run the following funtion to publish all yeti stuff from the lookDev scene.
    # #You need to specify the character name.
    # #The getUUID parameter must be set to False if you need to use the .id on the shape node.
    # #If you set the getUUID parameter to True, the function will get the UUID from the transform node.
    #
    # publishYeti(characterName="CharacterName", getUUID=False)
    # 
    # #The following function will load the Yeti plugin(need to refactor).
    #
    # loadYetiPlugin()
    #===============================================================================


    def YetiPublish(self, characterName='', getUUID=True):
        projectPath    = cmds.workspace( q=True, rd=True )
        yetiNodeList   = cmds.ls(type='pgYetiMaya')
        
        yetiOutputPath =  projectPath+"cache/groom/%s/"%characterName
        
        loadYetiPlugin()
        if yetiNodeList:
            for yetiNodeShape in yetiNodeList:
                yetiNode       = cmds.listRelatives(yetiNodeShape, parent=True)[0]
                grooms         = cmds.listConnections(yetiNodeShape, type='pgYetiGroom')
                
                #Disable display
                cmds.setAttr(yetiNodeShape + '.displayOutput', 0)
                
                #Add and set .id attribute
                if not cmds.objExists(yetiNodeShape+'.id'):
                    cmds.addAttr(yetiNodeShape, ln='id', dt='string')
                cmds.setAttr(yetiNodeShape+'.id', cmds.ls(yetiNodeShape, uuid=True)[0], type='string')
                
                groomShapeList = []
                for groom in grooms:
                    groomShapeList.append(cmds.listRelatives(groom, shapes=True)[0])
                
                inputGeos  = cmds.listConnections(yetiNodeShape + '.inputGeometry')
                
                jsonDict  = {}
                if inputGeos:
                    yetiNamespace                = None
                    newInputGeos                 = {}
                    featherObjList               = []
                    
                    newInputGeos['inputGeoList'] = []
                    for obj in inputGeos:
                        inputGeoDict             = {}
                        
                        #Check if there is a namespace
                        if ':' in obj:
                            yetiNamespace = obj.split(':')[0]
                        
                        #I get the first shape from the list
                        #Maybe you must improve this
                        objShape    = cmds.listRelatives(obj, shapes=True)[0]
                        
                        #Get the UUID os ID if not getUUID 
                        if getUUID:
                            if cmds.ls(objShape, uuid=True):
                                inputGeoDict['object']   = objShape
                                objectId                 = cmds.ls(objShape, uuid=True)[0]
                                inputGeoDict['objectId'] = objectId
                            else:
                                inputGeoDict['object']   = objShape
                                inputGeoDict['objectId'] = None
                        else:
                            if cmds.objExists(objShape+'.id'):
                                inputGeoDict['object']   = objShape
                                objectId                 = cmds.getAttr(objShape+'.id')
                                inputGeoDict['objectId'] = objectId
                            else:
                                inputGeoDict['object']   = objShape
                                inputGeoDict['objectId'] = None
                            
                        #Set as not feather type by default
                        isFeather   = False
                        faceSetDict = {}
                        
                        # Check for featherObjList objects
                        if cmds.nodeType(objShape) == 'pgYetiMayaFeather':
                            featherObjList.append(objShape)
                            isFeather = True
                        

                        #List the sets connected in the shape
                        #=======================================================
                        # #TODO 
                        # #Get list of sets from yeti nodes
                        #=======================================================
                        faceSetList = cmds.listConnections(objShape+'.instObjGroups[0].objectGroups', type='objectSet')
                        
                        if faceSetList:
                            for faceSet in faceSetList:
                                setList = cmds.sets(faceSet, q=True) 
                                if setList:
                                    faceList = ['.'+faceRange.split('.')[-1] for faceRange in setList if '.f[' in faceRange]
                                    if faceList:
                                        faceSetDict[faceSet] = faceList

                        newInputGeos['inputGeoList'].append(inputGeoDict)
                            
                        inputGeoDict['faceSetDict'] = faceSetDict                            
                        inputGeoDict['isFeather']   = isFeather
    
                    # select featherObjList and export
                    if featherObjList:
                        cmds.select(featherObjList)
                        # Export feathres as .ma file
                        featherFileOutput = yetiOutputPath + yetiNode + '_feathers.ma'
                        if os.path.exists(featherFileOutput):
                            os.remove(featherFileOutput)
                            
                        featherFile               = cmds.file(featherFileOutput, type="mayaAscii", exportSelected=True)
                        newInputGeos['feathers']  = featherFile
                        jsonDict['featherObject'] =  featherObjList
                    else:
                        newInputGeos['feathers'] = None
                        
                        
                    CusYetiVarVECTOR  = None
                    cusYetiVarVecList = cmds.listAttr(yetiNodeShape, string="yetiVariableV*")
                    if cusYetiVarVecList:
                        CusYetiVarVECTOR = [varName for varName in cusYetiVarVecList if (type(cmds.getAttr(yetiNodeShape+'.'+varName)) == list)]
                        
                    CusYetiVarFLOAT  = None
                    CusYetiVarFLOAT  = cmds.listAttr(yetiNodeShape, string='yetiVariableF*')

                    jsonDict['inputGeo']       = newInputGeos
                    jsonDict['sets']           = {}
                    jsonDict['guides_rest']    = {}
                    jsonDict['sets_attrs']     = {}
                    jsonDict['yetiNode']       = yetiNode
                    jsonDict['hasFeather']     = isFeather
                    jsonDict['grooms']         = groomShapeList
                    jsonDict['yetiOutputPath'] = yetiOutputPath
                    jsonDict['getUUID']        = getUUID  
                    jsonDict['CusVarVec']      = CusYetiVarVECTOR
                    jsonDict['CusVarFlt']      = CusYetiVarFLOAT
                    
                    # Check for guide sets
                    #===============================================================
                    # #WARNING
                    # #I do not to much efort in this guy
                    # #If guides are important for this job, take care :(
                    #===============================================================
                    guideSets = cmds.listConnections(yetiNodeShape + '.guideSets')
                    if guideSets:
                        for set in guideSets:
                            newSets = []
                            setObjs = cmds.sets(set, q=True)
                            for setObj in setObjs:
                                newSets.append(setObj.split(':')[-1])
                            setName                         = set.split(':')[-1]
                            jsonDict['sets'][setName]       = newSets
                            jsonDict['sets_attrs'][setName] = {}
                            setAttrs                        = cmds.listAttr(set)
                            
                            if 'maxNumberOfGuideInfluences' in setAttrs:
                                jsonDict['sets_attrs'][setName]['maxNumberOfGuideInfluences'] = cmds.getAttr(set+'.maxNumberOfGuideInfluences')
                            if 'lockToSurface' in setAttrs:
                                jsonDict['sets_attrs'][setName]['lockToSurface'] = cmds.getAttr(set+'.lockToSurface')
                            if 'ignoreRestNormalTriangulation' in setAttrs:
                                jsonDict['sets_attrs'][setName]['ignoreRestNormalTriangulation'] = cmds.getAttr(set+'.ignoreRestNormalTriangulation')
                                
                            for guide in newSets:
                                guideName                      = yetiNamespace + ':' + guide
                                guideShape                     = cmds.listRelatives(guideName, shapes=True)[0]
                                jsonDict['guides_rest'][guide] = {}
                                guideAttrs = cmds.listAttr(guideShape)
    
                                if 'width' in guideAttrs:
                                    jsonDict['guides_rest'][guide]['width'] = cmds.getAttr(guideShape+'.width')
                                if 'yetiReferenceNormalY' in guideAttrs:
                                    jsonDict['guides_rest'][guide]['yetiReferenceNormalY'] = cmds.getAttr(guideShape+'.yetiReferenceNormalY')
                                if 'yetiReferenceLength' in guideAttrs:
                                    jsonDict['guides_rest'][guide]['yetiReferenceLength'] = cmds.getAttr(guideShape+'.yetiReferenceLength')
                                if 'yetiReferencePositionY' in guideAttrs:
                                    jsonDict['guides_rest'][guide]['yetiReferencePositionY'] = cmds.getAttr(guideShape+'.yetiReferencePositionY')
                                if 'yetiReferenceNormalX' in guideAttrs:
                                    jsonDict['guides_rest'][guide]['yetiReferenceNormalX'] = cmds.getAttr(guideShape+'.yetiReferenceNormalX')
                                if 'yetiReferencePositionX' in guideAttrs:
                                    jsonDict['guides_rest'][guide]['yetiReferencePositionX'] = cmds.getAttr(guideShape+'.yetiReferencePositionX')
                                if 'yetiReferenceNormalZ' in guideAttrs:
                                    jsonDict['guides_rest'][guide]['yetiReferenceNormalZ'] = cmds.getAttr(guideShape+'.yetiReferenceNormalZ')
                                if 'yetiReferencePositionZ' in guideAttrs:
                                    jsonDict['guides_rest'][guide]['yetiReferencePositionZ'] = cmds.getAttr(guideShape+'.yetiReferencePositionZ')
    
      
                    #Create the Yeti output folder
                    if not os.path.exists(yetiOutputPath):
                        os.makedirs(yetiOutputPath)
                    
                    self.BrowseAndSet(folderPath=yetiOutputPath)
                    
                    #Export groom as file (.grm)
                    mel.eval('pgYetiCommand -exportGroom "' + yetiOutputPath + yetiNode + '.grm" "' + yetiNodeShape + '";')
                    cmds.setAttr(yetiNodeShape+'.cacheFileName', yetiOutputPath + yetiNode + '.grm', type='string')
                    cmds.setAttr(yetiNodeShape+'.fileMode', 0)
                    
                    #Write the jason file with all data colected
                    with open(yetiOutputPath + yetiNode + '.json', "w") as jsonData:
                        json.dump(jsonDict, jsonData, sort_keys = True, indent = 4)
                    
                    self.PublishYetiAttributes(yetiNodeShape)
                    
                    print yetiNode + ' published to: ' + yetiOutputPath


    #===========================================================================
    # #Rename and reconnect grooms
    #===========================================================================
    def GetAllGrooms(self):
        self.groomDict = {}
        return cmds.ls(type='pgYetiGroom')
    
                
    def RenameAllGrooms(self, characterName=''):
        for groomShape in self.GetAllGrooms():
            self.RenameGroom(cmds.listRelatives(groomShape, parent=True)[0], characterName)
        
        self.ReplaceAllGroomImportParam(self.groomDict)


    def RenameGroom(self, groom=None, newName=''):
        oldValue      = groom
        oldValueShape = cmds.listRelatives(oldValue, shapes=True)[0]

        if not newName in oldValue:
            newGroom      = cmds.rename(groom, newName+'_'+oldValue)
            newValue      = newGroom

            newValueShape = cmds.listRelatives(newValue, shapes=True)[0]
        
            self.groomDict[oldValueShape] = newValueShape
        else:
            self.groomDict[oldValueShape] = oldValueShape
    
    
    def ReplaceAllGroomImportParam(self, groomDict={}):
        yetiNodes = cmds.ls(type='pgYetiMaya')
        if yetiNodes:
            for yetiNode in yetiNodes:
                self.ReplaceGroomImportParam(self.groomDict, yetiNode)
    
    
    def ReplaceGroomImportParam(self, groomDict={}, yetiNode=None):
        for groom in self.groomDict.keys():
            nodeList = mel.eval('pgYetiGraph -listNodes -type "import" %s'%yetiNode)
            if nodeList:
                for node in nodeList:
                    currValue = mel.eval('pgYetiGraph -node "%s" -param "geometry" -getParamValue %s'%(node, yetiNode))
        
                    if currValue == groom:
                        mel.eval('pgYetiGraph -node "%s" -param "geometry" -setParamValueString "%s" %s'%(node, self.groomDict[groom], yetiNode))
                        print 'Renaming and connecting %s to %s'%(groom, self.groomDict[groom])


    #===========================================================================
    # #Rename and reconnect sets
    #===========================================================================
    def GetAllSets(self):
        yetiNodes        = cmds.ls(type='pgYetiMaya')
        faceSetListClean = []
        self.faceSetDict = {}
        if yetiNodes:
            for yetiNodeShape in yetiNodes:
                yetiNode  = cmds.listRelatives(yetiNodeShape, parent=True)[0]
                inputGeos = cmds.listConnections(yetiNode + '.inputGeometry')
        
                for inputGeo in inputGeos:
                    inputGeoShape = cmds.listRelatives(inputGeo, shapes=True)[0]
                    faceSetList   = cmds.listConnections(inputGeoShape+'.instObjGroups[0].objectGroups', type='objectSet')
        
                    if faceSetList:
                        for faceSet in faceSetList:
                            setList = cmds.sets(faceSet, q=True) 
                            if setList:
                                faceSet   = list(set([faceSet for faceRange in setList if '.f[' in faceRange]))
                                if faceSet:
                                    if not faceSet[0] in faceSetListClean:
                                        faceSetListClean.append(faceSet[0])
        return faceSetListClean


    def RenameAllFaceSets(self, characterName=''):
        for faceSet in self.GetAllSets():
            self.RenameSet(faceSet, characterName)
        
        self.ReplaceAllFaceSetScatterParam(self.faceSetDict)


    def RenameSet(self, faceSet=None, newName=''):
        oldValue   = faceSet
        
        if not newName in oldValue:
            newFaceSet = cmds.rename(faceSet, newName+'_'+oldValue)
            newValue   = newFaceSet
        
            self.faceSetDict[oldValue] = newValue
        else:
            self.faceSetDict[oldValue] = oldValue


    def ReplaceAllFaceSetScatterParam(self, faceSetDict={}):
        yetiNodes = cmds.ls(type='pgYetiMaya')
        if yetiNodes:
            for yetiNode in yetiNodes:
                self.ReplaceFaceSetScatterParam(self.faceSetDict, yetiNode)


    def ReplaceFaceSetScatterParam(self, faceSetDict={}, yetiNode=None):
        for faceSet in self.faceSetDict.keys():
            nodeList = mel.eval('pgYetiGraph -listNodes -type "scatter" %s'%yetiNode)
            
            if nodeList:
                for node in nodeList:
                    currValue = mel.eval('pgYetiGraph -node "%s" -param "faceSet" -getParamValue %s'%(node, yetiNode))
                    
                    if currValue == faceSet:
                        mel.eval('pgYetiGraph -node "%s" -param "faceSet" -setParamValueString "%s" %s'%(node, self.faceSetDict[faceSet], yetiNode))
                        print 'Renaming and connecting %s to %s'%(faceSet, self.faceSetDict[faceSet])


    #===========================================================================
    # #Rename All Yeti nodes
    #===========================================================================
    def RenameAllYetiNodes(self, characterName=''):
        yetiNodes = cmds.ls(type='pgYetiMaya')
        
        if yetiNodes:
            for yetiNode in yetiNodes:
                yetiNode = cmds.listRelatives(yetiNode, parent=True)[0]
                if not characterName in yetiNode:
                    cmds.rename(yetiNode, characterName+'_'+yetiNode)
                    print 'Renaming and connecting %s to %s'%(yetiNode, characterName+'_'+yetiNode)


    #===========================================================================
    # #Rename All Feathers
    #===========================================================================
    def ReplaceAllFeatherGeometryParam(self, characterName=''):
        if not characterName and (characterName == 'Character Name'):
            cmds.warning("Please set the character name!")
            return
        
        self.featherDict = self.RenameAllYetiFeatherNodes(characterName)
    
        yetiNodes = cmds.ls(type='pgYetiMaya')
        if yetiNodes:
            for yetiNode in yetiNodes:
                self.ReplaceFeatherGeometryParam(self.featherDict, yetiNode)


    def RenameAllYetiFeatherNodes(self, characterName=''):
        renamedYetiFeatherNodeList = []
        yetiNodes                  = cmds.ls(type='pgYetiMaya')
        featherDict = {}
        if yetiNodes:
            for yetiNode in yetiNodes:
                yetiFeatherNodes = cmds.listConnections(yetiNode, type='pgYetiMayaFeather')
                if yetiFeatherNodes:
                    for yetiFeatherNode in yetiFeatherNodes:
                        if not yetiFeatherNode in renamedYetiFeatherNodeList:
                            yetiFeatherNodeShape    = cmds.listRelatives(yetiFeatherNode, shapes=True)[0]
                            if not characterName in yetiFeatherNode:
                                newYetiFeatherNode      = cmds.rename(yetiFeatherNode, characterName+'_'+yetiFeatherNode)
                                newYetiFeatherNodeShape = cmds.listRelatives(newYetiFeatherNode, shapes=True)[0]
                                
                                renamedYetiFeatherNodeList.append(newYetiFeatherNode)
                                featherDict[yetiFeatherNodeShape] = newYetiFeatherNodeShape
                            else:
                                featherDict[yetiFeatherNodeShape] = yetiFeatherNodeShape
        return featherDict


    def ReplaceFeatherGeometryParam(self, featherDict={}, yetiNode=None):
        nodeList = mel.eval('pgYetiGraph -listNodes -type "import" %s'%yetiNode)
        if nodeList:
            for featherNode in self.featherDict.keys():
                for node in nodeList:
                    paramType = mel.eval('pgYetiGraph -node "%s" -param "type" -getParamValue %s'%(node, yetiNode))
            
                    #If FEATHER
                    if paramType == 3:
                        currValue = mel.eval('pgYetiGraph -node "%s" -param "geometry" -getParamValue %s'%(node, yetiNode))
    
                        if currValue == featherNode:
                            mel.eval('pgYetiGraph -node "%s" -param "geometry" -setParamValueString "%s" %s'%(node, self.featherDict[featherNode], yetiNode))
                            print 'Renaming and connecting %s to %s'%(currValue, self.featherDict[featherNode])


    #===========================================================================
    # #Save Yeti attributes preset
    #===========================================================================
    def PublishYetiAttributes(self, yetiNodeShape=None):
        if yetiNodeShape:
            allAttrList = cmds.listAttr(yetiNodeShape, se=True, r=True)
            
            defaultPresetPath = mel.eval('saveAttrPreset "%s" "%s" 0;'%(yetiNodeShape, yetiNodeShape))
            
            newPresetPath = cmds.workspace( q=True, rd=True )+'presets/'
            
            if not os.path.isdir(newPresetPath):
                os.makedirs(newPresetPath)
            copyfile(defaultPresetPath, newPresetPath+yetiNodeShape+'.mel')
            
            # Remove the local maya preset
            os.remove(defaultPresetPath)


    #===========================================================================
    # #Load Yeti attributes preset
    #===========================================================================
    def LoadYetiAttributes(self, yetiNodePreset='', yetiNodeShape=None):
        if yetiNodeShape:
            # Load the preset from a custom location
            preset_file = cmds.workspace( q=True, rd=True )+'presets/'+yetiNodePreset+'Shape.mel'
            mel.eval('applyAttrPreset "%s" "%s" 1;'%(yetiNodeShape, preset_file))

#===============================================================================
# #Load Yeti plugin. (Still need some work)
#===============================================================================
def loadYetiPlugin():
    #This guy need attention
    try:
        yetiPlugin = cmds.loadPlugin("pgYetiMaya.mll", quiet=True)
        if cmds.getAttr('defaultRenderGlobals.preMel', lock=True) or cmds.getAttr('defaultRenderGlobals.postMel', lock=True) or cmds.getAttr('defaultRenderGlobals.preRenderMel', lock=True) or cmds.getAttr('defaultRenderGlobals.postRenderMel', lock=True):
            preMelVal = cmds.getAttr('defaultRenderGlobals.preMel')
            postMelVal = cmds.getAttr('defaultRenderGlobals.postMel')
            preRenderMelVal = cmds.getAttr('defaultRenderGlobals.preRenderMel')
            postRenderMelVal = cmds.getAttr('defaultRenderGlobals.postRenderMel')

            cmds.setAttr('defaultRenderGlobals.preMel', lock=False)
            cmds.setAttr('defaultRenderGlobals.postMel', lock=False)
            cmds.setAttr('defaultRenderGlobals.preRenderMel', lock=False)
            cmds.setAttr('defaultRenderGlobals.postRenderMel', lock=False)
            
            pgYetiAttributes = None
            try: pgYetiAttributes = mel.eval('$temp2=$g_pgYetiAttributes')
            except: pass
            if pgYetiAttributes == None:
                mel.eval("source pgYeti;")

            cmds.setAttr('defaultRenderGlobals.preMel', preMelVal, type='string')
            cmds.setAttr('defaultRenderGlobals.postMel', postMelVal, type='string')
            cmds.setAttr('defaultRenderGlobals.preRenderMel', preRenderMelVal, type='string')
            cmds.setAttr('defaultRenderGlobals.postRenderMel', postRenderMelVal, type='string')
        else:
            pgYetiAttributes = None
            try: pgYetiAttributes = mel.eval('$temp2=$g_pgYetiAttributes')
            except: pass
            if pgYetiAttributes == None:
                mel.eval("source pgYeti;")

    except Exception, e:
        cmds.warning('Error on load Yeti Plugin: ' + str(e))
        


      
      
    
