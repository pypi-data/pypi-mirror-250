import json
import os

import pkg_resources
import upstride_argparse as argparse
from pyfiglet import Figlet
from rich import print as rprint

import ogre_cli
from ogre_cli.docker_management import DockerImage
from ogre_cli.menu import arguments, read_yaml_config


def ogre_main():

    pwd = os.getcwd()

    config = argparse.parse_cmd(arguments)

    # Overwrite 'config' values if 'ogre.yml' is present in the repo rootdir
    files_in_repo_rootdir = next(os.walk(pwd), (None, None, []))[2]  # [] if no file
    if 'ogre.yml' in files_in_repo_rootdir:
        config = read_yaml_config('{}/ogre.yml'.format(pwd), config)

    if config["version"] == True:
        # Display Ogre figlet
        f = Figlet(font="slant")
        # Get version
        ogre_version = pkg_resources.get_distribution('ogre_cli').version
        rprint("[cyan] {} [/cyan]".format(f.renderText("Ogre")))
        rprint("[blue bold]Ogre {} - {}[/blue bold]".format(ogre_version, ogre_cli.__website__))
        return None

    os.chdir(config["path"])

    docker_container = DockerImage(config)

    # Display Ogre figlet when building an environment
    f = Figlet(font="slant")
    ogre_version = pkg_resources.get_distribution('ogre_cli').version
    rprint("[cyan] {} [/cyan]".format(f.renderText("Ogre")))
    rprint("[blue bold]Ogre {} - {}[/blue bold]\n".format(ogre_version, ogre_cli.__website__))
    rprint("[bold]Project: {}\n".format(docker_container.project))

    # Test multiple commands 
    if config["stop"] == True:
        # Terminating Ogre
        docker_container.stop_ogre()
        return None
    if config["delete"] == True:
        # Terminating Ogre
        docker_container.delete_ogre()
        return None
    if config["package"] == True:
        # Package project into a tarball
        docker_container.create_tarball()
        return None
    if config["publish"] == True:
        # Publish to Ogre Cloud
        docker_container.publish()
        return None
    if config["ping"] == True:
        # Test connection to Ogre Cloud API
        docker_container.ping_api()
        return None
    if config["service_ls"] == True:
        # List services running in the Ogre cloud
        docker_container.service_ls()
        return None
    if config["config"] == True:
        # Create ogre.yml from template
        docker_container.generate_yml_file()
        return None
    if config["info"] == True:
        # Get information about ogre containers running in the system
        docker_container.info()
        return None
    if config["attach"] == True:
        # Run streamlit GUI
        docker_container.run_attach()
        os.wait()
        return None
    if config["gui"] == True:
        # Run streamlit GUI
        docker_container.gui()
        return None
    if config["save"] == True:
        # Save Ogre environment in a Docker image
        docker_container.ogre_save()
        return None

    # Either deploy in the cloud or locally
    if config["service_up"] == True:
        # Start service in Ogre cloud
        docker_container.service_up()
    elif config["service_down"] == True:
        # Stop service in Ogre cloud
        docker_container.service_down()
    elif config["service_delete"] == True:
        # Delete service in Ogre cloud
        docker_container.service_delete()
    else:
        print("Ogre summary \n: {}".format(json.dumps(config, indent=4)))
        # Start Ogre locally 
        docker_container.all()
