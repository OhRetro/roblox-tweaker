#Roblox Tweaker
VERSION = ["2.3", "Stable", 23]

#Imports
from os import environ as os_environ, name as os_name
from contextlib import suppress as cl_suppress
from types import NoneType
from traceback import format_exc as tb_format_exc
from sys import argv as sys_argv
from requests import get as re_get

ONLY_WINDOWS = "--no-windows" not in sys_argv

if ONLY_WINDOWS and os_name != "nt":
    print("Roblox Tweaker was intended to be runned on Windows, Exiting...")
    exit(2)
    
elif not ONLY_WINDOWS:
    print("Roblox Tweaker running with \"--no-windows\" flag.")
    
with cl_suppress(ImportError):
    from rich import print

try:
    from oreto_utils.terminal_utils import title as out_title, clear as out_clear, waitinput as out_waitinput
    from oreto_utils.file_utils import File as ouf_File
    from oreto_utils.folder_utils import Folder as ouf_Folder, folderselect as ouf_folderselect
    from oreto_utils.others_utils import countdown as ouo_countdown

except ImportError as missing_package:
    print(tb_format_exc())
    print("\n[!] Please try running \"pip install -r requirements.txt\"")
    exit(1)

class RobloxTweaker():
    def __init__(self):
        out_title(f"Roblox Tweaker v{VERSION[0]}")
        out_clear()
            
        running = True
                
        self._roblox_versions_path = os_environ["LocalAppData"]+"/Roblox/Versions"
        self._textures_folders_path = "PlatformContent/pc/textures"
            
        self._exception_texs = ["sky", "brdfLUT.dds", "studs.dds", "wangIndex.dds"]
        
        self.path_file = ouf_File("path.txt")
        self.path_dir = ouf_Folder("", self._roblox_versions_path)
        self.backup_dir = ouf_Folder("backup")
        
        if not self.path_file.exists():
            print("[Path File Not Found.]")
            self.writepath(True, True, False)
            out_clear()
            
        if self.path_file.exists:
            self.path = self.path_file.read()
            self.path_folder = ouf_Folder("", self.path)
            
        self.checkforupdates()
        
        while running:
            print(f"Roblox Tweaker v{VERSION[0]}\n")
            print("[1]Delete Textures\n[2]Show Textures List\n[3]Update Roblox Version Path\n[4]Backup Textures\n[5]Restore Textures from Backup\n[0]Exit\n\n[A]About\n")
            print(f"Current Roblox Version Path:\n\"{self.path}\"\nType: {self.gettype()}")
            _selected_option = input(">")
            
            if _selected_option == "1":
                self.deletetextures()    
                
            elif _selected_option == "2":
                self.listtextures()
            
            elif _selected_option == "3":
                self.writepath()
                self.path = self.path_file.read()
                self.path_folder = ouf_Folder("", self.path)

            elif _selected_option == "4":
                self.backuptextures()
                
            elif _selected_option == "5":
                self.restoretextures()
                  
            elif _selected_option == "0":
                out_clear()
                running = False
                
            elif _selected_option.lower() == "a":
                self.about()
                
            else:
                out_clear()
    
    #About
    def about(self):
        out_clear()
        print("[About]\n")
        print("Roblox Tweaker made by OhRetro.")
        print(f"Version: {VERSION[0]} - {VERSION[1]} | Version Code: {VERSION[2]}")
        print("Repository: https://github.com/OhRetro/Roblox-Tweaker \n")
        out_waitinput()
        out_clear()
    
    #Check for updates
    def checkforupdates(self):
        out_clear()
        response = re_get("https://api.github.com/repos/OhRetro/Roblox-Tweaker/releases/latest")
        tag_name = response.json()["tag_name"]
        latest =  int(tag_name.replace("v", "").replace(".", ""))
        
        if VERSION[2] < latest:
            print("[Update Available]")
            print(f"Version: {tag_name}")
            print(f"Version Code: {latest}")
            print("https://github.com/OhRetro/Roblox-Tweaker \n")
            out_waitinput()
            out_clear()

    #Delete Textures
    def deletetextures(self):
        out_clear()
        textures_path = ouf_Folder(self._textures_folders_path, self.path)
        textures_list = textures_path.list()
        
        option = None
        while option not in ["0", "1", "2"]:        
            print("[Delete Textures]\n")
            print("Do you want to delete ALL textures or leave some untouched?\nIt is recommended to backup if You are going to delete All.\n")
            option = input("[1]All\n[2]Leave (Recommended)\n[0]Cancel\n\n>")
            out_clear()
        
        if option != "0":
            ouo_countdown(3, "Deleting Textures in ", "Deleting Textures...")
        
        if option == "1":                              
            textures_path.deletecontents()

        elif option == "2":
            textures_path.deletecontents(self._exception_texs)            

        elif option == "0":
            out_clear()
            print("[Operation Cancelled]\n")
            return
        
        out_clear()
        
        if len(textures_list) <= len(self._exception_texs):
            print("[There's nothing to delete.]\n")
        else: 
            print("[Textures Deleted.]\n")
    
    #List Textures
    def listtextures(self):
        out_clear()
        textures_path = ouf_Folder(self._textures_folders_path, self.path)
        try:    
            textures_list = textures_path.list()
            success = True
        except FileNotFoundError:
            print("Unable to detemine type, path is inexistent, Try updating the path.")
            success = False
      
        if success:
            print("[Textures List]")
            for texture in textures_list:
                print(texture)
            print("")
            
        out_waitinput()
        out_clear()
    
    #Backup Textures
    def backuptextures(self):
        out_clear()
        textures_path = ouf_Folder(self._textures_folders_path, self.path)
        
        if not self.backup_dir.exists():
            self.backup_dir.create()
            
        print("[Copying contents to the backup directory]")
        if self.backup_dir.list():
            
            print("[Overwriting backup directory]")
            self.backup_dir.deletecontents()
            
        textures_path.copycontents(self.backup_dir._folder["FULL_PATH"])
        
        out_clear()
        print("[Backup Done]\n")
    
    #Restore Textures from Backup
    def restoretextures(self):
        out_clear()
        
        textures_path = ouf_Folder(self._textures_folders_path, self.path)
        
        if self.backup_dir.exists():
            if self.backup_dir.list():
                print("[Restoring Textures]")
                textures_path.deletecontents()
                self.backup_dir.copycontents(textures_path._folder["FULL_PATH"])
                out_clear()
                print("[Restoring Done]\n")
                
            else:
                print("[There's nothing to restore.]\n")
                
        else:
            print("[There's nothing to restore.]\n")
        
    #Write File
    #Should I bring how C# Edition does it?
    def writepath(self, force:bool=False, message:bool=True, clear:bool=True):
        if clear: out_clear()
        if message:
            print("[Please wait for Directory Dialog to appear]\n[If it doesn't appear after a while, try reopening the program]")
            
        if force:
            selectd = False
            while not selectd:
                roblox_version_path = ouf_folderselect("Select a Roblox Version", self._roblox_versions_path, True)
                
                if type(roblox_version_path) != NoneType and roblox_version_path.split("/")[-1].startswith("version-"):
                    selectd = True
        
        else:
            roblox_version_path = ouf_folderselect("Select a Roblox Version", self._roblox_versions_path, True)
            
            out_clear()
            if roblox_version_path == "":
                print("[Operation Cancelled]\n")
                return
            
            elif not roblox_version_path.split("/")[-1].startswith("version-"):
                print("[Invalid Path]\n")
                return
            
        self.path_file.write(roblox_version_path)
        out_clear()
        print("[Path File Written.]\n")
        
    #Get which Roblox Type is currently selected
    def gettype(self):
        roblox_exes = ["RobloxPlayerBeta.exe", "RobloxStudioBeta.exe"]
        try:    
            roblox_version_path = ouf_Folder("", self.path).list()
        
        except FileNotFoundError:
            return "Unable to detemine type, path is inexistent, Try updating the path."

        if roblox_exes[0] in roblox_version_path:
            return "Roblox Player"
        
        elif roblox_exes[1] in roblox_version_path:
            return "Roblox Studio"
        
        else:
            return "Unknown"
        
if __name__ == "__main__":
    RobloxTweaker()