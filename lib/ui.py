import streamlit as st
from PIL import Image

def set_state_if_absent(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

def set_init_state():
    set_state_if_absent('SHARE_COUNT',0)


def reset_results(*args):
    st.session_state.result = None

def set_email(email: str):
    st.session_state["EMAIL_ID"] = email

def set_name(name : str):
    st.session_state["NAME"] = name

def sidebar():
    with st.sidebar:
        if st.button("`VERSION`"):
            
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

        )

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

