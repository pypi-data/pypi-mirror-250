import random

import streamlit as st
from ogarantia_streamlit_card import card
from ogre_cli.docker_management.constants import *


def create_info_card(container_info, 
                     height = 200, 
                     width = 250, 
                     margin = 20, 
                     key = 0):

    """
    Create info card for an ogre process.
    """

    name_split = container_info[0].split("-")[1:]
    name = " ".join(name_split)
    ports = container_info[1]
    url = LOCALHOST + ":" + str(min(ports))
    hasClicked = card(
              title="{}".format(name),
              text="Ports: {}".format(ports),
              image="https://get.ogre.run/images/ogarantia_logoBlue.png",
              height=height,
              width=width,
              margin=margin,
              url="{}".format(url))

def display_cards(list_of_ogre_containers):

    """
    Display cards.

    Only supports rows of two cards.
    """

    if len(list_of_ogre_containers) == 1:
      col_card_1, col_card_2 = st.columns([1, 1])
      with col_card_1:
          create_info_card(list_of_ogre_containers[i], key = i + random.randint(0, RANDOM_UPPER_LIMIT))
    elif len(list_of_ogre_containers) % 2 == 0:
        if len(list_of_ogre_containers) == 2:
            col_card_1, col_card_2 = st.columns([1, 1])
            with col_card_1:
                create_info_card(list_of_ogre_containers[0], key = random.randint(0, RANDOM_UPPER_LIMIT))
            with col_card_2:
                create_info_card(list_of_ogre_containers[1], key = 1 + random.randint(0, RANDOM_UPPER_LIMIT))
        else:
          for i in range(len(list_of_ogre_containers) - 2):
              col_card_1, col_card_2 = st.columns([1, 1])
              with col_card_1:
                  create_info_card(list_of_ogre_containers[2*i], key = 2*i)
              with col_card_2:
                  create_info_card(list_of_ogre_containers[2*i+1], key = 2*i+1)
    else:
      for i in range(len(list_of_ogre_containers) - 2):
          col_card_1, col_card_2 = st.columns([1, 1])
          with col_card_1:
              create_info_card(list_of_ogre_containers[2*i], key = i + random.randint(0, RANDOM_UPPER_LIMIT))
          with col_card_2:
              create_info_card(list_of_ogre_containers[2*i+1], key = i + random.randint(0, RANDOM_UPPER_LIMIT))
      col_card_1, col_card_2 = st.columns([1, 1])
      with col_card_1:
          create_info_card(list_of_ogre_containers[len(list_of_ogre_containers)-1], key = i*random.randint(0, RANDOM_UPPER_LIMIT))
