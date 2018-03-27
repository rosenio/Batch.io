#===============================================================================
# #Autor: Rosenio Pinto
#===============================================================================

from SystemConfig import *
from Colors import *

#Font sizes
fontSize_H1 = QFont("Segoe UI", 12, QFont.Bold)
fontSize_H2 = QFont("Segoe UI", 10, QFont.Bold)
fontSize_H3 = QFont("Segoe UI", 8,  QFont.Bold)

#Corlors

Anim_Thread_Pool = QThreadPool()


#===============================================================================
# #Asset widget for a lot of purposes
#===============================================================================
class AssetWidget(QWidget):
    def __init__(self, parent=None):
        super(AssetWidget, self).__init__(parent)
        
        self.isDraggable    = False
        self.isDroppable    = False
        self.isAssetWidget  = True
        self.isTrigger      = False
        self.isHeader       = False
        self.asset_width    = 210
        self.asset_height   = 50
        self.button_size    = self.asset_height / 2 
        self.hasProgressBar = False
        self.hasContextMenu = False
        self.isInterative   = True
        self.colors         = Colors()
        self.asset_btn_list = []
        self.type           = None
        
        self.initUI()
        
    def initUI(self):
        self.mainLayout       = QVBoxLayout(self)
        self.setLayout        = self.mainLayout
        self.assetLayout      = QHBoxLayout()
        self.assetBtnLayout   = QHBoxLayout()
        self.assetComboLayout = QHBoxLayout()
        self.groupLayout      = QHBoxLayout()
        self.allLayout        = QVBoxLayout()
        
        self.mainLayout.setContentsMargins(2, 2, 2, 0)
        
        self.assetIconLbl   = QLabel()
        self.statusLevelLbl = QLabel()
        self.assetLbl       = QLabel('assetLabelTxt')
        self.checkBox       = QCheckBox()
        self.widgetGrpBox   = QFrame(self)

        self.assetBtnLayout.setAlignment(Qt.AlignRight)
        self.assetComboLayout.setAlignment(Qt.AlignRight)
        self.assetLayout.setAlignment(Qt.AlignLeft)
        
        self.widgetGrpBox.setFrameShape(QFrame.StyledPanel)
        self.widgetGrpBox.setLayout(self.allLayout)
        
        self.groupLayout.addLayout(self.assetLayout)
        self.allLayout.addLayout(self.groupLayout)
        
        self.mainLayout.addWidget(self.widgetGrpBox)
        self.mainLayout.addLayout(self.allLayout)

        self.setFixedHeight(self.asset_height)
  
        self.SetBackgroundColor(self.colors.background)
        self.SetFont('fontSize_H1', True)
        self.SetColor()
        
        QToolTip.setFont(fontSize_H3)
        
    #===========================================================================
    # #Progressbar
    #===========================================================================
    def SetProgress(self, height=5):
        self.progressBarFrame = QLabel(self.widgetGrpBox)
        self.progressBarFrame.setFixedHeight(height)
        self.progressBarFrame.setStyleSheet( "QLabel {background-color: rgb%s}"%str(self.colors.progressBar));
        self.progressBarFrame.move(0, 0)#self.asset_height-height)
        self.hasProgressBar = True
        self.SetProgressValue()

    def SetProgressValue(self, value=0):
        if self.hasProgressBar:
            factor = (self.asset_width/100.0) * value

            self.progressBarFrame.setFixedWidth(factor)


    #===========================================================================
    # #CheckBox
    #===========================================================================
    def SetCheckBox(self, state=True):
        self.assetLayout.addWidget(self.checkBox)
        self.checkBox.setChecked(state)
        self.checkBox.setStyleSheet('QCheckBox{ background-color: black}')

    def CheckStateCmd(self):
        return self.checkBox.checkState()
    
    def Set_CheckState_Value(self, value=None):
        if value:
            self.checkBox.setChecked(value)
        else:
            if self.CheckStateCmd():
                self.checkBox.setChecked(False)
            else:
                self.checkBox.setChecked(True)
    
    def SetCheckBoxChangeCmd(self, cmd):
        self.checkBox.stateChanged.connect(cmd)


    #===========================================================================
    # #Icon
    #===========================================================================
    def SetAssetIcon(self, icon=''):
        self.assetLayout.addWidget(self.assetIconLbl)
        pixmap = QPixmap(icon).scaled(self.button_size, self.button_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.assetIconLbl.setPixmap(pixmap)

    
    #===========================================================================
    # #Label
    #===========================================================================
    def SetAssetLabel(self, assetLabel=''):
        self.assetLayout.addWidget(self.assetLbl)
        self.assetLbl.setText(assetLabel)
        self.itemName = assetLabel
        self.setObjectName(self.itemName+'_uniqueId') 
        self.groupLayout.addWidget(self.statusLevelLbl)
        
    def SetStatusLabel(self, msg=''):
        self.statusLevelLbl.setText(msg)
        self.statusLevelLbl.setFont(AW.fontSize_H3)
        
        
    #===========================================================================
    # #Button
    #===========================================================================
    def SetAssetBtn(self, assetButtonLabel='', command=None, isSquare=False, isVisible=True, icon=None):
        assetBtn       = QPushButton(assetButtonLabel)
        
        self.groupLayout.addLayout(self.assetBtnLayout)
        self.assetBtnLayout.addWidget(assetBtn)
        
        self.asset_btn_list.append(assetBtn)
        
        assetBtn.setFont(fontSize_H3)
        assetBtn.clicked.connect(command)
        
        if isSquare:
            assetBtn.setFixedSize(QSize(self.button_size, self.button_size))
        
        assetBtn.setVisible(isVisible)
        assetBtn.pixIcon = None

        if icon:
            assetBtn.pixIcon = icon
    
        self.Set_Btn_Color()

    def Set_Btn_Color(self, status='foreground', color=None):
        for assetBtn in self.asset_btn_list:
            icon  = assetBtn.pixIcon
            current_color = QColor(self.colors.colors_[status][0], self.colors.colors_[status][1], self.colors.colors_[status][2])
            if color:
                current_color = QColor(color[0], color[1], color[2])
                
            if icon:
                pixmapAlpha       = QPixmap(icon).scaled(self.button_size, self.button_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                colorPixmap       = QPixmap(pixmapAlpha.size())
                colorPixmap.fill(current_color)
                colorPixmap.setMask(pixmapAlpha.mask())
                
                pixIcon = QIcon()
                pixIcon.addPixmap(colorPixmap)
                assetBtn.setIcon(pixIcon)

    #===========================================================================
    # #Combobox
    #===========================================================================
    def SetComboBox(self, assetComboBoxLabel='', changeCommand=None, removeBntCommand=None):
        self.assetComboBox = QComboBox()
        self.assetComboLbl = QLabel(assetComboBoxLabel)
        self.removeItemBtn = QPushButton('x')
        self.groupLayout.addLayout(self.assetComboLayout)
        
        self.assetComboLayout.addWidget(self.assetComboLbl)
        self.assetComboLayout.addWidget(self.assetComboBox)
        self.assetComboLayout.addWidget(self.removeItemBtn)
        self.assetComboBox.currentIndexChanged.connect(changeCommand)
        self.removeItemBtn.clicked.connect(removeBntCommand)

        self.assetComboBox.setFont(fontSize_H2)
        self.assetComboLbl.setFont(fontSize_H2)
        self.removeItemBtn.setFont(fontSize_H2)
        
        self.assetComboBox.setFixedWidth(250)
        self.assetComboBox.setFixedHeight(self.button_size)
        self.removeItemBtn.setFixedSize(QSize(self.button_size, self.button_size))

    
    #===========================================================================
    # #Radio Button
    #===========================================================================
    def SetRadioButton(self, radio_list=[], tittle='', default_checked=1, slot_to_set=None, msg=''):
        self.radio_grp = Custom_Radio_Button(radio_list, tittle, default_checked, slot_to_set, msg)
        self.radio_grp.set_height(self.button_size)
        
        self.assetBtnLayout.addWidget(self.radio_grp.gBox)
    
    def Set_Radio_Label(self):
        self.radio_grp.Set_Label()

    #===========================================================================
    # #Search
    #===========================================================================
    def SetSearch(self, search_data=[], enter_searching_mode_cmd=None, update=False, placeholder=''):
        if not update:
            self.search_widget             = Custom_Search_Widget(placeholder=placeholder)
            self.groupLayout.addLayout(self.assetBtnLayout)
            self.assetBtnLayout.addWidget(self.search_widget.gBox)

        self.search_widget.search_data = search_data
        self.search_widget.SetCharNameCompleter()
        self.search_widget.enter_searching_mode_cmd = enter_searching_mode_cmd
        self.search_widget.set_height(self.button_size-2)


    #===========================================================================
    # #Functions
    #===========================================================================
    def GetName(self):
        return self.itemName.replace(' ', '')
    
    def GetLabel(self):
        return self.assetLbl.text()

    def SetAssetType(self, asset_type):
        self.asset_type = asset_type

    def SetFont(self, fontSize='fontSize_H2', fontBold=True):
        self.assetLbl.setFont(fontSize_H2)
    
    def SetColor(self, status='foreground'):
        self.setStyleSheet('QWidget {color: rgb%s}'%str(self.colors.colors_[status]))
        self.colors.current = self.colors.colors_[status]
        self.Set_Btn_Color(status=status)


    def GetColor(self, color='bdbdbd'):
        return self.assetLbl.palette().text().color()
        
    def SetBackgroundColor(self, color):
        self.widgetGrpBox.setStyleSheet('QFrame {background-color: rgb%s}'%str(self.colors.background))
        
    def GetBGColor(self, *kargs):
        return QColor(self.colors.background[0], self.colors.background[1], self.colors.background[2])

    def SetBGColor(self, color=QColor(42, 42, 42)):
        self.widgetGrpBox.setStyleSheet('QFrame {background-color: rgb(%s, %s, %s);}'%(color.red(), color.green(), color.blue()))


    #===========================================================================
    # #Events
    #===========================================================================
    def SetSelected(self):
        current_color  = (self.colors.current[0]*1.0, self.colors.current[1]*1.0, self.colors.current[2]*1.0)
        self.setStyleSheet('QWidget {color: rgb%s}'%str(current_color))
        self.Set_Btn_Color(status='current', color=current_color)


    def SetUnselected(self):
        current_color  = (self.colors.current[0]*.5, self.colors.current[1]*.5, self.colors.current[2]*.5)
        self.setStyleSheet('QWidget {color: rgb%s}'%str(current_color))
        self.Set_Btn_Color(status='current', color=current_color)
        
    def SetMousePress(self):
        self.widgetGrpBox.setStyleSheet('QFrame {background-color: rgb%s;}'%str(self.colors.mousePress))

    def SetMouseRelease(self):
        self.widgetGrpBox.setStyleSheet('QFrame {background-color: rgb%s;}'%str(self.colors.mouseRelease))
        if self.isTrigger:
            self.asset_btn_list[-1].clicked.emit()

    def SetOnMouseEnter(self):
        self.widgetGrpBox.setStyleSheet('QFrame {background-color: rgb%s; border: 0px solid black; border-radius: 5px; overflow: hidden;}'%str(self.colors.mouseEnter))

    def SetOnMouseLeave(self):
        self.widgetGrpBox.setStyleSheet('QFrame {background-color: rgb%s;}'%str(self.colors.mouseLeave))
        
    def update(self):
        self.SetProgressValue()

    def resizeEvent(self, event):
        self.asset_width = self.parent().geometry().width()
        #self.setFixedHeight(self.asset_height)
        if self.hasProgressBar:
            self.SetProgressValue()

    def closeEvent(self, event):
        self.parent().update()


    #===========================================================================
    # #Mouse Events
    #===========================================================================
    def mouseMoveEvent(self, event):        
        if not self.isDraggable:
            return
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction)
    
    def mousePressEvent(self, event):
        self.SetMousePress()

    def mouseReleaseEvent(self, event):
        self.SetMouseRelease()

    def enterEvent(self, event):
        if self.isInterative:
            self.SetOnMouseEnter()

    def leaveEvent(self, event):
        self.SetOnMouseLeave()

    def SetDraggable(self, state=False):
        self.isDraggable = state

    def SetDroppable(self, state=False):
        self.setAcceptDrops(state)
    
    
    #===========================================================================
    # #Popup menu
    #===========================================================================
    #===========================================================================
    # #Ugly code need to clean
    #===========================================================================
    def contextMenuEvent(self, event):
        if self.hasContextMenu:
            menu = QMenu(self)
            for action_label, command in self.contextMenuDict.iteritems():
                action_name   = menu.addAction(action_label)
                action_name.triggered.connect(partial(command, self.GetName()))
            
            menu.exec_(self.mapToGlobal(event.pos()))
        
    def SetContextMenu(self, contextMenuDict={}):
        self.hasContextMenu  = True
        self.contextMenuDict = contextMenuDict
    
    #===========================================================================
    # #Animations
    #===========================================================================
    def animStart(self):
        self.asset_width = self.parent().geometry().width()
        duration      = 300
        start_animation = QPropertyAnimation(self, "size", self)
        start_animation.setEasingCurve(QEasingCurve.Linear)
        start_animation.setEasingCurve(QEasingCurve.Linear)
        start_animation.setDuration(duration)
        start_animation.setStartValue(QSize(self.asset_width, self.asset_height))
        start_animation.setEndValue(QSize(self.asset_width, self.asset_height))
        start_animation.setLoopCount(1)
        start_animation.setKeyValueAt(0.5, QSize(0, self.asset_height))
        
        animTHD = Anim_Thread(start_animation)

        
        Anim_Thread_Pool.start(animTHD)
        

    def animEnd(self):
        duration      = 100
        end_animation = QPropertyAnimation(self, "size", self)
        end_animation.setEasingCurve(QEasingCurve.Linear)
        end_animation.setEasingCurve(QEasingCurve.InOutQuad)
        end_animation.setDuration(duration)
        end_animation.setStartValue(QSize(self.asset_width, self.asset_height))
        end_animation.setEndValue(QSize(0, self.asset_height))
        end_animation.finished.connect(self.close)
        
        animTHD = Anim_Thread(end_animation)
        Anim_Thread_Pool.start(animTHD)
        animTHD.start_anim()

    def animRefresh(self):
        duration=200
        animRefresh = QPropertyAnimation(self, "color", self)
        animRefresh.setEasingCurve(QEasingCurve.InQuad)
        animRefresh.setEasingCurve(QEasingCurve.InOutQuad)
        animRefresh.setDuration(duration)
        animRefresh.setLoopCount(1)
        animRefresh.setStartValue(QColor(42, 42, 42))
        animRefresh.setEndValue(QColor(42, 42, 42))
        animRefresh.setKeyValueAt(0.5, QColor(60, 65, 65))

        animRefresh.finished.connect(self.SetBGColor)

        animTHD = Anim_Thread(animRefresh)
        Anim_Thread_Pool.start(animTHD)
        animTHD.start_anim()   
        
    color = Property(QColor, GetBGColor, SetBGColor)
           
#===============================================================================
# #The assetWidget holder
#===============================================================================
class AssetListWidget(QTabWidget):
    
    def __init__(self, parent=None, tab_title='Batch.io', isStatic=False):
        super(AssetListWidget, self).__init__(parent)
        
        self.setGeometry(0, 0, 240, 0)
        self.assetWidgets     = {}
        self.tab_dict         = {}
        self.isDroppable      = True
        self.titleLbl         = QLabel(tab_title)
        self.tab_title        = tab_title
        self.animWaitingColor = False
        self.log              = None
        self.colors           = Colors()
        self.isStatic         = isStatic
        
        self.initUI()
        
    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.mainLayout)        

        self.titleLayout       = QVBoxLayout()
        self.titleLayout.addWidget(self.titleLbl)
        self.titleLayout.setContentsMargins(5, 0, 5, 0)
        self.titleLayout.setAlignment(Qt.AlignLeft)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.animWaiting()

        self.set_tab(tab_title=self.tab_title)
        self.SetFont('fontSize_H2', True)
        self.setFont(fontSize_H2)
        
        self.current_tab_tittle = self.tab_title
        self.currentChanged.connect(self.OnTabChange)
        

    def set_tab(self, tab_title='The Batcher', tab_enabled=True):
        if not tab_title in self.tab_dict.keys():
            self.tab_dict[tab_title] = {}
            
            list_grp          = QWidget()
            assetWidgetLayout = QVBoxLayout()
            assetWidgetLayout.setAlignment(Qt.AlignTop)
            assetWidgetLayout.setContentsMargins(0, 0, 0, 0)

            #===================================================================
            # #Scroll Area Properties
            #===================================================================
            scroll = QScrollArea()

            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setWidgetResizable(True)
            scroll.setWidget(list_grp)
            scroll.setFrameShape(QFrame.NoFrame)
            
            list_grp.setLayout(assetWidgetLayout)

            #===================================================================
            # #Add a tab
            #===================================================================
            tab = self.addTab(scroll, tab_title)
            self.setTabEnabled(tab, tab_enabled)
            
            self.setCurrentWidget(list_grp)

            #===================================================================
            # #Store the tab name for feature use
            #===================================================================
            self.tab_dict[tab_title]['widget'] = list_grp
                        
            
            if self.isStatic:
                self.SetTitle(self.tab_title)
                self.setTabText(0, '')
                self.tabBar().setFixedWidth(0)

    #===========================================================================
    # #Call on main tab change    
    #===========================================================================
    def OnTabChange(self, i):
        self.current_tab_tittle = self.tabText(i)


    def Get_Layout(self, type=None):
        if not type:
            type = self.current_tab_tittle
        
        if type:
            widget = self.tab_dict[type]['widget']
            
            if widget:
                return widget.layout()


    #===========================================================================
    # #Functions UI
    #===========================================================================
    def GetColor(self, *kargs):
        return self.titleLbl.palette().text()

    def SetColor(self, color=None, status='foreground'):
        palette = self.titleLbl.palette()
        palette.setColor(self.titleLbl.foregroundRole(), color)
        self.titleLbl.setPalette(palette)
        if not color:
            self.titleLbl.setStyleSheet('QLabel {color: rgb%s}'%str(self.colors.colors_[status]))

    def SetBackgroundColor(self):
        self.setStyleSheet('QFrame {background-color: rgb(255, 0, 0)}')
 
    def SetStatus(self, data):
        self.titleLbl.setText(data)
    
    def SetTitle(self, title='', alignment=Qt.AlignCenter):
        self.titleLbl.setText(title)
        self.titleLbl.setAlignment(alignment)
        if self.isStatic:
            self.mainLayout.addLayout(self.titleLayout)

    def SetFont(self, fontSize='fontSize_H2', fontBold=True):
        self.titleLbl.setFont(fontSize_H2)

    def SetAssetUnselected(self, itemName=''):
        for i in reversed(range(self.Get_Layout().count())): 
            widget = self.Get_Layout().itemAt(i).widget()
            if not itemName == widget.itemName:
                widget.SetUnselected()
            else:
                widget.SetSelected()
                self.selectedWidget = widget
    
    def UpOneLevel(self, assetWidget=None):
        return
        index = self.Get_Layout().indexOf(assetWidget)
        self.Get_Layout().removeWidget(assetWidget)
        if index == 0:
            index = -1
        self.Get_Layout().insertWidget(index-1, assetWidget)
        assetWidget.animStart()


    #===========================================================================
    # #Sistem functions
    #===========================================================================
    def AddAssetWidget(self, assetWidget=None, animate=True, type=None):
        if not assetWidget.isHeader:
            if self.animWaitingColor:
                self.animWaitingColor.stop()
                self.animWaitingColor.finished.emit()

            self.Get_Layout(type).addWidget(assetWidget)
            
            #MUST IMPROVE
            if assetWidget.GetName() in self.assetWidgets.keys() and not self.isStatic:
                self.assetWidgets[assetWidget.GetName() +'_'+ str(assetWidget.winId())] = assetWidget
            else:
                self.assetWidgets[assetWidget.GetName()] = assetWidget
    
            if animate:
                assetWidget.animRefresh()
            
            assetWidget.myLayout = self.Get_Layout(type)
    
    def Remove_Widget(self, AssetWidget):
        AssetWidget.myLayout.removeWidget(AssetWidget)
        try:
            del self.assetWidgets[AssetWidget.GetName()]
        except:
            pass
    
    
    def CleanAssetWidgets(self):
        for assetWidget in self.assetWidgets.values():
            self.Remove_Widget(assetWidget)
            assetWidget.close()
                
        if not self.isStatic:
            for type in self.tab_dict.keys():
                del self.tab_dict[type]

        self.assetWidgets = {}
            

    def CleanAssetWidgetsAnim(self):
        for assetWidget in self.assetWidgets.values():  
            assetWidget.animEnd()


    def SortByName(self, sortList=[]):
        if sortList:
            for item in reversed(sortList):
                if item in self.assetWidgets:
                    assetWidget = self.assetWidgets[item]
                    if assetWidget:
                        assetWidget.myLayout.removeWidget(assetWidget)
                        assetWidget.myLayout.insertWidget(0, assetWidget)


    def Get_sorted_by_index(self):
        layout = self.Get_Layout()

        return [layout.itemAt(i).widget() for i in range(layout.count())]


    def Set_CheckState_Toggle(self, state=False):
        for reference_widget in self.Get_sorted_by_index():
            reference_widget.Set_CheckState_Value(state)
            
    #===========================================================================
    # #Mouse events
    #===========================================================================
    def SetDroppable(self, state=False):
        self.setAcceptDrops(state)


    def dragEnterEvent(self, event):
        event.setDropAction(Qt.CopyAction)

        event.accept()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.Set_CheckState_Toggle()

    color = Property(QColor, GetColor, SetColor)
    
    #===========================================================================
    # #Animations
    #===========================================================================
    def animWaiting(self):
        duration=1000
        self.animWaitingColor = QPropertyAnimation(self, "color", self)
        self.animWaitingColor.setEasingCurve(QEasingCurve.Linear)
        self.animWaitingColor.setEasingCurve(QEasingCurve.InOutQuad)
        self.animWaitingColor.setDuration(duration)
        self.animWaitingColor.setLoopCount(20)
        self.animWaitingColor.setStartValue(self.color)
        self.animWaitingColor.setEndValue(self.color)
        self.animWaitingColor.setKeyValueAt(0.5, QColor(self.colors.loading[0], self.colors.loading[1], self.colors.loading[2]))
        self.animWaitingColor.finished.connect(self.SetColor)

        animTHD = Anim_Thread(self.animWaitingColor)
        Anim_Thread_Pool.start(animTHD)
        animTHD.start_anim()

    
    
        
#===============================================================================
# Radio button example
# CRB = Custom_Radio_Button(['Idle', 'Normal', 'High', 'Ultra'], 'Priority', 1)
# CRB.show()
#         
#===============================================================================
class Custom_Radio_Button(QFrame):
    def __init__(self, radio_list=[], tittle='', default_checked=1, slot_to_set=None, msg=''):
        super(Custom_Radio_Button, self).__init__()
        self.radio_list      = radio_list
        self.title           = tittle
        self.default_checked = default_checked
        self.slot_to_set     = slot_to_set
        self.msg             = msg
        self.radio_btn_list  = []
        
        self.initUI()

    def initUI(self):
        self.mainLayout     = QVBoxLayout(self)
        self.setLayout      = self.mainLayout
        
        self.central_layout = QHBoxLayout()
        self.gBox           = QGroupBox()
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.gBox.setToolTip(self.title)
        
        self.gBox.setLayout(self.central_layout)
        self.mainLayout.addWidget(self.gBox)
        
        self.fill_radio_btn(self.radio_list, self.title, self.default_checked)
        
    def Set_Label(self):
        self.titleLbl = QLabel(self.title)
        self.titleLbl.setFixedWidth(70)
        self.titleLbl.setFont(fontSize_H3)
        self.titleLbl.setAlignment(Qt.AlignCenter)
        self.central_layout.insertWidget(0, self.titleLbl)
        
        
    def fill_radio_btn(self, radio_list=[], tittle='', default_checked=2, msg=''):
        count = 0
        for radio_name in radio_list:
            radio = QRadioButton()
            radio.setToolTip(radio_name)
            radio.setFixedHeight(20)
            radio.clicked.connect(partial(self.Get_Current_Radio, count, self.msg))
            if count == default_checked:
                radio.setChecked(True)
            
            self.radio_btn_list.append(radio)
            self.central_layout.addWidget(radio)
            count += 1

    def set_height(self, value):
        self.gBox.setFixedHeight(value)
        
    def Get_Current_Radio(self, value, msg, *args):
        return self.slot_to_set(value, msg)
    
    def Set_Current_Radio(self, value):
        return
        

class Custom_Search_Widget(QFrame):
    def __init__(self, placeholder=''):
        super(Custom_Search_Widget, self).__init__()
        self.placeholder              = placeholder
        self.search_data              = []
        self.enter_searching_mode_cmd = None

        self.initUI()
        
    def initUI(self):
        self.mainLayout     = QVBoxLayout(self)
        self.setLayout      = self.mainLayout
        
        self.central_layout = QHBoxLayout()
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        
        self.gBox           = QGroupBox()
        self.gBox.setLayout(self.central_layout)
        
        self.search_le      = QLineEdit()
        self.search_le.setFont(fontSize_H3)
        self.search_le.setPlaceholderText(self.placeholder)

        self.search_le.textChanged.connect(self.filter)
        
        self.search_icon    = QLabel(u"\U0001F50D")
        self.search_icon.setAlignment(Qt.AlignCenter)
        self.search_icon.setFont(fontSize_H3)
        
        self.search_icon.setFixedSize(QSize(20, 20))

        self.central_layout.addWidget(self.search_le)
        self.central_layout.addWidget(self.search_icon)
        
        self.mainLayout.addWidget(self.gBox)

    def set_height(self, value):
        self.search_le.setFixedHeight(value)
        self.gBox.setFixedHeight(value+2)
    

    def filter(self):
        item_to_find = self.search_le.text()
        
        if not item_to_find in self.search_data:
            self.enter_searching_mode_cmd()
            return
        
        for found_reference in self.search_data:
            if found_reference in item_to_find:
                self.enter_searching_mode_cmd(found_reference)
        

    def SetCharNameCompleter(self):
        #=======================================================================
        # #Set the completer
        #=======================================================================
        completer = QCompleter(list(set(self.search_data)), self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_le.setCompleter(completer)
    
    
class Anim_Thread(QRunnable):
    def __init__(self, anim=None):
        QRunnable.__init__(self)

        
        self.anim = anim
        
    def start_anim(self):
        self.anim.start()
        
        
        
        
        