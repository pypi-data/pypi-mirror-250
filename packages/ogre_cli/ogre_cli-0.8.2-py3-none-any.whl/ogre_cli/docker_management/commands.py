import json
import os
import shutil
import stat
import subprocess
import threading
import time
from datetime import datetime

import requests
from yaspin import yaspin

from .constants import *
from .subcommands import *
from .utilities import get_module_installation_path, hash_password


class DockerImage:
    def __init__(self, config):
        self.config = config
        self.date = datetime.today().strftime("%Y-%m-%d-%H%M%S")
        self.web = config["web"]
        self.company = config["docker"]["company"]
        self.project = get_project_folder()
        self.img_name = set_img_name(self.company, self.project)
        self.container_name = set_container_name(self.company, self.project)
        self.version = config["docker"]["version"]
        self.baseimage = config["docker"]["baseimage"]
        self.device = config["docker"]["device"]
        self.platform_name = set_platform_name(config["platform"])
        self.platform = self.platform_name
        self.platform_tag = set_platform_tag(config["platform"])
        self.tag = set_tag(self.version, self.device, self.platform_tag)
        self.img = set_img(config["docker"]["container_repo"], self.img_name, self.tag)
        self.volume = set_volume(config["docker"]["project_volume_path"], self.project)
        self.cmd = config["docker"]["cmd"]
        self.ttyd = config["docker"]["ttyd"]
        self.ttyd_version = config["docker"]["ttyd_version"]
        self.ttyd_url = config["docker"]["ttyd_url"]
        self.ttyd_port = config["docker"]["ttyd_port"]
        self.ttyd_cmd = set_ttyd(self.ttyd, self.ttyd_port)
        self.requirements_format = config["docker"]["requirements_format"]
        self.poetry_run_cmd = poetry_run(self.requirements_format)
        self.expose_ports = allocate_ports(config["jupyter_port"])
        self.expose_ports_command = set_up_cmd_expose_ports(self.expose_ports)
        self.device_command = set_up_device_command(config["docker"]["device"])
        self._pwd = os.getcwd()
        self.ogre_dir = os.path.join(self._pwd, config["docker"]["ogre_dir"])
        self.jupyter = config["jupyter"]
        self.jupyter_port = self.expose_ports[0]
        self.jupyter_password_hashed = hash_password(str(config["jupyter_password"]))
        self.cmd_jupyter = "'cd {}; {} jupyter-lab --port={} --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='' --NotebookApp.password='{}''".format(
            self.volume,
            self.poetry_run_cmd,
            self.jupyter_port,
            self.jupyter_password_hashed
        )
        self.no_cache = config["docker"]["no_cache"]
        self.api_url = get_value(config["api_url"])
        self.api_token = get_value(config["api_token"])
        self.openai_token = get_value(config["openai_token"])
        self.ping = config["ping"]
        self.mount = config["mount"]
        self.mount_command = set_up_mount_command(self.mount, self._pwd, self.volume)
        self.dry = config["dry"]

    def all(self):
        self.clean()
        self.initialize()
        if self.mount and check_image_existence(self.img):
            print("Mounting project folder inside container of pre-built docker image")
        else:    
            self.build()
        # self.get_ttyd()
        if self.web:
            self.run_ttyd()
        if self.jupyter:
            self.run_jupyter()

    def publish(self):
        print("> Publish project in the Ogre cloud")
        # Get tarball name
        tarball_filename = self.project + '.tar'
        if os.path.exists(tarball_filename) == False:
            print("> Tarball doesn't exist. Please run 'ogre --package' first.")
            return 0

        # Wait here for the result to be available before continuing
        # As in https://blog.miguelgrinberg.com/post/how-to-make-python-wait
        #print(">>> Wait for tarball to be created")
        #tarball_available.wait()
        
        # Data payload
        data_payload_filename = "{}/data_payload.json".format(os.getcwd())
        data_payload = json.dumps(self.config)
        with open(data_payload_filename, 'w') as outfile:
            outfile.write(data_payload)

        filename = '{}/{}'.format(os.getcwd(), tarball_filename)
        print("filename: {}".format(filename))

        #response = requests.request(
        #    "POST", "{}/ogre/publish".format(self.api_url),·
        #    headers={"Content-Type": "application/json"},
        #    files=file_payload,
        #    data=data_payload
        #)

        # TODO: add token to payload to be verified
        publish_command = "curl -X POST '{}/ogre/publish' -F 'file_obj=@{}' --header 'api-token: {}'".format(self.api_url, filename, self.api_token)

        print("publish_command: {}".format(publish_command))

        NamedPopen(
            publish_command,
            process_name="{}_publish".format(self.project),
            shell=True,
        )

    # @yaspin(text="Service is being deployed in the Ogre Cloud...").aesthetic
    def service_up(self):

        with yaspin().aesthetic as sp:
            sp.text = "Service is being deployed in the Ogre Cloud..."

            # TODO: Check if the project is published
            #tarball_filename = self.project + '.tar'
            #if os.path.exists(tarball_filename) == False:
            #    print(">>> Tarball doesn't exist. Please run 'ogre --package' and 'ogre --publish' first.")
            #    return 0

            # Data payload
            self.config["path"] = "{}".format(self.project)
            self.config["api_url"] = self.api_url
            self.config["api_token"] = self.api_token
            self.config["openai_token"] = self.openai_token
            self.config["platform"] = self.platform
            data_payload = json.dumps(self.config)

            print(data_payload)

            response = requests.request(
                "POST", "{}/ogre/service-up".format(self.api_url),
                headers={"Content-Type": "application/json", "api-token": self.api_token},
                data=data_payload
            )
            json_obj = json.loads(response.text)
            if response.status_code == 200:
                print("Done:\n{}".format(json.dumps(json_obj, indent=2)))
            else:
                print("Ogre Cloud is unreachable: {}".format(json.dumps(json_obj, indent=2)))

    # @yaspin(text="Service is being stopped in the Ogre Cloud...").aesthetic
    def service_down(self):

        with yaspin().aesthetic as sp:
            sp.text = "Service is being stopped in the Ogre Cloud..."

            # TODO: Check if the service for project is up

            # Data payload
            # TODO: add token to payload to be verified
            self.config["path"] = "{}".format(self.project)
            self.config["platform"] = self.platform
            data_payload = json.dumps(self.config)

            response = requests.request(
                "POST", "{}/ogre/service-down".format(self.api_url),
                headers={"Content-Type": "application/json", "api-token": self.api_token},
                data=data_payload
            )

            json_obj = json.loads(response.text)
            if response.status_code == 200:
                print("Done:\n{}".format(json.dumps(json_obj, indent=2)))
            else:
                print("Ogre Cloud is unreachable: {}".format(json.dumps(json_obj, indent=2)))

    # @yaspin(text="Service is being stopped in the Ogre Cloud...").aesthetic
    def service_delete(self):

        with yaspin().aesthetic as sp:
            sp.text = "Service is being deleted in the Ogre Cloud..."

            # TODO: Check if the service for project is up

            # Data payload
            # TODO: add token to payload to be verified
            self.config["path"] = "{}".format(self.project)
            self.config["platform"] = self.platform
            data_payload = json.dumps(self.config)

            response = requests.request(
                "POST", "{}/ogre/service-delete".format(self.api_url),
                headers={"Content-Type": "application/json", "api-token": self.api_token},
                data=data_payload
            )

            json_obj = json.loads(response.text)
            if response.status_code == 200:
                print("Done:\n{}".format(json.dumps(json_obj, indent=2)))
            else:
                print("Ogre Cloud is unreachable: {}".format(json.dumps(json_obj, indent=2)))

    def service_ls(self):
        print(">>> List services (containers) running in Ogre Cloud")

        # TODO: This need to be a POST method. Create payload with token to be verified
        print("API URL: {}\n".format(self.api_url))
        
        response = requests.get("{}/ogre/list".format(self.api_url),
            headers={"Content-Type": "application/json", "api-token": self.api_token}
        )
        
        json_obj = json.loads(response.text)
        if response.status_code == 200:
            print("Services running:")
            for service in json_obj:
                print("{}, port: {}".format(service['Names'][0], service['Ports'][0]['PrivatePort']))
        else:
            print("Ogre Cloud is unreachable: {}".format(json.dumps(json_obj, indent=2)))

    def ping_api(self):
        print(">>> Test connection to Ogre cloud API")

        # TODO: This need to be a POST method. Create payload with token to be verified
        print("API URL: {}".format(self.api_url))

        response = requests.get(
            "{}/ping".format(self.api_url),
            headers={"api-token": self.api_token},
            )

        json_obj = json.loads(response.text)
        if response.status_code == 200:
            print("Ogre Cloud pong:\n{}".format(json.dumps(json_obj, indent=2)))
        else:
            print("Ogre Cloud is unreachable: {}".format(json.dumps(json_obj, indent=2)))
        #if response.status_code == 200:
        #    print("API response: {}".format(response.text))
        #else:
        #    print("API is unreachable: {}".format(response))

    def clean(self):
        if self.no_cache:
            print("> no-cache = True. Clean all")
            shutil.rmtree(self.ogre_dir, ignore_errors=True)
        else:
            print("> Don't clean anything (no_cache = {})".format(self.no_cache))

    def initialize(self):
        """
        Initializes the project by setting up the necessary files and directories.
        This method performs the following tasks:
        1. Prints the initialization message if no_cache is True.
        2. Creates the ogre_dir.
        3. Sets up requirements.txt file inside the user's project folder if it does not exist.
        4. Sets up Dockerfile inside the user's project folder.
        5. Creates a bashrc file.
        If no_cache is set to False, this method will only print a message and skip the initialization process.
        """
        if self.no_cache:
            print("> Initializing Ogre")
            # Create ogre_dir
            set_up_ogre_dir(self.ogre_dir)
            # Check for requirements.py inside user's project folder
            set_up_requirements(self._pwd, self.ogre_dir, self.requirements_format,
                                self.api_url, self.api_token, self.openai_token, self.dry)
            # Check if there is a README with either .md or .txt extensions. If inexistent, requirements_format will be forced into `freeze`.
            #self.requirements_format = check_for_readme(self._pwd, self.ogre_dir, self.requirements_format, self.dry)

            # Check for Dockerfile inside user's project folder
            set_up_dockerfile(self._pwd, self.project, self.ogre_dir, self.baseimage,
                              self.requirements_format, self.dry)
            # create bashrc
            set_up_bashrc(
                self._pwd, self.ogre_dir, self.project, self.version, self.date
            )
        else:
            print("> Skip initialization (no_cache = {})".format(self.no_cache))

    def stop_container(self):
        """
        Stop all ogre-generated containers.
        """

        container_names = [
            "{}".format(self.container_name),
            "{}-ttyd".format(self.container_name),
            "{}-jupyter".format(self.container_name),
        ]
        for container in container_names:
            stop_container_cmd = "docker stop {}".format(container)
            print(stop_container_cmd)
            p = subprocess.Popen(stop_container_cmd, stdout=subprocess.PIPE, shell=True)
            (out, err) = p.communicate()
            p_status = p.wait()

    def delete_container(self):
        """
        Delete all ogre-generated containers.
        """

        container_names = [
            "{}".format(self.container_name),
            "{}-ttyd".format(self.container_name),
            "{}-jupyter".format(self.container_name),
        ]
        for container in container_names:
            delete_container_cmd = "docker rm -f {}".format(container)
            print(delete_container_cmd)
            p = subprocess.Popen(delete_container_cmd, stdout=subprocess.PIPE, shell=True)
            (out, err) = p.communicate()
            p_status = p.wait()

    def delete_image(self):
        """
        Delete all ogre-generated images.
        """

        image_names = [
            "{}".format(self.img),
        ]
        for image in image_names:
            delete_image_cmd = "docker rmi -f {}".format(image)
            print(delete_image_cmd)
            p = subprocess.Popen(delete_image_cmd, stdout=subprocess.PIPE, shell=True)
            (out, err) = p.communicate()
            p_status = p.wait()

    def stop_ogre(self):
        print("> Stop Ogre environment")
        self.stop_container()
        stop_process(self.ttyd)

    def delete_ogre(self):
        """
        Delete all assets (image and containers) generated by Ogre.
        """

        print("> Delete Ogre environment")
        self.stop_container()
        stop_process(self.ttyd)
        self.delete_container()
        self.delete_image()

    def build(self):
        if self.no_cache:
            # build docker image
            print("> Build docker image")
            print("platform = {}".format(self.platform_name))
            print("img = {}".format(self.img))
            print("device = {}".format(self.device))
            build_cmd = (
                "DOCKER_BUILDKIT=1 docker buildx build --load --progress=auto --platform {} -t {} -f {}/Dockerfile .".format(
                    self.platform_name, self.img, self.ogre_dir
                )
            )
            print(build_cmd)
            p = subprocess.Popen(build_cmd, stdout=subprocess.PIPE, shell=True)
            (out, err) = p.communicate()
            p_status = p.wait()

            return out

        else:
            print("> Skip docker image build (no_cache = {})".format(self.no_cache))

    def get_ttyd(self):
        print("> Get ttyd")
        if os.path.isfile("{}/{}".format(self._pwd, TTYD)):
            print("{}/{} already present.".format(self._pwd, TTYD))
        else:
            print("{} not present. Downloading it from {}".format(TTYD, TTYD_URL))
            r = requests.get(TTYD_URL, allow_redirects=False)
            with open("{}".format(TTYD), "wb") as file:
                file.write(r.content)
                time.sleep(0.2)
            st = os.stat("{}".format(TTYD))
            os.chmod("{}".format(TTYD), st.st_mode | stat.S_IEXEC)
            # TODO: the line below might be necessary for correct operation of the
            # rest API service.
            # os.popen('alias ttyd="{}/{}"'.format(self._pwd, TTYD))

    def run(self):
        print("> Run docker container")

        run_cmd = "docker run {} -d --rm \
                {} \
                {} \
                --name {} \
                {} {}".format(
            self.device_command,
            self.mount_command,
            self.expose_ports_command,
            self.container_name,
            self.img,
            self.cmd,
        )
        print(run_cmd)
        os.popen(run_cmd)

    def run_ttyd(self):
        print("> Run container with ttyd")

        run_ttyd_command = (
                "{} -p {} docker run {} -it {} --rm --name {}-ttyd {} {}".format(
                TTYD,
                self.ttyd_port,
                self.device_command,
                self.mount_command,
                self.container_name,
                self.img,
                self.cmd,
            )
        )
        print(run_ttyd_command)
        # TODO: Debug NamedPopen to fix custom name (it is not being set when running ttyd)
        NamedPopen(
            run_ttyd_command,
            process_name="{}_ttyd_{}".format(self.project, self.ttyd_port),
            shell=True,
        )

    def run_jupyter(self):
        print("> Run container with jupyter")

        if "jupyter" in self.baseimage:
            run_jupyter_command = "docker run {} -d --rm {} {} --name {}-jupyter {}".format(
                self.device_command,
                self.mount_command,
                self.expose_ports_command,
                self.container_name,
                self.img
            )
        else:
            run_jupyter_command = "docker run {} -d --rm {} {} --name {}-jupyter {} {} -c {}".format(
                self.device_command,
                self.mount_command,
                self.expose_ports_command,
                self.container_name,
                self.img,
                self.cmd,
                self.cmd_jupyter,
            )
        print(run_jupyter_command)
        # TODO: Debug NamedPopen to fix custom name (it is not being set when running ttyd)
        NamedPopen(
            run_jupyter_command,
            process_name="{}_jupyter_{}".format(self.project, self.jupyter_port),
            shell=True,
        )
        time.sleep(3)
        run_docker_logs_command = "docker logs {}-jupyter".format(
                self.container_name
            )
        print(run_docker_logs_command)
        NamedPopen(
            run_docker_logs_command,
            process_name="{}_jupyter_{}_logs".format(self.project, self.jupyter_port),
            shell=True,
        )
        print("Access Ogre environment at http://localhost:{}".format(self.jupyter_port))

    def run_attach(self):
        print("> Attach to container {}".format(self.container_name))

        attach_command = "docker exec -i --tty {}-jupyter bash".format(self.container_name)
        print(attach_command)
        # TODO: Debug NamedPopen to fix custom name (it is not being set when running ttyd)
        NamedPopen(
            attach_command,
            process_name="{}_attach".format(self.project),
            shell=True,
        )

    def create_tarball(self):
        print("> Create tarball of the directory {}".format(self._pwd))
        
        project_path = os.path.basename(self._pwd)
        create_tarball_command = "tar --exclude='{}/.git' --exclude='{}/ogre_dir' --exclude='{}/ogre.yml' -cvf {}.tar -C ../ {}".format(project_path, project_path,
                                                 project_path, self.project, 
                                                 project_path) 
        print(create_tarball_command)
        # TODO: Debug NamedPopen to fix custom name (it is not being set when running ttyd)
        NamedPopen(
            create_tarball_command,
            process_name="{}_create_tarball".format(self.project),
            shell=True,
        )

    def generate_yml_file(self):
        print("> Generate yml config file from template")
        set_up_yml_file(self._pwd)

    def info(self):
        print("> Info about ogre containers running in the local system")
        res = list_ogre_containers()

        for i in range(len(res)):
            print(res[i])

        #for i in range(len(res)):
        #    name = res[i][0]
        #    ports = res[i][1]
        #    print("{}, ports: {}, {}".format(name, 
        #                                     ports, 
        #                                     LOCALHOST + ":" + str(min(ports))))


    def gui(self):
        
        """
        Start local GUI based on Streamlit. 
        """
        print("> Start GUI")
        path_ogre_run = get_module_installation_path("ogre_cli")
        gui_filepath = os.path.join(path_ogre_run, GUI_PYTHONFILE)

        command_gui = "streamlit run --server.port {} {}".format(STREAMLIT_PORT,
                                                                 gui_filepath)
        
        NamedPopen(
            command_gui,
            process_name="ogre_gui",
            shell=True,
        )

    def ogre_save(self):

        """
        Save (commit) Ogre-environment container to docker image.

        This is handy if one needs to make extra modifications to the
        container after its creation (and after installation of the 
        original dependencies) and update the final image.
        """

        image= "{}".format(self.img)
        #TODO: remove the `-jupyter` that is hardcoded below. This is done here
        # because we want to commit the docker that runs the jupyter notebook.
        container = "{}-jupyter".format(self.container_name)
        container_commit_cmd = "docker commit {} {}".format(container, image)
        print(container_commit_cmd)
        p = subprocess.Popen(container_commit_cmd, stdout=subprocess.PIPE, shell=True)
        (out, err) = p.communicate()
        p_status = p.wait()

