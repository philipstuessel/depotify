from kit import Kit, DepotifyItems, printm
from controllers import RESTAPI
from services import github_url
from utils import *
import requests
import zipfile
import shutil
import json
import os

class Manager:
    
    def __init__(self, input = None):
        self.raw = input
        self.vendor = self.forks("vendor")
        self.package = self.forks("package")
        self.version = self.forks("version")
        self.work_dir = DepotifyItems().getFolder()
    
    def check(self, prefix = ""):
        folder = self.work_dir+"/"+self.package
        if os.path.exists(folder):
            print(LABLE_ERROR+RED+" The repo already exists"+RESET)
            return None
        else:
            print(GITHUB_LABLE+": Request to the API", end="\r")
            if self.version == "":
                return self.getTag("last")
            else:
                if self.getTag("last")["name"][:1] == "v":
                    prefix = "v"
                else:
                    prefix = ""
                tag = Kit().getVersion(self.version)
                if prefix == "":
                    tag = tag[1:] if tag.startswith("v") else tag
                return self.getTag(tag)

    def forks(self, type):
        parts = self.raw.split(":")
        vendor_package = parts[0]
        version = parts[1] if len(parts) > 1 else ""
        vendor_package_parts = vendor_package.split("/")
        vendor = vendor_package_parts[0]
        package = vendor_package_parts[1]
        if type == "vendor":
            return vendor
        if type == "package":
            return package
        if type == "version":
            return version
        
    def require(self, prefix = ""):
        data = self.check(prefix)
        if data == None:
            return None
        printm(LABLE+" response is processed")
        zipball = data["zipUrl"]
        version = data["name"]
        self.zipler(zipball, version, prefix)
    
    def zipler(self, url, version, prefix=""):
        response = requests.get(url)
        folder = self.work_dir+"/"
        if not os.path.exists(folder):
            os.makedirs(folder)
        printm(LABLE+" repo would be unpacked")
        if response.status_code == 200:
            with open(folder+f"/{self.package}.zip", "wb") as f:
                f.write(response.content)
                printm(LABLE+" downloaded successfully.")
        else:
            print(LABLE_ERROR+RED+"Error: downloading ZIP file. Status code:"+RESET, response.status_code)
        
        zip_file_path = folder+f"/{self.package}.zip"
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_contents = zip_ref.namelist()
            if len(zip_contents) > 1:
                parent_folder = zip_contents[0]
            else:
                print(LABLE_ERROR+RED+"Error: The ZIP file does not contain a parent folder."+RESET)
        self.unzip(zip_file_path, folder)
        os.remove(zip_file_path)
        os.rename(folder+parent_folder, folder+self.package)
        Kit().addRequire(self.vendor, self.package, version)
        printm("")
        if not prefix == "mute":
            print(LABLE+GREEN+f" The download from '{self.vendor}/{self.package}' [{version}] is complete"+RESET)
        
    def unzip(slef, zip_file, extract_to):
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(extract_to)

    def remove(self):
        folder = self.work_dir + "/" + self.package
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                repo = f"{self.vendor}/{self.package}"
                Kit().removeRequire(repo)
                print(LABLE + f" The repo '{repo}' has been removed")
            except Exception as e:
                print(LABLE_ERROR + RED + f" An error occurred while removing the repo: {e}" + RESET)
        else:
            print(LABLE_ERROR + RED + " The repo doesn't exist" + RESET)
            
    def getTag(self, type, meta = False):
        data = {}
        response = False
        if type == "last":
            response = (RESTAPI().get("tags", self.vendor, self.package))
            if response == []:
                print(LABLE_ERROR+RED+" No releases found for the repo\n")
                print(UNDERLINE+f"{github_url}{self.vendor}/{self.package}/releases\n"+RESET)
                return None
            if response == None:
                return None
            else:
                response = response[0]
        elif meta == "up":
            print(Kit().upVersion(type, self.vendor, self.package))
        else:
            responseData = RESTAPI().get("tags", self.vendor, self.package)
            if responseData == None:
                return None
            for tags in responseData:
                if type == tags["name"]:
                    response = tags
                    break
        if response == False:
            printm("")
            print(LABLE_ERROR+RED+" No data for this version"+RESET)
            return None
        else:
            data["name"] = response["name"]
            data["zipUrl"] = response["zipball_url"]
            data["sha"] = response["commit"]["sha"]
            return data
        
    def install(self):
        if not os.path.exists(self.path_depotify):
            print(LABLE_ERROR+RED+" No found 'depotify.json'"+RESET)
            return None
        else:
            DepotifyModel().loadRequire()
            
    def update(self):
        if not os.path.exists(self.path_depotify):
            print(LABLE_ERROR+RED+" No found 'depotify.json'"+RESET)
            return None
        else:
            DepotifyModel().updateRequire()
    
    def reinstall(self):
        self.path_depotify = os.getcwd()+"/depotify.json"
        if not os.path.exists(self.path_depotify):
            print(LABLE_ERROR+RED+" No found 'depotify.json'"+RESET)
            return None
        else:
            self.remove()
            self.require()
        


class DepotifyModel:
    def __init__(self):
        self.path_depotify = os.getcwd()+"/depotify.json"
        
    def loadRequire(self):
        if os.path.exists(self.path_depotify):
            with open(self.path_depotify, 'r') as file:
                data = json.load(file)
                if 'require' in data:
                    require_list = data['require']
                    print(LABLE+BWHITE+f" Install all require : {RESET}\n")
                    for package, version in require_list.items():
                        version = Kit().getVersion(version)
                        version = version[1:] if version.startswith("v") else version
                        repo_name = package.split("/")
                        response = (RESTAPI().get("tags", repo_name[0], repo_name[1]))[0]
                        prefix = ""
                        if (response["name"][:1] == "v"):
                            prefix = "v"
                        Manager(f"{package}:{prefix+version}").require(prefix)
            print("")
        else:
            print(LABLE_ERROR+RED+" No found 'depotify.json'"+RESET)

    def updateRequire(self):
        if os.path.exists(self.path_depotify):
            with open(self.path_depotify, 'r') as file:
                data = json.load(file)
                if 'require' in data:
                    require_list = data['require']
                    print(LABLE+BWHITE+f" Update require: {RESET}\n")
                    for package, version in require_list.items():
                        if version[:1] == "^":
                            repo_name = package.split("/")
                            new_version = Kit().upVersion(version, repo_name[0], repo_name[1])
                            if not new_version:
                                print(BOLD+package+RESET+GREEN+" Is up to date"+RESET)
                            else:
                                Kit().removeRequire(package)
                                manager = Manager(f"{package}:{new_version}")
                                work_dir = DepotifyItems().getFolder()
                                folder =  work_dir + "/" + repo_name[1]
                                shutil.rmtree(folder)
                                manager.require("mute")
                                version = Kit().getVersion(version)
                                new_version = Kit().getVersion(new_version)
                                print(BOLD+package+RESET+f" ({BLUE}{version}{RESET}) -> ({BLUE}{new_version}{RESET})")
            print("")
        else:
            print(LABLE_ERROR+RED+" No found 'depotify.json'"+RESET)