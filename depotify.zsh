name="depotify"
CORE="${JAP_FOLDER}/plugins/packages/${name}/core"
depotify () {
    if [[ "$1" == "v" ]];then 
        echo -e "${BGREEN}${BOLD} Depotify ${NC}"
        echo -e "${BOLD}v0.2.0${NC}"
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

    if [[ "$1" == "reinstall" ]];then
        py "$CORE/main.py" require:reinstall "$2" x
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

    if [[ "$1" == "run" ]];then
        if [[ "$2" == "l" || "$2" == "list" ]];then
            py "$CORE/main.py" script:list x x
        else
            if [ -e "depotify.json" ];then
                script_name="$2"
                JSON_DATA=$(cat depotify.json)
                script_command=$(jq -r ".scripts[\"$script_name\"]" <<< "$JSON_DATA")
                if [[ ! $script_command == null ]]; then
                    echo -e "Run the script:${BOLD} '${script_name}'${NC}"
                    eval "$script_command"
                else
                    echo -e "${RED}The name '$script_name' was not found in the scripts.${NC}"
                fi
            fi
        fi
    fi
}
