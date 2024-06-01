import hou
import os
from hutil.Qt import QtCore, QtWidgets, QtUiTools

scriptpath = os.path.dirname(__file__) 
print(scriptpath)


class GeoSheet(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        #    Load UI  

        self.setMinimumSize(800,400)
        loader_ui = QtUiTools.QUiLoader()
        self.ui = loader_ui.load(scriptpath + "/main.ui")

        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.setContentsMargins(0,0,0,0)
        mainlayout.addWidget(self.ui) 
        self.setLayout(mainlayout)
        
        
def run():
    dialog = GeoSheet()
    dialog.setParent(hou.qt.floatingPanelWindow(None), QtCore.Qt.Window)
    dialog.show()
   