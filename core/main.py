from package import Manager, DepotifyModel
from services import GitHub_Api_Version
from kit import Kit, DepotifyItems
from config import Config
import sys
import os

type = sys.argv[1]
a2 = sys.argv[2]
a3 = sys.argv[3]
path = os.getcwd()

def controller(type):
    if type == "token:add":
        Config().addGhToken(a2)
    if type == "token:get":
        Config().printToken()
    if type == "kit:init":
        Kit().init(True)
    if type == "require:package":
        Manager(a2).require("none")
    if type == "info:version":
        print(GitHub_Api_Version["X-GitHub-Api-Version"])
    if type == "require:remove":
        Manager(a2).remove()
    if type == "require:reinstall":
        Manager(a2).reinstall()
    if type == "require:install":
        DepotifyModel().loadRequire()
    if type == "require:update":
        DepotifyModel().updateRequire()
    if type == "require:list":
        DepotifyItems().listRequire()
    if type == "script:list":
        DepotifyItems().listScripts()

controller(type)