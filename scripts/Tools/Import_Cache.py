#===============================================================================
# Autor: Rosenio Pinto
# e-mail: kenio3d@gmail.com
#
# This code need to be cleaned
#===============================================================================
from SystemConfig import *


cmds.loadPlugin('AbcImport.mll')
cmds.loadPlugin('AbcExport.mll')

class ImportCache(QWidget):
    def __init__(self, parent=None):
        super(ImportCache, self).__init__(parent)
        #=======================================================================
        # #Parent widget under Maya main window
        #=======================================================================
        self.setParent(get_main_window())
        self.setWindowFlags(Qt.Window)

        self.setGeometry(0, 0, 300, 300)

        #=======================================================================
        # #Set the object name
        #=======================================================================
        self.setObjectName('ImportCacheWindow_uniqueId')
        self.setWindowTitle('Import Cache')

        self.current_category_tab = 0
        self.Import_Cache_Info    = {}


        self.initUI()


    #===========================================================================
    # #UI functions
    #===========================================================================
    def initUI(self):
        self.mainLayout            = QVBoxLayout(self)
        self.setLayout             = self.mainLayout

        self.centralLayout         = QHBoxLayout(self)
        self.scenes_layout         = QVBoxLayout(self)
        self.scene_list_widget     = AW.AssetListWidget(tab_title='Cached Scenes', isStatic=True)
        self.CachedAssetWidgetsTab = AW.AssetListWidget()

        self.scenes_widget = QWidget(self)
        self.scenes_widget.setLayout(self.scenes_layout)


        listWidgetSplitter = QSplitter(Qt.Horizontal)
        listWidgetSplitter.addWidget(self.scenes_widget)
        listWidgetSplitter.addWidget(self.CachedAssetWidgetsTab)
        listWidgetSplitter.setStyleSheet("QSplitter:handle{height: 16px; image: url(%sverticalHandle.png);}"%BATCH_io_IMAGES)

        listWidgetSplitter.setSizes([400, 200])


        self.scenes_layout.addWidget(self.Add_Scene_Widget_HeaderUI())
        self.scenes_layout.addWidget(self.scene_list_widget)
        self.centralLayout.addWidget(listWidgetSplitter)
        self.mainLayout.addLayout(self.centralLayout)

        self.scene_list_widget.SetFont('fontSize_H1', True)


    def Add_Scene_Widget_HeaderUI(self):
            #===================================================================
            # #Add header scene widgets
            #===================================================================
            self.header_widget = AW.AssetWidget()

            self.header_widget.SetCheckBox(True)
            self.header_widget.SetAssetLabel('scene name')
            self.header_widget.SetStatusLabel('status')


            self.header_widget.SetAssetBtn(u"\u25BC", self.print_none, True, True)

            self.header_widget.SetAssetBtn(u"X", self.Remove_Selected, True, True)


            self.header_widget.isTrigger    = False
            self.header_widget.isInterative = False


            checkbox_slot = self.Set_All_Scene_CheckState
            self.header_widget.SetCheckBoxChangeCmd(checkbox_slot)


            return self.header_widget


    def print_none(self):
        print 'None'


    def AddCachedSceneWidgetsUI(self, scene_short_name=''):
        self.scene_list_widget.CleanAssetWidgets()

        Asset_DB = Set_DB()
        self.Asset_DB_Query = Asset_DB.query()

        #=======================================================================
        # #Get all published scene names on db
        #=======================================================================
        published_SceneList = sorted(list(set([scene_short_name['scene_short_name'] for scene_short_name in self.Asset_DB_Query])))

        for scene_short_name in published_SceneList:

            sceneWidget = AW.AssetWidget()
            sceneWidget.SetCheckBox(True)
            sceneWidget.SetAssetIcon(BATCH_io_IMAGES+'maya-icon.png')
            sceneWidget.SetAssetLabel(scene_short_name)
            sceneWidget.SetAssetBtn(u"\u25BC", partial(self.ReferenceAllAlembic, scene_short_name), True, True)
            sceneWidget.SetAssetBtn(u"X", partial(self.RemoveAlembic, scene_short_name, sceneWidget), True, True)
            sceneWidget.SetAssetBtn(u"\u2699", partial(self.AddCachedAssetsUI, scene_short_name), True, False)
            sceneWidget.SetFont('fontSize_H3', True)
            sceneWidget.isTrigger = True

            #===========================================================
            # #Set the checkbox change state function
            #===========================================================
            checkboxslot = partial(self.Set_Scene_CheckState, sceneWidget)
            sceneWidget.SetCheckBoxChangeCmd(checkboxslot)

            self.scene_list_widget.AddAssetWidget(sceneWidget)



    def AddCachedAssetsUI(self, scene_short_name):
        self.CleanCachedAssetWidgetUI()
        self.scene_list_widget.SetAssetUnselected(scene_short_name)

        #=======================================================================
        # #Get all asset list published on db
        #=======================================================================
        Asset_DB   = Set_DB()
        sceneQuery = Asset_DB.query({'scene_short_name':scene_short_name})


        if sceneQuery:
            for cache_list in sceneQuery:
                assetDict = cache_list['reference_list']

                #===============================================================
                # Put the cache lists into the main cache dict to use later
                #===============================================================
                self.Import_Cache_Info[scene_short_name] = cache_list

                #===============================================================
                # Create a check state dict for references
                #===============================================================
                if not 'Reference_CheckState_Info' in self.Import_Cache_Info[scene_short_name].keys():
                    self.Import_Cache_Info[scene_short_name]['Reference_CheckState_Info'] = {}

                for cache_name, cache_list in assetDict.iteritems():
                    reference_type      = cache_list['reference_type']
                    reference_full_path = cache_list['cache_path']

                    #===========================================================
                    # #Populate check state dict
                    #===========================================================
                    check_state = True
                    if not reference_type in self.Import_Cache_Info[scene_short_name]['Reference_CheckState_Info'].keys():
                        self.Import_Cache_Info[scene_short_name]['Reference_CheckState_Info'][reference_type] = {cache_name:check_state}

                    if not cache_name in self.Import_Cache_Info[scene_short_name]['Reference_CheckState_Info'][reference_type].keys():
                        self.Import_Cache_Info[scene_short_name]['Reference_CheckState_Info'][reference_type][cache_name] = check_state


                    check_state = self.Import_Cache_Info[scene_short_name]['Reference_CheckState_Info'][reference_type][cache_name]
                    #===========================================================
                    # Create a tab for the proper category
                    #===========================================================
                    self.CachedAssetWidgetsTab.set_tab(reference_type)

                    #===========================================================
                    # #Create an asset widget for the asset to be impoted
                    #===========================================================
                    cache_widget = AW.AssetWidget()
                    cache_widget.SetCheckBox(check_state)
                    cache_widget.SetAssetIcon(BATCH_io_IMAGES+'PipelineCache.png')
                    cache_widget.SetAssetLabel(cache_name)
                    cache_widget.SetAssetBtn(u"\u25BC", partial(self.ReferenceAlembic,
                                                                    cache_list['cache_path'],
                                                                    sceneQuery['start_frame'],
                                                                    sceneQuery['end_frame'],
                                                                    cache_name),
                                                                    True)

                    cache_widget.setToolTip('Scene___________'+scene_short_name+'\n'+
                                            'Path____________'+reference_full_path+'\n'+
                                            'Namespace_____'+cache_name+'\n'+
                                            'Type:___________'+reference_type
                                            )


                    cache_widget.SetFont('fontSize_H3', True)
                    cache_widget.isTrigger = True

                    #===========================================================
                    # #Set the checkbox change state function
                    #===========================================================
                    checkboxslot = partial(self.Set_Cache_CheckState, scene_short_name, reference_type, cache_name)
                    cache_widget.SetCheckBoxChangeCmd(checkboxslot)

                    self.CachedAssetWidgetsTab.AddAssetWidget(cache_widget, True, reference_type)

                    self.Set_Cache_CheckState(scene_short_name, reference_type, cache_name, check_state)

            self.CachedAssetWidgetsTab.setCurrentIndex(self.current_category_tab)


    def RemoveAlembic(self, scene_short_name, scene_widget):
        result = self.Confirm_Dialog()

        if result == QMessageBox.Ok:
            Asset_DB   = Set_DB()
            sceneQuery = Asset_DB.query({'scene_short_name':scene_short_name})
            if sceneQuery:
                for reference_list in sceneQuery:
                    assetDict = reference_list['reference_list']
                    for assetItems in assetDict.values():
                        cachePath = assetItems['cache_path']
                        if os.path.isfile(cachePath):
                            try:
                                #===================================================
                                # #Delete the alembic file
                                #===================================================
                                os.remove(cachePath)

                                #===================================================
                                # #Update the UI
                                #===================================================
                                scene_widget.close()
                                self.CleanCachedAssetWidgetUI()

                                #===================================================
                                # #Update the DB
                                #===================================================
                                Asset_DB.cleanAll(sceneQuery['_id'])
                                self.Import_Cache_Info[scene_short_name] = None

                                #===================================================
                                # log
                                #===================================================
                                print 'The cache: [ %s ] from scene: >> %s << was removed.'%(cachePath.split('scenes')[-1], scene_short_name)

                            except Exception, e:
                                'This cache cannot be removed. Maybe in use.'
                                print e


    def Remove_Selected(self):
        for scene_short_name in self.Import_Cache_Info.keys():
            if self.Import_Cache_Info[scene_short_name]:
                scene_widget = self.scene_list_widget.assetWidgets[scene_short_name]
                self.RemoveAlembic(scene_short_name, scene_widget)



    def Confirm_Dialog(self):
        msgBox = QMessageBox()
        msgBox.setText("This action is undoable!")
        msgBox.setInformativeText("Do you want to remove your caches?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.setIcon(QMessageBox.Warning)
        result = msgBox.exec_()
        return result


    def CleanCachedAssetWidgetUI(self):
        self.current_category_tab = self.CachedAssetWidgetsTab.currentIndex()
        self.CachedAssetWidgetsTab.CleanAssetWidgets()
        self.CachedAssetWidgetsTab.clear()


    def RefreshUICmd(self):
        self.AddCachedSceneWidgetsUI()


    def Set_Scene_CheckState(self, *args):
        scene_widget     = args[0]
        scene_short_name = scene_widget.GetName()
        checkState       = True
        if args[1] == 0:
            checkState = False

        self.scene_list_widget.SetAssetUnselected(scene_widget.GetName())
        self.Import_Cache_Info[scene_short_name]['Scene_CheckState_Info'] = checkState

        scene_widget.animRefresh()


    def Set_All_Scene_CheckState(self, *args):
        for scene_widget in self.scene_list_widget.assetWidgets.values():
            scene_widget.Set_CheckState_Value(args[0])


    def Set_Cache_CheckState(self, *args):
        scene_short_name  = args[0]
        reference_type    = args[1]
        reference         = args[2]
        checkState        = args[3]
        if checkState == 0:
            checkState = False
        else:
            checkState = True

        if not checkState:
            print scene_short_name, reference_type, reference, "Will not be considered on the batch process."

        self.Import_Cache_Info[scene_short_name]['Reference_CheckState_Info'][reference_type][reference] = checkState


    #===========================================================================
    # #System
    #===========================================================================
    def ReferenceAlembic(self, cache_path='', start_frame=0, end_frame=10, namespace=''):
        self.SetTimeSlider(start_frame, end_frame)
        cache_path = cmds.file(cache_path, reference=True, mergeNamespacesOnClash=False, namespace=namespace)
        #=======================================================================
        # #Set reference relative path
        #=======================================================================
        uName = cache_path.split(Get_Project())[-1]
        refNode = cmds.referenceQuery(cache_path, referenceNode=True)

        cmds.file(uName, loadReference=refNode)

        return cmds.referenceQuery(refNode, namespace=True)


    def ReferenceAllAlembic(self, scene_short_name):
        #=======================================================================
        # #Reference all cached references for a scene
        #=======================================================================

        Asset_DB_Query = self.Import_Cache_Info[scene_short_name]
        assetDict      = Asset_DB_Query['reference_list']
        if assetDict:
            for assetItem in assetDict.values():
                namespace_name = assetItem['root_name'].split(':')[0]
                reference_type = assetItem['reference_type']

                if Asset_DB_Query['Reference_CheckState_Info'][reference_type][namespace_name]:

                    namespace_name = self.ReferenceAlembic(assetItem['cache_path'], Asset_DB_Query['start_frame'], Asset_DB_Query['end_frame'], namespace_name)

                    if not cmds.objExists(assetItem['root_name']):
                        alembicNode = cmds.ls('%s:*'%namespace_name, type='AlembicNode')

                        if alembicNode:
                            rootNodes   = cmds.listConnections(alembicNode)
                        else:
                            rootNodes = cmds.ls('%s:*'%namespace_name, type='transform')
                        if rootNodes:
                            try:
                                if not cmds.objExists('%s_MESH'%namespace_name):
                                    cmds.group(rootNodes, n='%s_MESH'%namespace_name)
                            except Exception, e:
                                print e
                                print "Problems to group alembic root nodes."


        self.SetOffset()


    #===========================================================================
    # #Set Offset
    #===========================================================================
    def SetOffset(self):
        alembic_nodes = cmds.ls(type='AlembicNode')

        for alembic_node in alembic_nodes:
            start_frame = cmds.getAttr(alembic_node+'.startFrame')
            end_frame   = cmds.getAttr(alembic_node+'.endFrame')

            offset = (end_frame - start_frame)+1

            cmds.setAttr(alembic_node+'.offset', -(start_frame-1))

        self.SetTimeSlider(1, offset)


    #===========================================================================
    # Set the scene timeslider
    #===========================================================================
    def SetTimeSlider(self, start_frame=0, end_frame=10):
        cmds.playbackOptions(min=start_frame, max=end_frame)
        cmds.playbackOptions(ast=start_frame, aet=end_frame)
