import streamlit as st

from lib.ui import set_init_state, reset_results, sidebar
from lib.bot import send
from lib.lib import Sentiment

# for drawing charts
import pandas as pd
import numpy as np

# json lib
import json

# set the init values
set_init_state()

# create sidebar
sidebar()

def set_pd_name(pd_name : str):
    st.session_state["PD_NAME"] = pd_name

def share(email : str):
    st.session_state["SHARE"] = email

def count_share(i : int):
    st.session_state["SHARE_COUNT"] += 1

def set_chat(msg : str):
    st.session_state["USER_MSG"] = msg

st.write('# `Sentzi`')

st.divider()

st.write("## Let's begin ! 🚀")

if st.session_state.get("EMAIL_ID") and st.session_state.get("NAME"):
    col1, col2 = st.columns(2)
    with col2:
        pd_name_input = st.text_input(
            "💡 Product Name",
            placeholder="Shoe",
            help="A fake product name . ",
            value=st.session_state.get("PD_NAME","")
        )

        if pd_name_input:
            set_pd_name(pd_name_input)

            # share the app
            st.markdown("## ✨ Share app ✨")

            share_input = st.text_input(
                "Friend's email address",
                placeholder="Paste your friend's email address here ",
                help="example@xyz.com",
                value=st.session_state.get("SHARE", "")
            )

            if share_input:
                share(share_input)

            #send the app link
            if send(
                share_input,
                st.session_state.get("EMAIL_ID",""),
                st.session_state.get("NAME",""),
                st.session_state.get("PD_NAME","")
            ):
                st.success(f'Shared !')

                # increase share count
                count_share(1)

            else:
                st.error("Sharing failed !")
    
    with col1:

        st.markdown(f"### {st.session_state.get('NAME','')}'s Dashboard")
        # make 3 tabs
        tab1, tab2, tab3 = st.tabs(["Shares", "Viz 1", "Viz 2"])
        with tab1:
            st.metric(
                label="🌐 Shares",
                value=st.session_state.get("SHARE_COUNT",""),
                delta=1

            )
        with tab2:
            st.markdown("### Viz 1")
        
        with tab3:
            st.markdown("### Viz 2")
        
    st.markdown("---")

    user = st.toggle('Become a user 🙂 !')
    if user:
        st.markdown('#### Reviews 🌟')

        prompt = st.chat_input(
            f'Write your thought about {st.session_state.get("PD_NAME","")}',
        )

        if prompt:
            set_chat(prompt)
        
            # analyse the chat
            sent_level = Sentiment(prompt).get().get('level')
            

