
 ______                                                                    ________         
/      |                                                                  /        |        
$$$$$$/  _______   __     __  ______    ______    _______   ______        $$$$$$$$/__    __ 
  $$ |  /       \ /  \   /  |/      \  /      \  /       | /      \       $$ |__  /  \  /  |
  $$ |  $$$$$$$  |$$  \ /$$//$$$$$$  |/$$$$$$  |/$$$$$$$/ /$$$$$$  |      $$    | $$  \/$$/ 
  $$ |  $$ |  $$ | $$  /$$/ $$    $$ |$$ |  $$/ $$      \ $$    $$ |      $$$$$/   $$  $$<  
 _$$ |_ $$ |  $$ |  $$ $$/  $$$$$$$$/ $$ |       $$$$$$  |$$$$$$$$/       $$ |     /$$$$  \ 
/ $$   |$$ |  $$ |   $$$/   $$       |$$ |      /     $$/ $$       |      $$ |    /$$/ $$  |
$$$$$$/ $$/   $$/     $/     $$$$$$$/ $$/       $$$$$$$/   $$$$$$$/       $$/     $$/   $$/ 
                                                                                            
                                                                                            
                                                                                            
Steps to install the HDA's

Step 1: Download all the files to your computer

Step 2: Move the Downloaded files to C:\Documents\Houdini(installed_version)\scripts\python\Houdini_HDA\
(Note: create a folder "Houdini_HDA" in C:\Documents\Houdini(installed_version)\scripts\python)

Step 3: Create a tool inside houdini and enter the code below 
         "from Houdini_HDA.file_cacher import file_cacher
	  import importlib
	  importlib.reload(file_cacher)
	  file_cacher()"

ENJOY THE TOOL!!!!!