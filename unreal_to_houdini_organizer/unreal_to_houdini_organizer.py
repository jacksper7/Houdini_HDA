import hou  
import os


from PySide2.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem,QTextCharFormat, QTextCursor, QColor
from PySide2.QtWidgets import QMainWindow, QFileDialog, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView,QApplication, QPushButton

from PySide2.QtCore import QModelIndex,QObject, QRectF, Qt
from hutil.Qt import QtCore, QtWidgets, QtUiTools
import sys

# scriptpath = os.path.dirname(__file__)
scriptpath = os.path.dirname(__file__) 
icon = scriptpath + "/organizer.png"
# color = (255,120,0)

class unreal_to_houdini_organizer(QtWidgets.QWidget):
    # rootdir = "hello"
    
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(scriptpath + "/main.ui")###importing the ui from the qtdesigner###

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.ui)
        #############Adding Icon and Title################################## 
        self.setWindowTitle("Organizer")
        # self.ui.title_label.setPixmap(QPixmap(image))
        self.setWindowIcon(QIcon(icon))

        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.setContentsMargins(0,0,0,0)
        mainlayout.addWidget(self.ui) 
        self.setLayout(mainlayout)

        
        self.ui.browse_btn.clicked.connect(self.browsefiles)
        # rootdir = self.ui.location.text()

        self.ui.submit_btn.clicked.connect(self.submit)
        self.ui.cancel_btn.clicked.connect(self.close)
    
    
        



        
    def browsefiles(self):
        fname=QFileDialog.getExistingDirectory(self, "select folder")
        self.ui.location.setText(fname)     

    def submit(self):
        # print("pass")
        rootdir = self.ui.location.text()
        value = os.path.isdir(rootdir)
        
        if len(rootdir)!=0:
            if value==True:
                self.go(rootdir)
            else:
                hou.ui.displayMessage("The directory you seleced doesn't exist")
            # self.go(rootdir)
        else:
            hou.ui.displayMessage("Please select a directory!")
        

    def go(self,rootDir):
        fbx_main = hou.selectedNodes()
        # rootDir = r"E:\Megascan_library\Downloaded\3d"
        # rootdir = hou.ui.selectFile(file_type=hou.fileType.Directory)
        for fbx in fbx_main:
            fbx_childs = fbx.children()
            construct_node=[]
            construct_node_name=[]
            asset_code=[]
            
            for fbx_child in fbx_childs:
                if fbx_child.type().name()=="geo":
                        construct_node_name.append(fbx_child.name())
                        construct_node.append(fbx_child)
            
            for node in construct_node:
                code = node.name().split("_")
                asset_code.append(code[-3])
            dir_list = next(os.walk(rootDir))[1]
            iso_code = list( dict.fromkeys(asset_code))
            long=[]
            obj_path=[]
            not_found = []
            for code in asset_code:
                
                value = 0
                for dir in dir_list:
                    if code in dir:
                        value = 1
                        relDir = rootDir+"\\"+dir
                        relobjDir = rootDir+"\\"+dir+"\\"+code+"_LOD0.fbx"
                        long.append(relDir)
                        obj_path.append(relobjDir)
                        break
                if value==0:
                    long.append(f"NOT FOUND {code}")
                    not_found.append(code)
            not_found = list( dict.fromkeys(not_found))
            
            if len(not_found)!=0:
                not_found=','.join(str(e) for e in not_found)
                hou.ui.displayMessage(f"Some assets need to be downloaded from the Quixel bridge\nKey word: {not_found}") 
                exit()
            # print(long)    
            
            
            obj = fbx.parent()
            # print(obj)
            parent_subnet = obj.createNode("subnet","Material_Syncer")
            # for const_node_name in construct_node_name:
            #     child_setter = parent_subnet.createNode("geo",f"setup_{const_node_name}")
            hou.copyNodesTo(construct_node, parent_subnet) 
            material_hub = parent_subnet.createNode("matnet","Material_hub") 
            material_hub.moveToGoodPosition()  

            new_fbx_childs = parent_subnet.children()
            new_construct_node=[]
            new_construct_node_name=[]
            
            material_list = []
            material_list_name = []
            
            for code in iso_code:
                material_node = material_hub.createNode("principledshader::2.0","Material_"+code)
                material_list.append(material_node)
                material_list_name.append(material_node.name())
                material_node.moveToGoodPosition()
                material_node.parm("basecolor_usePointColor").set(0) 
                material_node.parm("rough").set(1)
                material_node.parm("basecolorr").set(1.0)
                material_node.parm("basecolorg").set(1.0)
                material_node.parm("basecolorb").set(1.0)
                material_node.parm("basecolor_useTexture").set(1)
                for dir in dir_list:
                    if code in dir:
                        relDir = rootDir+"\\"+dir
                        file_list = next(os.walk(relDir))[2]
                        maps = ["Albedo","Roughness","Normal","Displacement"]
                        map_path = []
                        for map in maps:
                            img = []
                            for image in file_list:
                                if map.lower() in image.lower() and ".jpg" in image.lower():
                                    img.append(image)
                            # print(img)
                            # print("_______________________")        
                            for pic in img:
                                
                                if len(img)==1:
                                    image_location = relDir+"\\"+pic
                                    map_path.append(image_location)
                                    
                                else:
                                    if "LOD0" in pic:
                                        image_location = relDir+"\\"+pic
                                        map_path.append(image_location)
                                        
                                    else:
                                        base_search = map+".jpg" 
                                        if base_search in pic:
                                            image_location = relDir+"\\"+pic
                                            map_path.append(image_location)   
                        material_node.parm("basecolor_texture").set(map_path[0])
                        material_node.parm("rough_useTexture").set(1)
                        material_node.parm("rough_texture").set(map_path[1])
                        material_node.parm("baseBumpAndNormal_enable").set(1)
                        material_node.parm("baseNormal_texture").set(map_path[2])
                        material_node.parm("dispTex_enable").set(1)
                        material_node.parm("dispTex_texture").set(map_path[3])        

            for fbx_child in new_fbx_childs:
                if fbx_child.type().name()=="geo":#No needed for if statement but a checker is always good 
                    new_construct_node_name.append(fbx_child.name())
                    new_construct_node.append(fbx_child)

            for id,node in enumerate(new_construct_node):
                node.parm("shop_materialpath").set("")
                
                child = node.children()[0]
                
                #packing the imported mesh 
                pack = node.createNode("pack","Pack")
                pack.setInput(0,child)

                #Importin file sop
                file = node.createNode("file","Megascan_Mesh")
                file.parm("file").set(obj_path[id])

                a_del = node.createNode("attribdelete","delete_default_fbx_attribs")
                a_del.parm("ptdel").set("fbx_*")
                a_del.setInput(0,file)
                
                material_sop = node.createNode("material","Material")
                for count,mat in enumerate(material_list_name):
                    mat_code = mat.split("_")
                    mat_code = mat_code[1]
                    if mat_code in obj_path[id]:
                        # print(mat_code)
                        # print(obj_path[id])
                        material_sop.parm("shop_materialpath1").set(material_list[count].path())        
                material_sop.setInput(0,a_del)

                #MatchSize sop
                match_size = node.createNode("matchsize","Match_size")
                match_size.parm("justify_y").set(1)
                match_size.setInput(0,material_sop)

                #Transform Node
                xform1 = node.createNode("xform","Adjust1")
                xform1.parm("rx").set(90)
                xform1.setInput(0,match_size)

                # xform2 = node.createNode("xform","Adjust2")
                # xform2.parm("scale").set(100)
                # xform2.setInput(0,xform1)

                #MatchSize sop
                match_size2 = node.createNode("matchsize","Match_size_2")
                match_size2.setInput(0,xform1)

                pack2 = node.createNode("pack","Pack2")
                pack2.setInput(0,match_size2)

                #copytopoints
                copytopoints = node.createNode("copytopoints::2.0","Copy_to_points")
                copytopoints.setInput(0,pack2)
                copytopoints.setInput(1,pack)

                unpack = node.createNode("unpack","unpack")
                unpack.setInput(0,copytopoints)

                null = node.createNode("null","Out")
                null.setInput(0,unpack)
                null.setDisplayFlag(True)
                null.setRenderFlag(True)

                node.layoutChildren()     
                self.close()                      
def show():
    dialog = unreal_to_houdini_organizer()
    dialog.setParent(hou.qt.floatingPanelWindow(None), QtCore.Qt.Window)
    dialog.show()
        





             
                                 
                
                        
                            
                




  


            