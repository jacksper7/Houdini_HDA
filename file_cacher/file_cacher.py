import hou
import os

class file_cacher():

    GEO_PATH_compressed = "$GEO/"
    GEO_PATH = hou.expandString(GEO_PATH_compressed)
    OUTPUT = "$GEO/$OS/v00`chs('version')`/$OS.`pythonexprs('round(hou.frame()/hou.pwd().evalParm('f3'),1)')`.bgeo.sc"

    sel_node = hou.selectedNodes()[0]
    # print(hou.ui.readInput("Cache Name"))
    cache_b_name = ((hou.ui.readInput("Cache Name")[1]).upper())


    dirs =os.walk(GEO_PATH).__next__()[1] #this command will give thge folders that were inside the GEO folder (this is used to avoid overlapping file names)

    if " " in cache_b_name:
        cache_b_name = cache_b_name.replace(" ", "_")   # this will insert _ in the empyty spaces

    if cache_b_name in dirs:
        hou.ui.displayMessage("this name is already exist in cache")
        exit()
    elif cache_b_name == "":
        hou.ui.displayMessage("please provide a name to cache the file")
        exit()

        

    
    parent = sel_node.parent()
    null_before = parent.createNode("null","TO_CACHE_"+cache_b_name)
    null_before.setUserData('nodeshape', 'circle')
    null_before.setColor(hou.Color((0.1,0.1,0.1)))
    file_read = parent.createNode("filecache::2.0","FOR_CACHE_"+cache_b_name)
    file_read.setColor(hou.Color((0.5,0.5,0.5)))
    null_after = parent.createNode("null","CACHED_"+cache_b_name)
    null_after.setUserData('nodeshape', 'circle')
    null_after.setColor(hou.Color((0.1,0.1,0.1)))

    null_after.setInput(0,file_read)
    file_read.setInput(0,null_before)
    null_before.setInput(0,sel_node)


    null_before.moveToGoodPosition() 
    file_read.moveToGoodPosition()
    null_after.moveToGoodPosition() 
    # parent.layoutChildren()
    # summa.setUserData('nodeshape', 'circle')
    file_read.parm("sopoutput").deleteAllKeyframes()
    # create node in OUT context 

    rop = hou.node("/out")

    rop_cache = rop.createNode("geometry",cache_b_name)
    rop_cache.parm("soppath").set(null_before.path())
    rop_cache.parm("version").set(1)

    file_read.parm("sopoutput").set(rop_cache.parm("sopoutput"))
    rop_cache.parm("version").set(file_read.parm("version"))
    rop_cache.moveToGoodPosition()
    # Setting Display and render Flag 
    null_after.setDisplayFlag(True)
    null_after.setRenderFlag(True)
    exit()
