#===============================================================================
# Autor: Rosenio Pinto
# e-mail: kenio3d@gmail.com
#===============================================================================

#===============================================================================
# Class thats handle the batch widget settings
# This class must be improved
# In Progress
#===============================================================================
from SystemConfig import *

class Batch_Widget_Settings_UI(QDialog):
    
    def __init__(self, batch_widget=None):
        super(Batch_Widget_Settings_UI, self).__init__()
        self.batch_widget = batch_widget
        
        self.key_val_list = {}
        
        self.initUI()
    
    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)

        self.central_layout = QHBoxLayout()
        self.side_layout    = QVBoxLayout()
        self.side_layout.setAlignment(Qt.AlignTop)

        self.setParent(self.batch_widget.parent())
        self.setWindowFlags(Qt.Tool)
        self.setWindowTitle(self.batch_widget.GetLabel() +' '+ 'Settings - {KEY : VALUE}')
        
        self.setGeometry(300, 300, 600, 500)

        self.settings_layout = QVBoxLayout()
        self.settings_layout.setContentsMargins(5, 5, 5, 5)
        self.settings_layout.setAlignment(Qt.AlignTop)
        
        
        #===================================================================
        # #self.scroll Area Properties
        #===================================================================
        
        list_grp    = QWidget()
        list_grp.setFont(AW.fontSize_H2)
        list_grp.setLayout(self.settings_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(list_grp)

        for key, val in self.batch_widget.settings.iteritems():
            self.add_setting_field(key, val)

        button_layout  = QHBoxLayout()
        self.updateBtn = QPushButton('Save')
        self.newBtn    = QPushButton('New')
        self.saveBtn   = QPushButton('Save To File')
        self.loadBtn   = QPushButton('Load From File')
        self.cancelBtn = QPushButton('Cancel')
        
        self.side_layout.addWidget(self.updateBtn)
        self.side_layout.addWidget(self.newBtn)
        
        button_layout.addWidget(self.saveBtn)
        button_layout.addWidget(self.loadBtn)
        button_layout.addWidget(self.cancelBtn)
        
        button_layout.setAlignment(Qt.AlignBottom)

        self.updateBtn.clicked.connect(self.update_settings)
        self.newBtn.clicked.connect(self.add_setting_field)
        self.saveBtn.clicked.connect(self.writeToFile)
        self.loadBtn.clicked.connect(self.readFromFile)
        self.cancelBtn.clicked.connect(self.close)

        
        self.central_layout.addWidget(self.scroll)
        self.central_layout.addLayout(self.side_layout)
        
        self.main_layout.addLayout(self.central_layout)
        self.main_layout.addLayout(button_layout)
        
        
        self.show()
    
    #===========================================================================
    # #Add the variable key and value to ui
    #===========================================================================
    def add_setting_field(self, key='', val=None):
        setting_grp_layout = QHBoxLayout()
        setting_grp_layout.setContentsMargins(2, 2, 2, 2)
        setting_grp_layout.setAlignment(Qt.AlignTop)
        
        key_value_widget = QFrame()
        key_value_widget.setLayout(setting_grp_layout)
        
        key_layout = QHBoxLayout()
        val_layout = QHBoxLayout()
        
        key_layout.setContentsMargins(1, 1, 1, 1)
        val_layout.setContentsMargins(2, 2, 2, 2)
                
        key_grp = QFrame()
        val_grp = QFrame()
        
        key_grp.setFixedHeight(32)
        val_grp.setFixedHeight(32)
        
        key_grp.setFixedWidth(150)
        
        key_grp.setFrameShape(QFrame.StyledPanel)
        val_grp.setFrameShape(QFrame.StyledPanel)
        
        key_grp.setLayout(key_layout)
        val_grp.setLayout(val_layout)
        
        key_widget = QLineEdit(str(key))
        
        if val == None:
            value_types = ['CHOOSE A VALUE TYPE', 'string', 'dict', 'list', 'number', 'bool'] 
            val_widget_combo  = QComboBox()
            for val_type in value_types:
                val_widget_combo.addItem(val_type)
            
            val_widget_combo.currentIndexChanged.connect(partial(self.choosed_type, val_layout, val_widget_combo, key_widget))
            
            val_layout.addWidget(val_widget_combo)

        else:
            #String
            if isinstance(val, (str, unicode)):
                val_widget         = QLineEdit(str(val))
                val_widget.my_type = 1
                
            #Dict
            elif isinstance(val, dict):
                val_widget         = QLineEdit(str(val))
                val_widget.my_type = 2
            
            #List
            elif isinstance(val, list):
                val_widget = QComboBox()
                items      = [str(item) for item in val]
                val_widget.addItems(items)
                val_widget.setEditable(True)
                
                val_widget.my_type = 3
            
            #Bool    
            elif isinstance(val, bool):
                val_widget     = QCheckBox()
                val_widget.setChecked(val)
                val_widget.my_type = 5
                
            #Number
            elif isinstance(val, (int, float)):
                val_widget         = QLineEdit(str(val))
                val_widget.my_type = 4

            else:
                print 'Value not valid', val, type(val)
                val_widget = None
            
            #Add the val widget to be edited
            if val_widget:
                val_layout.addWidget(val_widget)
                self.key_val_list[key_widget] = val_widget
                
        
        key_layout.addWidget(key_widget)

        remove_btn = QPushButton('x')
        remove_btn.setFont(AW.fontSize_H3)
        remove_btn.setFixedSize(QSize(16 , 16))
        remove_btn.clicked.connect(partial(self.remove, key_widget, key_value_widget))

        setting_grp_layout.addWidget(key_grp)
        setting_grp_layout.addWidget(val_grp)
        
        setting_grp_layout.addWidget(remove_btn)
        
        
        self.settings_layout.addWidget(key_value_widget)
    
    
    #===========================================================================
    # #Handle the key value to be edited
    #===========================================================================
    def choosed_type(self, val_layout, val_widget_combo, key_widget, *args):
        val_type = args[0]
        
        if not val_type == 0:
            #String
            if val_type == 1:
                val_widget         = QLineEdit()
                val_widget.my_type = 1
            
            #Dict
            elif val_type == 2:
                val_widget         = QLineEdit('{}')
                val_widget.my_type = 2
            
            #List
            elif val_type == 3:
                val_widget         = QComboBox()
                val_widget.my_type = 3
                val_widget.setEditable(True)
            
            #Number
            elif val_type == 4:
                val_widget         = QLineEdit()
                val_widget.my_type = 4
            
            #Bool
            elif val_type == 5:
                val_widget         = QCheckBox()
                val_widget.my_type = 5
    
    
            val_widget_combo.close()
            val_layout.insertWidget(0, val_widget)
        
        self.key_val_list[key_widget] = val_widget

    
    #===========================================================================
    # #Put the settings on the widget
    #===========================================================================
    def update_settings(self):
        
        try:
            for key_widget, val_widget in self.key_val_list.iteritems():
    
                key = key_widget.text()
                #String
                if val_widget.my_type == 1:
                    val =  str(val_widget.text()) 
                
                #Dict
                elif val_widget.my_type == 2:
                    val = eval(val_widget.text())
                
                #List
                elif val_widget.my_type == 3:
                    val = []
                    for i in range(val_widget.count()):
                        try:
                            item_val = eval(val_widget.itemText(i))
                        except:
                            item_val = val_widget.itemText(i)
                    
                        val.append(item_val)
                
                #Number
                elif val_widget.my_type == 4:
                    val = eval(val_widget.text())
            
                #Bool
                elif val_widget.my_type == 5:
                    val = val_widget.isChecked()
                
                
                #===================================================================
                # #Update the batch widget settings
                #===================================================================
                self.batch_widget.settings[str(key)] = val
            
            print "Batch Widget [ %s ] was updated."%self.batch_widget.GetLabel()
            pprint(self.batch_widget.settings)
            
            self.close()
            
        except Exception, e:
            print e
            print 'Failed to update settings.'
            del self.key_val_list[key_widget]

        
    def remove(self, key_widget, key_val_widget):
        key = str(key_widget.text())
        
        key_val_widget.close()

        #=======================================================================
        # #remove the setting from batch widget settings
        #=======================================================================
        if key_widget in self.key_val_list.keys():
            del self.key_val_list[key_widget]
        
        if key in self.batch_widget.settings:
            del self.batch_widget.settings[key] 
            

    #=======================================================================
    # """ Read settings from a file. """
    #=======================================================================
    def readFromFile(self):
        filename = QFileDialog.getOpenFileName(self, "Open json file", dir=Get_Project(), filter='Json files (*.json)')
        
        with open(filename[0], "r") as settings_file:
            settings_data = json.load(settings_file)

        self.batch_widget.settings = settings_data
        
        self.refresh()
        

    #=======================================================================
    # """ Save settings to a file. """
    #=======================================================================
    def writeToFile(self):
        filename = QFileDialog.getSaveFileName(self, "Save json file", dir=Get_Project(), filter='Json files (*.json)')
        
        with open(filename[0], "w") as settings_file:
            json.dump(self.batch_widget.settings, settings_file)
  
    
    #===========================================================================
    # #Refresh the UI
    #===========================================================================
    def refresh(self):
        for key_widget, val_widget in self.key_val_list.iteritems():
            key_widget.parent().parent().close()
            
            
        self.key_val_list = {}


        for key, val in self.batch_widget.settings.iteritems():
            self.add_setting_field(key, val)
        

            