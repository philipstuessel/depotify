source ~/.zshrc

if command -v python3 &> /dev/null
then
    echo "Python3 is installed, version: $(python3 --version)"
else
    echo "${RED}install python3 (https://www.ionos.de/digitalguide/websites/web-entwicklung/python-installieren/)${NC}"
    return 0
fi

if command -v openssl &> /dev/null
then
    echo "OpenSSL is installed, version: $(openssl version)"
else
    echo "${RED}install openssl${NC}"
    return 0;
fi

name="depotify"
url=https://raw.githubusercontent.com/philipstuessel/depotify/main/
folder="${JAP_FOLDER}plugins/packages/${name}/"
folder_config="${folder}config/"
fetch2 $folder_config "${url}config/depotify.config.json"
fetch2 $folder_config "${url}config/depotify.template.json"
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
echo "--Depotify is installed--"
