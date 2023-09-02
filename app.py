import streamlit as st
import time

from lib.ui import set_init_state, reset_results, sidebar, reset_sent_scores
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

def set_positive_level(value : int):

    st.session_state["POS"] = value

def set_negative_level(value : int):

    st.session_state["NEG"] = value

def set_neutral_level(value : int): 

    st.session_state["NUT"] = value

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
            st.markdown("### ✨Share the product✨")

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
            
            show_score = st.toggle('show score',help="Show the sentiment score side by side")
            if show_score:
                tabPos , tabNeg, tabNut =  st.tabs(["Positive", "Negative","Neutral"])
                with tabPos:
                    st.markdown(f"{st.session_state.get('POS','')}")
                with tabNeg:
                    st.markdown(f"{st.session_state.get('NEG','')}")
                with tabNut:
                    st.markdown(f"{st.session_state.get('NUT','')}")
            
            if st.button("Just refresh", help="Can't see the changes in graph ? Hit `Just refresh`"):
                pass
    
    with col1:

        st.markdown(f"### {st.session_state.get('NAME','')}'s Dashboard")
        # make 3 tabs
        tab1, tab2, tab3 = st.tabs(["Shares", "Viz 1", "Viz 2"])
        with tab1:
            if st.button('# Reset shares',help="Reset all shares",use_container_width=True):
                st.session_state["SHARE_COUNT"] = 0
                st.toast('### Shares reseted ! 🔄')
            st.metric(
                label="🌐 Shares",
                value=st.session_state.get("SHARE_COUNT",""),
                delta=1

            )

        with tab2:
            st.markdown("### Viz 1 ")
            st.markdown('In the visualization below , '
                        'the line deviates towards the direction of greater score .'
                        'You may need to `Reset Graph` if the `positive` and `negative` reaches'
                        ' its max score (i.e `1.0` and `-1.0` resp)')

            # Assuming you have these values in your session_state
            positive_value = st.session_state.get("POS","")
            negative_value = st.session_state.get("NEG", "")
            neutral_value = st.session_state.get("NUT", "")

            # Create a DataFrame with a single row and three columns
            viz_data = pd.DataFrame(
                data=[
                    positive_value,
                    negative_value,
                    neutral_value
                ],
                index=[
                    f'{Sentiment.__emojiDic__.get("positive")[0]} positive',
                    f'{Sentiment.__emojiDic__.get("negative")[0]} negative',
                    f'{Sentiment.__emojiDic__.get("neutral")[0]} neutral'
                ],
                
            )

            if st.button('# Reset graph',help="Reset graph from all data",use_container_width=True):
                reset_sent_scores()
                time.sleep(0.5)
                reset_sent_scores()
                st.toast('### Graph 📈 reseted ! 🔄')
                st.toast("Hi ! 👋 Can't see the changes in graph ? Hit `Just refresh`")

            st.line_chart(
                viz_data,
                color=["#44f"]

            )

        with tab3:
            st.markdown("### Viz 2")
            st.markdown('In the visualization below , '
                        'the area will be more in the region of greater score .'
                        'You may need to `Reset Graph` if the `positive` and `negative` reaches'
                        ' its max score (i.e `1.0` and `-1.0` resp)')
            st.area_chart(
                viz_data,
                color=["#f0f"]
            )
        
    st.markdown("---")

    user = st.toggle('Become a user 🙂 !')
    if user:
        st.markdown('#### Reviews 🌟')

        prompt = st.chat_input(
            f'Write your thought about {st.session_state.get("PD_NAME","")}',
        )

        if prompt:
            set_chat(prompt)
            st.toast("Hi ! 👋 Can't see the changes in graph ? Hit `Just refresh`")
        
            # analyse the chat
            sent_level = Sentiment(prompt).get().get('level')
            sent_score = Sentiment(prompt).get().get('score')

            # set the score for viz
            {
                'negative' : lambda : set_negative_level(sent_score),
                'positive' : lambda : set_positive_level(sent_score),
                'neutral' : lambda : set_neutral_level(sent_score),
            }.get(sent_level , lambda : None)()

            

