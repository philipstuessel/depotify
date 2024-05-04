name="depotify"
CORE="${JAP_FOLDER}/plugins/packages/${name}/core"
depotify () {
    if [[ "$1" == "v" ]];then 
        echo -e "${BGREEN}${BOLD} Depotify ${NC}"
        echo -e "${BOLD}v0.1.0${NC}"
        echo -e "${YELLOW}JAP plugin${NC}"
        echo "-------------------"
        echo -e "${BLUE}$(python --version)${NC}"
        echo "-------------------"
        echo -e "${BOLD}X-GitHub-Api-Version:${NC}"
        echo -e $(py "$CORE/main.py" info:version x x)
    fi

    if [[ "$1" == "gh" ]];then
        if [[ "$2" == "token" ]];then
            if [[ ! "$3" == "" ]];then
                py "$CORE/main.py" token:add "$3" x
            else
                py "$CORE/main.py" token:get x x
            fi
        fi
    fi

    if [[ "$1" == "r" || "$1" == "require" ]];then
        if [[ ! "$2" == "" ]];then
            py "$CORE/main.py" require:package "$2" x
        fi
    fi

    if [[ "$1" == "i" || "$1" == "install" ]];then
        py "$CORE/main.py" require:install x x
    fi

    if [[ "$1" == "u" || "$1" == "update" ]];then
         py "$CORE/main.py" require:update x x
    fi

    if [[ "$1" == "uninstall" ]];then
        py "$CORE/main.py" require:remove "$2" x
    fi

    if [[ "$1" == "l" || "$1" == "list" ]];then
        py "$CORE/main.py" require:list x x
    fi

    if [[ "$1" == "init" ]];then
        if [[ -e "depotify.json" ]];then
            echo -e "There is already a depotify.json, do you really want to replace it?"
            echo -n "answer the question with yes[y] / no[n]: "
            read option
            if [[ $option == "y" || $option == "yes" ]];then
                py "$CORE/main.py" kit:init x x
            fi
        else
            py "$CORE/main.py" kit:init x x
        fi
    fi

    if [[ "$1" == "clear:cache" ]];then
        rm -r "${CORE}/__pycache__"
        echo -e "${BGREEN}${BOLD} Depotify ${NC} The cache has been emptied"
    fi
}
