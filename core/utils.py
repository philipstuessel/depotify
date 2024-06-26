# Define color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
MAGENTA = '\033[0;35m'
CYAN = '\033[0;36m'
WHITE = '\033[0;37m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

BRED = '\033[0;41m'
BGREEN = '\033[0;42m'
BYELLOW = '\033[0;43m'
BBLUE = '\033[0;44m'
BMAGENTA = '\033[0;45m'
BCYAN = '\033[0;46m'
BWHITE = '\033[0;47m'

# Reset color
RESET = '\033[0m'

LABLE = BGREEN+BOLD+" Depotify "+RESET
LABLE_ERROR = BRED+BOLD+" Depotify "+RESET
LABLE_WARN = BYELLOW+BOLD+" Depotify "+RESET
GITHUB_ERROR_LABLE = RED+BOLD+"[GitHub-REST-API]"+RESET+" "
GITHUB_LABLE = BLUE+BOLD+"[GitHub-REST-API]"+RESET