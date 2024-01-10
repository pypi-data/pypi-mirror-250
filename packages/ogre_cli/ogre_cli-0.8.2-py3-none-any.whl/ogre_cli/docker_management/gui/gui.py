import os

import streamlit as st
import streamlit.components.v1 as components
from ogarantia_streamlit_card import card
from ogre_cli.docker_management.constants import *
from ogre_cli.docker_management.subcommands import list_ogre_containers
from ogre_cli.docker_management.utilities import get_module_installation_path
from PIL import Image

from utils import display_cards

path_ogre_cli = get_module_installation_path("ogre_cli")
gui_filepath = os.path.join(path_ogre_cli, "docker_management/gui")

ogre_logo = Image.open("{}/images/ogre-run-1.png".format(gui_filepath))
ogarantia_logo = Image.open("{}/images/ogarantia_logoBlue.png".format(gui_filepath))
ogarantia_logo_path = "{}/images/ogarantia_logoBlue.png".format(gui_filepath)

with st.sidebar:
    st.image(ogre_logo, width=200)
    # st.title("Ogre.run")
    # st.markdown("Code once, run anywhere")
    st.text(" ")

    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")

    col1, col2 = st.columns([1, 5])
    with col1:
      st.image(ogarantia_logo, width=40)
    with col2:
      st.markdown("Made by [Ogarantia.com](https://ogarantia.com)")

# Get list of ogre continers running
res = list_ogre_containers()

# Display cards
display_cards(res)
