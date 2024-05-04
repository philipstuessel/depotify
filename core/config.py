from services import CONFIG_FILE
from utils import *
import json

class Config:
    
    def addGhToken(self, token):
        with open(CONFIG_FILE, "r+") as json_file:
            data = json.load(json_file)
            data["gh_token"] = token
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.truncate()
            print(LABLE+GREEN+f" add GitHub Token ({token})"+RESET)
    
    def printToken(self):
        with open(CONFIG_FILE, "r") as json_file:
            data = json.load(json_file)
            if data['gh_token'] == "":
                print(LABLE_ERROR+RED+f" No token has been added yet. Do this using: {BOLD}depotify gh token <token>"+RESET)
            else:    
                print(LABLE+GREEN+f" GitHub Token {BOLD}{data['gh_token']}"+RESET)

    def getToken(self):
        with open(CONFIG_FILE, "r") as json_file:
            data = json.load(json_file)
            if data['gh_token'] == "":
                return False
            else:
                return data['gh_token']