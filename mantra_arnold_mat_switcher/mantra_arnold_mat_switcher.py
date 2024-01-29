import hou 


def mat_con():
    assets = hou.selectedNodes()
    for asset in assets:

        obj_child = asset.children()
        matcount = 0
        for child in obj_child:
            if ( child.type().name())== "matnet":
                matcount+=1
                material_node = child
            elif (child.type().name())== "geo":
                geo_node = child

        if matcount ==0:
            hou.ui.displayMessage("No Material Network Found")
            exit()
        elif matcount ==1:
            buttons = ("Mantra to Arnold", "Arnold to Mantra","Cancel")
            selected_method = hou.ui.displayCustomConfirmation("Which conversion is needed?", buttons=buttons, default_choice=2)
            if selected_method==2:
                exit()
            elif selected_method==1:
                # hou.ui.displayMessage("Coming Soon")
                # exit()
                mantra_material_hub = asset.createNode("matnet", "Mantra_Material")
                mantra_shader = mantra_material_hub.createNode("principledshader::2.0")
                material_node_path= material_node.path()
                mat_children = material_node.children()[0].children()
                for child in mat_children:
                    exist_material = (child.type().name())
                    if "arnold::standard_surface"== exist_material:
                        albedo_node = child.input(1)
            elif selected_method==0:
                new_material_node = asset.createNode("matnet", "Arnold_Material")
                material_node_path= material_node.path()
                mat_children = material_node.children()
                material_child_list_type = []
                material_child_list = []
                # mantra_mat_build =
                for child in mat_children:
                    exist_material = (child.type().name())
                   #  print(exist_material)
                    if "principledshader::2.0"== exist_material:
                        mantra_mat_build = child
                    material_child_list.append(child)
                    material_child_list_type.append(exist_material)
                if "arnold_materialbuilder" in material_child_list_type:
                    hou.ui.displayMessage("You already have a arnold material in your material builder")
                    exit()
                if "principledshader::2.0" in material_child_list_type:
                    mantra_mat_build_name = mantra_mat_build.name()
                    material_node.setName("Mantra_Shader"+mantra_mat_build_name)
                    material_node.setColor(hou.Color((0,0,0)))

                    arnold_build = new_material_node.createNode("arnold_materialbuilder", "Nagoor_"+mantra_mat_build_name)
                    arnold_output = arnold_build.children()[0]
                    std_surface = arnold_build.createNode("arnold::standard_surface")
                    std_surface.moveToGoodPosition()

                    arnold_output.setInput(0,std_surface)
                    # Add code to modify contained geometries.
                    # Use drop down mensfdgu to select example
                    #  textures = mantra_mat_build.glob("*texture")
                    # print(textures)

                    tupl = mantra_mat_build.parms()

                    input_name = []
                    input_name_path = []

                    for tup in tupl:
                       tup_name = tup.name()
                       if "_useTexture" in tup_name:
                          checker= tup_name.endswith("_useTexture")
                          if checker == True:

                                checker_val = mantra_mat_build.evalParm(tup_name)
                                if checker_val == 1:

                                   # if "_texture" in tup_name:
                                   #     # tuups= tup_name.endswith("_useTexture")
                                   #     # if tuups==True:
                                   #     print(tup_name)
                                   tuupss = tup_name.split("_")[0]+"_texture"
                                   input_name.append(tuupss)
                       if tup_name == "dispTex_enable":
                          checker_val_disp = mantra_mat_build.evalParm(tup_name)
                          if checker_val_disp == 1:
                                disp_tuupss = tup_name.split("_")[0]+"_texture"
                                input_name.append(disp_tuupss)
                    for name in input_name:
                       t_node = arnold_build.createNode("arnold::image",name.split("_")[0])
                       path = mantra_mat_build.evalParm(name).split(".")[0]+".jpg"
                       if t_node.name() == "baseNormal":

                          # print(path)
                          t_node.parm("filename").set(path)
                          n_map = arnold_build.createNode("arnold::normal_map")
                          b_map = arnold_build.createNode("arnold::bump2d")
                          b_map.setInput(2, n_map)
                          n_map.setInput(0, t_node)
                          std_surface.setNamedInput("normal", b_map, "vector")
                       elif t_node.name() == "dispTex":
                          t_node.parm("filename").set(path)
                          # print(path)
                          mult = arnold_build.createNode("arnold::multiply")
                          range = arnold_build.createNode("arnold::range")
                          mult.parmTuple("input2").set([5,5,5])
                          range.parm("input_max").set(2)
                          range.parm("output_min").set(-0.5)
                          range.parm("output_min").set(0.5)
                          mult.setInput(0, t_node, 0)
                          range.setInput(0, mult, 0)
                          arnold_output.setInput(1, range, 0)
                       elif t_node.name() == "rough":
                          t_node.parm("filename").set(path)
                          # print(path)
                          std_surface.setNamedInput("specular_roughness", t_node, "rgba")
                       elif t_node.name() == "basecolor":
                          t_node.parm("filename").set(path)
                          # print(path)
                          std_surface.setNamedInput("base_color", t_node, "rgba")
                    arnold_build.layoutChildren()
        # geo_children = geo_node.children()
        # for child in geo_children:
        #       if ( child.type().name())== "material":
        #           arnold_build_path = arnold_build.path()
        #           child.parm("shop_materialpath1").set(arnold_build_path)
        # asset.layoutChildren()



               