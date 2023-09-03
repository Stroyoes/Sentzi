import streamlit as st
from PIL import Image
import requests

def set_state_if_absent(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

def set_init_state():
    set_state_if_absent('SHARE_COUNT',0)
    set_state_if_absent('POS',0)
    set_state_if_absent('NEG',0)
    set_state_if_absent('NUT',0)
    set_state_if_absent('USER_MSG',[])
    set_state_if_absent('SENT_LEVEL',[])

def reset_sent_scores(keys = ['POS','NEG','NUT']):
    for k in keys:
        st.session_state[k] = 0

def set_email(email: str):
    st.session_state["EMAIL_ID"] = email

def set_name(name : str):
    st.session_state["NAME"] = name

def sidebar():
    with st.sidebar:
        if st.button("# **version**",help="Show the version (floating)",use_container_width=True):
            version_file = "https://cdn.jsdelivr.net/gh/sreezx/Sentzi/version"
            version = requests.get(version_file).content.decode()
            st.toast(f'### 🏷️ version `{version}`')

        image = Image.open(r'C:\Users\MyLap\Documents\GitHub\Sentzi\data\logo.png')
        st.markdown(
            "Welcome 😊 to `Sentzi` \n\n"
            "This is a fun project ,\n "
            "designed to demonstrate the practical application "
            "of sentiment analysis \n\n"
            "Want to know more ?? [visit GitHub](https://github.com/sreezx/Sentzi#readme)"
        )

        st.markdown(
            "## How to use ?\n"
            "1. Enter your **email address** below\n"
            "2. Enter your **name** (but not your real one 😈)\n"
            "3. You will now see your dashboard getting loaded ... \n"
            "4. You can create only one product at a time .\n"
            "5. To ensure that all changes are distributed evenly throughout the app, you might need to occasionally tap the `Just Refresh` button. \n"

        ,help="Why `Just Refresh` 😞 ? Well , its actually a bug 🐞 i need to fix in the next release 🥺")

        email_id_input = st.text_input(
            "Your email address",
            placeholder="Paste your email address here ( example@xyz.com )",
            help="No email 😲 ? Are you really human ? ",
            value=st.session_state.get("EMAIL_ID", "")
        )

        if email_id_input:
            set_email(email_id_input)
        
        name_input = st.text_input(
            "Your name",
            placeholder="Sam",
            help="Just give your name . ",
            value=st.session_state.get("NAME","")
        )

        if name_input:
            set_name(name_input)
        
        st.markdown("---")
        st.markdown(
            "## How's this possible ?\n"
            "Built using `Python` and the beautiful web app framework - [`Streamlit`](https://streamlit.io) \n"
            "Uses the [`TextBlob`](https://github.com/sloria/textblob) library for sentiment analysis  \n\n"
            "The source code is also on [GitHub](https://github.com/sreezx/Sentzi#readme)"
        )
        st.markdown("---")

        st.markdown("Made by [`sreezx`](https://github.com/sreezx)")

        st.markdown("---")

        st.markdown("[![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/sreezx.y)"
                    " [![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sreezx/Sentzi)")

        st.markdown("---")
        st.image(image)

