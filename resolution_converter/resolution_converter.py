import hou      
import os.path   
class resolution_converter():
    def method_select(buttons,sel_method):
                                KKKK = (1,0,0)
                                KK = (0,1,1)
                                K = (1,1,0) 
                                reso = ["4K","2K","1K"]
                                
                                method = buttons[sel_method]
                                method_splitted=method.split()

                                frm = method_splitted[0]
                                to = method_splitted[2]
                                sel_reso = reso.index(to)
                                Cd = [KKKK,KK,K]
                                color = Cd[sel_reso]
                                ft = [frm,to,color]
                                if sel_method==6:
                                    exit()
                                return ft
    
    mat_hubs = hou.selectedNodes()
    buttons = ("4K to 2K", "4K to 1K","2K to 4K","2K to 1K","1K to 4K","1K to 2K","Cancel")
    selected_method = hou.ui.displayCustomConfirmation("Which conversion is needed?", buttons=buttons)
    for mat_hub in mat_hubs:
        mat_hub_childs = mat_hub.children()
        
        for mat_hub_child in mat_hub_childs:
            if mat_hub_child.type().name()=="subnet":
                mtlx_childs = mat_hub_child.children()
                for mtlx_child in mtlx_childs:
                    if mtlx_child.type().name()=="mtlximage":
                        path = mtlx_child.parm("file").eval()
                        if "8K" in path:
                            path_splited = path.split("/")
                            if len(path_splited)==1:
                                path_splited = path.split("\\")
                            fourk = ["Thumbs","4k"] 
                            twok = ["Thumbs","2k"]
                            # twok = ["Thumbs","2k"]
                            onek = ["Thumbs","1k"]
                            path_splited.insert(-1,"Thumbs")
                            path_splited.insert(-1, "1K")
                            path_splited[-1] = path_splited[-1].replace("4K","1K")
                            # print(path_splited)
                            gap = "/"
                            path_corrected = gap.join(path_splited)
                            chk_file = os.path.isfile(path_corrected)
                            
                            if chk_file is False:
                                path_corrected = path_corrected.replace("exr","jpg")
                                chk_file = os.path.isfile(path_corrected)
                            if chk_file is True:
                                mtlx_child.parm("file").set(path_corrected)
                                mtlx_child.setColor(hou.Color((1,0,0)))
                        elif "1K" or "4K" or "2K" in path:  
                            
                            
                            
                            x=method_select(buttons,selected_method)
                            
                            
                            path_splited = path.split("/")
                            path_splited[-2] = x[1]
                            image_file=path_splited[-1].replace(x[0],x[1])
                            path_splited[-1] =  image_file
                            
                            gap = "/"
                            path_corrected = gap.join(path_splited)
                           
                            chk_file = os.path.isfile(path_corrected)
                            
                            if chk_file is False:
                                path_corrected = path_corrected.replace("exr","jpg")
                                chk_file = os.path.isfile(path_corrected)
                            if chk_file is True:
                                mtlx_child.parm("file").set(path_corrected)
                                mtlx_child.setColor(hou.Color(x[2]))
                            
                            
                        
                        
                             
    
    
    