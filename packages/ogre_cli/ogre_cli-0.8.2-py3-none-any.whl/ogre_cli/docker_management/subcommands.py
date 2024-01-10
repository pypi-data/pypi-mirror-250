import json
import os
import platform
import subprocess
from datetime import datetime

import docker
import psutil
import requests
from pip._internal.operations import freeze

from .constants import *
from .imports import GetImports
from .utilities import *


class NamedPopen(subprocess.Popen):
    """
    Like subprocess.Popen, but returns an object with a process name (.process_name) member.

    Usage example:

    fred_process = NamedPopen('sleep 11; echo "yabba dabba doo"', shell=True, name="fred")

    Taken from https://stackoverflow.com/questions/58075187/name-process-when-creating-it-with-pythons-subprocess-popen
    """

    def __init__(self, *args, process_name=None, **kwargs):
        self.process_name = process_name
        super().__init__(*args, **kwargs)


def get_process_id_by_name(process_name):
    """
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName.

    Source: https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/
    """

    listOfProcessObjects = []
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name", "create_time"])
            # Check if process name contains the given name string.
            if process_name.lower() in pinfo["name"].lower():
                listOfProcessObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return listOfProcessObjects


def stop_process(process_name):
    """
    Kill linux process by name
    """

    proc_info = get_process_id_by_name(process_name)
    if len(proc_info) == 0:
        print("There are no processes {} to be terminated".format(process_name))
    else:
        print("Terminating process \n {}".format(proc_info))
        proc = psutil.Process(proc_info[0]["pid"])
        proc.terminate()


def get_project_folder():
    """
    Get project folder name. It is used to create the docker image name.
    """

    dirpath = os.getcwd()
    project_folder = os.path.basename(dirpath)
    #project_folder = project_folder.lower()
    return project_folder


def set_img_name(company_name, project_folder):
    """
    Set name of docker image based on company name and project folder name.
    """

    name = company_name.lower() + "-" + project_folder.lower() + "-ogre"
    return name


def set_container_name(company_name, project_folder):
    """
    Set label of docker image based on company name and project folder name.
    To be used at run time, to name the container.
    """

    name = "ogre-" + company_name.lower() + "-" + project_folder.lower()
    return name


def set_tag(version, device, platform):
    """
    Set docker tag based on version and device.
    """

    tag = version.lower() + "-" + device.lower() + "-" + platform.lower()
    return tag


def set_img(container_repo, name, tag):
    """
    Set docker image full name, with explicit container repository.
    """

    img = container_repo + "/" + name + ":" + tag
    return img


def set_volume(project_volume_path, project):
    """
    Set volume to be mounted inside docker.
    """

    volume = project_volume_path + "/" + project
    return volume


def set_ttyd(ttyd, ttyd_port):
    """
    Set ttyd command.
    """

    ttyd_cmd = ttyd + " -p " + str(ttyd_port)
    return ttyd_cmd


def set_ttyd_url(ttyd_url_root, ttyd_version, ttyd):
    """
    Set ttyd url to download the binary, if necessary.
    """

    ttyd_url = os.path.join(ttyd_url_root, ttyd_version, ttyd)
    return ttyd_url


def get_value(string):
    if string is not None:
        string = string.strip()
        if string.startswith('$'):
            var_name = string[1:]
            if var_name in os.environ:
                return os.environ[var_name]
            else:
                return None
    return string


def _freeze_requirements(ogre_dir, project_dir):
    """
    Crawl all .py files in the project and finds all the import modules. Then, a
    requirements file is created, listing the found modules.
    """

    find_imports = GetImports("{}".format(project_dir))
    find_imports.ipynb_to_py()
    find_imports.get_imported_modules()
    find_imports.remove_converted_ipynb_files()

    requirements_file = open("{}/requirements.txt".format(ogre_dir), "w")

    for p in find_imports.modules:
        native = find_imports.is_native_module(p)
        custom = find_imports.comes_with_repo(p)
        if not native and not custom:
            p = find_imports.get_alternative_name(p)
            requirements_file.write("%s\n" % p)

    requirements_file.close()


def _read_text_file(file_path):
    """
    Read the contents of a text file and return its contents as a string.
    Args:
        file_path (str): The path of the text file to be read.
    Returns:
        str: The contents of the text file.
    """
    with open(file_path, "r") as f:
        contents = f.read()
    return contents


def _auto_generate_requirements(ogre_dir, project_dir, api_url, api_token, openai_token):
    """
    Automatically generate a pip requirements file for a Python project using the existing README file.
    Args:
        ogre_dir (str): The path of the OGRE directory.
        project_dir (str): The path of the project directory.
        api_url (str): The URL of the OGRE API endpoint.
        api_token (str): The OGRE API key.
        openai_token (str): The OpenAI API key.
    """
    readme_file_names = ["README.md", "README.txt", "README"]
    for file_name in readme_file_names:
        if os.path.isfile(os.path.join(project_dir, file_name)):
            print(f"> README file ({file_name}) exists, processing it to extract project dependencies...")
            readme_contents = _read_text_file(file_name)
            break
    else:
        print("> README file does not exist")
        raise FileNotFoundError
    try:
        print("> Generating the requirements.txt file")
        headers = {
            'accept': 'application/json',
            'api-token': api_token,
            'Content-Type': 'application/json'
        }
        data = {
            "contents": readme_contents,
            'openai_token': openai_token
        }
        response = requests.post(api_url + "/requirements/generate", headers=headers, data=json.dumps(data))
        response_json = response.json()
        if "status" in response_json and response_json['status'] == 1:
            requirements = response_json['requirements']
            with open("{}/requirements.txt".format(ogre_dir), "w") as f:
                f.write(requirements)
            print("> SUCCESS: requirements.txt file generated")
        else:
            print("> FAILED: Unable to generate the requirements.txt file")
    except Exception as ex:
        print("Failed to communicate with the Ogre API. Exception: {}".format(ex))


def check_for_readme(project_dir, ogre_dir, requirements_format, dry = False):
    """
    Check for existence of a README file. If it exists, nothing is done. If it
    doesn't, requirements_format is changed to `freeze`, unless it is a dry build.

    Returns: `requirements_format`
    """

    extensions = ['txt', 'md']
    filenames = ['README', 'readme']

    if not dry:
        for filename in filenames:
            for ext in extensions:
                if os.path.isfile("{}/{}.{}".format(project_dir, filename, ext)):
                    print("{}.{} exists in {}. Keeping requirements_format = {}".format(filename, ext, project_dir, requirements_format))
                    found_filename = "{}.{}".format(filename, ext) 
                    break
                else:
                    requirements_format = "freeze"
                    print("{}.{} doesn't exist in {}. Thus, requirements_format must be `freeze` (currently, the `auto` option only works if there is a {}.{} file) ".format(filename, ext, project_dir, filename, ext))

    return requirements_format

def set_up_requirements(project_dir, ogre_dir, requirements_format, api_url, api_token, openai_token, dry = False):
    """
    Check for existence of requirements.txt. If it exists, nothing is done. If it
    doesn't, pip freeze is run and saves the result in a new requirements.txt.
    """
    if not dry:
        if os.path.isfile("{}/requirements.txt".format(project_dir)):
            print("requirements.txt already exists in {}".format(project_dir))
            os.popen(
                "cp {}/requirements.txt {}/requirements.txt".format(project_dir, ogre_dir)
            )
        else:
            if requirements_format.lower() == "none":
                print(
                    "Skipping generation of the requirements.txt file"
                    )
            else:
                print(
                    "requirements.txt doesn't exist. Creating one for you using {}".format(
                        requirements_format
                    )
                )
                if requirements_format == "freeze":
                    # os.popen("python -m pip freeze > {}/requirements.txt".format(ogre_dir))
                    _freeze_requirements(ogre_dir, project_dir)
                elif requirements_format == "auto":
                    try:
                        _auto_generate_requirements(ogre_dir, project_dir, api_url, api_token, openai_token)
                    except FileNotFoundError as ex:
                        print("Unable to auto generate requirements from README, using 'freeze' instead.")
                        _freeze_requirements(ogre_dir, project_dir)
                else:
                    print(
                        "requirements_format: only 'freeze', 'auto', or 'none' are accepted as formats."
                    )
                    raise NotImplementedError
        return os.path.isfile("{}/requirements.txt".format(ogre_dir))


def set_up_dockerfile(project_dir, project_name, ogre_dir,
                      baseimage, requirements_format, dry = False):
    """
    Check for existence of Dockerfile. If it exists, nothing is done. If it
    doesn't, a new Dockerfile is generate following the parameters in the
    config file.
    """

    if requirements_format == 'auto' or requirements_format == 'freeze':
        REQUIREMENTS_LINE = 'RUN cat ./{}/requirements.txt | xargs -L 1 pip3 install; exit 0'.format(os.path.basename(ogre_dir))

    if dry:
        print(
            "Dry build -- no requirements will be installed {}".format(
                baseimage
            )
        )

        if baseimage.startswith("ogarantia/ogre"):
            dockerfile_string = DOCKERFILE_BASEIMAGE_OGRE_DRY
        else:
            dockerfile_string = DOCKERFILE_DRY

        with open("{}/Dockerfile".format(ogre_dir), "w") as f:
            f.write(dockerfile_string.format(project_name))
        f.close()
        with open("{}/Dockerfile".format(ogre_dir), "r+") as f:
            content = f.read()
            f.seek(0, 0)
            f.write("FROM {}".format(baseimage) + content)
        f.close()

    
    else:

        if os.path.isfile("{}/Dockerfile".format(project_dir)):
            print("Dockerfile exists in {}".format(project_dir))
            os.popen("cp {}/Dockerfile {}/Dockerfile".format(project_dir, ogre_dir))
        else:
            print(
                "Dockerfile doesn't exist. Making a new one for you using {}".format(
                    baseimage
                )
            )

            if baseimage.startswith("ogarantia/ogre"):
                dockerfile_string = DOCKERFILE_BASEIMAGE_OGRE
            else:
                dockerfile_string = DOCKERFILE

            with open("{}/Dockerfile".format(ogre_dir), "w") as f:
                f.write(dockerfile_string.format(project_name))
            f.close()
            with open("{}/Dockerfile".format(ogre_dir), "r+") as f:
                content = f.read()
                f.seek(0, 0)
                f.write("FROM {}".format(baseimage) + content)
                # Find last line
                f.seek(0, 2)
                #while f.read(1) != b'\n':
                #    f.seek(-2, 1)
                f.write("{}".format(REQUIREMENTS_LINE))
            f.close()

    return os.path.isfile("{}/Dockerfile".format(ogre_dir))


def _run_welcome(product, version, ogre_dir, date):
    repo = os.popen("git remote get-url origin").read()
    author = os.popen("git log -1 --pretty=format:'%ae'").read()
    commit = os.popen("git log -1 --pretty=%h").read()
    # date = datetime.today().strftime("%Y-%m-%d-%H:%M:%S")

    BOILERPLATE = """
echo PRODUCT = {}
echo VERSION = {}
echo BUILD_DATE = {} 
echo REPOSITORY = {} 
echo COMMIT = {}echo COMMIT_AUTHOR = {} 
    """.format(
        product, version, date, repo[:-1], commit, author
    )

    #    print("BOILERPLATE = {}".format(BOILERPLATE))

    with open("{}/bashrc".format(ogre_dir), "a") as f:
        f.write(BOILERPLATE)
    f.close()


def set_up_bashrc(project_dir, ogre_dir, product, version, date):

    """
    Check for existence of bashrc. If it exists, nothing is done. If it
    doesn't, it is created.
    """

    if os.path.isfile("{}/bashrc".format(project_dir)):
        print("bashrc exists in {}".format(project_dir))
        os.popen("cp {}/bashrc {}/bashrc".format(project_dir, ogre_dir))

    else:
        print("bashrc doesn't exist. Making a new one for you.")
        with open("{}/bashrc".format(ogre_dir), "w") as f:
            f.write(BASHRC)
        f.close()
    _run_welcome(product, version, ogre_dir, date)

    return os.path.isfile("{}/bashrc".format(ogre_dir))


def set_up_ogre_dir(ogre_dir):
    """
    Check for existence of ogre_dir directory. If it exists, nothing is
    done. If it doesn't, it is created.
    """
    if not os.path.exists(ogre_dir):
        os.makedirs(ogre_dir)

    return os.path.exists(ogre_dir)

def set_up_cmd_expose_ports(list_ports):
    """
    Make command to expose container ports.
    """
    command_ports = ""

    if list_ports[0] != 0:
        for x in list_ports:
            command_ports = command_ports + "-p {}:{} ".format(x, x)
    return command_ports

def set_up_device_command(device):
    """
    Make command to run container on specific device (gpu or cpu).
    """
    command_device = ""
    if device.lower() == "gpu":
        command_device = "--gpus all"

    return command_device

def set_up_mount_command(mount, project_path, volume):
    """
    Make command to mount project folder inside container.
    """
    command_mount = ""
    if mount:
        command_mount = "-v {}:{}".format(project_path, volume)

    return command_mount

def check_image_existence(image_name):
    """
    Check if image with name='image_name' exists.
    """

    system_image_name = None
    try:
        client = docker.from_env()
        image_object = client.images.get(image_name)
        system_image_name = image_object.__dict__['attrs']['RepoTags'][0]
        print("Image exists = {}".format(system_image_name))
        return True
    except:
        print("Image doesn't exist")
        return False

def set_platform_tag(platform_name):
    """
    Format and set the platform (machine architecture) tag for the docker image.
    """

    if platform_name is None:
        res = "linux/{}".format(platform.machine())
        res = res.replace("/", "-")
    else:
        res = platform_name.replace("/", "-")

    return res

def set_platform_name(platform_name):
    """
    Set the platform (machine architecture) for the docker image.
    """

    if platform_name is None:
        # get local-system platform
        res = "linux/{}".format(platform.machine())
    else:
        res = platform_name

    return res

def set_up_yml_file(project_dir):

    """
    Check for existence of ogre.yml. If it exists, nothing is done. If it
    doesn't, it is created.
    """

    if os.path.isfile("{}/ogre.yml".format(project_dir)):
        print("ogre.yml already exists in {}".format(project_dir))
        # os.popen("cp {}/ogre.yml {}/ogre.yml".format(project_dir, ogre_dir))

    else:
        print("ogre.yml doesn't exist. Making a new one for you.")
        with open("{}/ogre.yml".format(project_dir), "w") as f:
            f.write(OGREYML)
        f.close()

    return os.path.isfile("{}/ogre.yml".format(project_dir))

def poetry_run(requirements_format):

    """
    Define if the command `poetry run` will be called in front of
    the juputer-lab. This enables the jupyter-lab environmet to
    to see the poetry packages.
    """

    res = ''
    if requirements_format == 'poetry':
        res = 'poetry run'

    return res

def list_ogre_containers():

    """
    Return a list containing the names and ports of the ogre-generated 
    containers that are running in the local system.
    """
    # Call 'docker ps' using the docker python library
    #client = docker.APIClient(base_url='unix://var/run/docker.sock')
    #res = client.containers()
    
    # TODO: remove this patch for something more stable

    containers = os.popen("docker ps --format '{{.Names}} {{.Ports}}'").read().split('\n')

    ogre_containers = []
    for i in range(len(containers)):
        if containers[i][:4] == 'ogre':
            ogre_containers.append(containers[i])
        

    #ogre_containers = []
    #for i in range(len(res)):
    #    name = res[i]['Names'][0][1:]
    #    if name[:4] == 'ogre':
    #        ports = []
    #        for j in range(len(res[i]['Ports'])):
    #            ports.append(res[i]['Ports'][j]['PublicPort'])
    #        ogre_containers.append((name, ports))

    return ogre_containers

def list_ogre_images():

    """
    Return a list containing the names of the ogre-generated 
    images that are present in the local system.
    """
    # Call 'docker ps' using the docker python library
    #client = docker.APIClient(base_url='unix://var/run/docker.sock')
    #res = client.containers()
    
    # TODO: remove this patch for something more stable

    containers = os.popen("docker ps --format '{{.Names}} {{.Ports}}'").read().split('\n')

    ogre_containers = []
    for i in range(len(containers)):
        if containers[i][:4] == 'ogre':
            ogre_containers.append(containers[i])
        

    #ogre_containers = []
    #for i in range(len(res)):
    #    name = res[i]['Names'][0][1:]
    #    if name[:4] == 'ogre':
    #        ports = []
    #        for j in range(len(res[i]['Ports'])):
    #            ports.append(res[i]['Ports'][j]['PublicPort'])
    #        ogre_containers.append((name, ports))

    return ogre_containers

def allocate_ports(list_ports_str):
    """
    Try to allocate ports in `list_ports_str` (string of ports
    separated by comma). If not free, find new ones.

    First port in the list is allocated to jupyter-lab.
    The other ones are used for potential applications
    that will be deployed from the ogre environment.
    """
    
    updated_list_ports = []
    list_ports = list_ports_str.split(",")
    list_ports = [int(i) for i in list_ports]
   
    # Check if ports are available
    for port in list_ports:
        res = is_port_free(port)
        if res is False:
            # If port is not available, find a free one
            free_port = find_free_port(PORT_LOWER_BOUND, PORT_UPPER_BOUND)
            updated_list_ports.append(free_port['port'])
        else:
            updated_list_ports.append(port)
    return updated_list_ports
