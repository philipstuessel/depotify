source ~/.zshrc
name="depotify"
url=https://raw.githubusercontent.com/philipstuessel/depotify/main/
folder="${JAP_FOLDER}plugins/packages/${name}/"
folder_config="${folder}config/"

fetch2 $folder "${url}depotify.zsh"
fetch2 $folder "${url}setup.zsh"
c=${folder}core/
cu=${url}core/
fetch2 $c "${cu}config.py"
touch ${c}__init__.py

fetch2 $c "${cu}controllers.py"
fetch2 $c "${cu}kit.py"
fetch2 $c "${cu}main.py"
fetch2 $c "${cu}package.py"
fetch2 $c "${cu}services.py"
fetch2 $c "${cu}utils.py"
zsh "${folder}setup.zsh"