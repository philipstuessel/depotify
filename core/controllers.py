from services import CONFIG_FILE, github_api_url, GitHub_Api_Version
from config import Config
from utils import *
import requests

class RESTAPI():
    def __init__(self):
        self.token = Config().getToken()
        
    def haeder(self):
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        headers['X-GitHub-Api-Version'] = GitHub_Api_Version["X-GitHub-Api-Version"]
        return headers
    
    def get(self, type, owner, repo):
        url = github_api_url+f"repos/{owner}/{repo}/{type}"
        if self.haeder() == {}:
            response = requests.get(url)
        else:
            response = requests.get(url, headers=self.haeder())
        
        if not response.status_code == 200:
            print(GITHUB_ERROR_LABLE+f"{RED}Error: {response.status_code}             "+RESET)
            return None
        else:
            return response.json()