import hou

nodes = hou.selectedNodes()
color = hou.ui.selectColor()

if (len(nodes)==0):
    hou.ui.displayMessage("please select a node")
    
else:
    for i in nodes:
        i.setColor(color)
   