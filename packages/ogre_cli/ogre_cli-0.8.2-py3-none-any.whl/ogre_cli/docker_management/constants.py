LOCALHOST = "http://localhost"
BASE_URL = "http://localhost:9000"
STREAMLIT_PORT = 7501
GUI_PYTHONFILE = "docker_management/gui/gui.py"

PORT_LOWER_BOUND = 8001
PORT_UPPER_BOUND = 9999

RANDOM_UPPER_LIMIT = 10000

ALTERNATIVE_MODULE_NAMES = {
    "cv2": "opencv-python",
    "mpl_toolkits": "matplotlib",
    "upstride": "",
    "gtda": "giotto-tda",
    "skimage": "scikit-image",
    "sklearn": "scikit-learn",
    "__future__": "",
    "pkg_resources": "",
    "PIL": "pillow",
}

APT_DEPENDENCIES = {"opencv-python": "ffmpeg libsm6 libxext6"}

OGRE_BASEIMAGES = ["ogre:baseimage-mini", "ogre:baseimage-standard", "ogre:baseimage-standard-gpu"]

TTYD = "ttyd"
TTYD_VERSION = "1.6.3"
TTYD_URL = "https://github.com/tsl0922/ttyd/releases/download/{}/ttyd.x86_64".format(
    TTYD_VERSION
)

DOCKERFILE_BASEIMAGE_OGRE = """
WORKDIR /opt/{}
COPY ogre_dir/bashrc /etc/bash.bashrc 
RUN chmod a+rwx /etc/bash.bashrc
COPY . .
"""

DOCKERFILE_BASEIMAGE_OGRE_DRY = """
WORKDIR /opt/{}
COPY ogre_dir/bashrc /etc/bash.bashrc 
RUN chmod a+rwx /etc/bash.bashrc
COPY . .
"""

DOCKERFILE = """
ENV TZ=Europe/Paris
WORKDIR /opt/{}
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# RUN apt update && apt install -y python3-dev python3-pip ffmpeg libsm6 libxext6 vim git
COPY ogre_dir/bashrc /etc/bash.bashrc 
RUN chmod a+rwx /etc/bash.bashrc
COPY . .
RUN pip install jupyterlab
"""

DOCKERFILE_DRY = """
WORKDIR /opt/{}
# RUN apt update && apt install -y python3-dev python3-pip
COPY ogre_dir/bashrc /etc/bash.bashrc 
RUN chmod a+rwx /etc/bash.bashrc
COPY . .
RUN pip install jupyterlab
"""

BASHRC = """
_python_argcomplete() {
    local IFS=$'\013'
    local SUPPRESS_SPACE=0
    if compopt +o nospace 2> /dev/null; then
        SUPPRESS_SPACE=1
    fi
    COMPREPLY=( $(IFS="$IFS" \
                  COMP_LINE="$COMP_LINE" \
                  COMP_POINT="$COMP_POINT" \
                  COMP_TYPE="$COMP_TYPE" \
                  _ARGCOMPLETE_COMP_WORDBREAKS="$COMP_WORDBREAKS" \
                  _ARGCOMPLETE=1 \
                  _ARGCOMPLETE_SUPPRESS_SPACE=$SUPPRESS_SPACE \
                  "$1" 8>&1 9>&2 1>/dev/null 2>/dev/null) )
    if [[ $? != 0 ]]; then
        unset COMPREPLY
    elif [[ $SUPPRESS_SPACE == 1 ]] && [[ "$COMPREPLY" =~ [=/:]$ ]]; then
        compopt -o nospace
    fi
}
complete -o nospace -o default -o bashdefault -F _python_argcomplete "az"

[ -z "$PS1" ] && return

export PS1="\[\e[31m\]ogre\[\e[m\] \[\e[33m\]\w\[\e[m\] > "
export TERM=xterm-256color
alias grep="grep --color=auto"
alias ls="ls --color=auto"

echo -e "\e[1;36m"
cat<<'OGRE'
  ___   __ _ _ __ ___
 / _ \ / _` | '__/ _ \ 
| (_) | (_| | | |  __/
 \___/ \__, |_|  \___|
       |___/
OGRE
echo -e "\e[0;33m"

echo "
Made by ogre.run

Reach out to us: contact@ogre.run
"

if [[ $EUID -eq 0 ]]; then
  cat <<WARN
WARNING: You are running this container as root, which can cause new files in
mounted volumes to be created as the root user on your host machine.

To avoid this, run the container by specifying your user's userid:

$ docker run -u \$(id -u):\$(id -g) args...
WARN
else
  cat <<EXPL
You are running this container as user with ID $(id -u) and group $(id -g),
which should map to the ID and group for your user on the Docker host. Great!
EXPL
fi

# Turn off colors
# echo -e "\e[m"

# Aliases
alias python="python3"
"""

OGREYML = """path: .
web: False
jupyter: True
jupyter_password: ogre123
jupyter_port: "8001"
mount: True
api_url: https://dev-cloud.ogre.run
api_token: $OGRE_API_TOKEN
docker:
  company: ogre-run
  version: 0.1.0
  baseimage: ogrerun/base:ubuntu22.04-amd64
  device: cpu
  container_repo: ogrerun
  project_volume_path: /opt
  cmd: bash
  ttyd: ttyd
  ttyd_version: 1.6.3
  ttyd_url: https://github.com/tsl0922/ttyd/releases/download/
  ttyd_port: 6007
  ogre_dir: ogre_dir
  requirements_format: freeze
  expose_ports: 8001
  no_cache: True
"""
