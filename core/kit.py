from services import depotify_template
from controllers import RESTAPI
from utils import *
import json
import sys
import os
import re

def printm(value):
    sys.stdout.write("\033[K") 
    sys.stdout.flush()
    print(value, end="\r")

class Kit:
    
    def __init__(self):
        self.path_depotify = os.getcwd()+"/depotify.json"
    
    def init(self, msg):
        with open(depotify_template, 'r') as source_file:
            content = json.load(source_file)
    
        with open(self.path_depotify, 'w') as destination_file:
            json.dump(content, destination_file, indent=2)
            if msg:
                print(LABLE+GREEN+f"Create depotify.json in this folder"+RESET)
    
    def addRequire(self, owner, repo, v):
        try:
            with open(self.path_depotify, "r+") as file:
                data = json.load(file)
                v = v[1:] if v.startswith("v") else v
                v = "^"+v
                new_required = {f"{owner}/{repo}": v}
                data["require"].update(new_required)
                file.seek(0)
                json.dump(data, file, indent=2)
                file.truncate()
        except FileNotFoundError:
            print(LABLE_ERROR+RED+" The specified 'depotify.json' was not found."+RESET)
        except json.JSONDecodeError:
            print(LABLE_ERROR+RED+" The JSON file could not be decoded."+RESET)

    def removeRequire(self, key_to_remove):
        try:
            with open(self.path_depotify, "r+") as file:
                data = json.load(file)
                data["require"].pop(key_to_remove)
                file.seek(0)
                json.dump(data, file, indent=2)
                file.truncate()
        except FileNotFoundError:
            print(LABLE_ERROR+RED+" The specified 'depotify.json' was not found."+RESET)
        except json.JSONDecodeError:
            print(LABLE_ERROR+RED+" The JSON file could not be decoded."+RESET)
    
    def getVersion(self, v):
        v = v[1:] if v.startswith("v") else v
        v = v[1:] if v.startswith("^") else v
        v = v[1:] if v.startswith("v") else "v"+v
        return v
    
    def upVersion(self, v, owner, repo):
        v = self.getVersion(v)
        version = v[1:] if v.startswith("v") else v
        response = (RESTAPI().get("tags", owner, repo))
        tags = []
        test_tag = ""
        for tag in response:
            tagVersion = tag["name"]
            test_tag = tagVersion
            tagV = self.getVersion(tagVersion)
            tagVF = tagV[1:] if tagV.startswith("v") else tagV
            tags.append(tagVF)
        
        return self.find_next_version(version, tags, self.check_prefix(test_tag))

    def check_prefix(self, tags):
        if tags and tags[0].startswith('v'):
            return 'v'
        return ''
    
    def parse_version(self, version):
        parts = re.split(r'[^0-9]+', version, maxsplit=3)[:3]
        major, minor, patch = map(int, parts)
        return major, minor, patch

    def find_next_version(self, version, tags, prefix=''):
        input_major, input_minor, input_patch = self.parse_version(version)
        compatible_versions = [v for v in tags if v.startswith(f"{input_major}.")]
        compatible_versions.sort(reverse=True)
        for v in compatible_versions:
            major, minor, patch = self.parse_version(v)
            if major == input_major:
                if minor > input_minor or (minor == input_minor and patch > input_patch):
                    return prefix + v
        return False

class DepotifyItems:
    
    def __init__(self):
        self.path_depotify = os.getcwd()+"/depotify.json"

    def getDJ(self):
        depotifyJson = f"{os.getcwd()}/depotify.json"
        if os.path.exists(depotifyJson):
            return depotifyJson
        else:
            Kit().init(False)
            return False
    
    def getFolder(self):
        work_dir = os.getcwd()
        default = work_dir+"/depotify_kit"
        dj = self.getDJ()
        if not dj:
            return default
        with open(dj, "r") as json_file:
            data = json.load(json_file)
            if data['folder'] == "":
                return default
            else:
                return work_dir+"/"+data['folder']
            
    def listRequire(self):
        if os.path.exists(self.path_depotify):
            with open(self.path_depotify, 'r') as file:
                data = json.load(file)
                if 'require' in data:
                    require_list = data['require']
                    if len(require_list) == 0:
                        print(LABLE_WARN+YELLOW+" You have not require install."+RESET)
                        return None
                    print(LABLE+BWHITE+f" List require: {RESET}\n")
                    for package, version in require_list.items():
                        print(BOLD+package+RESET+f" ({GREEN}{version}{RESET})")
            print("")
        else:
            print(LABLE_ERROR+RED+" No found 'depotify.json'"+RESET)
            
    def listScripts(self):
        if os.path.exists(self.path_depotify):
            with open(self.path_depotify, 'r') as file:
                data = json.load(file)
                if 'scripts' in data:
                    scripts_list = data['scripts']
                    if len(scripts_list) == 0:
                        print(LABLE_WARN+YELLOW+" No Scripts"+RESET)
                        return None
                    print(LABLE+BWHITE+f" List Scripts: {RESET}\n")
                    for alias, cmd in scripts_list.items():
                        print(BOLD+alias+RESET+f" => {CYAN}'{cmd}'{RESET}")
            print("")
        else:
            print(LABLE_ERROR+RED+" No found 'depotify.json'"+RESET)