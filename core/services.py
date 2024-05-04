import os

home_dir = os.getenv('HOME')
japFolder_dir = home_dir+"/jap/"
depotify_dir = japFolder_dir+"plugins/packages/depotify/"
CONFIG_FILE = depotify_dir+"config/depotify.config.json"
depotify_template = depotify_dir+"config/depotify.template.json"
github_api_url = "https://api.github.com/"
github_url = f"https://github.com/"
GitHub_Api_Version = {'X-GitHub-Api-Version': '2022-11-28'}
