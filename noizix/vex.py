import hou 
import os
from PySide2.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem
from PySide2.QtCore import QModelIndex
from hutil.Qt import QtCore, QtWidgets, QtUiTools
import sys
import vex 

# scriptpath = os.path.dirname(__file__)
scriptpath = "C:/Users/nagoo/OneDrive/Documents/houdini19.0/scripts/python/jks/noizix"
image = scriptpath + "/noise5.png"
icon = scriptpath + "/noise4.png"


class noizix(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(scriptpath + "/main.ui")###importing the ui from the qtdesigner###

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.ui)
        #############Adding Icon and Title################################## 
        self.setWindowTitle("Noizix v1.0(beta)")
        self.ui.title_label.setPixmap(QPixmap(image))
        self.setWindowIcon(QIcon(icon))


        #################### getting Geo Attribs###########################
        self.sel_nodes()## Calling the Selected Node fucton ##
        self.ui.sel_nodelbl.setText("Selected Node: " + self.sel_nodes().name())
        self.node = self.sel_nodes()
        self.node_geo = self.node.geometry()
        self.basic_function = ["Addition","Subraction","Multiplication","Division"] 
        self.attribs = []
        self.attribs_name = []
        self.point_values = []
        self.group = ["point","primitive","vertices"]
        self.type = ["float","vector2","vector","vector4"]
        self.v_att_suffix = ['x','y','z']
        self.p_att_suffix = ['0','1','2','3']
        self.u_att_suffix = ['u','v']
        self.splited_attrib = []
        self.pt_attribs = []
        self.pt_attribs_name = []
        self.pr_attribs = []
        self.pr_attribs_name = []
        self.vx_attribs = []
        self.vx_attribs_name = []
        self.ptf = []
        self.pt2 = []
        self.pt3 = []
        self.pt4 = []
        self.prf = []
        self.pr2 = []
        self.pr3 = []
        self.pr4 = []
        self.vf = []
        self.v2 =[]
        self.v3 = []
        self.v4 = []
        self.geo_datas = [
            {
                "point":[
                    {"float":self.ptf},
                    {"vector2":self.pt2},
                    {"vector":self.pt3},
                    {"vector4":self.pt4}
                ]
            },
            {
                "vertices":[
                    {"float":self.vf},
                    {"vector2":self.v2},
                    {"vector":self.v3},
                    {"vector4":self.v4}
                ]
            },
            {
                "primitive":[
                    {"float":self.prf},
                    {"vector2":self.pr2},
                    {"vector":self.pr3},
                    {"vector4":self.pr4}
                ]
            }
        ]

        for datas in self.geo_datas:
            for key in datas:
                self.ui.grp_combo.addItem(key.capitalize())
            self.ui.grp_combo.setCurrentIndex(-1)    
        self.get_all_attribs()##Calling Get Attrib Function##
               
        for func in self.basic_function:##adding basic function##
            self.ui.list_basic_func.addItem(func)

        self.ui.grp_combo.currentTextChanged.connect(self.get_type_combo)
        self.ui.type_combo.currentTextChanged.connect(self.get_attrib) 
        self.ui.attrib_split.clicked.connect(self.split_attrib)   
        self.ui.to_create_attrib.clicked.connect(self.enable_create_tab)
        self.ui.type_combo.currentTextChanged.connect(self.list_all_attrib)
        self.ui.attrib_combo.currentTextChanged.connect(self.seg_attribs)

        ### adding splitted attrib data###
        self.ui.attrib_splitted.setEnabled(False)
        
        self.ui.attrib_split.setEnabled(False)
        self.ui.rad_float.setEnabled(False)
        self.ui.rad_vector2.setEnabled(False)
        self.ui.rad_vector.setEnabled(False)
        self.ui.rad_vector4.setEnabled(False)
        self.ui.export_attrib_enter.setPlaceholderText("Enter the Name of the Attribute")
        self.ui.export_attrib_enter.setEnabled(False)
        self.ui.create_attrib.setEnabled(False)

        # print(self.geo_datas)

        
        
        self.setLayout(mainLayout)



    def sel_nodes(self): # For getting info of the Selected Nodes
        try:
            return hou.selectedNodes()[0]
            
        except:
            hou.ui.displayMessage("Please select some nodes and try again")
            sys.exit(0)   

    def get_all_attribs(self):
        self.get_point_attribs()
        self.get_vertices_attribs()
        self.get_primitive_attribs()

    def get_point_attribs(self):
        point_attribs=self.node_geo.pointAttribs()
        # print(point_attribs[0].name())
        for point_attrib in point_attribs:
            if point_attrib!= None:
                pt_attr = point_attrib
                pt_attr_name = point_attrib.name().lower()
                self.pt_attribs.append(pt_attr)
                self.pt_attribs_name.append(pt_attr_name)
                if pt_attr.size() == 1:
                    point_float_dict = {}
                    pt_float_segregated = []
                    pt_float_segregated.append(pt_attr_name)
                    point_float_dict[pt_attr_name] = pt_float_segregated
                    self.ptf.append(point_float_dict)
                elif pt_attr.size() == 2:
                    point_vector2_dict = {}
                    point_vector2_segeregated = []
                    for i in range(pt_attr.size()):
                        point_vector2_segeregated.append(pt_attr_name+"."+self.u_att_suffix[i])
                    point_vector2_dict[pt_attr_name] = point_vector2_segeregated 
                    self.pt2.append(point_vector2_dict)
                elif pt_attr.size() == 3:
                    point_vector_dict = {}
                    point_vector_segeregated = []
                    for i in range(pt_attr.size()):
                        point_vector_segeregated.append(pt_attr_name+"."+self.v_att_suffix[i])
                    point_vector_dict[pt_attr_name] = point_vector_segeregated    
                    self.pt3.append(point_vector_dict)  
                elif pt_attr.size() == 4:
                    point_vector4_dict = {}
                    point_vector4_segeregated = []
                    for i in range(pt_attr.size()):
                        point_vector4_segeregated.append(pt_attr_name+"."+self.p_att_suffix[i])
                    point_vector4_dict[pt_attr_name] = point_vector4_segeregated    
                    self.pt4.append(point_vector4_dict)  
                       
    def get_vertices_attribs(self):
        vx_attribs=self.node_geo.vertexAttribs()
        # print(point_attribs[0].name())
        for vx_attrib in vx_attribs:
            if vx_attrib!= None:
                vx_attr = vx_attrib
                vx_attr_name = vx_attrib.name().lower()
                self.vx_attribs.append(vx_attr)
                self.vx_attribs_name.append(vx_attr_name)
                if vx_attr.size() == 1:
                    vertices_float_dict = {}
                    vx_float_segregated = []
                    vx_float_segregated.append(vx_attr_name)
                    vertices_float_dict[vx_attr_name] = vx_float_segregated
                    self.vf.append(vertices_float_dict)
                elif vx_attr.size() == 2:
                    vertices_vector2_dict = {}
                    vx_vector2_segeregated = []
                    for i in range(vx_attr.size()):
                       vx_vector2_segeregated.append(vx_attr_name+"."+self.u_att_suffix[i])
                    vertices_vector2_dict[vx_attr_name] = vx_vector2_segeregated 
                    self.v2.append(vertices_vector2_dict)
                elif vx_attr.size() == 3:
                    vertices_vector_dict = {}
                    vx_vector_segeregated = []
                    for i in range(vx_attr.size()):
                       vx_vector_segeregated.append(vx_attr_name+"."+self.v_att_suffix[i])
                    vertices_vector_dict[vx_attr_name] = vx_vector_segeregated 
                    self.v3.append(vertices_vector_dict) 
                elif vx_attr.size() == 4:
                    vertices_vector4_dict = {}
                    vx_vector4_segeregated = []
                    for i in range(vx_attr.size()):
                       vx_vector4_segeregated.append(vx_attr_name+"."+self.p_att_suffix[i])
                    vertices_vector4_dict[vx_attr_name] = vx_vector4_segeregated 
                    self.v4.append(vertices_vector4_dict)
    def get_primitive_attribs(self)   :
        prim_attribs=self.node_geo.primAttribs()
        # print(point_attribs[0].name())
        for prim_attrib in prim_attribs:
            if prim_attrib!= None:
                pr_attr = prim_attrib
                pr_attr_name = prim_attrib.name().lower()
                self.pr_attribs.append(pr_attr)
                self.pr_attribs_name.append(pr_attr_name)
                if pr_attr.size() == 1:
                    prim_float_dict = {}
                    pr_float_segregated = []
                    pr_float_segregated.append(pr_attr_name)
                    prim_float_dict[pr_attr_name] = pr_float_segregated
                    self.prf.append(prim_float_dict)
                elif pr_attr.size() == 2:
                    prim_vector2_dict = {}
                    pr_vector2_segeregated = []
                    for i in range(pr_attr.size()):
                       pr_vector2_segeregated.append(pr_attr_name+"."+self.u_att_suffix[i])
                    prim_vector2_dict[pr_attr_name] = pr_vector2_segeregated 
                    self.pr2.append(prim_vector2_dict)
                elif pr_attr.size() == 3:
                    prim_vector_dict = {}
                    pr_vector_segeregated = []
                    for i in range(pr_attr.size()):
                       pr_vector_segeregated.append(pr_attr_name+"."+self.v_att_suffix[i])
                    prim_vector_dict[pr_attr_name] = pr_vector_segeregated 
                    self.pr3.append(prim_vector_dict)  
                elif pr_attr.size() == 4:
                    prim_vector4_dict = {}
                    pr_vector4_segeregated = []
                    for i in range(pr_attr.size()):
                       pr_vector4_segeregated.append(pr_attr_name+"."+self.p_att_suffix[i])
                    prim_vector4_dict[pr_attr_name] = pr_vector4_segeregated 
                    self.pr4.append(prim_vector4_dict)  

    def get_type_combo(self):
        if self.ui.type_combo.count() == 0:
            grp_parent = self.ui.grp_combo.currentText().lower()
            for datas in self.geo_datas:
                for key in datas:
                    if key == grp_parent:
                        key_value = datas[key]
                        for attribs in key_value:
                            for attrib_key in attribs:
                                self.ui.type_combo.addItem(attrib_key)
        self.ui.type_combo.setCurrentIndex(-1) 
        self.ui.attrib_split.setChecked(False)
        self.ui.attrib_split.setEnabled(False)

    def get_attrib(self):
        if self.ui.type_combo.count()==4:
            if self.ui.type_combo.currentIndex() != -1:
                self.ui.attrib_combo.clear()
                for data in self.geo_datas:
                    for key in data:
                        if key == self.ui.grp_combo.currentText().lower():
                            for type in data[key]:
                                for type_name in type:
                                    if type_name == self.ui.type_combo.currentText().lower():
                                        for attrib in type[type_name]:
                                            self.ui.attrib_combo.addItem((list(attrib.keys())[0]))             
                self.ui.attrib_combo.setCurrentIndex(-1) 
            if self.ui.type_combo.currentText() ==self.type[0]:
                self.ui.attrib_splitted.clear()
                self.ui.attrib_split.setChecked(False)
                self.ui.attrib_split.setEnabled(False)        
            if self.ui.type_combo.currentIndex()!=-1:
                if self.ui.type_combo.currentIndex()!=0:
                    self.ui.attrib_split.setEnabled(True)
        if self.ui.type_combo.currentIndex()==-1:
            self.ui.attrib_combo.clear()    
        
            
    def split_attrib(self):
        if self.ui.attrib_split.isChecked():
            self.ui.attrib_splitted.setEnabled(True)
            if self.ui.attrib_splitted.count() == 0:
                grp_parent = self.ui.grp_combo.currentText().lower()
                grp_type = self.ui.type_combo.currentText().lower()
                attrib = self.ui.attrib_combo.currentText().lower()
                for datas in self.geo_datas:
                    for key in datas:
                        if key == grp_parent:
                            key_value = datas[key]
                            for attribs in key_value:
                                for attrib_key in attribs:
                                    if attrib_key == grp_type:
                                        list_attribs = attribs[attrib_key]
                                        for attribs in list_attribs:
                                            if attrib == list(attribs.keys())[0]:
                                                seg_attrib = list(attribs.values())[0]
                                                self.ui.attrib_splitted.addItems(seg_attrib)
                                        

            self.ui.attrib_splitted.setCurrentIndex(-1)
            

        else:
            self.ui.attrib_splitted.setEnabled(False)    

    def seg_attribs(self):
        if self.ui.attrib_split.isChecked():
            self.ui.attrib_splitted.clear()
            self.split_attrib()

    def enable_create_tab(self):
        if self.ui.to_create_attrib.isChecked():
            self.ui.rad_float.setEnabled(True)
            self.ui.rad_vector2.setEnabled(True)
            self.ui.rad_vector.setEnabled(True)
            self.ui.rad_vector4.setEnabled(True)
            self.ui.export_attrib_enter.setEnabled(True)
            self.ui.create_attrib.setEnabled(True)
        else:
            self.ui.rad_float.setEnabled(False)
            self.ui.rad_vector2.setEnabled(False)
            self.ui.rad_vector.setEnabled(False)
            self.ui.rad_vector4.setEnabled(False)
            self.ui.export_attrib_enter.setEnabled(False)
            self.ui.create_attrib.setEnabled(False)   

    def list_all_attrib(self):
        if self.ui.type_combo.count()==4:
            if self.ui.type_combo.currentIndex() != -1:
                self.ui.list_attrib.clear()
                for data in self.geo_datas:
                            for key in data:
                                if key == self.ui.grp_combo.currentText().lower():
                                    for type in data[key]:
                                        for type_name in type:
                                            if type_name == self.ui.type_combo.currentText().lower():
                                                for attrib in type[type_name]:
                                                    self.ui.list_attrib.addItem(list(attrib.keys())[0])
            
        
        
        if self.ui.type_combo.currentIndex()==-1:
                self.ui.list_attrib.clear()
        
        
                           

def show():
    dialog = noizix()
    dialog.setParent(hou.qt.floatingPanelWindow(None), QtCore.Qt.Window)
    dialog.show()

  